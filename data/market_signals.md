# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-07-02 (oldest: 2026-06-30 ^HSI)
> Freshness: OK (oldest 2d ≤ 5d)
> Generated: 2026-07-02 22:01:54 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 98.8100 | KOSPI YoY=+178.85%, KOSDAQ YoY=+18.77%, KOSPI 4W=-5.66% |
| 2 | Breadth | 🔵 중립 | 0.2886 | RSP/SPY=0.2886 (Ratio, 무차원), 4W Δ=+0.0115, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9269 | SPHB/SPLV=1.9269 (Ratio, 무차원), 4W Δ=-0.1968 |
| 4 | VIX Term | 🟢 contango | 0.8640 | VIX3M=19.04, VIX/VIX3M=0.8640 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.38 |
| 5 | 섹터 로테이션 | 🔵 중립 | 0.8400 | XLK 4W=-7.86%, XLE 4W=-8.70%, XLK-XLE=+0.84%p, XLP 4W=+4.16%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🔵 중립 | 0.7337 | HYG/LQD=0.7337 (Ratio, OAS 아님), 4W Δ=+0.0010 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 98.81
- **상세**: KOSPI YoY=+178.85%, KOSDAQ YoY=+18.77%, KOSPI 4W=-5.66%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.288555
- **상세**: RSP/SPY=0.2886 (Ratio, 무차원), 4W Δ=+0.0115, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.926886
- **상세**: SPHB/SPLV=1.9269 (Ratio, 무차원), 4W Δ=-0.1968
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.864
- **상세**: VIX3M=19.04, VIX/VIX3M=0.8640 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.38
- **시리즈**: ^VIX3M, VIXCLS

### 🔵 섹터 로테이션 — 중립
- **값**: 0.84
- **상세**: XLK 4W=-7.86%, XLE 4W=-8.70%, XLK-XLE=+0.84%p, XLP 4W=+4.16%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.733708
- **상세**: HYG/LQD=0.7337 (Ratio, OAS 아님), 4W Δ=+0.0010
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*