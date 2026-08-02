# Judgment Craft

Judgment Craft is a Codex plugin that grounds consequential choices in real outcomes and repairs current action after correction or contrary evidence.

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
| `$judgment-craft` | Choose or revalidate a materially costly or hard-to-reverse direction before commitment. |
| `$judgment-repair` | A user correction, observed contradiction, or repeated same-mechanism failure invalidates the current judgment. |

For example, use `$judgment-craft` before promoting a technical demo to a product milestone. If observed use later contradicts its premise, `$judgment-repair` replaces the recommendation and next action.

After installation or update, start a new Codex task so the refreshed skills are loaded.

[docs/PRODUCT.md](docs/PRODUCT.md) owns the product promise and activation boundaries. Follow [CONTRIBUTING.en.md](CONTRIBUTING.en.md) for contribution, validation, and release procedures.

## Development

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate_plugin.py
git diff --check
```

## License

[MIT](LICENSE)
