# R2 2단계 seed scan 예외 설계 v1 DRAFT

상태: 검토용 설계 초안. `decision:seed-scan-exception-pairs-r2`의 승인 범위를 구현 가능한 계약으로 옮긴다. 이 문서의 배치는 예외 등록, 검사기 구현, 설계 확정, 모듈 채택 또는 PR 병합을 뜻하지 않는다. 이번 변경은 이 문서 하나뿐이다.

## 기준과 출처

- 기준 결정: FruitFly 공간의 [decision:seed-scan-exception-pairs-r2](https://vincs.io/app/?space=01a0b944-ecb4-737b-b3e6-5cc99ff37654#view/trace/decision:seed-scan-exception-pairs-r2). 본문 전체와 관계를 직접 확인했으며 현재 유효하고 후속 대체 결정은 표시되지 않았다. 결정 원문의 날짜 표기는 2026-10-07이다. 이 문서도 해당 작업 순서의 날짜를 따른다.
- 승인 대상의 측정 목록: [R2 1단계 rev 3](https://github.com/Vinculums/Fruitfly/blob/eaa149f57449a1827a8acf6227f69dab6763a4ae/notes/recommendations/2026-10-06-r2-step1-seed-scan-pairs.md).
- 전체 owner 결과: [로컬 scan 원본](https://github.com/Vinculums/Fruitfly/blob/b65a083ed6f8322b8e89817662d0f8f09062f93c/notes/recommendations/2026-10-07-r2-step1-owner-local-scan.txt). 당시 각 검사기는 492개 파일을 검사했다. 이는 이후 문서 추가까지 포함한 고정 파일 수가 아니다.
- 원본을 읽어 집계한 것이며 owner 로컬 NPZ와 JSON 세 파일의 바이트를 여기서 독립 검사한 것은 아니다. 원본에는 이 파일들의 실제 digest가 없다. 미확보 digest를 추정하거나 빈 값으로 등록하지 않는다.
- 설계 기준 소스와 기록 데모는 위 rev 3와 같은 커밋이다. [ph32](https://github.com/Vinculums/Fruitfly/blob/eaa149f57449a1827a8acf6227f69dab6763a4ae/src/ph32.py), [ph33](https://github.com/Vinculums/Fruitfly/blob/eaa149f57449a1827a8acf6227f69dab6763a4ae/src/ph33.py), [ph35](https://github.com/Vinculums/Fruitfly/blob/eaa149f57449a1827a8acf6227f69dab6763a4ae/src/ph35.py).

결정은 의도적 인용 4개 파일과 우연 일치 8개 파일에서 **측정된 쌍만** 승인했다. 기존 rev 3의 '후보'와 'owner 검토 대기'는 측정 당시 상태이며, 승인 근거는 그 뒤의 결정이다. 승인 범위를 확대해 읽지 않는다.

## 승인 범위와 근거

의도적 인용은 h12 설계 v1·v2와 h29 설계 v1·v2의 과거 seed 등록 문장이다. FINAL 실험 기록을 보존하므로 내용을 고치지 않고 측정된 쌍에만 예외를 준다. 우연 일치는 h12 진단 JSON과 그 로컬 복제본 세 개의 수치 배열, NPZ의 압축 바이트, synthesis 세 문서의 master_plan 줄 번호 인용이다. seed 사용을 뜻하지 않는다는 근거이며, NPZ 압축 영역 판정과 복제본의 동일성은 owner 보고다.

| 검사기 | 적중 파일 | 승인 쌍 | 총 등장 횟수 | 의도적 인용 쌍 | 우연 일치 쌍 |
|---|---:|---:|---:|---:|---:|
| ph35 | 9 | 17 | 17 | 10 | 7 |
| ph33 | 9 | 25 | 29 | 20 | 5 |

중복 제거 파일은 12개, 공통 파일은 6개다. 공통 **파일**이 같은 seed 별칭이나 같은 횟수를 뜻하지 않는다. ph33의 JSON 네 파일은 각 `eval_a` 2회라서 25쌍과 29회가 다르다. tracked 파일 8개와 owner 로컬 파일 4개를 모두 목록에 둔다.

다음 표는 실행 manifest에 펼쳐 넣을 행의 범위다. `base_five`는 설명용 약칭이며 `dev_w, dev_a, eval_w, eval_a, bench_w` 각각 별도 행을 뜻한다. 실행 형식에는 그룹 별칭이나 glob을 넣지 않는다. 개별 경로의 철자는 rev 3와 로컬 결과를 그대로 사용한다.

| 파일 또는 명시적 파일 묶음 | ph35 별칭과 횟수 | ph33 별칭과 횟수 |
|---|---|---|
| experiments/h12/h12_design_v1.md 및 h12_design_v2.md | base_five 각각 1 | base_five 각각 1 |
| experiments/h29/h29_design_v1.md 및 h29_design_v2.md | 추가 예외 없음 | base_five 각각 1 |
| experiments/h12/diagnosis/summary.json | eval_w 1 | eval_a 2 |
| notes/reviews/remote-runs/36260387653-summary/diagnosis/summary.json | eval_w 1 | eval_a 2 |
| notes/reviews/remote-runs/36260387653/h12-remote-36260387653-1/diagnosis/summary.json | eval_w 1 | eval_a 2 |
| notes/reviews/remote-runs/36261176952-summary/diagnosis/summary.json | eval_w 1 | eval_a 2 |
| experiments/h18/arrays_b/K5b_restart_rand.npz | dev_a 1 | 추가 예외 없음 |
| notes/synthesis/2026-09-29-level6-synthesis-design-v1.md | eval_w 1 | 추가 예외 없음 |
| notes/synthesis/2026-09-29-level6-synthesis-design-v2.md | 추가 예외 없음 | eval_w 1 |
| notes/synthesis/2026-09-29-level6-synthesis.md | eval_w 1 | 추가 예외 없음 |

기존 `decision:seed-scan-exclusion-ph31-eval`은 그대로 둔다. 기존 `(파일, 숫자)` 예외는 해당 파일의 그 숫자 모든 등장을 허용한다. 이를 이번의 횟수·바이트 결합 계약으로 소급 변경하거나 다시 승인하지 않는다.

## 제안하는 배치와 형식

하나의 데이터 manifest `config/seed-scan-exceptions-r2.json`과 ph33·ph35 내부의 작은 어댑터를 제안한다. 목록을 각 소스에 복제하면 승인 행과 digest가 따로 바뀔 수 있으므로 데이터는 한 곳에 둔다. 별도 실행 모듈을 새로 import하지 않고 두 어댑터가 같은 제한된 스키마를 검증한다. 어댑터의 동일 동작은 공통 fixture로 검사한다. 이 경로와 형식은 이번 DRAFT의 제안이며 아직 파일을 만들지 않는다.

manifest는 UTF-8 JSON, BOM 없음, LF, 마지막 개행 하나로 고정한다. 최상위 필드는 `schema`, `decision`, `entries`로 제한하고 schema 값은 `r2-v1`이다. 중복 JSON key, 알 수 없는 필드, 중복 행, 비정상 타입을 거부한다. 행은 `(checker, path, alias)` 사전순으로 정렬한다. 각 행은 다음 필드를 갖는다.

| 필드 | 계약 |
|---|---|
| checker | ph33 또는 ph35 |
| path | 대소문자까지 정확한 저장소 상대 경로, 구분자는 `/` |
| alias | 해당 검사기의 승인된 base 별칭 하나 |
| occurrences | 양의 정수, bool·문자열·실수 불가 |
| file_sha256_ap | 파일 원시 바이트 SHA-256을 아래 문자 전용 형식으로 표현 |
| reason | historical_quotation 또는 incidental_match |
| presence | required 또는 owner_local_optional |

결정의 예외 키는 `(checker, path, alias, occurrences, file sha256)`이다. reason은 근거 설명이며 비교를 완화하지 않는다. presence의 optional은 위 owner 로컬 네 파일에만 허용한다. 빈 digest, 자리표시자, 임의 별칭, 식, 정규식, glob, 디렉터리 단위 행을 허용하지 않는다. 실행 manifest에는 이 표를 펼친 검사기별 행 전체가 필요하다.

별칭은 외부 문자열을 eval하지 않고 검사기 안의 고정 매핑으로 해석한다. `dev_w/dev_a`와 `eval_w/eval_a`는 각각 그 검사기의 `SEEDS` 쌍, `bench_w`는 그 검사기의 `BENCH` 상수에서 얻는다. 해석된 값이 해당 `seed_numbers()`에 있는지도 확인한다. 다른 검사기의 숫자를 재사용하지 않는다. alias 중복 해석 등 seed 정의가 바뀌면 검토 없이 행을 재해석하지 않는다. 소스 변경 검토에서 seed 상수와 seed_numbers 정의의 불변을 별도 확인한다.

## manifest 자체의 무결성과 P5

hex digest는 hex 문자 사이의 숫자 덩어리가 seed와 우연히 같을 수 있다. 이를 피하기 위해 **각 digest nibble을 순서대로 a부터 p까지의 문자에 대응**시킨다. SHA-256 한 값은 소문자 a–p 64자로 저장한다. 이는 같은 digest의 무손실 표현이며 암호화나 새 해시 알고리즘이 아니다. 디코더는 길이와 문자 집합을 엄격히 확인하고 원래 digest 바이트로 되돌려 비교한다. seed 숫자는 manifest에 쓰지 않는다.

manifest 바이트 전체의 SHA-256도 이 문자 형식으로 ph33과 ph35 각각의 고정 상수에 pin한다. 두 pin은 같아야 한다. manifest 안에 자기 digest를 넣지 않으므로 순환 계산이 없다. 먼저 파일의 원시 바이트 hash를 pin과 비교한 뒤 JSON과 스키마를 해석한다. pin 불일치, manifest 없음, 읽기 실패, 디코딩·스키마 오류는 명시적 실패다. 빈 목록으로 fallback하거나 이전 목록을 사용하지 않는다. pin 검증은 assertion에만 맡기지 않는다.

manifest는 양쪽 검사기의 기존 파일 순회에 그대로 포함한다. 이름으로 제외하거나 manifest 자신의 예외를 만들지 않는다. 문자 digest만 안전하다고 가정하지 말고 경로·별칭·집계 숫자·버전·메타데이터까지 **manifest 원문 전체**에 양쪽 실제 seed 집합과 기존 숫자 경계 규칙을 적용한다. 충돌하면 출하하지 않는다. 필요한 경우 digit-free 문자열 표현을 새 설계 개정으로 검토하며 blanket 예외를 추가하지 않는다. pin이 들어간 소스도 상대 검사기에서 읽히므로 동일하게 검사한다.

새 노트와 보고서는 seed를 별칭으로만 적는다. 새 인용은 절 제목·커밋 고정 링크 등 안정적인 참조를 사용한다. 줄 번호·날짜·경로·commit hash·집계 수·digest도 P5 검사 대상이다. 기존 synthesis 줄 번호 세 건의 승인은 새 줄 번호 일반 허용이 아니다. 보고서에 digest가 필요하면 문자 전용 표현을 쓰고, 링크를 포함한 문서 최종 바이트를 실제 seed 집합으로 검사한다.

## 검사기별 변경 경계

- **ph32**: 파일 전체를 그대로 보존한다. `EXCLUDED_PAIRS`, seed scan, 기록 hash를 고치지 않는다.
- **ph33**: 현재 `ph32.EXCLUDED_PAIRS` 차감 경로를 유지하고, 별도로 R2 어댑터를 적용한다. `header()`의 ph32 전체 SHA-256 비교와 `PH32_SHA`, mismatch 시 종료를 그대로 둔다. ph32의 목록에 R2 행을 넣지 않는다.
- **ph35**: 현재 ph31_eval 경로·숫자 pair 처리와 그 상수 참조는 유지하고, 별도로 R2 어댑터를 적용한다.
- 새 적용 지점은 두 검사기의 seed-scan 판정뿐이다. agent, world, seed, RNG 순서, 통계, bar, 측정 필드, demo의 행동 assertion, 채택된 모듈을 바꾸지 않는다. 런타임 monkeypatch, 환경변수에 의한 pin/예외 교체, `-O` 우회는 쓰지 않는다.

따라서 'ph35만 바꾸면 된다'는 구현 경로는 사용하지 않는다. 두 harness의 자기 소스 hash는 바뀌겠지만 ph32나 다른 import 대상의 hash는 바뀌지 않아야 한다. 새 공유 실행 모듈을 도입하지 않는 제안이므로 기존 import 목록도 보존한다.

## 파일 비교와 실패 계약

기존 순회 규칙은 그대로다. `.git`, `__pycache__`, 각 harness의 자기 이름·기록 출력·자기 설계 패턴, 기존 master_plan/notes/viewer 규칙을 확대하거나 축소하지 않는다. binary·remote-runs·untracked·ignored를 새로 제외하지 않는다. `.npz`도 압축을 풀거나 텍스트로 decode하지 않고 기존처럼 원시 바이트에서 검사한다. ph33의 h29 설계 적중을 ph35에도 추가하는 식으로 검사기별 범위를 통합하지 않는다.

1. manifest의 path는 절대 경로, 드라이브 경로, 빈 segment, `.`·`..`, 역슬래시, NUL을 거부한다. manifest 문자열을 임의로 정규화해 다른 파일에 예외를 주지 않는다. Windows에서도 순회에서 얻은 저장소 상대 경로를 `/`로 표현한 뒤 정확히 비교한다. 대소문자 접기나 basename 비교를 하지 않는다.
2. R2 예외는 저장소 안의 원래 regular file에만 적용한다. 해당 경로나 부모가 symlink/reparse redirect이거나 저장소 밖으로 해석되면 예외를 적용하지 않고 실패한다. 기존 비예외 경로의 순회 자체를 조용히 생략하는 변경은 하지 않는다. 플랫폼별 검증 수단이 부족하면 통과를 선언하지 않는다.
3. 파일을 읽은 **같은 바이트 buffer**에서 SHA-256과 숫자 경계별 등장 횟수를 계산한다. 기존 `(?<!\d)` / `(?!\d)`의 bytes 의미를 보존한다. 정수 값의 집합은 기존 scanner 의미대로 세고, 각 승인 숫자의 전체 등장 횟수는 별도 센다.
4. 해당 checker/path/alias의 digest와 전체 횟수가 모두 같을 때만 그 숫자의 매치를 허용한다. 다른 숫자나 다른 경로에는 영향이 없다. 일부 위치만 잘라 허용하거나 추가 등장을 숨기지 않는다.
5. 존재하는 등록 파일에서 digest나 횟수가 다르면 등록이 만료된 것으로 명시적 실패한다. 등장 수가 줄거나 영이 되어도 manifest가 그 파일을 계속 보증하지 않게 한다. 같은 횟수의 다른 내용, 개행 변환, 무관한 편집도 실패한다. 자동 재서명하지 않는다.
6. 결정대로 owner 로컬 optional 파일이 처음부터 없는 클론에서는 그 행을 `absent/unused`로 보고하고 예외를 적용하지 않는다. 이는 그 파일의 검증 성공이 아니다. 나중에 나타나면 정확한 바이트와 횟수를 검사한다. required 파일 누락, 읽기 권한 오류, 순회 도중 사라짐은 실패로 구분한다.
7. manifest 검증은 scan 전에 수행한다. scan 결과의 기존 반환 형식과 `nums`, `nf` 의미는 보존하고 무결성 오류는 명시적 실패로 전달한다. 미등록 적중은 기존처럼 남는다. 파일 수는 작업 트리 상태에 따라 달라지며 승인 쌍 수와 혼동하지 않는다.

### 읽기 도중 변경과 snapshot 범위

한 파일의 hash와 count를 따로 다시 열어 조합하지 않는다. open 전후의 파일 정체성과 상태를 확인하고 같은 descriptor로 읽는다. 경로 교체·크기·수정 상태의 변경이 검출되면 해당 실행을 실패시킨다. manifest도 pin 검사와 parsing에 같은 buffer를 사용한다. scan 종료 전에는 순회 inventory와 대상 파일 상태, manifest 상태를 재확인한다. 이것만으로 동시 쓰기에 대한 원자적 전체 저장소 snapshot을 증명할 수는 없다.

3단계의 수용 실행은 작업 트리 쓰기를 멈춘 상태 또는 owner 로컬 파일까지 포함한 일관된 read-only snapshot에서 한다. 시작·끝 inventory와 상태를 기록하며 변화가 있으면 새 실행으로 다시 검사한다. snapshot을 만들 때 ignored/untracked 파일을 빼지 않는다. 일부 바이트만 읽을 수 있었거나 동시 변경을 배제할 수 없으면 결과는 미완료다. 검사 이후의 파일 변경까지 통과로 보증하지 않는다.

## 최초 등록과 갱신 절차

1. 3단계 실행 승인을 별도로 받은 뒤, 기준 source와 승인 행 목록을 확인한다. owner 로컬 파일을 가진 환경에서 같은 snapshot의 파일별 count와 실제 SHA-256을 수집한다. tracked 파일도 원시 바이트 기준이며 Git blob SHA와 혼동하지 않는다.
2. 모든 행을 rev 3와 대조한다. owner 로컬 digest가 없는 상태에서는 production manifest를 완성했다고 하지 않는다. JSON 복제본은 동일하다는 과거 보고만으로 digest를 대입하지 않고 각 파일을 직접 측정한다.
3. canonical manifest를 만들고 문자 전용 digest를 넣는다. 전체 원문 seed scan, 스키마 검증, 행·횟수 합계를 검사한 후 manifest pin을 계산한다. 그 pin을 양쪽 어댑터에 함께 넣는다. 새 manifest와 두 소스의 변경 내역을 한 검토 단위로 제출한다.
4. 파일 또는 count drift가 생기면 자동 갱신하지 않는다. 변경 내용, 기존 승인 근거가 유지되는지, 새 count·digest를 owner가 검토해야 한다. 새 쌍 추가나 범위 확장은 별도 승인이 필요하다.
5. 재승인 후에만 manifest와 두 pin을 함께 갱신하고 전체 수용·음성 검사를 다시 한다. 한쪽 pin만 갱신하거나 pin check를 끄는 방법은 없다. rollback도 승인된 manifest와 대응 pin의 일치된 세트로 한다.

기존 FINAL 설계와 기록 출력은 갱신 절차의 편집 대상이 아니다. 현재 결정은 그 기록을 보존하려는 것이므로 먼저 기록을 고쳐 예외 필요성을 없애지 않는다.

## 3단계 수용 검사 계획

기준 출력은 [ph33 기록 demo](https://github.com/Vinculums/Fruitfly/blob/eaa149f57449a1827a8acf6227f69dab6763a4ae/experiments/h28/ph33_demo.txt)와 [ph35 기록 demo](https://github.com/Vinculums/Fruitfly/blob/eaa149f57449a1827a8acf6227f69dab6763a4ae/experiments/h29/ph35_demo.txt)다. 기준 파일을 수정하지 않는다. 신규 실행 출력과 대조 보고서를 별도로 둔다.

| 검사 | 합격 조건 |
|---|---|
| 정상 demo | ph33·ph35 모두 assertion ON, 정상 종료, seed scan 통과 |
| 측정 출력 | seed-scan 줄 이외의 모든 측정 줄이 기록 demo와 정확히 일치 |
| 행동·필드 | 기존 identity, trajectory, RNG, 모든 recorded field 검증을 유지하고 모두 통과 |
| ph32 보존 | 파일 전체 SHA-256이 기존 PH32_SHA와 같고 기존 guard가 살아 있음; scratch 변조는 종료 유발 |
| 승인 inventory | owner 전체 snapshot에서 ph35 17쌍 17회, ph33 25쌍 29회; 12파일·공통 6파일을 별도 대조 |
| 제한 클론 | 없는 local 행은 unused로 명시; 전체 owner 검증을 대신하지 않음 |
| P5 | manifest, 양쪽 변경 소스, 새 문서·보고서가 각 실제 seed 집합의 숫자 경계 검사에 새 적중을 만들지 않음 |

출처 변경은 행동 차이와 분리해 **허용 목록을 좁게** 작성한다. 변경 가능한 항목은 ph33·ph35의 자기 소스 digest 값, 새 R2 manifest 식별·검증 상태와 적용/unused 통계, seed-scan 설명·파일 수·적중 결과다. 기존 header 전체를 통째로 무시하지 않는다. 기존 source hash guard의 boolean, import 대상 digest, design digest, seeds, readings 및 그 밖의 문구는 그대로 비교한다. 새로운 provenance 항목도 줄 단위로 나열해 검토하고 숫자 충돌을 검사한다. 환경 차이로 다른 측정 줄이 바뀌면 허용 차이로 밀어 넣지 않고 원인을 해결하거나 실패로 보고한다.

### scratch 음성 검사

역사 기록 원본 대신 분리된 scratch 복사본과 fixture를 사용한다. fixture는 실제 값 자체를 노트에 쓰지 않고 trusted 상수에서 생성한다.

- 미등록 (파일, 숫자) 쌍은 실패한다.
- 예외 파일에 다른 seed를 넣으면 실패한다.
- 같은 seed를 다른 파일에 넣으면 실패한다.
- 예외 파일에 같은 숫자를 한 번 더 넣으면 실패한다.
- 횟수를 그대로 두고 바이트만 바꾸거나, 숫자를 제거하거나, LF/CRLF를 바꾸면 실패한다.
- checker를 바꾸거나 alias를 잘못 적거나 다른 검사기의 alias 해석을 쓰면 실패한다.
- manifest 변조·pin 불일치·누락·중복 key·중복 행·잘못된 digest 표현·잘못된 count 타입은 실패한다.
- 경로 traversal, 대소문자/구분자 별칭, 다른 경로로의 복사, symlink/reparse redirect로 승인을 옮길 수 없다.
- 읽기 중 파일 교체, manifest 교체, 권한 오류는 통과 대신 실패한다.
- optional 로컬 파일이 없으면 unused, 정확한 파일이 나타나면 적용, 다른 파일이 나타나면 실패한다.
- 기존 ph31_eval pair의 동작은 그대로이고, 그 파일의 다른 seed는 기존 규칙대로 실패한다.
- manifest를 이름으로 건너뛰지 않음을 검증한다. scratch의 검토용 pin을 대응시킨 fixture에서도 manifest 원문의 새 seed 적중은 실패해야 한다. production pin의 runtime override는 만들지 않는다.
- 원래 숫자 경계의 앞뒤 digit/non-digit 사례와 ph33/ph35 반환 형식을 회귀 검사한다.

fixture 통과와 실제 owner 로컬 파일 검증은 다른 증거다. NPZ와 로컬 JSON을 보유하지 않은 환경에서 만든 모형으로 실제 네 파일의 검증 완료를 선언하지 않는다.

## 검토할 제안과 다음 단계

이 DRAFT에서 검토할 것은 중앙 JSON 경로·스키마, 문자 전용 digest 표현, 두 harness의 pin과 내부 어댑터, 정확한 byte/count·경로·snapshot 실패 계약, 수용 결과의 출처 차이 목록이다. 결정이 이미 승인한 예외 근거와 쌍 범위를 새로 넓히지 않는다.

현재는 설계 문서만 추가한다. 구현용 manifest, digest 등록, checker 변경, demo 재실행 결과는 아직 없다. 설계 검토와 owner의 다음 단계 지시 후에만 3단계로 진행한다.
