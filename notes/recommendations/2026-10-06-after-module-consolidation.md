# 최근 테스트 결과 해석 및 다음 방향 권고안 (2026-10-06)

상태: 권고안(제안). 결정 노드가 아니며 아무것도 채택하지 않는다. 결정은 owner의 몫이다.

## 1. 가장 최근 테스트: 모듈 통합 identity run (record:module-identity-result, ec6d442, 2026-09-29)

- 대상: src/fly.py (Agent17 2채널, Agent16 3채널을 nch 인자로 통합한 단일 numpy 파일)
- 기준: 채택된 class tree와 비트 단위 동일성, 3개 층(L1 기록 필드, L2 매 step 전체 속성 및 생성기 상태 해시, L3 행별 점수), 허용오차 0
- 결과: S0, A1-A7, A7r, B1-B3 12개 행 전부 IDENTICAL. 실행 중 fly.py 수정 없음(22개 헤더 sha256 동일). 검토 세션에서 A1, B1 독립 재실행도 IDENTICAL.
- 상수 99개 전부 추적: 77개 fly.py(core 54, body 23), 22개는 ph 체인(world/harness, rng3 offset)에 잔류.
- 음성 대조: TURN_NOISE 1 ulp 변경은 L2가 첫 이벤트에서 검출. MARGIN 1 ulp 변경은 상태에 영향이 없어 미검출(상수는 효과로만 보인다는 한계).
- 부수 발견(이번 작업 원인 아님): ph35, ph33 demo가 HEAD에서 seed-scan assertion에 실패. H28/H29 이후 커밋된 9개 파일에 해당 seed 숫자열이 포함됨. scan을 assert 대신 보고로 돌리면 기록된 출력 전 줄 재현.

## 2. 해석

1. 통합은 공학적으로 성공했다. 가설 검정이 아니라 동치 검사이므로 "행동 변화 없음"이 정확한 결론이며, 성능이나 생물학적 충실도에 대한 주장은 없다.
2. 동일성은 검사한 11개 조건에서만 확인됐다. 3채널 학습 경로는 미검사, A7(Agent17 학습 on)은 기록 기준값이 없는 coverage 행이다. 이후 설계가 이 두 경로에 의존하면 그 시점에 행을 추가해야 한다.
3. 음성 대조 결과상, 상태에 영향을 주지 않는 상수의 오타는 이 검사로 잡히지 않는다. fly.py를 기준 구현으로 쓸 경우 상수 목록 자체를 문서로 고정하는 것이 보완책이다.
4. seed-scan 실패는 재현성 장치가 작동한다는 증거이지만, 현재 HEAD에서 두 demo가 실패 상태라는 것은 Phase 0(비교 신뢰성) 관점의 결함이다. 빨리 닫을수록 좋다.
5. 과학적 진척 측면에서 Level 6 synthesis 결론(navigation은 진전, choice holding과 extinction은 미진전)은 그대로다. 통합은 이 둘을 다룰 기반을 정리한 것이다.

## 3. 권고 (우선순위 순)

R1. fly.py를 이후 설계의 기준 구현으로 지정하고 item (b)를 닫는다.
  - 근거: 12행 3층 0 허용오차 동일, 위험 없음, 이후 (d), Q1-Q3 설계의 비교 대상이 단일 파일로 줄어듦.
  - 조건: 3채널 학습 경로와 Agent17 학습 on은 "코드 판독상 동일, 미검증"으로 명시.

R2. seed-scan은 redaction이 아니라 exclusion 결정(decision:seed-scan-exclusion-ph31-eval 형식)으로 처리한다.
  - 근거: 9개 파일 중 다수가 이미 기록된 설계/리뷰/synthesis 문서이고 sha가 master_plan에 인용돼 있어 수정 시 기록 무결성이 깨진다. exclusion은 목록만 추가하면 두 demo가 복구된다.
  - 재발 방지: 이후 새 문서는 P5(seed 숫자 미기재)를 커밋 전 scan으로 확인.

R3. 다음 실행 항목은 확정된 순서대로 (d) hold's benefit. 단, 측정 가능성 확인을 먼저 한다.
  - 근거: L12로 두 번 "미측정"이었고, 현재 world에서는 nav가 held 여부와 무관하게 top present odour의 whiff를 따르므로(master_plan 1717 부근) 구조적으로 측정 불가였다.
  - 제안: 설계 v1에서 첫 단계로 "hold가 행동에 차이를 만들 수 있는 조건이 존재하는가"를 fly.py 위에서 measurement only로 확인하고, 없으면 world 변경 또는 (d) 보류를 owner에게 올린다. 세 번째 미측정을 피하는 것이 목적.

R4. Q3(turn direction vs encounter timing, 측정 전용)는 (d)와 독립적이고 저비용이므로 (d) 설계 검토 대기 시간에 병행 후보로 제안.
  - 순서 변경은 결정 노드가 필요하므로 owner 판단 사항.

R5. G 2 채택 여부를 이번에 결정할 것을 권고.
  - 근거: fly.py docstring에 "unsettled"로 남아 있고, fly.py가 기준 구현이 되면 모든 후속 설계가 이 미결 상태를 상속한다.

## 4. owner 결정 대기 목록

1. fly.py 기준 구현 지정 및 (b) 종료 (R1)
2. seed-scan exclusion vs redaction (R2, exclusion 권고)
3. (d) 설계 v1 착수, 측정 가능성 선행 확인 포함 (R3)
4. Q3 병행 여부 (R4)
5. G 2 채택 여부 (R5)
