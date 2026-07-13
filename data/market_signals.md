# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-07-13 (oldest: 2026-07-10 ^KS11)
> Freshness: OK (oldest 3d ≤ 5d)
> Generated: 2026-07-13 21:50:11 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 75.2700 | KOSPI YoY=+143.38%, KOSDAQ YoY=+7.16%, KOSPI 4W=-7.97% |
| 2 | Breadth | 🔵 중립 | 0.2860 | RSP/SPY=0.2860 (Ratio, 무차원), 4W Δ=+0.0020 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9067 | SPHB/SPLV=1.9067 (Ratio, 무차원), 4W Δ=-0.0792 |
| 4 | VIX Term | 🟢 contango | 0.8065 | VIX3M=19.64, VIX/VIX3M=0.8065 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.78 |
| 5 | 섹터 로테이션 | 🟡 둔화 | -0.9900 | XLK 4W=-0.94%, XLE 4W=+0.05%, XLK-XLE=-0.99%p, XLP 4W=-0.11%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟢 완화 | 0.7435 | HYG/LQD=0.7435 (Ratio, OAS 아님), 4W Δ=+0.0114 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 75.27
- **상세**: KOSPI YoY=+143.38%, KOSDAQ YoY=+7.16%, KOSPI 4W=-7.97%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.285956
- **상세**: RSP/SPY=0.2860 (Ratio, 무차원), 4W Δ=+0.0020
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.906688
- **상세**: SPHB/SPLV=1.9067 (Ratio, 무차원), 4W Δ=-0.0792
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8065
- **상세**: VIX3M=19.64, VIX/VIX3M=0.8065 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.78
- **시리즈**: ^VIX3M, VIXCLS

### 🟡 섹터 로테이션 — 둔화
- **값**: -0.99
- **상세**: XLK 4W=-0.94%, XLE 4W=+0.05%, XLK-XLE=-0.99%p, XLP 4W=-0.11%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.743455
- **상세**: HYG/LQD=0.7435 (Ratio, OAS 아님), 4W Δ=+0.0114
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*