# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-08-10 (oldest: 2026-08-07 ^KS11)
> Freshness: OK (oldest 3d ≤ 5d)
> Generated: 2026-08-10 21:34:40 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 47.4100 | KOSPI YoY=+95.83%, KOSDAQ YoY=-1.01%, KOSPI 4W=-14.17% |
| 2 | Breadth | 🔵 중립 | 0.2849 | RSP/SPY=0.2849 (Ratio, 무차원), 4W Δ=-0.0011 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9387 | SPHB/SPLV=1.9387 (Ratio, 무차원), 4W Δ=+0.0285 |
| 4 | VIX Term | 🟢 contango | 0.7982 | VIX3M=18.98, VIX/VIX3M=0.7982 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.59 |
| 5 | 섹터 로테이션 | 🟠 경계 | -3.2800 | XLK 4W=+2.78%, XLE 4W=+6.06%, XLK-XLE=-3.28%p, XLP 4W=+0.43% |
| 6 | 신용 방향 | 🟢 완화 | 0.7501 | HYG/LQD=0.7501 (Ratio, OAS 아님), 4W Δ=+0.0070 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 47.41
- **상세**: KOSPI YoY=+95.83%, KOSDAQ YoY=-1.01%, KOSPI 4W=-14.17%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.284879
- **상세**: RSP/SPY=0.2849 (Ratio, 무차원), 4W Δ=-0.0011
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.938705
- **상세**: SPHB/SPLV=1.9387 (Ratio, 무차원), 4W Δ=+0.0285
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.7982
- **상세**: VIX3M=18.98, VIX/VIX3M=0.7982 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.59
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -3.28
- **상세**: XLK 4W=+2.78%, XLE 4W=+6.06%, XLK-XLE=-3.28%p, XLP 4W=+0.43%
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.750094
- **상세**: HYG/LQD=0.7501 (Ratio, OAS 아님), 4W Δ=+0.0070
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*