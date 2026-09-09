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
match, so a host-protocol bug cannot freeze the shell. Known gaps are listed
in docs/ai/hooks-setup.md (git restore, `git checkout .`, quoted prose false
positives from the secondary net). The high-risk list is hardcoded in
DESTRUCTIVE_RULES until Phase 5 externalizes it to config/policy.yml.
"""

import argparse
import json
import re
import shlex
import sys
from pathlib import Path

MAX_STDIN_BYTES = 1 << 20

# Hardcoded initial policy (Phase 5 -> config/policy.yml).
# checkout: interactive patch mode (-p/--patch) is the AGENTS.md-preferred
# fine-grained rollback tool and must stay allowed; the `--` path-separator
# forms are unconditional discards. branch -D == --delete --force; plain
# `-d` refuses unmerged branches and stays allowed.
DESTRUCTIVE_RULES = [
    {"subcommand": "checkout", "path_separator": True, "allow_patch": True},
    {"subcommand": "reset", "flags": ["hard"]},
    {"subcommand": "clean", "force": True},
    {"subcommand": "stash", "subcommands": ["drop", "clear"]},
    {"subcommand": "branch", "force_delete": True},
]

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


def analyze_statement(stmt, rules):
    """Return the matched rule name for one shell statement, or None."""
    try:
        toks = shlex.split(stmt, posix=True)
    except ValueError:
        return _secondary(stmt)
    k = 0
    while k < len(toks) and _ENV_ASSIGN.match(toks[k]):
        k += 1
    if k < len(toks) and toks[k] in ("command", "exec"):
        k += 1
    if k >= len(toks) or not _is_git_token(toks[k]):
        return _secondary(stmt)
    k += 1
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


def decide(command, rules=None):
    """Return the first matched destructive rule name in a command line."""
    if rules is None:
        rules = DESTRUCTIVE_RULES
    for stmt in split_statements(command or ""):
        matched = analyze_statement(stmt, rules)
        if matched:
            return matched
    return None


def deny_reason(rule_name, command):
    display = command if len(command) <= 120 else command[:117] + "..."
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
    args = ap.parse_args()

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

    rule = decide(command)
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
