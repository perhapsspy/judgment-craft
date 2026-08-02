# Contributing

[한국어](CONTRIBUTING.md)

## Change Ownership

Content owner first. Edit the canonical plugin copy directly under `plugins/judgment-craft`. Do not add `sources.lock`, `sync_skills`, generated snapshots, or mirror flows.

Before changing the product promise, skill roles, or activation boundaries, update [docs/PRODUCT.md](docs/PRODUCT.md).

## Version Rules

- Patch: compatible wording, explanation, validation, or documentation fixes that preserve the existing activation and behavior contract.
- Pre-1.0 Minor: experimental changes that may be incompatible, including skill additions or removals, material trigger changes, role redesigns, or starter prompt changes. Record the migration path in the changelog.
- Post-1.0 Major: a source or package contract break, canonical plugin path change, or public contract break relied on by callers or marketplace consumers.

A repository-root operations-doc change does not require an immediate plugin release. Apply the classification above when selecting the version for the next release.

## Validation

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate_plugin.py
git diff --check
```

## Release

1. Run validation.
2. Update the version in `plugins/judgment-craft/.codex-plugin/plugin.json` and both changelogs.
3. Apply the verified change to `main` and confirm that main CI passes.
4. Create an immutable `v<version>` tag on that exact commit.
5. Confirm the release workflow checks `--release-tag v<version>` and completes GitHub release creation.
6. Update the `perhapsspy/codex-plugins` marketplace pin to the release commit full SHA.
7. Run remote marketplace validation and an install round trip.

A PR is not a required release step. Use one only when separate review or collaboration is useful.

## Rollback

Re-pin the marketplace entry to the last validated release commit full SHA. Never move or overwrite a published tag. Fix forward and issue a new patch or minor release.

## Explicit Exclusions

While the plugin and skills share one canonical repo, do not add `sources.lock`, `sync_skills`, generated snapshots, or `THIRD_PARTY_NOTICES`.
