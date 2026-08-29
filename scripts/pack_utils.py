"""Utilities for harness pack manifests."""

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
PACKS_DIR = ROOT / "packs"
INSTALLED_PATH = ROOT / ".dev-guidelines-installed.yml"

# Directories under ROOT that never contain harnesses. Shared by every script
# that walks the repo for harness files (validate.py, generate_index.py,
# check_review_signals.py) so a single edit stays consistent across all of them.
# Drift here would let one script see a harness another skips (or vice versa).
HARNESS_SKIP_DIRS = {".git", ".claudine", "archive", "templates", "docs", ".github"}


def load_pack(pack_id):
    path = PACKS_DIR / pack_id / "pack.yml"
    if not path.exists():
        raise KeyError(f"unknown pack: {pack_id}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    data["_path"] = path.relative_to(ROOT).as_posix()  # posix: goes into packs/index.yml (machine-crossing)
    return data


def list_packs():
    packs = []
    if not PACKS_DIR.exists():
        return packs
    for manifest in sorted(PACKS_DIR.glob("*/pack.yml")):
        data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
        data["_path"] = manifest.relative_to(ROOT).as_posix()  # posix: goes into packs/index.yml (machine-crossing)
        packs.append(data)
    return packs


def resolve_packs(pack_ids):
    resolved = []
    seen = set()

    def visit(pack_id):
        if pack_id in seen:
            return
        pack = load_pack(pack_id)
        for dep in pack.get("requires", []) or []:
            visit(dep)
        seen.add(pack_id)
        resolved.append(pack)

    for pack_id in pack_ids:
        visit(pack_id)
    return resolved


def installed_paths_for(pack_ids):
    paths = []
    seen = set()
    for pack in resolve_packs(pack_ids):
        for item in pack.get("includes", []) or []:
            if item not in seen:
                seen.add(item)
                paths.append(item)
    return paths


def read_installed():
    if not INSTALLED_PATH.exists():
        return None
    return yaml.safe_load(INSTALLED_PATH.read_text(encoding="utf-8"))


def pack_index():
    items = []
    for pack in list_packs():
        items.append(
            {
                "id": pack["id"],
                "title": pack["title"],
                "version": pack["version"],
                "requires": pack.get("requires", []) or [],
                "manifest": pack["_path"],
            }
        )
    return {"packs": items}
