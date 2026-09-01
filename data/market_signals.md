# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-09-01 (oldest: 2026-08-28 ^KS11)
> Freshness: OK (oldest 4d ≤ 5d)
> Generated: 2026-09-01 00:17:18 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 56.6500 | KOSPI YoY=+110.46%, KOSDAQ YoY=+2.84%, KOSPI 4W=+21.37% |
| 2 | Breadth | 🔵 중립 | 0.2860 | RSP/SPY=0.2860 (Ratio, 무차원), 4W Δ=-0.0005 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9588 | SPHB/SPLV=1.9588 (Ratio, 무차원), 4W Δ=+0.0734 |
| 4 | VIX Term | 🟢 contango | 0.8277 | VIX3M=17.53, VIX/VIX3M=0.8277 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-2.04 |
| 5 | 섹터 로테이션 | 🟠 경계 | -4.0400 | XLK 4W=+4.75%, XLE 4W=+8.79%, XLK-XLE=-4.04%p, XLP 4W=+0.14% |
| 6 | 신용 방향 | 🔵 중립 | 0.7514 | HYG/LQD=0.7514 (Ratio, OAS 아님), 4W Δ=+0.0040 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 56.65
- **상세**: KOSPI YoY=+110.46%, KOSDAQ YoY=+2.84%, KOSPI 4W=+21.37%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.286018
- **상세**: RSP/SPY=0.2860 (Ratio, 무차원), 4W Δ=-0.0005
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.958763
- **상세**: SPHB/SPLV=1.9588 (Ratio, 무차원), 4W Δ=+0.0734
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8277
- **상세**: VIX3M=17.53, VIX/VIX3M=0.8277 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-2.04
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -4.04
- **상세**: XLK 4W=+4.75%, XLE 4W=+8.79%, XLK-XLE=-4.04%p, XLP 4W=+0.14%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.751436
- **상세**: HYG/LQD=0.7514 (Ratio, OAS 아님), 4W Δ=+0.0040
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*