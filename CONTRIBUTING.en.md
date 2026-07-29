# Contributing

[한국어](CONTRIBUTING.md)

## Change Ownership

Content owner first. Edit the canonical plugin copy directly under `plugins/judgment-craft`. Do not add `sources.lock`, `sync_skills`, generated snapshots, or mirror flows.

Before changing the product promise, skill roles, activation model, or composition meaning, update [docs/PRODUCT.md](docs/PRODUCT.md).

## Version Rules

- Patch: compatible wording, explanation, typo, validation, or documentation fixes that preserve the existing activation and composition contract.
- Minor: skill additions or removals, material trigger changes, composition role changes, or starter prompt changes.
- Major candidate: a source/package contract break, canonical plugin path change, or public contract break that installers or marketplace consumers rely on.

## Validation

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate_plugin.py
git diff --check
```

## Release

1. Run validation.
2. Update the version in `plugins/judgment-craft/.codex-plugin/plugin.json` and both changelogs.
3. Open a PR and pass CI.
4. Create an immutable `v<version>` tag on the same merged commit.
5. Confirm the release workflow checks `--release-tag v<version>` and completes GitHub release creation.
6. Update the `perhapsspy/codex-plugins` marketplace pin to the release commit full SHA.
7. Run remote marketplace validation and an install round trip.

## Rollback

Re-pin the marketplace entry to the last validated release commit full SHA. Never move or overwrite a published tag. Fix forward and issue a new patch or minor release.

## Explicit Exclusions

While the plugin and skills share one canonical repo, do not add `sources.lock`, `sync_skills`, generated snapshots, or `THIRD_PARTY_NOTICES`.
