#!/usr/bin/env python3
"""Regression tests for config/policy.yml externalization (Phase 5).

Covers:
- load_policy parses the real repo policy into the expected rule dicts
- every invalid-policy shape raises PolicyError (missing file, invalid
  YAML, missing destructive_patterns, unknown subcommand, missing required
  field, wrong type, unknown field)
- fail-closed end-to-end: with a missing policy the hook denies EVERY git
  command (including safe ones) with a fail-closed reason, while non-git
  commands still pass
- explicit --policy override selects an alternate policy file
- the default (repo) policy reproduces the Phase 1 behavior spot checks
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "hooks"))
from block_destructive_git import PolicyError, load_policy  # noqa: E402

HOOK = ROOT / "scripts" / "hooks" / "block_destructive_git.py"
REPO_POLICY = ROOT / "config" / "policy.yml"

VALID_YAML = """
destructive_patterns:
  - subcommand: checkout
    path_separator: true
    allow_patch: true
  - subcommand: reset
    flags: [hard]
"""


def run_hook(command, extra_args=()):
    payload = {"tool_name": "Bash", "tool_input": {"command": command}}
    return subprocess.run(
        [sys.executable, str(HOOK), *extra_args],
        input=json.dumps(payload),
        capture_output=True, text=True, check=False,
    )


def main():
    errors = []

    # Real repo policy parses into the Phase 1 rule set.
    rules = load_policy(REPO_POLICY)
    by_sub = {r["subcommand"]: r for r in rules}
    if set(by_sub) != {"checkout", "reset", "clean", "stash", "branch"}:
        errors.append(f"repo policy rules wrong: {sorted(by_sub)}")
    if not (by_sub["checkout"]["allow_patch"] and by_sub["reset"]["flags"] == ["hard"]
            and by_sub["clean"]["force"] and by_sub["stash"]["subcommands"] == ["drop", "clear"]
            and by_sub["branch"]["force_delete"]):
        errors.append(f"repo policy values drifted: {by_sub}")

    # Invalid policy shapes all fail.
    with tempfile.TemporaryDirectory() as tmp:
        bad_cases = {
            "missing file": str(Path(tmp) / "nope.yml"),
            "invalid yaml": None,  # filled below
            "no destructive_patterns": "foo: bar\n",
            "unknown subcommand": "destructive_patterns:\n  - subcommand: rebase\n",
            "missing required field": ("destructive_patterns:\n"
                                        "  - subcommand: checkout\n"
                                        "    path_separator: true\n"),
            "wrong type": ("destructive_patterns:\n"
                           "  - subcommand: reset\n"
                           "    flags: hard\n"),
            "unknown field": ("destructive_patterns:\n"
                              "  - subcommand: clean\n"
                              "    force: true\n"
                              "    extra: 1\n"),
        }
        bad_path = Path(tmp) / "broken.yml"
        bad_path.write_text("patterns: [unclosed\n", encoding="utf-8")
        bad_cases["invalid yaml"] = str(bad_path)

        for label, target in bad_cases.items():
            try:
                load_policy(target)
                errors.append(f"invalid policy accepted ({label})")
            except PolicyError:
                pass

    # Fail-closed end-to-end: missing policy denies all git, passes non-git.
    with tempfile.TemporaryDirectory() as tmp:
        missing = str(Path(tmp) / "absent.yml")
        r = run_hook("git reset --hard", ["--policy", missing])
        if r.returncode != 2 or "fail-closed" not in r.stderr:
            errors.append(f"fail-closed deny missing for destructive git: rc={r.returncode}")
        r = run_hook("git status", ["--policy", missing])
        if r.returncode != 2 or "fail-closed" not in r.stderr:
            errors.append("fail-closed must deny even safe git commands")
        r = run_hook("ls -la", ["--policy", missing])
        if r.returncode != 0:
            errors.append("fail-closed must not affect non-git commands")
        r = run_hook("git status", ["--policy", missing, "--output", "json"])
        decision = json.loads(r.stdout)["hookSpecificOutput"]
        if decision.get("permissionDecision") != "deny":
            errors.append("fail-closed json protocol did not deny")

    # Default repo policy: Phase 1 behavior spot checks via CLI.
    for cmd in ("git reset --hard", "git clean -fd", "git stash clear"):
        r = run_hook(cmd)
        if r.returncode != 2:
            errors.append(f"default policy regression: {cmd!r} not denied")
    for cmd in ("git checkout -p HEAD~1 -- f", "git status", "git stash push -m w"):
        r = run_hook(cmd)
        if r.returncode != 0:
            errors.append(f"default policy regression: {cmd!r} wrongly denied")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        sys.exit(1)

    print("Policy config tests passed "
          "(repo policy parse, 7 invalid shapes, fail-closed e2e, default spot checks).")


if __name__ == "__main__":
    main()
