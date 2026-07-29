# Judgment Craft

현재 판단을 명확히 하고, 사용자의 정정에 맞춰 재계산하며, 반복 마찰에 필요한 최소 대응을 고르는 3가지 스킬 패키지입니다.

## 설치

```bash
codex plugin marketplace add perhapsspy/codex-plugins
codex plugin add judgment-craft@perhapsspy
```

| 스킬 | 선택할 때 |
| --- | --- |
| `$practical-judgment` | 현재 선택에 대한 직접 권고가 필요할 때 |
| `$calibrate-judgment` | 이전 판단의 기준·범위·의미를 명시적으로 정정했을 때 |
| `$friction-distillation` | 반복 마찰의 재발 방지 대응 수준을 결정할 때 |

정정으로 현재 판단을 다시 계산한 뒤 재발 방지 여부까지 결정해야 한다면 `$calibrate-judgment`와 `$friction-distillation`을 순서대로 함께 사용하세요.

패키지 경로: `plugins/judgment-craft/`

MIT 라이선스입니다.
