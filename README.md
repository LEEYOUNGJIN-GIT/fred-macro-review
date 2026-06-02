# 📊 FRED Macro Review — 거시경제 자동 모니터링

> **FRED API → 101개 지표 수집 → 18개 파생 신호 → 2×2 레짐 분류 → Yahoo Finance 보조 25지표 → claude.ai 자동 분석**

[![FRED Daily Fetch](https://github.com/LEEYOUNGJIN-GIT/fred-macro-review/actions/workflows/fred_daily.yml/badge.svg)](https://github.com/LEEYOUNGJIN-GIT/fred-macro-review/actions/workflows/fred_daily.yml)
[![Market Daily Fetch](https://github.com/LEEYOUNGJIN-GIT/fred-macro-review/actions/workflows/market_daily.yml/badge.svg)](https://github.com/LEEYOUNGJIN-GIT/fred-macro-review/actions/workflows/market_daily.yml)
[![AV Daily Fetch](https://github.com/LEEYOUNGJIN-GIT/fred-macro-review/actions/workflows/av_daily.yml/badge.svg)](https://github.com/LEEYOUNGJIN-GIT/fred-macro-review/actions/workflows/av_daily.yml)

---

## 📐 아키텍처

```
┌─────────────┐     98 API calls     ┌──────────────────────┐
│  FRED API   │ ──────────────────►  │  fred_fetch.py       │
│ (stlouisfed)│                      │  98 시리즈 + 3 파생  │
└─────────────┘                      │  = 101개 지표        │
                                     └──────┬───────────────┘
                                            │
                                 ┌──────────▼──────────┐
                                 │  data/               │
                                 │  ├ fred_latest.csv   │  ← 원천 데이터
                                 │  └ fred_latest.md    │  ← 팩트 테이블
                                 └──────────┬───────────┘
                                            │
                        ┌───────────────────┼───────────────────┐
                        ▼                                       ▼
              ┌──────────────────┐                   ┌──────────────────┐
              │ Fred_signals.py  │                   │ Fred_regime.py   │
              │ 18개 파생 신호    │                   │ 성장·인플레 점수  │
              │ 종합 위험도       │                   │ 2×2 레짐 분류    │
              └────────┬─────────┘                   └────────┬─────────┘
                       │                                      │
                       ▼                                      ▼
              fred_signals.md                        fred_regime.md
                       │                                      │
                       └──────────────┬───────────────────────┘
                                      ▼
                              ┌───────────────┐
                              │  claude.ai    │
                              │  GitHub 연동   │
                              │  자동 분석     │
                              └───────────────┘

┌──────────────┐                      ┌──────────────────────┐
│ Yahoo Finance│ ──────────────────►  │  market_fetch.py     │
│  (yfinance)  │                      │  22 + 3 derived = 25 │
└──────────────┘                      └──────┬───────────────┘
                                             │
                                  ┌──────────▼──────────┐
                                  │  data/ (보조지표)    │
                                  │  market_latest.*    │
                                  └──────────┬───────────┘
                                             ▼
                                  ┌──────────────────────┐
                                  │ Market_signals.py    │
                                  │ 6개 보조 신호         │
                                  └──────────┬───────────┘
                                             ▼
                                  market_signals.md
                                             │
                       (FRED 레이어와 merge 없음 — 충돌 시 FRED 우선)

┌──────────────────┐                      ┌──────────────────────┐
│ Alpha Vantage    │ ─ 11 calls/day ───►  │  av_fetch.py         │
│ (commodities/FX/ │                      │  12 series           │
│  crypto)         │                      └──────┬───────────────┘
└──────────────────┘                             │
                                      ┌──────────▼──────────┐
                                      │  data/ (AV 보조)     │
                                      │  av_latest.*         │
                                      └──────────┬───────────┘
                                                 ▼
                                      ┌──────────────────────┐
                                      │  Av_signals.py       │
                                      │  5개 보조 신호        │
                                      └──────────┬───────────┘
                                                 ▼
                                      av_signals.md
                                                 │
              (FRED > Market/Global > AV — merge 없음)
```

---

## 📁 파일 구조

```
fred-macro-review/
├── .github/
│   └── workflows/
│       ├── fred_daily.yml          ← FRED (매일 KST 06:10)
│       ├── market_daily.yml        ← Market 보조 (KST 화~토 06:00)
│       ├── global_daily.yml        ← Global 보조 (매일 KST 06:20)
│       ├── av_daily.yml            ← AV 보조 (매일 KST 06:25)
│       └── sync_claude_project.yml ← Claude Project 5파일 sync
├── scripts/
│   ├── Fred_signals.py             ← 18개 파생 신호 대시보드
│   ├── Fred_regime.py              ← 2×2 레짐 분류 엔진
│   ├── Market_signals.py           ← 6개 보조 신호
│   ├── Global_signals.py           ← 5개 글로벌 보조 신호
│   └── Av_signals.py               ← 5개 AV 보조 신호
├── data/
│   ├── .gitkeep
│   ├── fred_latest.csv             ← FRED 원천 (공식)
│   ├── fred_latest.md
│   ├── fred_signals.md
│   ├── fred_regime.md
│   ├── market_latest.csv           ← Yahoo 보조 (25 row 고정)
│   ├── market_latest.md
│   ├── market_signals.md
│   ├── global_latest.csv           ← WB/OECD/IMF/ECB 보조
│   ├── global_latest.md
│   ├── global_signals.md
│   ├── av_latest.csv               ← Alpha Vantage 보조 (12 row)
│   ├── av_latest.md
│   ├── av_signals.md
│   ├── fred_history/
│   ├── market_history/
│   ├── global_history/
│   └── av_history/
├── fred_fetch.py
├── market_fetch.py                 ← Yahoo Finance 보조 수집
├── global_fetch.py
├── av_fetch.py                     ← Alpha Vantage 보조 수집
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Market 보조 레이어 (v1)

**공식 거시 = FRED** / **보조 = Yahoo Finance** (merge 없음)

| 항목 | 내용 |
|------|------|
| 지표 수 | 25 row 고정 (22 raw + 3 Ratio) |
| fetch 정책 | 100% 성공 아니면 파일 미갱신 |
| 단위 | Index / USD(ETF) / Ratio(무차원) — md·note에 명시 |
| 미포함 | 금리, VIX, SP500, WTI, USD/KRW 등 FRED 담당 |
| 신호 | 6개 (`Market_signals.py`) — fred_signals 보완 |

### 보조 지표 manifest (25)

| cat | series | unit |
|-----|--------|------|
| 한국 | ^KS11, ^KQ11 | Index |
| 미국 | ^NDX, ^RUT | Index |
| 변동성 | ^VIX3M | Index |
| breadth/risk | RSP, SPY, SPHB, SPLV | USD |
| 섹터 | XLK, XLF, XLE, XLP, XLU, XLY | USD |
| 신용 | KRE, HYG, LQD | USD |
| 글로벌 | ^N225, ^HSI, EEM | Index/USD |
| FX | AUDJPY=X | JPY_per_AUD |
| 파생 | MARKET_BREADTH, MARKET_RISK_ON, HYG_LQD_RATIO | Ratio |

---

## 📊 시리즈 레지스트리 (101개 = 98 API + 3 파생)

| # | 카테고리 | 시리즈 수 | 주요 시리즈 |
|---|----------|-----------|-------------|
| 01 | 금리·채권 | 14 | T10Y2Y, DFII10, T10YIE, DGS2, DGS10, DFF, FEDFUNDS, SOFR, BAA10Y |
| 02 | 리스크·신용 | 3 | VIXCLS, BAMLH0A0HYM2, TOTBKCR |
| 03 | 금융 스트레스 | 4 | NFCI, STLFSI4, KCFSI, CFNAI |
| 04 | 노동시장 | 9 | UNRATE, PAYEMS, ICSA, CCSA, JTSJOL, JTSQUR, CIVPART, LNS11300060, CES0500000003 |
| 05 | 물가·인플레 | 6 | CPIAUCSL, CPILFESL, PCEPI, PCEPILFE, PPIFIS, MICH |
| 06 | GDP·생산 | 6 | GDP, GDPC1, INDPRO, RSAFS, DGORDER, CMRMTSPL |
| 07 | 소비심리·통화 | 2 | UMCSENT, M2SL |
| 08 | 주택시장 | 5 | CSUSHPINSA, HOUST, PERMIT, MORTGAGE30US, EXHOSLUSM495S |
| 09 | 무역·국제수지 | 5 | NETFI, FYFSD, BOPGSTB, EXPGS, IMPGS |
| 10 | 환율·달러 | 6 | DEXKOUS, DTWEXBGS, DTWEXAFEGS, DTWEXEMEGS, DEXJPUS, DEXCHUS |
| 11 | Fed 유동성 | 7 | WALCL, TREAST, WSHOMCB, RRPONTSYD, WTREGEN, TOTRESNS, BOGMBASE |
| 12 | 원자재 | 11 | NASDAQQGLDI, DCOILWTICO, PCOPPUSDM, PNICKUSDM, PALLFNFINDEXM 등 |
| 13 | 주가지수 | 1 | SP500 |
| 15 | 파생지표 | 3 | COPPER_GOLD_RATIO, KOR_US_POLICY_SPREAD, KOR_US_10Y_SPREAD |
| 16 | 침체 조기 경보 | 2 | T10Y3M, SAHMREALTIME |
| 17 | 생산·경기 | 4 | TCU, ISRATIO, AMTMNO, MANEMP |
| 18 | 소비·가계 | 4 | PSAVERT, TOTALSA, DSPIC96, PCEC96 |
| 19 | 신용·연체 | 4 | DRCCLACBS, DRSFRMACBS, BUSLOANS, CONSUMER |
| 20 | 한국 거시 | 5 | IRSTCI01KRM156N, IRLTLT01KRM156N, LRHUTTTTKRM156S, KORLOLITOAASTSAM, NGDPRSAXDCKRQ |

---

## 📡 신호 대시보드 (18개)

`scripts/Fred_signals.py`가 생성하는 18개 파생 신호:

| # | 신호 | 주요 입력 | 임계 기준 |
|---|------|----------|-----------|
| 1 | 장단기 스프레드 | T10Y2Y, T10Y3M | <0 역전 → 침체 경고 |
| 2 | Sahm Rule | SAHMREALTIME, UNRATE | ≥0.5 발동 → 침체 확인 |
| 3 | 실질금리 갭 | DFF − Core PCE YoY | ≥2.0 강한 긴축 |
| 4 | TIPS 실질금리 | DFII10 | ≥2.5 강한 긴축 |
| 5 | VIX 레짐 | VIXCLS | ≥30 위기, ≥40 패닉 |
| 6 | 인플레이션 레짐 | PCEPILFE, CPIAUCSL, PPIFIS | ≥3.5 고인플레 |
| 7 | 인플레 기대 | MICH, T5YIE, T5YIFR | 점수 ≥4 디앵커링 경계 |
| 8 | 신용 스트레스 | BAMLH0A0HYM2, BAA10Y, DRCCLACBS | HY OAS ≥4 경계 |
| 9 | 금융 스트레스 | NFCI, STLFSI4, KCFSI | 평균 ≥0.5 스트레스 |
| 10 | 노동 시장 | UNRATE, PAYEMS, ICSA, JTSJOL, JTSQUR, LNS11300060 | 종합점수 0-10 |
| 11 | 유동성 | RRPONTSYD, TOTRESNS, WALCL, BOGMBASE, TREAST, WSHOMCB | 종합점수 0-10 |
| 12 | 원자재 압력 | DCOILWTICO, PALLFNFINDEXM, PCOPPUSDM | 압력지수 ±4 |
| 13 | 달러 추세 | DTWEXBGS, DEXKOUS, DEXJPUS, DEXCHUS | YoY ≥5 강한 강세 (status); FX detail |
| 14 | 소비자 심리 | UMCSENT | <50 심각한 위축 |
| 15 | 주택시장 | MORTGAGE30US, HOUST, CSUSHPINSA | 종합점수 0-10 |
| 16 | 무역·재정 | BOPGSTB, FYFSD | 적자 확대 경계 |
| 17 | 한국 크로스 | KOR_US_*_SPREAD, CLI, DEXKOUS, DEXCHUS | 종합점수 0-10 |
| 18 | 소비 동향 | PCEC96, PSAVERT, TOTALSA | 종합점수 0-10 |

**종합 위험도**: 70%×평균 + 30%×최대 → 5단계 (🟢안정 → 🔴위험)

---

## 🏛️ 레짐 분류 (2×2 매트릭스)

`scripts/Fred_regime.py`가 생성하는 매크로 레짐:

```
        인플레 ↑ (>5)
             │
 ⚠️ Stagflation  │  🔥 Overheating
  (성장↓ 인플레↑) │  (성장↑ 인플레↑)
─────────────┼──────────────  성장 →
 ❄️ Recession    │  ✨ Goldilocks
  (성장↓ 인플레↓) │  (성장↑ 인플레↓)
             │
        인플레 ↓ (≤5)
```

| 레짐 | 성장 | 인플레 | 시사점 |
|------|------|--------|--------|
| ✨ Goldilocks | >5 | ≤5 | 위험자산 우호, 안정적 정책 |
| 🔥 Overheating | >5 | >5 | 긴축 가능성, 실질금리 상승 |
| ⚠️ Stagflation | ≤5 | >5 | 정책 딜레마, 방어적 포지셔닝 |
| ❄️ Recession Risk | ≤5 | ≤5 | 부양 기대, 안전자산 선호 |

**성장 점수** (10요소): GDP, 산업생산, 소매판매, 고용, CFNAI, 소비자심리, 제조업신규주문, 설비가동률, S&P500, 실질소비
**인플레 점수** (10요소): Core PCE, CPI, PPI, 인플레기대, 5Y5Y선도, 임금, 원자재, 유가, 주택가격, 모기지

---

## ⚙️ 설정 방법

### 1단계: FRED API 키 발급

[FRED API Keys](https://fred.stlouisfed.org/docs/api/api_key.html)에서 무료 발급

### 2단계: GitHub Secrets 등록

`Settings → Secrets → Actions → New repository secret`

| Name | Value |
|------|-------|
| `FRED_API_KEY` | 발급받은 API 키 |
| `ALPHAVANTAGE_API_KEY` | [Alpha Vantage](https://www.alphavantage.co/support/#api-key) 무료 키 (일 25 calls, 5/min) |

### 3단계: 워크플로우 확인

`.github/workflows/fred_daily.yml`이 매일 **KST 06:10** (UTC 21:10)에 실행.

```yaml
# 실행 순서
1. fred_fetch.py          → data/fred_latest.csv, data/fred_latest.md
2. scripts/Fred_signals.py → data/fred_signals.md
3. scripts/Fred_regime.py  → data/fred_regime.md
4. git commit & push
```

`Actions` 탭 → `Run workflow` 로 수동 실행도 가능.

### 4단계: Market 보조 워크플로우

`.github/workflows/market_daily.yml` — **KST 화~토 06:00** (미국 일봉 확정 후).

```yaml
# 실행 순서
1. market_fetch.py           → data/market_latest.csv, data/market_latest.md
2. scripts/Market_signals.py → data/market_signals.md
3. git commit & push
```

- FRED API 키 불필요 (yfinance)
- 22 ticker 중 1개라도 실패 시 **파일 미갱신** (100% 정책)

### 5단계: Alpha Vantage 보조 워크플로우

`.github/workflows/av_daily.yml` — **매일 KST 06:25** (Global 06:20 직후).

```yaml
# 실행 순서
1. av_fetch.py           → data/av_latest.csv, data/av_latest.md
2. scripts/Av_signals.py → data/av_signals.md
3. git commit & push
```

- **12 API calls / 12 series** (GLD/SLV 금속 프록시, 원자재 5종 incl. BRENT, FX 3, BTC/ETH)
- `REQUEST_DELAY=13s` + 분당 5회 슬라이딩 윈도우로 rate limit 준수
- 1 call이라도 실패 시 **파일 미갱신** (strict)
- 공식 유가는 FRED `DCOILWTICO`(WTI); BRENT·크립토는 보조

---

## AV 보조 레이어 (v2)

**우선순위**: FRED > Market / Global > **AV**

| 항목 | 내용 |
|------|------|
| 지표 수 | 12 row (12 API calls) |
| fetch 정책 | 12/12 성공 필수, 아니면 미갱신 |
| Rate limit | 무료 25/day, 5/min — 코드에서 throttle |
| 원자재 | Cu, Al, Wheat, Corn, **Brent** (월간, FRED IMF 보완) |
| FX | USD/KRW, USD/JPY, USD/CNY (일간) |
| 크립토 | BTC, ETH (일간, risk sentiment 보조) |
| 금속 | GLD/SLV ETF daily (AV gold/silver spot API 미지원) |
| 신호 | 5개 (`Av_signals.py`) |

---

## 🤖 claude.ai 연동

### GitHub 통합

1. [claude.ai](https://claude.ai) → Settings → Integrations → **GitHub** 연결
2. `LEEYOUNGJIN-GIT/fred-macro-review` 레포 선택
3. 대화 시작 시 참조 파일:
   - **공식 (FRED)**: `fred_latest.md`, `fred_signals.md`, `fred_regime.md`
   - **보조 (Yahoo)**: `market_latest.md`, `market_signals.md`
   - **보조 (Global)**: `global_latest.md`, `global_signals.md`
   - **보조 (AV)**: `av_latest.md`, `av_signals.md`
   - 충돌 시 **FRED > Market/Global > AV**

### 분석 프롬프트 예시

```
@fred-macro-review 의 fred_latest.md, fred_signals.md, fred_regime.md 를 공식 거시 기준으로,
market_latest.md, market_signals.md 를 보조(시장·한국·breadth)로 읽고 아래 분석을 수행해 주세요:

1. FRED 레짐·18신호 핵심 시사점
2. Market 보조 6신호 (한국/Breadth/섹터 등)
3. 향후 1~3개월 Bull/Base/Bear
4. 한국 투자자 관점 시사점
```

---

## 📅 스케줄

| 항목 | FRED | Market | Global | AV |
|------|------|--------|--------|-----|
| 실행 주기 | 매일 KST 06:10 | 화~토 06:00 | 매일 06:20 | 매일 06:25 |
| API | FRED 98회 | yfinance 22 | WB/OECD/IMF/ECB | AV 12 calls |
| fetch 정책 | 50% 미만 중단 | 100% strict | 50% 미만 | **100% strict** |
| 히스토리 | fred_history/ | market_history/ | global_history/ | av_history/ |
| 수동 실행 | FRED Daily Fetch | Market Daily Fetch | Global Daily Fetch | AV Daily Fetch |

---

## 📦 requirements.txt

```
pandas>=2.1
requests>=2.31
numpy>=1.24
yfinance>=0.2
```

---

## 🔑 License

이 프로젝트는 개인 학습·분석 목적으로 제작되었습니다.
FRED 데이터는 [Federal Reserve Bank of St. Louis](https://fred.stlouisfed.org/)의 이용약관을 따릅니다.
