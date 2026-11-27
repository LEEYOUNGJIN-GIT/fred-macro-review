# FRED 파이프라인 감사 (Phase 0)

- 감사일: 2026-10-12 (커밋 `aa54c3a` 기준)
- 방법: README가 아니라 실제 파일(`fred_fetch.py`, `data/`, `.github/workflows/*.yml`)을 읽고 확인했다.
- 제약:
  - 이 세션에서 `api.stlouisfed.org` 호출은 프록시가 막았다(`CONNECT tunnel failed, response 403`). `FRED_API_KEY`도 없었다. 그래서 **FRED 실측이 필요한 항목은 모두 "미확인"**으로 표시했다.
  - 클론이 얕아서(shallow, 커밋 50개) 2026-09-29 이전의 git 이력은 볼 수 없었다.

## 요약표

| # | 항목 | 확인 결과 | 근거 |
| --- | --- | --- | --- |
| 1 | observations 호출 방식 | `observation_start`=오늘−1095일, `observation_end`=오늘, `sort_order=desc`. `limit`·`units`·`realtime_*`는 쓰지 않는다(FRED 기본값: limit 100000, units=lin, realtime=오늘). `"."` 값은 **버린다** | `fred_fetch.py` `fetch_fred_series()` |
| 2 | fred_latest.csv | 시리즈당 1행, 102행, 14열. 최신값·기준일과 전기·중기·YoY 변화(파생 열)를 담고 원시 이력은 없다. 인코딩은 UTF-8-SIG | `save_csv()`, 실제 파일 헤더 |
| 3 | data/fred_history/ | **실행 시점마다 찍는 fred_latest.csv 스냅샷**(`fred_YYYYMMDD_HHMMSS.csv`)이다. 시리즈별 이력이 아니다. 파일 136개(2026-05-28 ~ 2026-10-12), 3.2MB. 삭제·보존기간 로직이 없어 무기한 누적된다. 하루에 여러 개인 날도 있다(05-28, 08-07, 08-29, 09-01, 09-04, 09-22, 10-03) | `main()`, 디렉터리 목록 |
| 4 | 시리즈 레지스트리 | `fred_fetch.py` 안의 dict `REG`(102개, 그중 calculated 3개). 필드는 cat/kr/en/freq/unit/src/tf/note뿐이다. **SA/NSA 정보는 없다**. unit은 자유 텍스트 약칭 | `REG` 리터럴 |
| 5 | 지정 시리즈 존재 여부 | DFII10 ○, T5YIFR ○, DEXKOUS ○ / DFII5 ✕, DGS5 ✕, DGS3MO ✕, CPIAUCNS ✕ | `REG` 키 |
| 5a | DFII10·DEXKOUS "빈 파일" | **저장소 쪽 수집 누락은 확인되지 않았다.** 스냅샷 136개 모두 두 시리즈의 `latest_value`가 들어 있다. 원인은 미확인이다(아래 §5) | 스냅샷 전수 검사 |
| 6 | 워크플로 | 4개 수집 워크플로가 UTC 21:00/21:10/21:20/21:25에 돈다. 모두 `git commit` → `git pull --rebase origin main` → `git push`. **concurrency 설정 없음, push 재시도 없음.** 변경이 없으면 커밋하지 않는다(`git diff --cached --quiet`) | `.github/workflows/*.yml` |

## 1. observations 호출 방식 (`fred_fetch.py`)

```python
params = {"series_id": ..., "api_key": ..., "file_type": "json",
          "observation_start": START_DATE,   # now(UTC) - 1095일
          "observation_end":   END_DATE,     # now(UTC)
          "sort_order": "desc"}
```

- `limit`: 지정하지 않는다(FRED 기본값 100000). 3년 창이라 잘리지 않는다.
- `units`: 지정하지 않는다(=lin, 원값). YoY 같은 변환은 코드에서 `calc_change`로 계산한다.
- `realtime_start/end`: 쓰지 않는다. 항상 최신 vintage만 받는다.
- 결측: `[... for o in obs if o["value"] != "."]`로 **결측 관측을 제거**한다. 그래서 "직전 관측"은 결측을 건너뛴 직전 유효값이 된다.
- 재시도: 모든 예외에 대해 3회까지, 2·4초 백오프. 4xx도 재시도한다. 실패하면 `[]`를 돌려주고, 해당 행은 빈 값으로 남는다.
- 비교 기간은 "관측 개수" 기준이다(D: 1/20/252개 전, M: 1/3/12개 전). 결측을 지운 뒤의 인덱스라서 달력 기준과 어긋날 수 있다.
- 모듈을 import하기만 해도 `FRED_API_KEY`가 없으면 `sys.exit(1)`하고, 날짜 전역값도 그 시점에 계산한다. 그래서 신규 수집기는 `REG`를 **import하지 않고 AST로 읽는다**. 이 방식이면 `fred_fetch.py`를 고칠 필요가 없다.

## 2. fred_latest.csv

헤더(실제 파일, BOM 포함):
`series_id,category,korean_name,english_name,frequency,unit,source,transform,latest_date,latest_value,chg_prev,chg_mid,chg_yoy,note`

- 시리즈당 1행, 총 102행(API 시리즈 99개와 파생 3개).
- `latest_date`/`latest_value`: desc 응답에서 결측을 뺀 첫 관측.
- `chg_prev/mid/yoy`: `transform`(level/yoy_pct/mom_pct/mom_diff/calculated)에 따라 차이 또는 %변화를 담는다.
- 소비자: `scripts/Fred_signals.py`, `scripts/Fred_regime.py`(`read_csv`), `sync_claude_project.yml`(업로드).

## 3. data/fred_history/

- 파일명은 `fred_{UTC타임스탬프}.csv`이고, 내용은 그 실행의 fred_latest.csv와 똑같다(`save_csv`를 두 번 호출).
- 시계열 분석에 쓸 수 있는 "시리즈별 이력"이 아니다. 시점마다 최신값 1개씩만 남는다.
- 행 수는 101행 파일 96개, 102행 파일 40개다. 2026-09-04 스냅샷부터 `DGS30`이 추가됐다.
- 보존: 삭제 로직이 없어 무기한 누적된다(2026-10-12 기준 3.2MB, 하루 약 24KB씩).
- 결측 행: 2026-07-15 스냅샷에서 `CCSA` 1건만 비어 있었다(수집 실패로 보인다).

## 4. 시리즈 레지스트리

- 위치는 `fred_fetch.py`의 `REG` 리터럴 하나뿐이다. 별도 파일은 없다.
- 빈도 분포(REG 기준): D 27 / W 10 / M 56 / Q 8 / A 1.
- SA/NSA 필드가 없다. 일부 시리즈만 한국어 이름(`kr`)에 "(SA)"라고 적혀 있다. **그래서 신규 메타의 `seasonal_adjustment`는 FRED `series` 응답의 `seasonal_adjustment_short`에서 가져온다.**
- 발견 사항(범위 밖이라 수정하지 않음): `AAA`와 `BAA`가 `freq: 'D'`로 등록돼 있는데, 실제 `fred_latest.csv`의 `latest_date`는 `2026-09-01`이다. 월간 시리즈의 모습이다(FRED의 일간판은 `DAAA`/`DBAA`). 그러면 D 비교 기간(20/252개 전)이 월 단위로 적용된다. `chg_mid`는 20개월 전과의 비교가 되고, `chg_yoy`는 3년 창에 관측이 36개뿐이라 252개 전 값이 없어 비게 된다. 레지스트리를 수정할지는 별도로 판단해야 한다.

## 5. 지정 시리즈 존재·수집 상태

| 시리즈 | REG | 수집 상태(저장소 근거) | 비고 |
| --- | --- | --- | --- |
| DFII10 | ○ (01_금리채권, D) | 스냅샷 136/136에 값 있음. 최신 2026-10-08 = 2.87 | 실측 메타는 미확인 |
| DEXKOUS | ○ (10_환율달러, D) | 스냅샷 136/136에 값 있음. 최신 2026-10-02 = 1345.75 | 다른 D 시리즈보다 약 1주 늦다. DTWEX* 3종도 같은 날짜다 |
| T5YIFR | ○ (D) | 값 있음(2026-10-09) | |
| DFII5 | ✕ | 수집 안 함 | 제안 목록 참조 |
| DGS5 | ✕ | 수집 안 함 | 제안 목록 참조 |
| DGS3MO | ✕ | 수집 안 함 | `T10Y3M`, `TB3MS`(월간)는 있다 |
| CPIAUCNS | ✕ | 수집 안 함 | SA판 `CPIAUCSL`만 있다 |

### 5a. DFII10·DEXKOUS "빈 파일" 이력의 원인 구분

- **수집 누락: 저장소에서는 확인되지 않음.** 볼 수 있는 스냅샷 136개(2026-05-28 이후)와 현재 `fred_latest.csv`·`fred_latest.md` 모두 두 시리즈의 값이 들어 있다. 2026-05-28 이전은 얕은 클론이라 **미확인**이다.
- **내보내기 문제: 미확인.** 이 저장소의 산출물은 102개 시리즈를 한 파일에 담는다. 시리즈별 파일을 만드는 경로가 없으므로, "DFII10 파일", "DEXKOUS 파일"이 비어 보였다면 이 저장소 밖의 경로(사용자 측 내보내기, 별도 스킬이나 스크립트)에서 생겼을 가능성이 높다. 이 세션에서는 그 경로를 재현할 수 없다.
- 오인될 수 있는 정상 동작:
  1. DEXKOUS는 H.10 주간 공표라서 최신일이 다른 일간 시리즈보다 약 1주 늦다. 최근 날짜로 잘라 보면 빈 구간처럼 보인다.
  2. `fred_fetch.py`는 `"."`(휴일 결측)를 버리므로 결측 날짜 행 자체가 없다.
- 신규 레이어의 대응: 시리즈별 파일 `data/series/fred/DFII10.csv`, `DEXKOUS.csv`를 만든다. `validate_series.py`는 관측 0행 파일을 **오류**로 잡는다. 빈 파일이 다시 나타나면 원인 단계(수집이냐 내보내기냐)를 이 파일들로 가릴 수 있다. fixture 테스트(`test_backfill_dfii10_dexkous_nonempty`)로 비어 있지 않은 파일이 생성되는 것을 증명했다.

## 6. 기존 워크플로

| 워크플로 | 트리거(UTC / KST) | 커밋 경로 | 커밋 방식 | concurrency | push 충돌 처리 |
| --- | --- | --- | --- | --- | --- |
| market_daily.yml | 21:00 월~금 / 06:00 화~토 | data/market_* | add→diff 확인→commit→`pull --rebase`→push | 없음 | 없음(1회 시도) |
| fred_daily.yml | 21:10 / 06:10 | data/fred_latest.*, fred_signals.md, fred_regime.md, fred_history/ | 동일 | 없음 | 없음 |
| global_daily.yml | 21:20 / 06:20 | data/global_* | 동일 | 없음 | 없음 |
| av_daily.yml | 21:25 / 06:25 | data/av_* | 동일 | 없음 | 없음 |
| sync_claude_project.yml | workflow_run(FRED/Market/Global 완료 + success) | 커밋 없음 | claude.ai 프로젝트 문서 삭제·업로드 | 없음 | 해당 없음 |

관찰 사항:
- 실제 실행은 크게 늦어진다. 2026-10-12 커밋 시각이 FRED 09:32, Global 09:36, AV 09:41(KST)로 예정보다 약 3시간 반 늦고, 서로 4~5분 간격으로 몰렸다. 실행이 겹칠 수 있다는 뜻이다.
- 각 워크플로의 커밋 경로는 겹치지 않는다. 그래서 `pull --rebase`에서 내용 충돌은 생기지 않는다. 남는 위험은 pull과 push 사이에 다른 워크플로가 push해서 생기는 non-fast-forward 거절이며, 지금은 재시도가 없어 그 실행이 실패한다.
- `sync_claude_project.yml`은 `conclusion == 'success'`일 때만 돈다. FRED 워크플로에 단계를 더하고 그 단계가 실패하면 동기화가 멈춘다.

### 신규 단계 배치 결정: 별도 워크플로(`fred_series_daily.yml`)

근거:
1. `fred_daily.yml`에 넣으면 부분 실패(종료코드 1) 때 "FRED Daily Fetch"가 failure가 되고, 그러면 `sync_claude_project`가 실행되지 않는다. 기존 산출물의 소비가 막히는 것이다.
2. 최초 전체 백필은 `fred_daily.yml`의 `timeout-minutes: 15`를 넘을 수 있다.
3. 커밋 경로를 `data/series/`로 격리하면 기존 커밋 로직을 건드릴 필요가 없다.

신규 워크플로의 push 처리:
- 자체 concurrency 그룹 `fred-series-history`를 둔다(`cancel-in-progress: false`). 스케줄 실행과 수동 실행이 겹치는 것만 막는다.
- `git pull --rebase` + push를 최대 5회 재시도한다(15·30·45·60초 대기).
- 변경이 없으면 커밋하지 않는다.
- `validate_series.py`가 실패하면 커밋하지 않는다.
- 부분 실패라도 성공한 시리즈는 커밋하고, 마지막 단계에서 job을 failure로 보고한다.

### "동일 concurrency 그룹" 요구에 대한 판단 (적용 보류, 근거 포함)

요구는 모든 워크플로에 같은 concurrency 그룹을 지정하는 것이었지만, **기존 4개 워크플로에는 적용하지 않았다.** GitHub Actions의 concurrency 그룹은 실행 중 1개와 대기 1개만 유지하고, 그 사이에 새 실행이 들어오면 **기존 대기 실행을 취소**한다. 위에서 관찰했듯 실제 실행은 4~5분 간격으로 몰려 들어온다. 공유 그룹을 쓰면 예컨대 FRED가 실행되는 동안 Global과 AV가 차례로 대기열에 들어오고, 이때 Global이 취소되어 그날 데이터가 빠질 수 있다. 또 지시상 "기존 경로 커밋 로직은 건드리지 않는다"는 조건도 있다.
대신 제안한다(별도 PR 권장): 기존 4개 워크플로의 push 단계에 신규 워크플로와 같은 재시도 루프를 넣는다. 그룹 공유는 대기 취소 위험 때문에 권장하지 않는다.

## 7. 수집 동작 산정 (실측 아님, 추정)

| 항목 | 값 | 근거 |
| --- | --- | --- |
| 대상 | REG의 API 시리즈 99개(calculated 3개 제외) | `registry_series_ids()` |
| 호출 수/일 | 약 198회(시리즈당 `series` 1회 + `observations` 1회, 페이지가 더 있으면 추가) | 코드 |
| FRED 한도 | 120 req/min | FRED API 문서(이 세션에서 재확인 불가) |
| 호출 간격 | 0.6초 → 최대 약 100 req/min | `REQUEST_DELAY` |
| 백필 용량 | 수 MB 규모로 추정(일간 27개 × 시리즈당 수천~2.5만 행 × 약 18B/행) | 추정이며, 실행 후 `du -sh data/series`로 확인 필요 |
| 증분 diff | 시리즈당 신규 관측 0~1행과 재조회 구간의 개정 행 | 설계 |

## 8. Vintage(2단계, 기본 off) 산정

- 대상(확정): `CPIAUCSL, CPILFESL, PCEPILFE, UNRATE, PAYEMS, GDPC1`. 모두 REG에 있다.
- 방식: `realtime_start=1776-07-04`, `realtime_end=9999-12-31`로 관측 구간 전체의 vintage를 받는다.
- **범위 축소**: 전체 이력의 vintage는 과다하다. 예컨대 PAYEMS는 매년 벤치마크 개정이 과거 수년치를 다시 쓰므로 행 수가 관측 수 × 개정 횟수로 늘어난다. 그래서 **관측 구간을 최근 10년(`VINTAGE_YEARS=10`)으로 제한했다.** 월간 120개 관측 × 개정 약 5~10회 = 시리즈당 수백~1천여 행으로 추정한다(실측 아님).
- 호출 수: 실행당 6회 이상(페이지 수만큼 추가).
- 실행: `workflow_dispatch`에서 `vintages=true`일 때만 수집한다. 스케줄 실행에서는 수집하지 않는다.
- 전체 이력 vintage가 필요하면 먼저 한 시리즈로 실측해서 행 수와 용량을 확인한 뒤 범위를 늘릴 것을 제안한다.

## 9. 추가 시리즈 제안 (수집하지 않음, 목록만)

REG에 없는 시리즈는 "신규 시리즈 임의 추가 금지" 원칙에 따라 기본 수집에 넣지 않았다. 수집기는 `--series`로 개별 실행할 수 있지만, 스케줄 워크플로는 REG 전체만 수집한다.

| 시리즈 | 용도 | 비고 |
| --- | --- | --- |
| CPIAUCNS | CPI NSA판, CPIAUCSL(SA)과 쌍 | SA/NSA 쌍 저장 구조는 이미 지원하고 테스트로 확인했다 |
| DFII5 | 5Y 실질금리 | T5YIE와 함께 5Y 명목 분해 |
| DGS5 | 5Y 명목금리 | |
| DGS3MO | 3M 명목금리(일간) | 현재 TB3MS(월간)만 있다 |
| DAAA, DBAA | AAA/BAA의 일간판 | §4의 freq 불일치 해소용(REG 변경은 별도 판단) |

## 10. 이 세션에서 실행하지 못한 것

- FRED 실호출(백필, 메타 실측, years_available 실측): **미실행. 사용자 로컬이나 Actions에서 실행해야 한다.**
  - Actions: "FRED Series History" 워크플로를 수동 실행(`workflow_dispatch`)한다.
  - 로컬: `FRED_API_KEY=... python scripts/fred_series_collect.py`
- 실행 후 `python scripts/validate_series.py --short-report`의 출력으로 `docs/SERIES_SCHEMA.md` §4 표를 채운다.
