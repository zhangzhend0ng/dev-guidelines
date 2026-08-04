#!/usr/bin/env python3
"""Generate the INDEX.md auto-generation zone from harness frontmatter.

Usage:
    python scripts/generate_index.py [--check]

With --check: exit 1 if INDEX.md is out of sync with current harnesses.
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

from pack_utils import installed_paths_for, read_installed, HARNESS_SKIP_DIRS

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "INDEX.md"
START_MARKER = "<!-- INDEX_START -->"
END_MARKER = "<!-- INDEX_END -->"

CATEGORY_ORDER = [
    "Security", "Design", "Correctness", "Resource Management",
    "Testing", "Performance", "Tooling/Process", "Cross-Language",
]


def parse_frontmatter(filepath):
    import yaml
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None


def find_harnesses():
    harnesses = []
    for md_path in ROOT.rglob("*.md"):
        parts = md_path.relative_to(ROOT).parts
        if parts[0] in HARNESS_SKIP_DIRS:
            continue
        fm = parse_frontmatter(md_path)
        if fm and fm.get("type") == "harness":
            harnesses.append((str(md_path.relative_to(ROOT)), fm))
    return harnesses


def selected_paths_from_args(args):
    if args.installed:
        installed = read_installed()
        if not installed:
            print("ERROR: .dev-guidelines-installed.yml not found", file=sys.stderr)
            sys.exit(1)
        return set(installed.get("installed_paths", []) or [])
    if args.pack:
        return set(installed_paths_for(args.pack))
    return None


def build_index_table(harnesses):
    by_category = defaultdict(list)
    for relpath, fm in harnesses:
        cat = fm.get("category", "Uncategorized")
        by_category[cat].append((relpath, fm))

    lines = []
    sorted_cats = [c for c in CATEGORY_ORDER if c in by_category]
    sorted_cats += sorted(c for c in by_category if c not in CATEGORY_ORDER)

    for cat in sorted_cats:
        lines.append(f"### {cat}")
        lines.append("")
        lines.append("| ID | Title | Language | Tier | Status | Version |")
        lines.append("|----|-------|----------|------|--------|---------|")
        for relpath, fm in sorted(
            by_category[cat], key=lambda x: x[1].get("title", "")
        ):
            hid = fm.get("id", "-")
            title = f"[{fm.get('title', '-')}]({relpath})"
            lang = fm.get("language", "-")
            tier = fm.get("tier", "-")
            status = fm.get("status", "-")
            version = fm.get("version", "-")
            lines.append(
                f"| {hid} | {title} | {lang} | {tier} | {status} | {version} |"
            )
        lines.append("")
    return "\n".join(lines)


def read_index():
    if not INDEX_PATH.exists():
        return None
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(description="Generate INDEX.md")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--pack", action="append", help="Generate index for pack and dependencies")
    parser.add_argument("--installed", action="store_true", help="Generate index for installed pack set")
    parser.add_argument("--output", help="Write generated index to another file")
    args = parser.parse_args()

    harnesses = find_harnesses()
    selected_paths = selected_paths_from_args(args)
    if selected_paths is not None:
        harnesses = [
            (path, fm) for path, fm in harnesses if path in selected_paths
        ]
    new_table = build_index_table(harnesses)
    index_content = read_index()

    if not index_content:
        updated = (
            "# Harness Index\n\n"
            "## All Harnesses by Category\n\n"
            f"{START_MARKER}\n{new_table}\n{END_MARKER}\n"
        )
    else:
        start_pos = index_content.find(START_MARKER)
        end_pos = index_content.find(END_MARKER)
        if start_pos == -1 or end_pos == -1:
            print("ERROR: INDEX.md missing START/END markers")
            sys.exit(1)
        updated = (
            index_content[: start_pos + len(START_MARKER)]
            + "\n"
            + new_table
            + "\n"
            + index_content[end_pos:]
        )

    if args.output:
        Path(args.output).write_text(updated, encoding="utf-8")
        print(f"Written {args.output}")
    elif args.check:
        current = read_index()
        if current != updated:
            print("ERROR: INDEX.md is out of sync. Run scripts/generate_index.py")
            sys.exit(1)
        print("INDEX.md is up to date.")
    else:
        with open(INDEX_PATH, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"Written {INDEX_PATH}")


if __name__ == "__main__":
    main()
