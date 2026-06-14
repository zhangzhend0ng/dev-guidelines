#!/usr/bin/env python3
"""List available harness packs."""

from pack_utils import list_packs


def main():
    print("| ID | Title | Version | Requires |")
    print("|----|-------|---------|----------|")
    for pack in list_packs():
        requires = ", ".join(pack.get("requires", []) or [])
        print(f"| {pack['id']} | {pack['title']} | {pack['version']} | {requires} |")


if __name__ == "__main__":
    main()

