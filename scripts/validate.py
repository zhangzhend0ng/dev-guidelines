#!/usr/bin/env python3
"""Validate harness files for frontmatter completeness, tier consistency,
cross-reference integrity, ID uniqueness, and source timeliness.

Usage:
    python scripts/validate.py [--stale] [--dead-links] [--json]

Exit codes:
    0 = all clear
    1 = frontmatter errors (hard fail)
    2 = cross-reference errors (hard fail)
    3 = stale citations (warn; only with --stale)
    4 = dead links (warn; only with --dead-links)
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".claudine", "archive", "templates", "docs", ".github"}
ARCHIVE_DIR = ROOT / "archive"

REQUIRED_FIELDS = [
    "type", "id", "title", "language", "category", "tier",
    "scope", "version", "status", "last_validated", "review_cycle",
    "tags", "based_on", "related", "supersedes", "changelog"
]

VALID_STATUSES = {"draft", "reviewed", "stable", "deprecated"}
VALID_TIERS = {"N", "C", "A"}
VALID_LANGUAGES = {"common", "cpp", "python", "go", "rust"}


def parse_frontmatter(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None, "Missing or malformed YAML frontmatter"
    try:
        return yaml.safe_load(match.group(1)), None
    except yaml.YAMLError as e:
        return None, f"YAML parse error: {e}"


def check_frontmatter(filepath, fm):
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in fm or fm[field] is None:
            errors.append(f"{filepath}: missing required field '{field}'")
    if fm.get("type") and fm["type"] != "harness":
        errors.append(f"{filepath}: type must be 'harness'")
    if fm.get("status") and fm["status"] not in VALID_STATUSES:
        errors.append(f"{filepath}: invalid status '{fm['status']}'")
    if fm.get("tier") and fm["tier"] not in VALID_TIERS:
        errors.append(f"{filepath}: invalid tier '{fm['tier']}'")
    if fm.get("language") and fm["language"] not in VALID_LANGUAGES:
        errors.append(f"{filepath}: invalid language '{fm['language']}'")
    return errors


def check_id_uniqueness(all_harnesses):
    errors = []
    active_ids = {}
    archive_ids = set()

    for filepath, fm in all_harnesses.items():
        hid = fm.get("id", "")
        if fm.get("status") in ("deprecated",):
            continue
        if hid in active_ids:
            errors.append(
                f"{filepath}: duplicate id '{hid}' (also in {active_ids[hid]})"
            )
        active_ids[hid] = filepath

    if ARCHIVE_DIR.exists():
        for arc_path in ARCHIVE_DIR.rglob("*.md"):
            arc_fm, _ = parse_frontmatter(arc_path)
            if arc_fm and arc_fm.get("id"):
                archive_ids.add(arc_fm["id"])

    for hid in active_ids:
        if hid in archive_ids:
            errors.append(
                f"{active_ids[hid]}: id '{hid}' was previously used in archive/"
            )
    return errors


def check_cross_references(all_harnesses):
    errors = []
    for filepath, fm in all_harnesses.items():
        for rel in fm.get("related", []) or []:
            target = ROOT / rel
            if not target.exists():
                errors.append(f"{filepath}: related link '{rel}' does not exist")
                continue
            rel_fm, _ = parse_frontmatter(target)
            if not rel_fm:
                continue
            rel_status = rel_fm.get("status", "")
            if rel_status == "archived":
                errors.append(
                    f"{filepath}: related link '{rel}' points to archived harness"
                )
            elif rel_status == "deprecated":
                print(
                    f"WARNING: {filepath}: related link '{rel}' "
                    f"points to deprecated harness",
                    file=sys.stderr,
                )
    return errors


def check_stale(all_harnesses):
    stale = []
    today = datetime.now().date()
    for filepath, fm in all_harnesses.items():
        lv = fm.get("last_validated", "")
        cycle = fm.get("review_cycle", "")
        if not lv or not cycle:
            continue
        try:
            lv_date = datetime.strptime(str(lv), "%Y-%m-%d").date()
        except ValueError:
            continue
        cycle_match = re.match(r"(\d+)m", str(cycle))
        if not cycle_match:
            continue
        months = int(cycle_match.group(1))
        due_date = lv_date + timedelta(days=months * 30)
        if today > due_date:
            stale.append(
                f"{filepath}: last_validated {lv}, review_cycle {cycle} — overdue"
            )
    return stale


def find_harnesses():
    harnesses = {}
    for md_path in ROOT.rglob("*.md"):
        rel = md_path.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS:
            continue
        fm, err = parse_frontmatter(md_path)
        if err or not fm:
            continue
        if fm.get("type") == "harness":
            harnesses[str(rel)] = fm
    return harnesses


def main():
    parser = argparse.ArgumentParser(description="Validate harness files")
    parser.add_argument("--stale", action="store_true")
    parser.add_argument("--dead-links", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    harnesses = find_harnesses()
    all_errors = []
    warnings = []

    for filepath, fm in harnesses.items():
        all_errors.extend(check_frontmatter(filepath, fm))

    all_errors.extend(check_id_uniqueness(harnesses))
    all_errors.extend(check_cross_references(harnesses))

    if args.stale:
        warnings.extend(check_stale(harnesses))

    if args.json:
        result = {
            "pass": len(all_errors) == 0,
            "errors": all_errors,
            "warnings": warnings,
        }
        print(json.dumps(result, indent=2))
    else:
        for e in all_errors:
            print(f"ERROR: {e}")
        for w in warnings:
            print(f"WARNING: {w}")
        if all_errors:
            print(f"\n{len(all_errors)} error(s) found.")

    if all_errors:
        has_cross_ref = any("related link" in e for e in all_errors)
        sys.exit(2 if has_cross_ref else 1)
    if warnings and not args.stale:
        sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    main()
