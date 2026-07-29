# 기여 가이드

[English](CONTRIBUTING.en.md)

## 변경 소유권

콘텐츠 소유자를 먼저 확인합니다. 플러그인은 `plugins/judgment-craft`의 canonical 사본을 직접 편집합니다. `sources.lock`, `sync_skills`, 생성 snapshot, mirror 흐름은 추가하지 않습니다.

제품 약속, 스킬 역할, activation 모델, composition 의미를 바꾸기 전에는 [docs/PRODUCT.md](docs/PRODUCT.md)를 갱신합니다.

## 버전 규칙

- Patch: 기존 activation과 composition 계약을 유지하는 문구·설명·검증·문서 수정.
- Minor: 스킬 추가·삭제, 중요한 trigger 변경, composition 역할 변경, starter prompt 변경.
- Major 후보: 패키지 계약, 설치 경로, marketplace가 의존하는 공개 계약을 깨는 변경.

## 검증

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate_plugin.py
git diff --check
```

## 릴리스

1. 검증 명령을 실행합니다.
2. manifest 버전과 두 changelog를 갱신합니다.
3. PR을 열고 CI를 통과시킵니다.
4. 같은 merge 커밋에 변경 불가능한 `v<version>` 태그를 만듭니다.
5. release workflow가 `--release-tag v<version>`을 확인하고 GitHub Release를 생성하는지 확인합니다.
6. `perhapsspy/codex-plugins` marketplace를 릴리스 커밋의 전체 SHA로 갱신합니다.
7. 원격 marketplace 검증과 설치 round trip을 수행합니다.

## 롤백

marketplace 항목을 마지막 검증 릴리스 커밋의 전체 SHA로 다시 pin합니다. 공개 태그를 이동하거나 덮어쓰지 않습니다.

## 명시적 제외

canonical 저장소를 공유하는 동안 `sources.lock`, `sync_skills`, 생성 snapshot, `THIRD_PARTY_NOTICES`를 추가하지 않습니다.
