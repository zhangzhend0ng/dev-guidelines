#!/usr/bin/env python3
"""Record installed harness packs in .dev-guidelines-installed.yml."""

import argparse

import yaml

from pack_utils import INSTALLED_PATH, installed_paths_for, resolve_packs


def main():
    parser = argparse.ArgumentParser(description="Install harness packs")
    parser.add_argument("packs", nargs="+", help="Pack IDs to install")
    args = parser.parse_args()

    resolved = resolve_packs(args.packs)
    installed = {
        "installed_packs": [pack["id"] for pack in resolved],
        "installed_paths": installed_paths_for(args.packs),
    }
    INSTALLED_PATH.write_text(
        yaml.safe_dump(installed, sort_keys=False), encoding="utf-8"
    )
    print(f"Wrote {INSTALLED_PATH}")
    print("Installed packs: " + ", ".join(installed["installed_packs"]))


if __name__ == "__main__":
    main()

