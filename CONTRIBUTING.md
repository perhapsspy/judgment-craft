# 기여 가이드

[English](CONTRIBUTING.en.md)

## 변경 소유권

콘텐츠 소유자를 먼저 확인합니다. 플러그인은 `plugins/judgment-craft`의 canonical 사본을 직접 편집합니다. `sources.lock`, `sync_skills`, 생성 snapshot, mirror 흐름은 추가하지 않습니다.

제품 약속, 스킬 역할, activation 경계를 바꾸기 전에는 [docs/PRODUCT.md](docs/PRODUCT.md)를 갱신합니다.

## 버전 규칙

- Patch: 기존 activation과 행동 계약을 유지하는 문구·설명·검증·문서 수정.
- 1.0 이전 Minor: 스킬 추가·삭제, 중요한 trigger 변경, 역할 재편, starter prompt 변경처럼 호환되지 않을 수 있는 실험적 변경. changelog에 이전 경로를 명시합니다.
- 1.0 이후 Major: 패키지 계약, 설치 경로, marketplace 또는 기존 스킬 호출자가 의존하는 공개 계약을 깨는 변경.

저장소 루트의 운영 문서만 바뀐 경우 즉시 plugin release는 필요하지 않습니다. 위 분류는 다음 release의 version을 선택할 때 적용합니다.

## 검증

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate_plugin.py
git diff --check
```

## 릴리스

1. 검증 명령을 실행합니다.
2. manifest 버전과 두 changelog를 갱신합니다.
3. 검증된 변경을 `main`에 반영하고 main CI 통과를 확인합니다.
4. 같은 commit에 변경 불가능한 `v<version>` 태그를 만듭니다.
5. release workflow가 `--release-tag v<version>`을 확인하고 GitHub Release를 생성하는지 확인합니다.
6. `perhapsspy/codex-plugins` marketplace를 릴리스 커밋의 전체 SHA로 갱신합니다.
7. 원격 marketplace 검증과 설치 round trip을 수행합니다.

PR은 필수 릴리스 단계가 아닙니다. 별도 검토나 협업이 필요할 때만 선택적으로 사용합니다.

## 롤백

marketplace 항목을 마지막 검증 릴리스 커밋의 전체 SHA로 다시 pin합니다. 공개 태그를 이동하거나 덮어쓰지 않습니다. 수정은 새 patch 또는 minor로 전진 릴리스합니다.

## 명시적 제외

canonical 저장소를 공유하는 동안 `sources.lock`, `sync_skills`, 생성 snapshot, `THIRD_PARTY_NOTICES`를 추가하지 않습니다.
