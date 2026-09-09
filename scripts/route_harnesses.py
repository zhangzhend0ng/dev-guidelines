#!/usr/bin/env python3
"""Path-driven harness routing: assign harnesses to files via `apply_globs`.

Downsinks harness selection from "model scans INDEX.md and picks" to a
deterministic path lookup. Each harness's frontmatter may declare an optional
`apply_globs: []` list; a file matching any glob means that harness is
applicable. This is the L1 (context routing) layer of the constraint stack -
the router output is the STARTING point for harness selection, not a
replacement for human judgment (fallback: manual INDEX.md lookup).

Glob semantics (gitignore-flavored, matched against repo-relative POSIX paths):
- `*` matches within one path segment, `**` spans segments, `?` one non-`/` char,
  `[...]` character classes (leading `!` negates).
- A pattern containing `/` is anchored to the repo root; a bare pattern
  (`*.py`) matches a SINGLE SEGMENT anywhere in the path (basename semantics,
  including ancestor directories: `agents/` matches pattern `*agent*`).
- A trailing `/` means "anything under this directory".
- A leading `/` just anchors (redundant with the slash rule).

Usage:
    python scripts/route_harnesses.py --files <path...> [--json]

Exit codes: 0 = every file matched at least one harness;
            1 = at least one file matched nothing (fallback to INDEX.md).
"""

import argparse
import json
import re
import sys
from pathlib import Path

from generate_index import find_harnesses


def glob_to_regex(pattern):
    """Compile one gitignore-flavored glob into an anchored regex."""
    if not isinstance(pattern, str) or not pattern.strip():
        raise ValueError("glob pattern must be a non-empty string")
    pat = pattern.strip()
    dir_only = pat.endswith("/")
    if dir_only:
        pat = pat.rstrip("/")
    if not pat:
        raise ValueError(f"glob pattern is only a slash: {pattern!r}")
    anchored = "/" in pat
    if pat.startswith("/"):
        pat = pat.lstrip("/")
        anchored = True
    inner = []
    i, n = 0, len(pat)
    while i < n:
        c = pat[i]
        if c == "*":
            if pat[i:i + 3] == "**/":
                inner.append("(?:[^/]+/)*")
                i += 3
            elif pat[i:i + 2] == "**":
                inner.append(".*")
                i += 2
            else:
                inner.append("[^/]*")
                i += 1
        elif c == "?":
            inner.append("[^/]")
            i += 1
        elif c == "[":
            j = i + 1
            if j < n and pat[j] == "!":
                j += 1
            if j < n and pat[j] == "]":  # POSIX: `]` first in class is literal
                j += 1
            j = pat.find("]", j)
            if j == -1:
                raise ValueError(f"unterminated character class in glob: {pattern!r}")
            cls = pat[i + 1:j]
            if cls.startswith("!"):
                cls = "^" + cls[1:]
            if cls.startswith("]"):
                cls = "\\]" + cls[1:]
            inner.append("[" + cls + "]")
            i = j + 1
        else:
            inner.append(re.escape(c))
            i += 1
    body = "".join(inner)
    if anchored:
        return re.compile("^" + body + "$")
    # bare or directory pattern: matches any single segment, descendants allowed
    return re.compile("^(?:.*/)?" + body + "(?:/.*)?$")


def compile_globs(patterns):
    return [glob_to_regex(p) for p in patterns]


def normalize_path(path):
    """Canonicalize any input path to a clean repo-relative POSIX path."""
    p = str(path).replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    return p.lstrip("/")


def path_matches(compiled, path):
    p = normalize_path(path)
    return any(rx.match(p) for rx in compiled)


def build_routes(harnesses):
    """(id, compiled_globs) for every harness whose apply_globs parse."""
    routes = []
    for rel, fm in harnesses:
        globs = fm.get("apply_globs")
        if not isinstance(globs, list) or not globs:
            continue
        try:
            routes.append((fm.get("id", rel), compile_globs(globs)))
        except ValueError:
            # invalid globs are validate.py's job to report; router must not crash
            continue
    return routes


def route_files(files, routes):
    """{normalized path: [harness id, ...]} plus the list of unmatched paths."""
    result, unmatched = {}, []
    for f in files:
        p = normalize_path(f)
        hit = [hid for hid, rxs in routes if path_matches(rxs, p)]
        result[p] = hit
        if not hit:
            unmatched.append(p)
    return result, unmatched


def main():
    ap = argparse.ArgumentParser(description="Route files to harnesses via apply_globs")
    ap.add_argument("--files", nargs="+", required=True, help="file paths to route")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    routes = build_routes(find_harnesses())
    routed, unmatched = route_files(args.files, routes)

    if args.json:
        print(json.dumps({
            "routes": [{"path": p, "harnesses": h} for p, h in routed.items()],
            "unmatched": unmatched,
        }, indent=2))
    else:
        for p, hit in routed.items():
            if hit:
                print(f"{p} -> {'; '.join(hit)}")
            else:
                print(f"{p} -> (no match)")

    if unmatched:
        print(
            "无命中的路径：回退到 INDEX.md 手选适用 harness（路由表只覆盖已回填 apply_globs 的目录）。",
            file=sys.stderr,
        )
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
