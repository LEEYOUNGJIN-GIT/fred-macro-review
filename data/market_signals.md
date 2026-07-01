# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-07-01 (oldest: 2026-06-30 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-07-01 22:14:14 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 101.3400 | KOSPI YoY=+185.19%, KOSDAQ YoY=+17.50%, KOSPI 4W=-3.55% |
| 2 | Breadth | 🔵 중립 | 0.2862 | RSP/SPY=0.2862 (Ratio, 무차원), 4W Δ=+0.0100, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.0242 | SPHB/SPLV=2.0242 (Ratio, 무차원), 4W Δ=-0.1155 |
| 4 | VIX Term | 🟢 contango | 0.9212 | VIX3M=19.16, VIX/VIX3M=0.9212 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.50 |
| 5 | 섹터 로테이션 | 🔵 중립 | 1.9900 | XLK 4W=-6.24%, XLE 4W=-8.23%, XLK-XLE=+1.99%p, XLP 4W=+2.50%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🔵 중립 | 0.7338 | HYG/LQD=0.7338 (Ratio, OAS 아님), 4W Δ=+0.0003 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 101.34
- **상세**: KOSPI YoY=+185.19%, KOSDAQ YoY=+17.50%, KOSPI 4W=-3.55%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.286164
- **상세**: RSP/SPY=0.2862 (Ratio, 무차원), 4W Δ=+0.0100, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.024189
- **상세**: SPHB/SPLV=2.0242 (Ratio, 무차원), 4W Δ=-0.1155
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.9212
- **상세**: VIX3M=19.16, VIX/VIX3M=0.9212 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.50
- **시리즈**: ^VIX3M, VIXCLS

### 🔵 섹터 로테이션 — 중립
- **값**: 1.99
- **상세**: XLK 4W=-6.24%, XLE 4W=-8.23%, XLK-XLE=+1.99%p, XLP 4W=+2.50%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.733819
- **상세**: HYG/LQD=0.7338 (Ratio, OAS 아님), 4W Δ=+0.0003
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*