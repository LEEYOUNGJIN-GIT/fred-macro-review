# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-07-14 (oldest: 2026-07-13 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-07-14 21:52:15 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 61.1600 | KOSPI YoY=+120.31%, KOSDAQ YoY=+2.00%, KOSPI 4W=-20.35% |
| 2 | Breadth | 🔵 중립 | 0.2839 | RSP/SPY=0.2839 (Ratio, 무차원), 4W Δ=-0.0011 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9470 | SPHB/SPLV=1.9470 (Ratio, 무차원), 4W Δ=-0.0515 |
| 4 | VIX Term | 🟢 contango | 0.7788 | VIX3M=19.30, VIX/VIX3M=0.7788 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-2.12 |
| 5 | 섹터 로테이션 | 🟡 둔화 | -0.1900 | XLK 4W=-0.52%, XLE 4W=-0.33%, XLK-XLE=-0.19%p, XLP 4W=-2.12% |
| 6 | 신용 방향 | 🟢 완화 | 0.7432 | HYG/LQD=0.7432 (Ratio, OAS 아님), 4W Δ=+0.0107 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 61.16
- **상세**: KOSPI YoY=+120.31%, KOSDAQ YoY=+2.00%, KOSPI 4W=-20.35%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.283907
- **상세**: RSP/SPY=0.2839 (Ratio, 무차원), 4W Δ=-0.0011
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.947042
- **상세**: SPHB/SPLV=1.9470 (Ratio, 무차원), 4W Δ=-0.0515
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.7788
- **상세**: VIX3M=19.30, VIX/VIX3M=0.7788 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-2.12
- **시리즈**: ^VIX3M, VIXCLS

### 🟡 섹터 로테이션 — 둔화
- **값**: -0.19
- **상세**: XLK 4W=-0.52%, XLE 4W=-0.33%, XLK-XLE=-0.19%p, XLP 4W=-2.12%
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.743214
- **상세**: HYG/LQD=0.7432 (Ratio, OAS 아님), 4W Δ=+0.0107
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*