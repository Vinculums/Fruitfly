# R2 1단계: seed-scan 허용 후보 (파일, 숫자) 쌍 목록 (2026-10-06, rev 2)

상태: 측정 결과(제안). 결정 노드가 아니며 아무것도 등록하거나 채택하지 않는다. 검사기와 기록 파일은 수정하지 않았다.
P5에 따라 이 문서에는 seed 숫자를 적지 않는다. 숫자는 각 harness의 seed_numbers() 안의 이름으로 부른다
(예: eval_w = SEEDS['eval'][0], dev_a = SEEDS['dev'][1], bench_w = BENCH['seed_w']).

## 방법

- 기준: 현재 브랜치(main ec6d442 + 권고 문서 커밋), 이 클론의 작업 트리.
- ph35.seeds_unused(), ph33.seeds_unused()를 수정 없이 호출해 걸린 파일을 얻고, 각 파일에서 seed_numbers()의 숫자별로
  같은 숫자 경계 규칙(앞뒤가 숫자가 아님)으로 다시 세어 (파일, 숫자) 단위로 분해했다. 문맥은 숫자를 가린 채로 확인했다.
- 분해 스크립트: notes/recommendations/seed_scan_pairs.py (읽기 전용, 출력에 seed 숫자 없음). owner의 로컬 작업 트리에서 같은 방식으로 다시 돌릴 수 있다.
- 스캔 규모: 두 harness 모두 419개 파일. ph35는 18개 숫자, ph33은 24개 숫자.

## 결과: 저장소에 있는 파일

| 파일 | ph35에서 걸린 seed | ph33에서 걸린 seed | 문맥 | 성격 |
|---|---|---|---|---|
| experiments/h12/h12_design_v1.md | dev_w, dev_a, eval_w, eval_a, bench_w (각 1회) | dev_w, dev_a, eval_w, eval_a, bench_w (각 1회) | 같은 한 줄. 이전 harness들의 development/evaluation/bench seed를 열거하는 seed 등록 문장 | 의도적 인용 |
| experiments/h12/h12_design_v2.md | 위와 같음 | 위와 같음 | v1과 같은 문장 | 의도적 인용 |
| experiments/h29/h29_design_v1.md | 해당 없음(ph35 자기 설계라 이름 규칙으로 제외) | dev_w, dev_a, eval_w, eval_a, bench_w (각 1회) | 같은 형식의 seed 열거 문장 | 의도적 인용 |
| experiments/h29/h29_design_v2.md | 해당 없음 | 위와 같음 | 같은 형식 | 의도적 인용 |
| experiments/h12/diagnosis/summary.json | eval_w (1회) | eval_a (2회) | 수치 배열 안의 정수 값 | 우연 일치 |
| notes/synthesis/2026-09-29-level6-synthesis-design-v1.md | eval_w (1회) | 없음 | master_plan.md 줄 번호 범위 인용 | 우연 일치 |
| notes/synthesis/2026-09-29-level6-synthesis-design-v2.md | 없음 | eval_w (1회) | master_plan.md 줄 번호 범위 인용 | 우연 일치 |
| notes/synthesis/2026-09-29-level6-synthesis.md | eval_w (1회) | 없음 | master_plan.md 줄 번호 인용 | 우연 일치 |

요약 (이 클론의 작업 트리 기준):
- 검사기별: ph35는 5개 파일 13개 쌍, ph33은 6개 파일 22개 쌍(파일별 seed 별칭 기준).
- 전체 중복 제거: 8개 파일. ph35와 ph33이 겹치는 파일은 3개(h12 설계 v1, v2, h12 diagnosis summary.json).
- 걸린 숫자는 모두 base seed(dev, eval, bench)이며 derived 또는 extra 숫자는 없었다.

## 결과: 이 클론에 없는 파일 (목록 미완)

모듈 보고서(experiments/module/module_report.md 6절)가 든 항목 중 다음 2개 항목, 파일 4개는 이 클론에 없다.
- experiments/h18/arrays_b/K5b_restart_rand.npz (1개): .gitignore 대상. owner의 로컬 작업 트리에만 있다.
- notes/reviews/remote-runs/ 아래 summary.json (3개): git이 추적하지 않는다.

'9개 중 몇 개'는 완성도 기준으로 쓰지 않는다. 보고서의 항목 단위와 파일 단위가 다르기 때문이다. 완성 기준은 다음 두 목록이다.
1. 검사기별 (파일, seed 별칭) 쌍 목록 (ph35, ph33 각각)
2. 전체 중복 제거 파일 목록
현재 확정: 추적 파일 8개. 미확정: 로컬 파일 4개.

검사 범위는 줄이지 않는다. 검사기는 추적 여부와 관계없이 작업 트리를 검사하며, git 추적 파일로 한정하면 지금까지 잡던 로컬
파일의 문제를 놓친다. 로컬 4개 파일은 파일 자체를 공유하지 않고, owner의 로컬에서 seed_scan_pairs.py를 돌려 다음 항목만 받는다.
- 상대 경로와 해당 검사기
- seed 별칭
- 발견 횟수와 숫자를 가린 문맥
- 예외가 필요한 이유

## 해석 (결정은 owner)

1. 예외 근거는 두 종류로 따로 기록한다. 둘 다 쌍 단위 예외 후보다.
   - 의도적 인용(h12, h29 설계 문서): 과거 실험 기록을 보존해야 해서 예외.
   - 우연한 일치(summary.json의 측정값, synthesis 문서의 master_plan 줄 번호): 값이 seed 숫자와 같을 뿐이라 예외.
2. P5에는 줄 번호를 자동으로 허용하는 조항이 없다. 기존 줄 번호 인용 3건은 개별 예외로 검토한다. 새 문서는 줄 번호 대신
   절 제목이나 안정적인 참조를 쓰는 것이 좋다. '모든 줄 번호 허용'은 별도 규칙 변경이다.
3. 쌍 예외의 범위: 현재 구현(ph32.EXCLUDED_PAIRS, ph35의 단일 pair)은 특정 위치가 아니라 '그 파일 안의 해당 숫자 전체'를 허용한다.
   이후 같은 파일에 같은 숫자가 추가돼도 통과한다. 횟수, 문맥, 또는 파일 버전(sha)까지 묶을지는 구현 전에 정한다.

## 적용 경로의 제약 ('ph35만 구현하면 된다'는 철회)

- ph33은 ph32.EXCLUDED_PAIRS를 읽지만, 동시에 ph32.py 전체의 sha256을 기록값(PH32_SHA)과 비교하고 다르면 실행을 멈춘다
  (src/ph33.py header의 chk["ph32"]). ph32의 목록을 직접 고치면 ph32 자체의 검사 결과가 바뀌고 ph33의 무결성 검사도 깨진다.
- 따라서 ph32는 보존하고, 승인된 예외를 ph33(과 ph35)에 어떻게 더할지 따로 설계해야 한다. 해시 검사를 끄거나 기록 해시를
  새 값으로 바꾸는 방식은 쓰지 않는다.
- 설계 대상: 두 검사기가 공유할 승인 목록의 위치와 형식, 그 목록 자체의 무결성 확인 방법, ph33과 ph35의 소스 변경이
  기록된 소스 해시에 주는 영향.

## 3단계 완료 기준 (보완안)

1. assertion을 그대로 켠 정상 데모가 ph35, ph33 모두 통과한다.
2. 행동과 검사 결과(seed-scan 줄 제외 모든 측정 출력)는 기록된 데모와 같다. 검사기 소스를 바꾸면 데모가 출력하는 소스 해시도
   바뀌므로, 소스 해시 등 출처 정보의 변경은 따로 나열해 검토한다.
3. 음성 검사(scratch에서, 기록 파일은 건드리지 않음):
   - 등록하지 않은 쌍은 계속 실패한다.
   - 예외 파일 안의 다른 seed는 계속 실패한다.
   - 예외 seed가 다른 파일에 나오면 계속 실패한다.
   - (횟수나 버전까지 묶기로 했다면) 같은 파일에 같은 숫자가 하나 더 추가되면 실패한다.

## 다음 순서

1. owner 로컬에서 seed_scan_pairs.py 실행, 로컬 4개 파일 목록 확정
2. 검사기별 쌍 목록과 전체 중복 제거 목록 확정, 쌍마다 근거 종류 기재
3. P5를 유지한 개별 예외와 두 검사기의 적용 경로 설계 (ph32 보존)
4. 그 뒤 구현. 아직 예외 등록이나 코드 변경은 하지 않았다.
