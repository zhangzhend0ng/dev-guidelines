#!/usr/bin/env python3
"""Regression tests for scripts/route_harnesses.py (Phase 2).

Covers:
- glob_to_regex translation: bare basename semantics (including ancestor
  directory segments), root anchoring, `**` spanning, trailing `/` directory
  prefixes, `?` and `[...]` classes, leading `/` anchors
- invalid patterns raise ValueError (validate.py's apply_globs gate)
- Windows backslash and `./` input normalization
- end-to-end CLI routing on the real pilot backfill (16 harnesses),
  including multi-hit files and the no-match exit 1 + fallback hint
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from route_harnesses import (  # noqa: E402
    compile_globs,
    glob_to_regex,
    normalize_path,
    path_matches,
    route_files,
)

ROUTER = ROOT / "scripts" / "route_harnesses.py"


def matches(pattern, path):
    return path_matches(compile_globs([pattern]), path)


def main():
    errors = []

    # --- glob translation -------------------------------------------------
    cases = [
        # bare `*.py`: final segment, plus ancestor-segment semantics
        ("*.py", "a.py", True),
        ("*.py", "src/a.py", True),
        ("*.py", "x/y/a.py", True),
        ("*.py", "a.pyc", False),
        ("*.py", "a.py.bak", False),
        # bare pattern also matches a matching ANCESTOR directory
        ("*agent*", "agent/tools.py", True),
        ("*agent*", "x/agents/tools.py", True),
        ("*agent*", "my_agent.py", True),
        ("*agent*", "src/main.py", False),
        # anchored via `/`: root-relative only
        ("src/**", "src/a.py", True),
        ("src/**", "src/x/y.py", True),
        ("src/**", "src", False),
        ("src/**", "x/src/a.py", False),
        ("src/*.py", "src/a.py", True),
        ("src/*.py", "src/x/a.py", False),
        # `**/name` matches at any depth including root
        ("**/tests/**", "tests/x.py", True),
        ("**/tests/**", "a/b/tests/x.py", True),
        ("**/tests/**", "a/b/testsx.py", False),
        # trailing `/`: anything under the directory, at any depth
        ("build/", "build/x.o", True),
        ("build/", "x/build/y", True),
        ("build/", "buildx/y", False),
        # leading `/` = anchor
        ("/dist", "dist", True),
        ("/dist", "x/dist", False),
        # `?` one char within a segment
        ("?.cpp", "a.cpp", True),
        ("?.cpp", "ab.cpp", False),
        # character classes
        ("[abc].py", "b.py", True),
        ("[abc].py", "d.py", False),
        ("[!a].py", "b.py", True),
        ("[!a].py", "a.py", False),
    ]
    for pattern, path, expected in cases:
        got = matches(pattern, path)
        if got != expected:
            errors.append(f"glob {pattern!r} vs {path!r}: expected {expected}, got {got}")

    for bad in ("abc[", "", "   ", "/", None, 42):
        try:
            glob_to_regex(bad)
            errors.append(f"invalid glob accepted: {bad!r}")
        except ValueError:
            pass

    # --- normalization ----------------------------------------------------
    if normalize_path("src\\memory\\a.cpp") != "src/memory/a.cpp":
        errors.append("backslash normalization failed")
    if normalize_path("./src/a.py") != "src/a.py":
        errors.append("./ prefix not stripped")
    if not matches("**/memory/**", "src\\memory\\a.cpp"):
        errors.append("backslash path not matched after normalization")

    # --- end-to-end CLI on the real pilot backfill ------------------------
    sample = [
        "src/memory/arena.cpp",      # cpp/memory 三件套
        "src/smart_ptr_demo.cpp",    # ownership
        "tools/gen.py",              # type-hints（通用 *.py）
        "tests/test_router.py",      # type-hints + pytest
        "app/json_parser.dart",      # dart error-handling + json-boundaries
        "test/api_test.dart",        # dart 三件套
        "agent/tools.py",            # type-hints + tool-calling
        "docs/README.md",            # 无命中
    ]
    result = subprocess.run(
        [sys.executable, str(ROUTER), "--files", *sample, "--json"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 1:  # docs/README.md intentionally unmatched
        errors.append(f"router exit code: expected 1 (one unmatched), got {result.returncode}")
    if "INDEX.md" not in result.stderr:
        errors.append("no-match run missing INDEX.md fallback hint on stderr")

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        errors.append(f"router --json output unparseable: {result.stdout[:200]!r}")
        payload = {"routes": [], "unmatched": []}

    routed = {r["path"]: r["harnesses"] for r in payload.get("routes", [])}
    expectations = {
        "src/memory/arena.cpp": [
            "cpp-raii", "cpp-ownership", "cpp-move-semantics",
        ],
        "src/smart_ptr_demo.cpp": ["cpp-ownership"],
        "tools/gen.py": ["python-type-hints-mypy"],
        "tests/test_router.py": ["python-type-hints-mypy", "python-pytest-patterns"],
        "agent/tools.py": [
            "python-type-hints-mypy", "common-tool-calling-agent-control",
        ],
        "docs/README.md": [],
    }
    for path, expected_ids in expectations.items():
        got_ids = routed.get(path, None)
        if got_ids is None:
            errors.append(f"router output missing path {path!r}")
            continue
        if path == "docs/README.md":
            if got_ids:
                errors.append(f"{path} expected no match, got {got_ids}")
            continue
        for hid in expected_ids:
            if hid not in got_ids:
                errors.append(f"{path}: expected harness {hid}, got {got_ids}")

    dart_checks = [
        ("app/json_parser.dart", ["dart-error-handling", "dart-json-boundaries"]),
        ("test/api_test.dart",
         ["dart-error-handling", "dart-json-boundaries", "dart-testing"]),
    ]
    for path, expected_ids in dart_checks:
        for hid in expected_ids:
            if hid not in routed.get(path, []):
                errors.append(f"{path}: expected harness {hid}, got {routed.get(path)}")

    if payload.get("unmatched") != ["docs/README.md"]:
        errors.append(f"unmatched list wrong: {payload.get('unmatched')}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        sys.exit(1)

    print(f"Route harnesses tests passed "
          f"({len(cases)} glob cases, {len(sample)} e2e paths).")


if __name__ == "__main__":
    main()
