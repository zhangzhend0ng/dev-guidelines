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

Packs can be exported as a repository slice or zip artifact:

```bash
python scripts/export_pack.py cpp-testing --out dist --zip
```

The export contains a repository slice with:

- selected pack manifests and dependency manifests
- every included harness path
- required validation/index scripts
- `.dev-guidelines-installed.yml`
- `packs/index.yml`
- optional `<pack>.zip` and `<pack>.zip.sha256`

Consumers can validate an exported pack from the export root:

```bash
python scripts/validate.py --installed --json
python scripts/generate_index.py --installed --output /tmp/index.md
```
