# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-06-30 (oldest: 2026-06-29 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-06-30 22:11:53 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 101.6100 | KOSPI YoY=+184.54%, KOSDAQ YoY=+18.68%, KOSPI 4W=-0.96% |
| 2 | Breadth | 🔵 중립 | 0.2849 | RSP/SPY=0.2849 (Ratio, 무차원), 4W Δ=+0.0095, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.0773 | SPHB/SPLV=2.0773 (Ratio, 무차원), 4W Δ=-0.0346 |
| 4 | VIX Term | 🔵 중립 | 0.9689 | VIX3M=19.00, VIX/VIX3M=0.9689 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.34 |
| 5 | 섹터 로테이션 | 🟢 확장 | 4.0800 | XLK 4W=-2.56%, XLE 4W=-6.64%, XLK-XLE=+4.08%p, XLP 4W=+1.97%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🔵 중립 | 0.7332 | HYG/LQD=0.7332 (Ratio, OAS 아님), 4W Δ=+0.0003 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 101.61
- **상세**: KOSPI YoY=+184.54%, KOSDAQ YoY=+18.68%, KOSPI 4W=-0.96%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.28492
- **상세**: RSP/SPY=0.2849 (Ratio, 무차원), 4W Δ=+0.0095, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.077303
- **상세**: SPHB/SPLV=2.0773 (Ratio, 무차원), 4W Δ=-0.0346
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🔵 VIX Term — 중립
- **값**: 0.9689
- **상세**: VIX3M=19.00, VIX/VIX3M=0.9689 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.34
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 4.08
- **상세**: XLK 4W=-2.56%, XLE 4W=-6.64%, XLK-XLE=+4.08%p, XLP 4W=+1.97%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.733199
- **상세**: HYG/LQD=0.7332 (Ratio, OAS 아님), 4W Δ=+0.0003
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*