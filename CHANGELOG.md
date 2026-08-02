# 변경 기록

[English](CHANGELOG.en.md)

## Unreleased

- 아직 릴리스되지 않은 변경 사항이 없습니다.

## 0.2.0 - 2026-08-02

- 세 개의 작업 유형 중심 스킬을 `$judgment-craft`, `$judgment-repair` 두 개의 증거 중심 역할로 재편했습니다.
- `$judgment-craft`는 중요한 약속 전에 실제 결과와 만나는 최소 행동을 선택하고 `preserve`, `narrow`, `redirect`를 판정합니다.
- `$judgment-repair`는 명시적 정정뿐 아니라 관찰된 반증과 같은 메커니즘의 재발에서도 현재 판단을 수리합니다.
- `$practical-judgment`, `$calibrate-judgment`, `$friction-distillation` 호출자는 각각 새 두 스킬의 activation 경계로 이전해야 합니다.
- 세션 사례 재생에서 알려진 실패 3개를 막고 정상 대조 3개를 보존했습니다. 이는 제한된 회귀 검증이며 일반적 효과의 증명은 아닙니다.

## 0.1.0 - 2026-07-29

- Judgment Craft 최초 릴리스.
- `$practical-judgment`, `$calibrate-judgment`, `$friction-distillation` 스킬 포함.
- 직접 판단, 정정 재보정, 반복 마찰 대응의 기본 composition 계약 정의.
