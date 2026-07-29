# Judgment Craft

Judgment Craft is a Codex plugin for bounded judgment: direct current recommendations, explicit recalibration after correction, and the smallest sufficient response to recurring friction.

Korean: [README.md](README.md)

## Install

```bash
codex plugin marketplace add perhapsspy/codex-plugins
codex plugin add judgment-craft@perhapsspy
```

Update:

```bash
codex plugin marketplace upgrade perhapsspy
codex plugin add judgment-craft@perhapsspy
```

Remove:

```bash
codex plugin remove judgment-craft@perhapsspy
```

## Skills

| Skill | Use when |
| --- | --- |
| `$practical-judgment` | You need a direct recommendation for a current choice or judgment. |
| `$calibrate-judgment` | You explicitly corrected the criteria, scope, or meaning of a prior judgment. |
| `$friction-distillation` | You need to choose the response level for recurring friction. |

When a corrected current judgment may also require recurrence prevention, use `$calibrate-judgment` first and then `$friction-distillation`.

Package path: `plugins/judgment-craft/`

The product promise and role boundaries are owned by [docs/PRODUCT.md](docs/PRODUCT.md). Follow [CONTRIBUTING.en.md](CONTRIBUTING.en.md) for changes. Keep [CONTRIBUTING.md](CONTRIBUTING.md) and [CHANGELOG.md](CHANGELOG.md) aligned.

After installation or update, start a new Codex task so the refreshed skills are loaded.

## Development

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate_plugin.py

## License
[MIT](LICENSE)
```
