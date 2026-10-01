# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-10-01 (oldest: 2026-09-29 ^KS11)
> Freshness: OK (oldest 2d ≤ 5d)
> Generated: 2026-10-01 00:18:12 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 51.3300 | KOSPI YoY=+102.35%, KOSDAQ YoY=+0.32%, KOSPI 4W=+1.21% |
| 2 | Breadth | 🔵 중립 | 0.2741 | RSP/SPY=0.2741 (Ratio, 무차원), 4W Δ=-0.0115, 4W 하락=대형주 쏠림 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.1327 | SPHB/SPLV=2.1327 (Ratio, 무차원), 4W Δ=+0.1720 |
| 4 | VIX Term | 🟢 contango | 0.8748 | VIX3M=18.37, VIX/VIX3M=0.8748 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.04 |
| 5 | 섹터 로테이션 | 🟢 확장 | 7.6200 | XLK 4W=+4.41%, XLE 4W=-3.21%, XLK-XLE=+7.62%p, XLP 4W=-3.05% |
| 6 | 신용 방향 | 🔵 중립 | 0.7554 | HYG/LQD=0.7554 (Ratio, OAS 아님), 4W Δ=+0.0049 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 51.33
- **상세**: KOSPI YoY=+102.35%, KOSDAQ YoY=+0.32%, KOSPI 4W=+1.21%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.274143
- **상세**: RSP/SPY=0.2741 (Ratio, 무차원), 4W Δ=-0.0115, 4W 하락=대형주 쏠림
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.132743
- **상세**: SPHB/SPLV=2.1327 (Ratio, 무차원), 4W Δ=+0.1720
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8748
- **상세**: VIX3M=18.37, VIX/VIX3M=0.8748 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.04
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 7.62
- **상세**: XLK 4W=+4.41%, XLE 4W=-3.21%, XLK-XLE=+7.62%p, XLP 4W=-3.05%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.755395
- **상세**: HYG/LQD=0.7554 (Ratio, OAS 아님), 4W Δ=+0.0049
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*