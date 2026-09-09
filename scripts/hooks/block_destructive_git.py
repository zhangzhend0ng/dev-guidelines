#!/usr/bin/env python3
"""PreToolUse guard hook: deterministically block destructive git commands.

Downsinks the user-level AGENTS.md git guardrail from natural language to a
runtime PreToolUse interception. Motivating incident: a `git checkout -- <file>`
irreversibly discarded ~1956 lines of uncommitted work.

Protocol (verified against https://code.claude.com/docs/en/hooks, 2026-09):
- stdin  : one JSON object, e.g. {"tool_name": "Bash",
           "tool_input": {"command": "git status"}}
- allow  : exit 0, no output
- deny A : exit 2 + reason on stderr (Claude Code blocking exit code)
- deny B : --output json -> exit 0 + stdout JSON
           {"hookSpecificOutput": {"hookEventName": "PreToolUse",
            "permissionDecision": "deny", "permissionDecisionReason": "..."}}

Fail-open ONLY when the hook's own input cannot be parsed (malformed JSON,
missing/non-string command) - an unanalyzable command is never treated as a
match, so a host-protocol bug cannot freeze the shell. Policy (the destructive
pattern list) lives in config/policy.yml; when the policy is missing,
unreadable, or invalid the hook FAILS CLOSED: every git command is denied
until the config is fixed. Known gaps are listed in docs/ai/hooks-setup.md
(git restore, `git checkout .`, quoted prose false positives from the
secondary net).
"""

import argparse
import json
import re
import shlex
import sys
from pathlib import Path

import yaml

MAX_STDIN_BYTES = 1 << 20

DEFAULT_POLICY_PATH = Path(__file__).resolve().parents[2] / "config" / "policy.yml"

# Per-subcommand parameter schema. Every key listed here is REQUIRED in the
# policy file for that subcommand - a silently-missing flag would quietly
# weaken the guardrail, so absence is a config error (fail-closed).
RULE_SCHEMA = {
    "checkout": {"path_separator": bool, "allow_patch": bool},
    "reset": {"flags": list},
    "clean": {"force": bool},
    "stash": {"subcommands": list},
    "branch": {"force_delete": bool},
}


class PolicyError(Exception):
    pass


def load_policy(path):
    """Parse + validate config/policy.yml into rule dicts (see RULE_SCHEMA)."""
    try:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, yaml.YAMLError) as e:
        raise PolicyError(f"无法读取策略配置 {path}: {e}")
    if not isinstance(data, dict) or not isinstance(data.get("destructive_patterns"), list):
        raise PolicyError(f"策略配置缺少 destructive_patterns 列表: {path}")
    rules = []
    for i, entry in enumerate(data["destructive_patterns"]):
        if not isinstance(entry, dict) or entry.get("subcommand") not in RULE_SCHEMA:
            raise PolicyError(f"destructive_patterns[{i}] 的 subcommand 非法: {entry!r}")
        sub = entry["subcommand"]
        spec = RULE_SCHEMA[sub]
        unknown = set(entry) - {"subcommand"} - set(spec)
        if unknown:
            raise PolicyError(f"destructive_patterns[{i}] 含未知字段: {sorted(unknown)}")
        rule = {"subcommand": sub}
        for key, typ in spec.items():
            if key not in entry:
                raise PolicyError(f"destructive_patterns[{i}] ({sub}) 缺少字段 {key}")
            value = entry[key]
            if not isinstance(value, typ):
                raise PolicyError(
                    f"destructive_patterns[{i}].{key} 类型应为 {typ.__name__}: {value!r}"
                )
            rule[key] = value
        rules.append(rule)
    return rules

# Secondary net per statement: catches git nested in command substitution
# (`$(git reset --hard)`, backticks) where tokenization sees only the outer
# command. Cost: the same words inside quoted prose also deny (safe direction,
# documented in docs/ai/hooks-setup.md). The checkout pattern carries a
# negative lookahead so `checkout -p/--patch` stays allowed.
_SECONDARY = [
    ("reset", r"git\b[^;&|\n]*?\breset\b[^;&|\n]*?--hard\b"),
    ("checkout", r"git\b[^;&|\n]*?\bcheckout\b(?![^;&|\n]*\s(?:-p|--patch)\b)"
                 r"[^;&|\n]*?\s--\s+\S"),
    ("clean", r"git\b[^;&|\n]*?\bclean\b[^;&|\n]*?(?:-\w*f|--force\b)"),
    ("stash", r"git\b[^;&|\n]*?\bstash\b[^;&|\n]*?\b(?:drop|clear)\b"),
    ("branch", r"git\b[^;&|\n]*?\bbranch\b[^;&|\n]*?(?:-D\b|--delete\b[^;&|\n]*?--force\b|--force\b[^;&|\n]*?--delete\b)"),
]
_SECONDARY = [(name, re.compile(pat)) for name, pat in _SECONDARY]

_STATEMENT_SPLIT = re.compile(r"&&|\|\||[;&|\n]")
_ENV_ASSIGN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")


def split_statements(cmd):
    """Split a shell command line on top-level operators only.

    Quote-aware: `;`/`&&`/`|`/newlines inside single or double quotes (or
    backslash-escaped) do not split, so `git commit -m "a; b"` stays one
    statement.
    """
    stmts, buf, quote = [], [], None
    i, n = 0, len(cmd)
    while i < n:
        ch = cmd[i]
        if quote == "'":
            if ch == "'":
                quote = None
            buf.append(ch)
            i += 1
            continue
        if quote == '"':
            if ch == "\\" and i + 1 < n:
                buf.append(cmd[i:i + 2])
                i += 2
                continue
            if ch == '"':
                quote = None
            buf.append(ch)
            i += 1
            continue
        if ch in ("'", '"'):
            quote = ch
            buf.append(ch)
            i += 1
            continue
        if ch == "\\" and i + 1 < n:
            buf.append(cmd[i:i + 2])
            i += 2
            continue
        m = _STATEMENT_SPLIT.match(cmd, i)
        if m:
            stmts.append("".join(buf))
            buf = []
            i = m.end()
            continue
        buf.append(ch)
        i += 1
    stmts.append("".join(buf))
    return [s.strip() for s in stmts if s.strip()]


def _is_git_token(tok):
    name = Path(tok).name.lower()
    if name.endswith(".exe"):
        name = name[:-4]
    return name == "git"


def _rule_matches(rule, args):
    sub = rule["subcommand"]
    if sub == "checkout":
        if rule.get("allow_patch") and any(a in ("-p", "--patch") for a in args):
            return False
        if "--" in args:
            # unambiguous path restore; needs at least one path after `--`
            return args.index("--") < len(args) - 1
        return False
    if sub == "reset":
        return any(a == "--hard" or a.startswith("--hard=") for a in args)
    if sub == "clean":
        return any(a == "--force" or (a.startswith("-") and not a.startswith("--")
                                      and "f" in a[1:]) for a in args)
    if sub == "stash":
        positional = [a for a in args if not a.startswith("-")]
        return bool(positional) and positional[0] in rule["subcommands"]
    if sub == "branch":
        short_d = any(a.startswith("-") and not a.startswith("--") and "D" in a[1:]
                      for a in args)
        both = "--delete" in args and "--force" in args
        return short_d or both
    return False


def _statement_is_git(stmt):
    """True if the statement's primary binary is git (env/builtin prefixes stripped)."""
    try:
        toks = shlex.split(stmt, posix=True)
    except ValueError:
        return False
    k = 0
    while k < len(toks) and _ENV_ASSIGN.match(toks[k]):
        k += 1
    if k < len(toks) and toks[k] in ("command", "exec"):
        k += 1
    return k < len(toks) and _is_git_token(toks[k])


def analyze_statement(stmt, rules):
    """Return the matched rule name for one shell statement, or None."""
    if not _statement_is_git(stmt):
        return _secondary(stmt)
    try:
        toks = shlex.split(stmt, posix=True)
    except ValueError:
        return _secondary(stmt)
    k = 0
    subcommand = None
    while k < len(toks):
        t = toks[k]
        if t in ("-C", "-c"):  # global options that consume a value
            k += 2
            continue
        if t.startswith("-"):
            k += 1
            continue
        subcommand = t
        k += 1
        break
    args = toks[k:]
    for rule in rules:
        if rule["subcommand"] == subcommand and _rule_matches(rule, args):
            return subcommand
    return _secondary(stmt)


def _secondary(stmt):
    for name, pat in _SECONDARY:
        if pat.search(stmt):
            return name
    return None


def decide(command, rules):
    """Return the first matched destructive rule name in a command line."""
    for stmt in split_statements(command or ""):
        matched = analyze_statement(stmt, rules)
        if matched:
            return matched
    return None


def deny_reason(rule_name, command, policy_error=""):
    display = command if len(command) <= 120 else command[:117] + "..."
    if rule_name == "fail-closed":
        return (
            f"[block_destructive_git] 策略配置不可用，按 fail-closed 拒绝所有 git 命令：{display}\n"
            f"{policy_error}\n"
            "修复 config/policy.yml（或用 --policy 指定正确路径）后重试；"
            "先做只读核查确认影响范围：git diff HEAD -- <path> / git status。\n"
        )
    return (
        f"[block_destructive_git] 已拦截高危 git 命令（{rule_name}）：{display}\n"
        "该命令会不可逆丢弃 git 数据。先做只读核查确认影响范围："
        "git diff HEAD -- <path> / git status。\n"
        "确需回退时改用细粒度工具：Edit 逐 hunk 改写、git checkout -p 选择性回退、"
        "git stash push 可逆暂存。\n"
    )


def main():
    ap = argparse.ArgumentParser(description="PreToolUse destructive-git guard")
    ap.add_argument("--output", choices=("exit2", "json"), default="exit2",
                    help="deny protocol: exit 2 + stderr (default) or stdout JSON decision")
    ap.add_argument("--policy", help=f"policy file (default: {DEFAULT_POLICY_PATH})")
    args = ap.parse_args()

    policy_error = ""
    try:
        rules = load_policy(args.policy or DEFAULT_POLICY_PATH)
    except PolicyError as e:
        rules = None
        policy_error = str(e)

    raw = b""
    try:
        raw = sys.stdin.buffer.read(MAX_STDIN_BYTES + 1)
    except Exception:
        pass
    if not raw or len(raw) > MAX_STDIN_BYTES:
        sys.exit(0)  # empty or oversized: cannot analyze, fail-open (see docstring)
    try:
        payload = json.loads(raw.decode("utf-8", "replace"))
    except json.JSONDecodeError:
        sys.exit(0)
    tool_input = payload.get("tool_input") if isinstance(payload, dict) else None
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if not isinstance(command, str) or not command.strip():
        sys.exit(0)

    if rules is None:
        # fail-closed: policy unavailable -> deny every git command, pass the rest
        if not any(_statement_is_git(s) for s in split_statements(command)):
            sys.exit(0)
        rule, reason = "fail-closed", deny_reason("fail-closed", command, policy_error)
    else:
        rule = decide(command, rules)
        if rule is None:
            sys.exit(0)
        reason = deny_reason(rule, command)

    if args.output == "json":
        json.dump({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }}, sys.stdout)
        sys.exit(0)
    sys.stderr.write(reason)
    sys.exit(2)


if __name__ == "__main__":
    main()
