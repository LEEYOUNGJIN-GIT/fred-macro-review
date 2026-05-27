# 📊 FRED Macro Review — 거시경제 자동 모니터링

> **FRED API → 95개 지표 수집 → 18개 파생 신호 → 2×2 레짐 분류 → claude.ai 자동 분석**

[![FRED Daily Fetch](https://github.com/LEEYOUNGJIN-GIT/fred-macro-review/actions/workflows/fred_daily.yml/badge.svg)](https://github.com/LEEYOUNGJIN-GIT/fred-macro-review/actions/workflows/fred_daily.yml)

---

## 📐 아키텍처

```
┌─────────────┐     92 API calls     ┌──────────────────────┐
│  FRED API   │ ──────────────────►  │  fred_fetch.py       │
│ (stlouisfed)│                      │  92 시리즈 + 3 파생  │
└─────────────┘                      │  = 95개 지표         │
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
```

---

## 📁 파일 구조

```
fred-macro-review/
├── .github/
│   └── workflows/
│       └── fred_daily.yml          ← GitHub Actions (매일 KST 06:10)
├── scripts/
│   ├── Fred_signals.py             ← 18개 파생 신호 대시보드
│   └── Fred_regime.py              ← 2×2 레짐 분류 엔진
├── data/
│   ├── .gitkeep
│   ├── fred_latest.csv             ← 최신 원천 데이터 (자동 생성)
│   ├── fred_latest.md              ← Claude용 팩트 테이블 (자동 생성)
│   ├── fred_signals.md             ← 18개 신호 보고서 (자동 생성)
│   ├── fred_regime.md              ← 레짐 분류 보고서 (자동 생성)
│   └── fred_history/
│       └── fred_YYYYMMDD_HHMMSS.csv  ← 일별 히스토리 (자동)
├── fred_fetch.py                   ← FRED API 수집 + 팩트 테이블 생성
├── requirements.txt                ← pandas, requests
├── .gitignore
└── README.md
```

---

## 📊 시리즈 레지스트리 (95개 = 92 API + 3 파생)

| # | 카테고리 | 시리즈 수 | 주요 시리즈 |
|---|----------|-----------|-------------|
| 01 | 금리·채권 | 14 | T10Y2Y, DFII10, T10YIE, DGS2, DGS10, DFF, FEDFUNDS, SOFR, BAA10Y |
| 02 | 리스크·신용 | 3 | VIXCLS, BAMLH0A0HYM2, TOTBKCR |
| 03 | 금융 스트레스 | 4 | NFCI, STLFSI4, KCFSI, CFNAI |
| 04 | 노동시장 | 7 | UNRATE, PAYEMS, ICSA, CCSA, JTSJOL, CIVPART, CES0500000003 |
| 05 | 물가·인플레 | 6 | CPIAUCSL, CPILFESL, PCEPI, PCEPILFE, PPIFIS, MICH |
| 06 | GDP·생산 | 6 | GDP, GDPC1, INDPRO, RSAFS, DGORDER, CMRMTSPL |
| 07 | 소비심리·통화 | 2 | UMCSENT, M2SL |
| 08 | 주택시장 | 5 | CSUSHPINSA, HOUST, PERMIT, MORTGAGE30US, EXHOSLUSM495S |
| 09 | 무역·국제수지 | 5 | NETFI, FYFSD, BOPGSTB, EXPGS, IMPGS |
| 10 | 환율·달러 | 4 | DEXKOUS, DTWEXBGS, DTWEXAFEGS, DTWEXEMEGS |
| 11 | Fed 유동성 | 5 | WALCL, RRPONTSYD, WTREGEN, TOTRESNS, BOGMBASE |
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
| 10 | 노동 시장 | UNRATE, PAYEMS, ICSA, JTSJOL | 종합점수 0-10 |
| 11 | 유동성 | RRPONTSYD, TOTRESNS, WALCL, BOGMBASE | 종합점수 0-10 |
| 12 | 원자재 압력 | DCOILWTICO, PALLFNFINDEXM, PCOPPUSDM | 압력지수 ±4 |
| 13 | 달러 추세 | DTWEXBGS, DEXKOUS | YoY ≥5 강한 강세 |
| 14 | 소비자 심리 | UMCSENT | <50 심각한 위축 |
| 15 | 주택시장 | MORTGAGE30US, HOUST, CSUSHPINSA | 종합점수 0-10 |
| 16 | 무역·재정 | BOPGSTB, FYFSD | 적자 확대 경계 |
| 17 | 한국 크로스 | KOR_US_*_SPREAD, CLI, DEXKOUS | 종합점수 0-10 |
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

---

## 🤖 claude.ai 연동

### GitHub 통합

1. [claude.ai](https://claude.ai) → Settings → Integrations → **GitHub** 연결
2. `LEEYOUNGJIN-GIT/fred-macro-review` 레포 선택
3. 대화 시작 시 자동으로 `data/` 폴더의 4개 파일 참조:
   - `fred_latest.md` — 95개 원천 팩트 테이블
   - `fred_signals.md` — 18개 신호 대시보드
   - `fred_regime.md` — 레짐 분류 보고서
   - `fred_latest.csv` — 상세 데이터 (필요 시)

### 분석 프롬프트 예시

```
@fred-macro-review 의 data/fred_signals.md, data/fred_regime.md, data/fred_latest.md 를 읽고
아래 분석을 수행해 주세요:

1. 현재 매크로 레짐과 18개 신호의 핵심 시사점 요약
2. 전주 대비 가장 큰 변화를 보인 상위 3개 지표
3. 향후 1~3개월 리스크 시나리오 (Bull / Base / Bear)
4. 한국 투자자 관점의 시사점 (원화, 금리, 주식)
```

---

## 📅 스케줄

| 항목 | 값 |
|------|-----|
| 실행 주기 | 매일 KST 06:10 (UTC 21:10, GitHub 부하 시 지연 가능) |
| API 호출 수 | 92회 (시리즈당 1회, 0.5초 간격) |
| 금일 데이터 포함 여부 | FRED 발표 시점 의존 (D: 당일·전일, M/Q: 전월·전분기) |
| 히스토리 보관 | data/fred_history/ 에 일별 CSV 자동 저장 |
| 수동 실행 | Actions → `Run workflow` |

---

## 📦 requirements.txt

```
pandas>=2.0
requests>=2.28
numpy>=1.24
```

---

## 🔑 License

이 프로젝트는 개인 학습·분석 목적으로 제작되었습니다.
FRED 데이터는 [Federal Reserve Bank of St. Louis](https://fred.stlouisfed.org/)의 이용약관을 따릅니다.
