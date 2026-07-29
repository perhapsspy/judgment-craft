# Judgment Craft

Judgment Craft는 현재 선택에 대한 직접적인 판단, 명시적 정정 이후의 재보정, 반복되는 마찰에 대한 최소 충분 대응을 제공하는 Codex 플러그인입니다.

English: [README.en.md](README.en.md)

## 설치

```bash
codex plugin marketplace add perhapsspy/codex-plugins
codex plugin add judgment-craft@perhapsspy
```

업데이트:

```bash
codex plugin marketplace upgrade perhapsspy
codex plugin add judgment-craft@perhapsspy
```

제거:

```bash
codex plugin remove judgment-craft@perhapsspy
```

## 스킬

| 스킬 | 사용 시점 |
| --- | --- |
| `$practical-judgment` | 현재 선택이나 판단에 대한 직접적인 추천이 필요할 때 |
| `$calibrate-judgment` | 이전 판단의 기준·범위·의미를 명시적으로 정정했을 때 |
| `$friction-distillation` | 반복되는 마찰에 맞는 대응 수준을 정해야 할 때 |

정정된 현재 판단이 재발 방지도 요구하면 `$calibrate-judgment`를 먼저 사용한 뒤 `$friction-distillation`으로 이어갑니다.

패키지 경로: `plugins/judgment-craft/`

제품 약속과 역할 경계는 [docs/PRODUCT.md](docs/PRODUCT.md)가 소유합니다. 변경 시 [CONTRIBUTING.md](CONTRIBUTING.md)를 따르고, 영어 문서는 [CONTRIBUTING.en.md](CONTRIBUTING.en.md)와 [CHANGELOG.en.md](CHANGELOG.en.md)를 함께 갱신합니다.

설치 또는 업데이트 후에는 새 Codex 작업을 시작해 갱신된 스킬이 로드되도록 합니다.

## 개발

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate_plugin.py

## 라이선스
[MIT](LICENSE)
```
