#!/usr/bin/env python3
"""Regression tests for scripts/hooks/block_destructive_git.py (Phase 1).

Covers:
- the 7-item destructive list sunk from the user-level AGENTS.md guardrail
- variant tolerance: quotes, extra whitespace, `git -C <path>` prefix,
  `--` separator, other global options, env-assignment prefixes,
  compound statements (&&, ;, |, newline)
- bypass attempts: command substitution ($(), backticks), option shuffling,
  config/global-option prefixes
- non-targets: safe operations must stay allowed (checkout -p/--patch,
  reset --soft, clean -n, stash push, branch -d)
- both denial protocols (exit 2 + stderr; stdout JSON permissionDecision)
  and the documented fail-open path for malformed hook input
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / "scripts" / "hooks" / "block_destructive_git.py"

# The 7 documented list items, in their canonical spelling.
CANONICAL_DENY = [
    "git checkout -- file.txt",
    "git checkout HEAD -- file.txt",
    "git reset --hard",
    "git clean -fd",
    "git stash drop",
    "git stash clear",
    "git branch -D feature/x",
]

# Variants and bypass attempts; every entry MUST still be denied.
VARIANT_DENY = [
    "git reset --hard HEAD~3",
    "git checkout abc1234 -- src/",
    "git  checkout   --  file.txt",                # 多空格
    'git "checkout" -- file.txt',                  # 引号
    "git 'checkout' -- file.txt",
    "git -C sub reset --hard",                     # -C 前缀
    "git -C sub checkout -- file.txt",
    "git -c core.excludesfile=/x clean -fd",       # -c 配置前缀
    "FOO=1 BAR=2 git reset --hard",                # env 前缀
    "git --work-tree=/tmp reset --hard",           # 全局选项
    "git --no-pager checkout -- f",
    "git reset -q --hard",
    "cd a && git reset --hard",                    # 复合语句
    "git status; git clean -fd",
    "git status && git stash drop",
    "echo hi | git branch -D x",
    "git reset --hard # cleanup comment",
    "git status\ngit reset --hard",                # 换行复合
    "git clean --force -d",
    "git clean -df",
    "git clean -f",
    "git clean -xdf",
    "git stash drop stash@{0}",
    "git branch --delete --force x",
    'git commit -m "$(git reset --hard)"',         # 命令替换
    "git commit -m \"`git clean -fd`\"",           # 反引号
]

# Safe operations that must remain allowed.
ALLOW = [
    "git status",
    "git diff HEAD -- file.txt",
    "git log --oneline -5",
    "git checkout main",
    "git checkout -b feature/x",
    "git checkout -p HEAD~1 -- file.txt",          # AGENTS.md 推荐的细粒度回退
    "git checkout --patch -- file.txt",
    "git reset --soft HEAD~1",
    "git reset",
    "git clean -n",
    "git clean -nd",
    "git stash push -m wip",
    "git stash list",
    "git branch -d old-branch",
    'echo "never run git checkout -p on this"',
    "ls -la",
    "python scripts/validate.py",
    "git stash push; git status",
]


def run_hook(command, extra_args=()):
    payload = {"tool_name": "Bash", "tool_input": {"command": command}}
    return subprocess.run(
        [sys.executable, str(HOOK), *extra_args],
        input=json.dumps(payload),
        capture_output=True, text=True, check=False,
    )


def run_hook_raw(stdin_text):
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=stdin_text, capture_output=True, text=True, check=False,
    )


def main():
    errors = []

    def expect_deny(cmd):
        r = run_hook(cmd)
        if r.returncode != 2:
            errors.append(f"DENY exit2 协议漏拦（rc={r.returncode}）: {cmd!r}")
        if "只读核查" not in r.stderr or "git diff HEAD" not in r.stderr:
            errors.append(f"DENY stderr 缺只读核查指引: {cmd!r}")
        r = run_hook(cmd, ["--output", "json"])
        if r.returncode != 0:
            errors.append(f"DENY json 协议 exit 非 0（rc={r.returncode}）: {cmd!r}")
        try:
            decision = json.loads(r.stdout)["hookSpecificOutput"]
            if decision.get("permissionDecision") != "deny":
                errors.append(f"DENY json 协议 decision 非 deny: {cmd!r}")
            if "permissionDecisionReason" not in decision:
                errors.append(f"DENY json 协议缺 reason: {cmd!r}")
        except (json.JSONDecodeError, KeyError):
            errors.append(f"DENY json 协议输出不可解析: {cmd!r} stdout={r.stdout!r}")

    def expect_allow(cmd):
        r = run_hook(cmd)
        if r.returncode != 0:
            errors.append(f"ALLOW 误拦（rc={r.returncode} stderr={r.stderr[:80]!r}）: {cmd!r}")
        if r.stdout.strip():
            errors.append(f"ALLOW 却有 stdout 输出: {cmd!r}")

    for cmd in CANONICAL_DENY:
        expect_deny(cmd)
    for cmd in VARIANT_DENY:
        expect_deny(cmd)
    for cmd in ALLOW:
        expect_allow(cmd)

    # Fail-open path: malformed / incomplete hook input must never deny.
    for raw in ("not-json", "{}", '{"tool_name": "Bash"}',
                '{"tool_name": "Bash", "tool_input": {}}',
                '{"tool_name": "Bash", "tool_input": {"command": 42}}',
                '{"tool_name": "Bash", "tool_input": {"command": "   "}}',
                '{"tool_name": "Read", "tool_input": {"file_path": "x"}}'):
        r = run_hook_raw(raw)
        if r.returncode != 0 or r.stdout.strip():
            errors.append(f"fail-open 被破坏: input={raw!r} rc={r.returncode}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        sys.exit(1)

    print(f"Hook guard tests passed "
          f"({len(CANONICAL_DENY)} canonical + {len(VARIANT_DENY)} variant "
          f"deny, {len(ALLOW)} allow, 7 fail-open).")


if __name__ == "__main__":
    main()
