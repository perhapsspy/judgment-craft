# Changelog

[한국어](CHANGELOG.md)

## Unreleased

- No unreleased changes yet.

## 0.2.0 - 2026-08-02

- Replaced three task-type skills with two evidence-centered roles: `$judgment-craft` and `$judgment-repair`.
- `$judgment-craft` selects the smallest action that reaches real evidence before consequential commitment and returns `preserve`, `narrow`, or `redirect`.
- `$judgment-repair` repairs current judgment after explicit correction, observed contradiction, or repeated failure with the same mechanism.
- Callers of `$practical-judgment`, `$calibrate-judgment`, and `$friction-distillation` must migrate to the activation boundaries of the two new skills.
- Session replay blocked three known failures and preserved three controls. This is bounded regression evidence, not proof of general effectiveness.

## 0.1.0 - 2026-07-29

- Initial Judgment Craft release.
- Includes `$practical-judgment`, `$calibrate-judgment`, and `$friction-distillation`.
- Defines the baseline composition contract for direct judgment, correction recalibration, and recurring friction response.
