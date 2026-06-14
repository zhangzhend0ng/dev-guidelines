#!/usr/bin/env python3
"""Export harness packs to a distributable directory or zip archive."""

import argparse
import hashlib
import shutil
import zipfile
from pathlib import Path

import yaml

from pack_utils import ROOT, installed_paths_for, pack_index, resolve_packs


def copy_file(relpath, out_root):
    source = ROOT / relpath
    if not source.exists():
        raise FileNotFoundError(f"pack path does not exist: {relpath}")
    target = out_root / relpath
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def write_yaml(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def make_zip(source_dir, zip_path):
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source_dir))


def export_pack(pack_ids, out_dir, zip_output=False):
    resolved = resolve_packs(pack_ids)
    export_id = "-".join(pack_ids)
    export_root = out_dir / export_id
    if export_root.exists():
        shutil.rmtree(export_root)
    export_root.mkdir(parents=True)

    installed_paths = installed_paths_for(pack_ids)
    manifest_paths = [pack["_path"] for pack in resolved]
    support_paths = [
        "scripts/pack_utils.py",
        "scripts/install_pack.py",
        "scripts/list_packs.py",
        "scripts/validate.py",
        "scripts/generate_index.py",
        "scripts/check_ai_protocol.py",
        "scripts/run_ai_protocol_check.py",
        "scripts/test_ai_protocol.py",
        "scripts/check_plan_protocol.py",
        "scripts/check_debug_report.py",
        "scripts/test_plan_debug_protocol.py",
    ]

    for relpath in manifest_paths + installed_paths + support_paths:
        if (ROOT / relpath).exists():
            copy_file(relpath, export_root)

    installed = {
        "installed_packs": [pack["id"] for pack in resolved],
        "installed_paths": installed_paths,
    }
    write_yaml(export_root / ".dev-guidelines-installed.yml", installed)
    write_yaml(export_root / "packs" / "index.yml", pack_index())

    metadata = {
        "export_id": export_id,
        "packs": [pack["id"] for pack in resolved],
        "paths": installed_paths,
    }
    write_yaml(export_root / "export.yml", metadata)

    result = {"directory": str(export_root)}
    if zip_output:
        zip_path = out_dir / f"{export_id}.zip"
        make_zip(export_root, zip_path)
        checksum_path = out_dir / f"{export_id}.zip.sha256"
        checksum_path.write_text(
            f"{sha256_file(zip_path)}  {zip_path.name}\n", encoding="utf-8"
        )
        result["zip"] = str(zip_path)
        result["sha256"] = str(checksum_path)
    return result


def main():
    parser = argparse.ArgumentParser(description="Export harness packs")
    parser.add_argument("packs", nargs="+", help="Pack IDs to export")
    parser.add_argument("--out", default="dist", help="Output directory")
    parser.add_argument("--zip", action="store_true", help="Create a zip archive")
    args = parser.parse_args()

    result = export_pack(args.packs, Path(args.out), args.zip)
    print(f"Exported directory: {result['directory']}")
    if "zip" in result:
        print(f"Exported zip: {result['zip']}")
        print(f"Checksum: {result['sha256']}")


if __name__ == "__main__":
    main()
