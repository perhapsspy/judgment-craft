# AGENTS.md

- 일반 문서는 한국어로 작성하고, README·CONTRIBUTING·CHANGELOG는 한국어와 영어 쌍을 함께 갱신합니다.
- `plugins/judgment-craft`가 유일한 canonical 플러그인 사본입니다. mirror, snapshot, lock, 동기화 생성물을 추가하지 않습니다.
- 제품 약속, 세 activation 역할, calibrate 후 friction 조합, SemVer 의미는 `docs/PRODUCT.md`가 소유합니다.
- 변경 전 `CONTRIBUTING.md`의 검증·릴리스·롤백 절차를 따릅니다. marketplace는 검증된 릴리스 커밋의 전체 SHA만 가리켜야 합니다.

## 검증

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate_plugin.py
git diff --check
```
