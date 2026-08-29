#!/usr/bin/env python3
"""List available harness packs."""

import sys

from pack_utils import PACKS_DIR, list_packs


def main():
    if not PACKS_DIR.exists():
        print(f"WARNING: packs directory missing: {PACKS_DIR}", file=sys.stderr)
    print("| ID | Title | Version | Requires |")
    print("|----|-------|---------|----------|")
    for pack in list_packs():
        requires = ", ".join(pack.get("requires", []) or [])
        # .get fallbacks: a malformed manifest must not kill the whole listing
        pid = pack.get("id", "?")
        title = pack.get("title", "?")
        version = pack.get("version", "?")
        if "?" in (pid, title, version):
            print(f"WARNING: malformed manifest near id={pid!r}", file=sys.stderr)
        print(f"| {pid} | {title} | {version} | {requires} |")


if __name__ == "__main__":
    main()

