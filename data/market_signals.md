# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-06-15 (oldest: 2026-06-12 ^KS11)
> Freshness: OK (oldest 3d ≤ 5d)
> Generated: 2026-06-15 22:59:12 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 119.1700 | KOSPI YoY=+198.59%, KOSDAQ YoY=+39.76%, KOSPI 4W=+3.56% |
| 2 | Breadth | 🔵 중립 | 0.2820 | RSP/SPY=0.2820 (Ratio, 무차원), 4W Δ=+0.0093, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.0787 | SPHB/SPLV=2.0787 (Ratio, 무차원), 4W Δ=+0.1652 |
| 4 | VIX Term | 🔵 중립 | 1.0041 | VIX3M=19.36, VIX/VIX3M=1.0041 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-2.00 |
| 5 | 섹터 로테이션 | 🟢 확장 | 15.3500 | XLK 4W=+8.81%, XLE 4W=-6.54%, XLK-XLE=+15.35%p, XLP 4W=+0.99% |
| 6 | 신용 방향 | 🔵 중립 | 0.7344 | HYG/LQD=0.7344 (Ratio, OAS 아님), 4W Δ=-0.0013 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 119.17
- **상세**: KOSPI YoY=+198.59%, KOSDAQ YoY=+39.76%, KOSPI 4W=+3.56%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.282024
- **상세**: RSP/SPY=0.2820 (Ratio, 무차원), 4W Δ=+0.0093, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.078706
- **상세**: SPHB/SPLV=2.0787 (Ratio, 무차원), 4W Δ=+0.1652
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🔵 VIX Term — 중립
- **값**: 1.0041
- **상세**: VIX3M=19.36, VIX/VIX3M=1.0041 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-2.00
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 15.35
- **상세**: XLK 4W=+8.81%, XLE 4W=-6.54%, XLK-XLE=+15.35%p, XLP 4W=+0.99%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.734379
- **상세**: HYG/LQD=0.7344 (Ratio, OAS 아님), 4W Δ=-0.0013
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*