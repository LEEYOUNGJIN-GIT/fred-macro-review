# macro/ — 지표 조합 방향 시나리오 (시장 내재 상태 -> 조건부 확률)

목적: "지금 어떤 지표 조합이 어떤 방향으로 흘러갈 수 있는가"를 확률 범위로 보여주고, 그 확률이 실제로 맞는지 사전등록으로 채점한다.
산출물은 `data/macro_outlook.md` 한 파일이며 Claude Project로 자동 동기화된다.

## 파이프라인
fetch_history.py -> checks.py -> (월 1회) backtest.py --save-summary -> forecast.py register/grade/verify -> build_outlook.py

| 파일 | 역할 |
|---|---|
| series_catalog.csv | 시리즈·발표 시차·기대 이력·결함 허용치 (변경 시 config_hash 변경) |
| states.yaml | 상태 축·백분위·검정·확률 규칙 (데이터를 보기 전에 고정) |
| macro_lib.py | 알려진 값(look-ahead 차단), 후행 10년 백분위, 히스테리시스, 패널 |
| conditional_dist.py | 상태별 3분위 조건부 분포, 순열검정, Bonferroni, 수축 |
| backtest.py | 워크포워드 Brier/BSS, 검증 게이트 요약 |
| forecast.py | 주간 사전등록(append-only, 해시), 자동 채점, 점수 |
| checks.py | 빈 파일·이력 절단·지연·급변·고정값 검출 |
| build_outlook.py | 사람이 읽는 리포트 생성 |

## 실행
    pip install -r requirements.txt
    python tests/test_macro.py
    export ECOS_API_KEY=...                     # 한국 일별 4종
    python macro/fetch_history.py --full        # 최초 1회 (FRED_API_KEY 없으면 fredgraph.csv 사용)
    python macro/checks.py && python macro/backtest.py --save-summary
    python macro/forecast.py register && python macro/build_outlook.py

## 정직한 한계
- 현재 검증 게이트를 통과한 것은 VIX 평균회귀뿐이며 효과는 작다. 금리·환율·신용·BEI 방향은 기저율 대비 우위가 확인되지 않았다.
- 게이트 선정은 백테스트 전체를 본 뒤의 표본 내 선택이다. 진짜 검증은 forecast_log.csv의 채점 누적(수개월~1년 이상)이다.
- shrink_k=30, 상태 축 선택은 주관 판단이다. 하이일드 OAS는 3년, S&P500은 10년만 제공된다.
- 한국은 ECOS 일별 4종(국고채 3Y·10Y, KOSPI, 원/달러 매매기준율)만 포함한다. `ECOS_API_KEY`(GitHub Secret)가 필요하며, 이력 수집 전에는 outlook에 '미수집'으로 표시되고 확률은 기저율이다. 월간 한국 지표(CPI·기준금리·GDP)는 개정·발표 시차·표본 수 때문에 조건부 분포에 쓰지 않는다. CPI 등 개정 지표와 발표 일정 달력도 포함하지 않았다.
- 규칙(states.yaml, series_catalog.csv)을 바꾸면 해시가 바뀌어 기존 검증이 무효가 되므로 backtest를 다시 실행해야 한다.
