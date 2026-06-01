#!/usr/bin/env python3
"""
collect-context.py — Collect work context for a given date (cross-platform)
Usage: python collect-context.py <YYYY-MM-DD> [workdir]
Example: python collect-context.py 2026-05-08 /path/to/workspace
"""

import os
import sys
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Fix encoding for Windows console and subprocess output
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TARGET_DATE = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d")
WORKDIR = sys.argv[2] if len(sys.argv) > 2 else "."
HOME_DIR = Path(os.environ.get("USERPROFILE", os.environ.get("HOME", "~"))).expanduser()

try:
    target_dt = datetime.strptime(TARGET_DATE, "%Y-%m-%d")
    next_dt = target_dt + timedelta(days=1)
except ValueError:
    print(f"Invalid date format: {TARGET_DATE}, expected YYYY-MM-DD")
    sys.exit(1)

target_ts = target_dt.timestamp()
next_ts = next_dt.timestamp()

def file_modified_on_date(filepath):
    try:
        mtime = os.path.getmtime(filepath)
        return target_ts <= mtime < next_ts
    except OSError:
        return False

def classify_file(filepath):
    ext = Path(filepath).suffix.lower().lstrip(".")
    mapping = {
        "md": "DOC", "pdf": "DOC", "docx": "DOC", "txt": "DOC",
        "py": "CODE", "js": "CODE", "ts": "CODE", "go": "CODE", "java": "CODE",
        "json": "DATA", "csv": "DATA", "xlsx": "DATA",
        "yaml": "CONFIG", "yml": "CONFIG", "toml": "CONFIG",
    }
    return mapping.get(ext, "FILE")

print(f"=== Work Context for {TARGET_DATE} ===\n")

# 1. Memory files modified on target date
print(f"--- Memory Files (modified {TARGET_DATE}) ---")
memory_root = HOME_DIR / ".claude" / "projects"
if memory_root.exists():
    for mem_file in sorted(memory_root.rglob("memory/*.md")):
        if file_modified_on_date(mem_file):
            print(f"  [MEM] {mem_file}")
print()

# 2. Sub-project .claude directories
print("--- Sub-project .claude dirs ---")
workdir = Path(WORKDIR).resolve()
for claude_dir in sorted(workdir.glob("*/*/.claude")):
    if ".git" not in str(claude_dir):
        print(f"  [DIR] {claude_dir}")
for claude_dir in sorted(workdir.glob("*/.claude")):
    print(f"  [DIR] {claude_dir}")
print()

# 3. Files changed on target date
SKIP_DIRS = {".git", "node_modules", ".claude", "__pycache__", ".playwright-mcp", ".venv", "venv"}

print(f"--- Files Changed ({TARGET_DATE}) ---")
for root, dirs, files in os.walk(workdir):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        filepath = os.path.join(root, f)
        if file_modified_on_date(filepath):
            tag = classify_file(filepath)
            rel = os.path.relpath(filepath, workdir)
            print(f"  [{tag}] {rel}")
print()

# 4. Existing work diaries
print("--- Existing Work Diaries ---")
diary_dir = workdir / "工作日记"
if diary_dir.exists():
    for d in sorted(diary_dir.glob("*.md")):
        print(f"  [DIARY] {d.name}")
else:
    print("  (no 工作日记 directory found)")
print()

# 5. Git commits on target date
print(f"--- Git Commits ({TARGET_DATE}) ---")
git_dirs = []
if (workdir / ".git").exists():
    git_dirs.append(("", workdir))
else:
    for sub in sorted(workdir.iterdir()):
        if sub.is_dir() and (sub / ".git").exists():
            git_dirs.append((sub.name, sub))

for proj_name, git_dir in git_dirs:
    label = f"GIT:{proj_name}" if proj_name else "GIT"
    try:
        result = subprocess.run(
            ["git", "log", "--oneline",
             f"--after={TARGET_DATE} 00:00:00",
             f"--before={TARGET_DATE} 23:59:59", "--all"],
            cwd=str(git_dir), capture_output=True, text=True,
            timeout=10, encoding="utf-8", errors="replace"
        )
        for line in result.stdout.strip().split("\n"):
            if line:
                print(f"  [{label}] {line}")
    except Exception:
        pass

print(f"\n=== Collection Complete ===")
