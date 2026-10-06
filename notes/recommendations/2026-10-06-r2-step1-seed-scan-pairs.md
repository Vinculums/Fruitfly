# R2 1단계: seed-scan 허용 후보 (파일, 숫자) 쌍 목록 (2026-10-06, rev 3)

상태: owner 로컬 결과를 반영한 측정 목록(제안). 결정 노드가 아니며 아무것도 등록하거나 채택하지 않는다. 이번 개정은 이 문서만 수정하며 검사기와 실험 기록 파일은 수정하지 않는다.
P5에 따라 이 문서에는 seed 숫자를 적지 않는다. 숫자는 각 harness의 seed_numbers() 안의 이름으로 부른다
(예: eval_w = SEEDS['eval'][0], dev_a = SEEDS['dev'][1], bench_w = BENCH['seed_w']).

## 방법과 출처

- 기존 클론 기준: main ec6d442 + 권고 문서 커밋의 작업 트리. 두 harness 모두 419개 파일을 검사한 rev 2 측정이다.
- owner 로컬 기준: origin/main ec6d442 + PR #2 파일 + 로컬 untracked/ignored 파일. 두 harness 모두 492개 파일을 검사했다.
  이는 아래 결과 파일이 기록한 당시 작업 트리의 범위이며, 결과 파일과 rev 3 자체를 추가한 뒤의 재검사 결과는 아니다.
- 로컬 결과 원본: [2026-10-07-r2-step1-owner-local-scan.txt](https://github.com/Vinculums/Fruitfly/blob/b65a083ed6f8322b8e89817662d0f8f09062f93c/notes/recommendations/2026-10-07-r2-step1-owner-local-scan.txt).
  원본의 실행일 표기 2026-10-07을 유지한다. 이 문서는 그 결과를 대조·집계했으며 owner 로컬 파일 자체를 독립적으로 재검사하지 않았다.
- ph35.seeds_unused(), ph33.seeds_unused()를 수정 없이 호출해 걸린 파일을 얻고, 각 파일에서 seed_numbers()의 숫자별로
  같은 숫자 경계 규칙(앞뒤가 숫자가 아님)으로 다시 세어 (파일, seed 별칭) 단위로 분해한다.
  ph35는 18개 숫자, ph33은 24개 숫자이며 별칭은 검사기별로 해석한다.
- 분해 스크립트: notes/recommendations/seed_scan_pairs.py. seed 값은 별칭으로, 문맥의 모든 숫자는 #으로 표시한다.
  출력의 집계 숫자는 별도로 P5 충돌 여부를 확인해야 한다.
- 실행 확인과 쌍 목록의 근거는 구분한다. owner의 채팅 확인은 helper 7b9f379, Windows cp949 콘솔, 정상 종료,
  로컬 포함 전체 검사 및 숫자 없는 문맥 출력에 대한 보고다. 위 원본도 같은 환경에서 PYTHONUTF8 없이 exit 0을 기록하고,
  PYTHONUTF8=1로 실행한 98231db 결과와 쌍·합집합 줄이 같다고 보고한다. 쌍의 실제 내용은 위 원본에서 읽었다.

## 결과: 추적 파일

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

추적 파일 부분집합 요약 (기존 클론 측정과 owner 로컬 결과에서 일치):
- 검사기별: ph35는 5개 파일 13개 쌍, ph33은 6개 파일 22개 쌍(파일별 seed 별칭 기준).
- 전체 중복 제거: 8개 파일. ph35와 ph33이 겹치는 파일은 3개(h12 설계 v1, v2, h12 diagnosis summary.json).
- 걸린 숫자는 모두 base seed(dev, eval, bench)이며 derived 또는 extra 숫자는 없었다.

## 결과: owner 로컬 파일

기존 클론에 없던 아래 4개 파일의 (검사기, 파일, seed 별칭, 횟수)를 owner 결과 파일로 보완했다.
성격은 예외 검토를 위한 분류이며 승인된 예외가 아니다.

| 파일 | ph35에서 걸린 seed | ph33에서 걸린 seed | 문맥·추가 확인의 출처 | 성격 |
|---|---|---|---|---|
| experiments/h18/arrays_b/K5b_restart_rand.npz | dev_a (1회) | 없음 | owner가 ZIP member 경계를 확인한 결과 head.npy의 deflate 압축 데이터 안이며 header나 파일명은 아니라고 보고. 압축 바이트 문맥은 원본에서 생략 | 압축 바이트의 우연 일치 후보 |
| notes/reviews/remote-runs/36260387653-summary/diagnosis/summary.json | eval_w (1회) | eval_a (2회) | 숫자를 가린 배열 문맥. owner의 sha256 비교에 따르면 추적된 h12 diagnosis summary.json과 byte-identical | 수치 배열의 우연 일치 |
| notes/reviews/remote-runs/36260387653/h12-remote-36260387653-1/diagnosis/summary.json | eval_w (1회) | eval_a (2회) | 위와 같은 문맥 및 owner의 동일성 확인 | 수치 배열의 우연 일치 |
| notes/reviews/remote-runs/36261176952-summary/diagnosis/summary.json | eval_w (1회) | eval_a (2회) | 위와 같은 문맥 및 owner의 동일성 확인 | 수치 배열의 우연 일치 |

- 원본의 추가 확인에 따르면 remote-runs/는 owner 클론의 .git/info/exclude 대상이고 NPZ는 .gitignore 대상이다.
  git에서 제외되어도 두 검사기의 작업 트리 검사 대상이다.
- NPZ는 압축 바이트에서의 매치다. 이를 압축 해제된 배열의 seed 값이나 실제 seed 사용으로 해석하지 않는다.
- 원본에는 NPZ의 실제 offset·member 경계 수치와 sha256 digest 자체가 없으므로, 경계 판정과 byte-identical 여부는
  owner의 추가 확인 보고로 기록한다. 이 문서에서 파일 원본을 받아 독립 재검증했다는 뜻은 아니다.

## 전체 집계와 목록의 범위

| 범위 | ph35 파일 / 쌍 | ph33 파일 / 쌍 | 중복 제거 파일 | 두 검사기 공통 파일 |
|---|---|---|---|---|
| 추적 파일 부분집합 | 5 / 13 | 6 / 22 | 8 | 3 |
| owner 로컬 파일 추가분 | 4 / 4 | 3 / 3 | 4 | 3 |
| owner 실행 전체 | 9 / 17 | 9 / 25 | 12 | 6 |

- 위 두 파일 표의 모든 행이 전체 중복 제거 목록이다. 공통 파일은 h12 설계 v1·v2, 추적된 h12 diagnosis summary.json,
  그리고 remote-runs 아래 summary.json 세 개다. 나머지는 ph35만 NPZ와 synthesis v1·본편, ph33만 h29 설계 v1·v2와 synthesis v2다.
- 쌍 수는 검사기별 (파일, seed 별칭) 수다. 한 쌍에 여러 번 등장해도 한 쌍이다.
  ph33의 summary.json 네 파일에서 eval_a가 각각 두 번 등장하는 것을 쌍 수에 중복 합산하지 않는다.
- owner 결과의 기존 추적 파일 쌍은 rev 2와 일치하고, 로컬 추가분까지 모두 base seed(dev, eval, bench) 별칭이다.
  derived 또는 extra 별칭의 적중은 없다.
- 모듈 보고서의 항목 수를 파일 수나 완성도 분모로 쓰지 않는다. 해당 owner 실행에 대한 검사기별 쌍 목록과
  전체 중복 제거 파일 목록은 이제 위 표로 정리되었다. 향후 작업 트리에 대한 완전성이나 예외 승인을 뜻하지 않는다.
- 검사 범위는 줄이지 않는다. git 추적 파일로 한정하면 이번에 보완한 로컬 파일의 적중을 놓친다.

## 해석 (결정은 owner)

1. 예외 근거는 두 종류로 따로 기록한다. 둘 다 쌍 단위 예외 후보다.
   - 의도적 인용(h12, h29 설계 문서): 과거 실험 기록을 보존해야 한다는 근거로 개별 예외를 검토한다.
   - 우연한 일치(summary.json의 측정값과 로컬 복제본, synthesis 문서의 master_plan 줄 번호, NPZ 압축 바이트):
     실제 seed 사용이 아닌 숫자·바이트 일치라는 근거로 개별 예외를 검토한다. NPZ의 압축 영역 판정은 owner 보고에 근거한다.
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

1. 위 검사기별 쌍 목록과 전체 중복 제거 목록을 기준으로 owner가 각 예외 후보의 근거와 범위를 검토한다.
2. P5를 유지한 개별 예외와 두 검사기의 적용 경로를 설계한다 (ph32 보존).
3. 승인된 범위에 한해 그 뒤 구현한다. 예외 등록, 검사 범위 축소, 해시 검사 변경은 아직 승인하거나 적용하지 않았다.
