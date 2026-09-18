# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-09-18 (oldest: 2026-09-17 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-09-18 22:57:06 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 55.9400 | KOSPI YoY=+109.80%, KOSDAQ YoY=+2.08%, KOSPI 4W=-2.00% |
| 2 | Breadth | 🔵 중립 | 0.2787 | RSP/SPY=0.2787 (Ratio, 무차원), 4W Δ=-0.0101, 4W 하락=대형주 쏠림 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.0318 | SPHB/SPLV=2.0318 (Ratio, 무차원), 4W Δ=+0.0929 |
| 4 | VIX Term | 🔵 중립 | 0.9709 | VIX3M=18.24, VIX/VIX3M=0.9709 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.82 |
| 5 | 섹터 로테이션 | 🔵 중립 | 2.6700 | XLK 4W=+3.55%, XLE 4W=+0.88%, XLK-XLE=+2.67%p, XLP 4W=-2.95% |
| 6 | 신용 방향 | 🔵 중립 | 0.7500 | HYG/LQD=0.7500 (Ratio, OAS 아님), 4W Δ=+0.0009 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 55.94
- **상세**: KOSPI YoY=+109.80%, KOSDAQ YoY=+2.08%, KOSPI 4W=-2.00%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.278709
- **상세**: RSP/SPY=0.2787 (Ratio, 무차원), 4W Δ=-0.0101, 4W 하락=대형주 쏠림
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.031827
- **상세**: SPHB/SPLV=2.0318 (Ratio, 무차원), 4W Δ=+0.0929
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🔵 VIX Term — 중립
- **값**: 0.9709
- **상세**: VIX3M=18.24, VIX/VIX3M=0.9709 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.82
- **시리즈**: ^VIX3M, VIXCLS

### 🔵 섹터 로테이션 — 중립
- **값**: 2.67
- **상세**: XLK 4W=+3.55%, XLE 4W=+0.88%, XLK-XLE=+2.67%p, XLP 4W=-2.95%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.750048
- **상세**: HYG/LQD=0.7500 (Ratio, OAS 아님), 4W Δ=+0.0009
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*