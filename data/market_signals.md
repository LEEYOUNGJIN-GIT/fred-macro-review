# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-09-09 (oldest: 2026-09-07 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-09-08 23:05:59 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 60.4800 | KOSPI YoY=+117.93%, KOSDAQ YoY=+3.03%, KOSPI 4W=+11.77% |
| 2 | Breadth | 🔵 중립 | 0.2830 | RSP/SPY=0.2830 (Ratio, 무차원), 4W Δ=-0.0019 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.0052 | SPHB/SPLV=2.0052 (Ratio, 무차원), 4W Δ=+0.0629 |
| 4 | VIX Term | 🟢 contango | 0.7787 | VIX3M=18.39, VIX/VIX3M=0.7787 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.18 |
| 5 | 섹터 로테이션 | 🟠 경계 | -6.8000 | XLK 4W=+0.83%, XLE 4W=+7.63%, XLK-XLE=-6.80%p, XLP 4W=-1.09% |
| 6 | 신용 방향 | 🔵 중립 | 0.7501 | HYG/LQD=0.7501 (Ratio, OAS 아님), 4W Δ=+0.0010 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 60.48
- **상세**: KOSPI YoY=+117.93%, KOSDAQ YoY=+3.03%, KOSPI 4W=+11.77%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.282952
- **상세**: RSP/SPY=0.2830 (Ratio, 무차원), 4W Δ=-0.0019
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.005231
- **상세**: SPHB/SPLV=2.0052 (Ratio, 무차원), 4W Δ=+0.0629
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.7787
- **상세**: VIX3M=18.39, VIX/VIX3M=0.7787 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.18
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -6.8
- **상세**: XLK 4W=+0.83%, XLE 4W=+7.63%, XLK-XLE=-6.80%p, XLP 4W=-1.09%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.750095
- **상세**: HYG/LQD=0.7501 (Ratio, OAS 아님), 4W Δ=+0.0010
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*