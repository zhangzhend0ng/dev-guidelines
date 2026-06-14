# Harness Pack Design

## Goal

Allow users to install only the harness modules they need while keeping the repository usable as a monorepo.

## Pack Manifest

Each pack lives under `packs/<pack-id>/pack.yml`.

```yaml
id: cpp-testing
title: C++ Testing Harness Pack
version: "2026.06"
requires:
  - common-core
includes:
  - cpp/testing/static-analysis.md
  - cpp/testing/sanitizers.md
```

## Installed State

`scripts/install_pack.py` writes `.dev-guidelines-installed.yml`:

```yaml
installed_packs:
  - common-core
  - cpp-testing
installed_paths:
  - common/code-review/harness-driven-review.md
  - cpp/testing/static-analysis.md
```

## Validation Semantics

- Default validation still scans all harnesses in the monorepo.
- `--pack <id>` validates only that pack and its dependencies.
- `--installed` validates only paths in `.dev-guidelines-installed.yml`.
- Cross-pack `related` links outside the selected path set are warnings, not errors, when validating installed subsets.

## Distribution

Initial distribution is monorepo + manifest + install script. Release zip artifacts can be added later without changing the manifest schema.

