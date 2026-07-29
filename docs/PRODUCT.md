# Judgment Craft 제품 계약

Judgment Craft는 현재 상황에서 필요한 판단 유형을 분리하고, 그 판단에 필요한 최소 충분 응답을 고르는 플러그인입니다.

## 제품 약속

- 현재 선택에는 즉시 실행 가능한 제한된 추천을 제공합니다.
- 사용자가 이전 판단의 기준·범위·의미를 정정하면 그 정정을 반영해 현재 판단을 다시 계산합니다.
- 반복되는 마찰에는 원인을 자동으로 구조화한다고 가정하지 않고, 증거와 비용에 맞는 최소 충분 개입을 고릅니다.

## 세 가지 activation 역할

`$practical-judgment`는 현재 선택이나 판단에 대한 직접 추천을 담당합니다. 과거 판단의 정정이나 반복 마찰의 예방 구조가 핵심이면 주 역할이 아닙니다.

`$calibrate-judgment`는 사용자가 이전 판단의 기준·범위·의미를 명시적으로 정정했을 때 활성화됩니다. 정정을 현재 판단에 반영하며, 반복 방지 구조를 직접 설계하지는 않습니다.

`$friction-distillation`은 반복되는 마찰에 대해 재발 방지 개입이 필요한지와 대응 수준을 판단합니다. 반복 자체를 증거로 과장하지 않고, 현재 비용과 실행 가능성에 맞춰 선택합니다.

## Calibrate 후 Friction 조합

명시적 정정과 재발 방지 판단을 함께 요청하면 `$calibrate-judgment`가 먼저 정정된 현재 판단과 전제를 제공하고, `$friction-distillation`이 이어서 재사용 가능한 개입을 판단합니다.

순서가 중요합니다. calibrate는 이번 판단의 의미를 바로잡고, friction은 그 정정 또는 유사 조건에서 재발을 줄일 최소 대응을 선택합니다.

## SemVer 의미

Patch는 기존 activation 경계와 composition 순서를 깨지 않는 호환 가능한 문구·설명·검증·문서 수정입니다.

Minor는 스킬 추가·삭제, 중요한 trigger 변경, starter prompt 변경, 또는 calibrate와 friction 사이의 composition 역할 변경입니다.

Major 후보는 canonical 패키지 계약, 설치 경로, marketplace 공개 구조, 기존 스킬 호출 계약을 호환 불가능하게 바꾸는 변경입니다.
