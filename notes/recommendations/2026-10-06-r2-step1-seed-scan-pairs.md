# R2 1단계: seed-scan 허용 후보 (파일, 숫자) 쌍 목록 (2026-10-06)

상태: 측정 결과(제안). 결정 노드가 아니며 아무것도 등록하거나 채택하지 않는다. 검사기와 기록 파일은 수정하지 않았다.
P5에 따라 이 문서에는 seed 숫자를 적지 않는다. 숫자는 각 harness의 seed_numbers() 안의 이름으로 부른다
(예: eval_w = SEEDS['eval'][0], dev_a = SEEDS['dev'][1], bench_w = BENCH['seed_w']).

## 방법

- 기준: 현재 브랜치(main ec6d442 + 권고 문서 커밋), 이 클론의 작업 트리.
- ph35.seeds_unused(), ph33.seeds_unused()를 수정 없이 호출해 걸린 파일을 얻고, 각 파일에서 seed_numbers()의 숫자별로
  같은 숫자 경계 규칙(앞뒤가 숫자가 아님)으로 다시 세어 (파일, 숫자) 단위로 분해했다. 문맥은 숫자를 가린 채로 확인했다.
- 스크립트는 세션 scratchpad에 두었고 저장소에는 넣지 않았다(실행만 하고 판정은 하지 않음).
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

요약: ph35는 5개 파일, 13개 쌍. ph33은 6개 파일, 22개 쌍(파일별 seed 이름 기준). 걸린 숫자는 모두 base seed(dev, eval, bench)이며
derived 또는 extra 숫자는 없었다.

## 결과: 이 클론에 없는 파일 (목록 미완)

모듈 보고서(experiments/module/module_report.md 6절)가 든 9개 중 다음은 이 저장소 클론에 없어 쌍을 만들 수 없었다.
- experiments/h18/arrays_b/K5b_restart_rand.npz: .gitignore 대상(experiments/h18/arrays_b/*.npz). owner의 로컬 작업 트리에만 있다.
- notes/reviews/remote-runs/ 아래 summary.json 3개: git에 추적되지 않는다.

둘 다 커밋된 기록이 아니므로 판단이 갈린다. (a) 로컬 산출물도 쌍으로 등록하거나, (b) 검사 범위를 git이 추적하는 파일로
한정하는 것(검사기 범위 변경이므로 별도 결정)을 생각할 수 있다. 어느 쪽이든 owner의 로컬 클론에서 같은 분해를 한 번 더
돌려야 목록이 완성된다.

## 해석과 2단계 제안 (결정은 owner)

1. 의도적 인용(h12, h29 설계 문서)과 우연 일치(summary.json의 수치, synthesis 문서의 줄 번호)는 성격이 다르다.
   쌍 등록은 둘 다에 쓸 수 있지만, 근거 문구는 따로 적는 것이 좋다.
2. synthesis 문서의 일치는 master_plan.md 줄 번호이므로 master_plan이 길어지면 앞으로도 재발할 수 있다.
   P5가 '줄 번호 인용'까지 다루는지는 owner가 정할 사항이다.
3. 구현 상태: ph33은 이미 ph32.EXCLUDED_PAIRS 집합을 읽는다. ph35는 단일 pair(pair_file, pair_num)만 지원하므로
   3단계에서 집합으로 일반화가 필요하다.
4. 쌍은 숫자 이름 단위로 등록하고, 같은 파일의 다른 seed 숫자는 계속 검사 대상으로 남긴다.
