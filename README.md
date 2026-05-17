# 📊 FRED Macro Review — 거시경제 자동 모니터링

> **FRED API 78개 거시경제 지표 → GitHub Actions 자동 수집 → claude.ai 연동 분석**

---

## 🏗️ 아키텍처

```
┌──────────────────┐     ┌─────────────────────┐     ┌─────────────────┐
│  GitHub Actions   │────▶│  FRED API (77개)     │────▶│  data/ 폴더      │
│  cron: KST 08:30 │     │  + 파생지표 1개       │     │  CSV + MD 저장   │
└──────────────────┘     └─────────────────────┘     └────────┬────────┘
                                                              │
                                                              ▼
                                                     ┌─────────────────┐
                                                     │  claude.ai       │
                                                     │  GitHub 연동      │
                                                     │  분석 보고서 생성  │
                                                     └─────────────────┘
```

---

## 📁 파일 구조

```
fred-macro-review/
├── .github/
│   └── workflows/
│       └── fred_daily.yml        ← GitHub Actions 워크플로우
├── data/
│   ├── .gitkeep                  ← 빈 폴더 추적용
│   ├── fred_latest.csv           ← 최신 원천 데이터 (자동 생성)
│   ├── fred_latest.md            ← Claude용 요약 컨텍스트 (자동 생성)
│   └── fred_history/
│       └── fred_YYYYMMDD_HHMMSS.csv  ← 히스토리 보관
├── fred_fetch.py                 ← FRED API 조회 + 팩트 테이블 생성
├── requirements.txt              ← Python 의존성
├── .gitignore
└── README.md
```

---

## 🚀 셋업 가이드 (3단계)

### Step 1: GitHub Repository 생성

```bash
# 1. 이 폴더를 repo로 초기화
git init
git add .
git commit -m "Initial commit"

# 2. GitHub에 새 repo 생성 후 push
git remote add origin https://github.com/<USERNAME>/fred-macro-review.git
git branch -M main
git push -u origin main
```

### Step 2: GitHub Secrets 등록

1. **Repository** → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** 클릭
3. 다음 시크릿 추가:

| Name | Value |
|------|-------|
| `FRED_API_KEY` | FRED API 키 (https://fred.stlouisfed.org/docs/api/api_key.html 에서 발급) |

### Step 3: GitHub Actions 실행 확인

1. **Actions** 탭 → **FRED Daily Fetch for Claude** 선택
2. **Run workflow** 클릭 → 수동 실행
3. 성공 시 `data/` 폴더에 파일 생성 확인

---

## 🔗 claude.ai 연동

1. [claude.ai](https://claude.ai) 접속
2. **Settings** → **Connected Apps** → **GitHub** 연결
3. **Project** 생성 → **Project Knowledge** → **Add from GitHub**
4. 해당 repo 선택 → `data/fred_latest.md`, `data/fred_latest.csv` 추가
5. **Sync** 활성화 → Actions 실행마다 자동 최신화

> ⚠️ **Private repo**인 경우 GitHub App 권한 승인이 필요합니다.

---

## 📋 수집 지표 (15개 카테고리, 78개 시리즈)

| # | 카테고리 | 개수 | 대표 시리즈 |
|--:|----------|:----:|-------------|
| 01 | 금리·채권 | 15 | DGS2, DGS10, DGS30, T10Y2Y, DFF, SOFR, BAA10Y |
| 02 | 리스크·신용 | 3 | VIX, HY Spread, Bank Credit |
| 03 | 금융스트레스 | 4 | NFCI, STL FSI, KC FSI, CFNAI |
| 04 | 노동시장 | 7 | 실업률, NFP, JOLTS, 신규실업청구, 임금 |
| 05 | 물가·인플레 | 7 | CPI, Core CPI, PCE, Core PCE, PPI, Michigan |
| 06 | GDP·생산 | 6 | 명목/실질 GDP, 산업생산, 소매판매, 내구재 |
| 07 | 소비심리·통화 | 2 | Michigan Sentiment, M2 |
| 08 | 주택시장 | 5 | Case-Shiller, 착공, 허가, 모기지, 기존주택 |
| 09 | 무역·국제수지 | 5 | 경상수지, 재정적자, 무역수지, 수출/수입 |
| 10 | 환율·달러 | 5 | USD/KRW, USD/BRL, Dollar Index |
| 11 | Fed 유동성 | 5 | Fed 총자산, 역레포, TGA, 지준, 본원통화 |
| 12 | 원자재 | 12 | 금, WTI, 구리, 철광석, 곡물, 전체 Index |
| 13 | 주가지수 | 1 | S&P 500 |
| 14 | 브라질 | 2 | SELIC 프록시, 재정수지 |
| 15 | 파생지표 | 1 | 구리/금 비율 (Calculated) |

---

## 📊 분석 프롬프트

`fred_latest.md`가 생성되면 claude.ai에서 아래 프롬프트로 분석을 요청합니다:

```
당신은 글로벌 매크로 이코노미스트입니다.
연결된 fred_latest.md 팩트 테이블을 분석하여 거시경제 검토 보고서를 작성하세요.

보고서 구조:
1. 핵심 요약 (Executive Summary) — 레짐 정의 + 핵심 변화 3가지 + 위험도 5단계
2. 카테고리별 분석 (15개) — 현황·방향성·추세·리스크 수준
3. 교차 시그널 분석 (7개 조합) — 장단기스프레드+실업률, Core PCE+기준금리 등
4. 레짐 판단 — Goldilocks/Reflation/Overheating/Stagflation/Slowdown/Recession
5. 모니터링 우선순위 (Top 5) — 임계값 시나리오 제시
```

> 상세 분석 프롬프트는 FRED.txt 섹션 8을 참고하세요.

---

## ⏰ 실행 스케줄

| 항목 | 값 |
|------|-----|
| **자동 실행** | 매일 UTC 23:30 (KST 08:30) |
| **수동 실행** | Actions 탭 → Run workflow |
| **데이터 범위** | 최근 3년 (1,095일) |
| **API 호출** | 77회 (rate limit: 0.5초 간격) |
| **예상 소요** | 약 1~2분 |
| **최소 성공률** | 50% 미만 시 자동 중단 |

---

## 📜 라이선스

이 프로젝트는 내부 업무용으로 제작되었습니다.
FRED API 데이터는 [Federal Reserve Bank of St. Louis](https://fred.stlouisfed.org/) 제공이며,
해당 데이터의 이용 약관을 준수해야 합니다.
