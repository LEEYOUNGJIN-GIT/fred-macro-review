# 시계열 저장 레이어 스키마 (`data/series/`)

기존 산출물(`data/fred_latest.*`, `fred_signals.md`, `fred_regime.md`, `fred_history/` 등)과 별개의 레이어다. 기존 파일은 바꾸지 않는다. `sync_claude_project.yml`의 업로드 대상이 아니며, GitHub 통합이나 외부 파이프라인에서 직접 읽는 용도다.

```
data/series/
├── fred/{SERIES_ID}.csv        시리즈별 전체 이력
├── fred_meta.csv               시리즈별 실측 메타
├── _revisions.csv              개정 감지 로그 (append-only)
└── fred_vintage/{ID}.csv       개정 이력 (--vintages, 2단계)
```

생성: `scripts/fred_series_collect.py` / 검사: `scripts/validate_series.py`

## 1. 시리즈 이력 `fred/{SERIES_ID}.csv`

| 열 | 형식 | 설명 |
| --- | --- | --- |
| date | `YYYY-MM-DD` | FRED 관측일 그대로. 월·분기·연 시리즈는 기간 첫날(FRED 규약). 주간은 FRED의 주 기준일(예: 토요일 마감) |
| value | float 또는 빈칸 | FRED 원값(`units=lin`, 최신 vintage). FRED의 `"."`(결측)은 **빈칸**으로 저장한다. 보간·직전값 채움 없음 |

- UTF-8, BOM 없음, LF, 헤더 필수, pandas `to_csv`로만 기록한다.
- 날짜는 오름차순이고 중복이 없다. 시리즈당 파일 1개라서 일일 변경은 대개 끝에 한 줄이 붙는 정도다.
- 값은 파이썬 `repr(float)`로 기록한다. FRED 문자열 `"158000"`은 `158000.0`이 된다. 숫자로는 같다.
- 결측 행은 **보존**한다. 휴일 등 `"."` 날짜도 행으로 남는다. 이 점이 `fred_fetch.py`와 다르다(그쪽은 결측 행을 버린다).
- 읽기 예시:

```python
import pandas as pd
df = pd.read_csv("data/series/fred/DFII10.csv", parse_dates=["date"],
                 keep_default_na=False, na_values=[""])
```

## 2. 메타 `fred_meta.csv`

| 열 | 출처 | 설명 |
| --- | --- | --- |
| series_id | REG | |
| title | FRED `series.title` | |
| units | FRED `series.units` | 예: `Percent`, `Index 1982-1984=100` |
| frequency | FRED `series.frequency_short` | `D/W/BW/M/Q/SA/A` |
| seasonal_adjustment | FRED `series.seasonal_adjustment_short` | `SA/NSA/SAAR` 등. **응답값을 그대로 쓰고 추정하지 않는다** |
| series_type | 수집기의 명시 매핑 `SERIES_TYPE` | `level/rate/spread/fx/price_index/count` (§3) |
| observation_start | FRED `series.observation_start` | FRED가 공시한 시작일 |
| observation_end | FRED `series.observation_end` | |
| years_available | **실측** | 저장된 비결측 관측의 첫날부터 끝날까지의 기간(년, 소수 1자리). FRED 공시 시작일과 다르면 API가 제공하는 기간이 제한된 것이다 |
| last_updated | FRED `series.last_updated` | |
| vintage | 수집기 설정 | `Y`=개정 이력 대상(`VINTAGE_SERIES`), `N`=아님 |
| probed_at | 수집 시각(UTC) | `YYYY-MM-DDTHH:MM:SSZ`, 해당 시리즈를 마지막으로 성공 수집한 시각 |
| short_history | 실측 | `years_available < 10`이면 `True`. **장기 백분위 계산 불가 플래그** |

- 수집에 실패한 시리즈는 이전 메타 행을 그대로 유지한다.
- `probed_at`은 실행할 때마다 바뀐다. 그래서 meta 파일은 매일 1회 diff가 생긴다. 시리즈 파일은 값이 바뀔 때만 diff가 생긴다.

## 3. series_type 분류 규칙

| 값 | 기준 | 예 |
| --- | --- | --- |
| rate | 수익률·금리, 또는 % 단위 비율 지표 | DGS10, DFII10, UNRATE, TCU, MICH, DRCCLACBS |
| spread | 두 금리의 차로 정의된 지표 | T10Y2Y, T10Y3M, BAA10Y, BAMLH0A0HYM2, T10YIE/T5YIE(명목−실질) |
| fx | 환율, 달러지수 | DEXKOUS, DEXJPUS, DTWEXBGS |
| price_index | 물가·가격 **지수** | CPIAUCSL, CPIAUCNS, PCEPILFE, PPIFIS, CSUSHPINSA, PALLFNFINDEXM |
| count | 사람·건·호·대 수 | PAYEMS, ICSA, HOUST, PERMIT, TOTALSA |
| level | 그 밖의 수준값: 금액, 활동·심리·스트레스 지수, 현물가격, 주가지수 | GDPC1, WALCL, VIXCLS, NFCI, DCOILWTICO, SP500 |

- T5YIFR(5Y5Y 선도 기대인플레)은 스프레드 조합으로 계산되지만, 그 자체는 선도 "율"이라서 `rate`로 분류했다.
- 현물가격(원자재 USD/MT 등)은 `level`이다. 지수형 가격(`PALLFNFINDEXM`)은 `price_index`다.
- 이 매핑은 FRED 메타에서 추정한 것이 아니라 코드에 명시한 분류다. 레지스트리에 시리즈가 추가됐는데 매핑이 없으면 테스트(`test_registry_loaded_without_import_and_types_complete`)가 실패한다.

## 4. years_available < 10 시리즈

**미측정.** 이 세션에서는 FRED 호출이 막혀 실측 값이 없다. 첫 실행 뒤 아래 명령의 출력으로 이 표를 채운다.

```
python scripts/validate_series.py --short-report
```

| series_id | years_available | observation_start(FRED) | frequency |
| --- | --- | --- | --- |
| (미측정) | | | |

실측 전 점검 후보(사전 지식 기반, **실측 아님**):

| series_id | 의심 이유 |
| --- | --- |
| BAMLH0A0HYM2 | ICE BofA 지수는 라이선스 사유로 FRED API의 제공 기간이 제한됐을 수 있다 |
| SP500 | S&P 라이선스로 FRED의 제공 기간이 약 10년으로 제한된 것으로 알려져 있다 |
| SOFR | 2018-04 시작 |
| NASDAQQGLDI, DTWEXBGS, DTWEXAFEGS, DTWEXEMEGS, KCFSI, STLFSI4 | 시작 시점 확인 필요 |

`short_history=True`인 시리즈는 장기 백분위·장기 평균 비교에 쓰지 않는다. 이 레이어는 플래그만 남기며, 분석 로직은 구현하지 않는다.

## 5. 개정 로그 `_revisions.csv`

| 열 | 설명 |
| --- | --- |
| series_id | |
| date | 개정된 관측일 |
| old | 이전 저장값(결측이면 빈칸) |
| new | 새 값(결측이면 빈칸) |
| detected_at | 감지 시각(UTC, `YYYY-MM-DDTHH:MM:SSZ`) |

- 증분 수집은 저장된 최근 **12개 관측**의 첫 날짜부터 다시 조회한다. 이 구간에서 값이 달라지면(결측에서 값으로, 값에서 결측으로 바뀐 경우 포함) 시리즈 파일을 갱신하고 이 파일에 1행을 추가한다.
- 한계: 재조회 구간 **밖**의 개정(예: 연간 벤치마크 개정)은 증분에서 보이지 않는다(테스트 `test_revision_outside_window_not_seen`). 이런 개정은 `fred_vintage/`가 담당하거나 백필을 다시 해서 반영한다.
- 재조회 응답에 없는 저장 날짜는 삭제하지 않고 경고만 출력한다.

## 6. Vintage `fred_vintage/{ID}.csv` (2단계, 기본 off)

| 열 | 설명 |
| --- | --- |
| date | 관측일 |
| value | 해당 vintage의 값(결측은 빈칸) |
| realtime_start | 이 값이 유효했던 실시간 구간의 시작 |
| realtime_end | 구간 끝(`9999-12-31` = 현재 유효) |

- 대상: `CPIAUCSL, CPILFESL, PCEPILFE, UNRATE, PAYEMS, GDPC1`
- 관측 구간: 실행 연도 기준 최근 10년(1월 1일부터, `VINTAGE_YEARS`). 용량 근거는 `docs/AUDIT_fred.md` §8 참조.
- 실행할 때마다 파일 전체를 다시 쓴다. 내용이 같으면 쓰지 않는다.
- 정렬: `(date, realtime_start)` 오름차순, 중복 없음.

## 7. 수집기 동작 요약

| 항목 | 동작 |
| --- | --- |
| 대상 | `fred_fetch.py`의 `REG`를 AST로 읽은 뒤 calculated를 뺀 99개. `--series`로 일부만 지정할 수 있다 |
| 백필 | 저장 파일이 없으면 `observation_start` 없이 전체 이력을 받는다(`sort_order=asc`, `limit=100000`, `offset` 페이지) |
| 증분 | 저장된 최근 12개 관측의 첫 날짜부터 다시 조회한다 |
| 재시도 | 429·5xx·연결 오류는 2·4·8초 지수 백오프로 최대 4회 시도한다. 그 밖의 4xx는 재시도하지 않고 기록한다 |
| 격리 | 시리즈 하나가 실패해도 다음 시리즈로 넘어가고, 실패 시리즈의 기존 파일은 유지한다 |
| 종료코드 | 0 = 전체 성공, 1 = 일부 실패(성공분은 저장), 2 = API 키 없음 |
| 키 보호 | 모든 로그와 예외 문자열에서 `api_key=` 값과 키 문자열을 `***`로 바꾼다. 테스트가 출력과 생성 파일 전체를 grep해 확인한다 |
| 멱등 | 같은 응답을 다시 처리하면 파일이 바뀌지 않는다. 내용이 같으면 쓰지 않는다 |

## 8. 테스트

```
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest -q tests
```

- `tests/test_golden_fred_fetch.py`: `fred_fetch.py`의 fred_latest.csv/md 출력이 골든 파일과 바이트 단위로 같은지 확인한다(회귀 계약).
- `tests/test_series_collect.py`: 백필, 증분, 멱등, 개정 감지, 결측 보존, 스키마, SA/NSA, 부분 실패, 재시도, 키 노출, vintage, 워크플로 계약.
- `tests/test_validate_series.py`: 무결성 검사기의 정상 판정과 오류 검출.
- fixture는 `tests/fixtures/fred_fixtures.py`의 **합성 데이터**로, 실제 FRED 값이 아니다.
