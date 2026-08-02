# Judgment Craft

Judgment Craft는 중요한 선택을 실제 결과에 연결하고, 정정이나 반증이 생기면 현재 행동까지 수리하는 Codex 플러그인입니다.

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
| `$judgment-craft` | 비용이 크거나 되돌리기 어려운 선택 전에 방향을 고르거나 다시 검증할 때 |
| `$judgment-repair` | 사용자 정정, 관찰된 반증, 이전 수리 뒤 같은 실패가 현재 판단을 무너뜨렸을 때 |

예를 들어 기술 데모를 제품 이정표로 올릴지 판단할 때는 `$judgment-craft`를 사용합니다. 실제 사용 결과가 전제를 반박했다면 `$judgment-repair`가 추천과 다음 행동을 교체합니다.

설치 또는 업데이트 후에는 새 Codex 작업을 시작해야 갱신된 스킬이 로드됩니다.

제품 약속과 활성화 경계는 [docs/PRODUCT.md](docs/PRODUCT.md)가 소유합니다. 기여·검증·릴리스 절차는 [CONTRIBUTING.md](CONTRIBUTING.md)를 따릅니다.

## 개발

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate_plugin.py
git diff --check
```

## 라이선스

[MIT](LICENSE)
