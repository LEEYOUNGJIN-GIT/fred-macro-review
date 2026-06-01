# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-06-01 (oldest: 2026-05-29 ^KS11)
> Freshness: OK (oldest 3d ≤ 5d)
> Generated: 2026-06-01 22:59:00 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 135.4500 | KOSPI YoY=+222.67%, KOSDAQ YoY=+48.23%, KOSPI 4W=+27.63% |
| 2 | Breadth | 🔵 중립 | 0.2758 | RSP/SPY=0.2758 (Ratio, 무차원), 4W Δ=-0.0056, 4W 하락=대형주 쏠림 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.1105 | SPHB/SPLV=2.1105 (Ratio, 무차원), 4W Δ=+0.2825 |
| 4 | VIX Term | 🟢 contango | 0.8101 | VIX3M=19.43, VIX/VIX3M=0.8101 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.94 |
| 5 | 섹터 로테이션 | 🟢 확장 | 23.5700 | XLK 4W=+20.94%, XLE 4W=-2.63%, XLK-XLE=+23.57%p, XLP 4W=-2.54% |
| 6 | 신용 방향 | 🔵 중립 | 0.7329 | HYG/LQD=0.7329 (Ratio, OAS 아님), 4W Δ=-0.0043 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 135.45
- **상세**: KOSPI YoY=+222.67%, KOSDAQ YoY=+48.23%, KOSPI 4W=+27.63%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.275806
- **상세**: RSP/SPY=0.2758 (Ratio, 무차원), 4W Δ=-0.0056, 4W 하락=대형주 쏠림
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.110504
- **상세**: SPHB/SPLV=2.1105 (Ratio, 무차원), 4W Δ=+0.2825
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8101
- **상세**: VIX3M=19.43, VIX/VIX3M=0.8101 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.94
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 23.57
- **상세**: XLK 4W=+20.94%, XLE 4W=-2.63%, XLK-XLE=+23.57%p, XLP 4W=-2.54%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.732948
- **상세**: HYG/LQD=0.7329 (Ratio, OAS 아님), 4W Δ=-0.0043
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*