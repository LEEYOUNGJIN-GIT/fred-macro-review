# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-09-23 (oldest: 2026-09-18 ^N225)
> Freshness: OK (oldest 4d ≤ 5d)
> Generated: 2026-09-22 23:24:22 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 59.9100 | KOSPI YoY=+117.66%, KOSDAQ YoY=+2.16%, KOSPI 4W=+4.64% |
| 2 | Breadth | 🔵 중립 | 0.2752 | RSP/SPY=0.2752 (Ratio, 무차원), 4W Δ=-0.0152, 4W 하락=대형주 쏠림 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.1315 | SPHB/SPLV=2.1315 (Ratio, 무차원), 4W Δ=+0.2136 |
| 4 | VIX Term | 🟢 contango | 0.8410 | VIX3M=17.61, VIX/VIX3M=0.8410 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.95 |
| 5 | 섹터 로테이션 | 🟢 확장 | 10.6700 | XLK 4W=+9.14%, XLE 4W=-1.53%, XLK-XLE=+10.67%p, XLP 4W=-4.78% |
| 6 | 신용 방향 | 🔵 중립 | 0.7486 | HYG/LQD=0.7486 (Ratio, OAS 아님), 4W Δ=-0.0011 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 59.91
- **상세**: KOSPI YoY=+117.66%, KOSDAQ YoY=+2.16%, KOSPI 4W=+4.64%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.275156
- **상세**: RSP/SPY=0.2752 (Ratio, 무차원), 4W Δ=-0.0152, 4W 하락=대형주 쏠림
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.131498
- **상세**: SPHB/SPLV=2.1315 (Ratio, 무차원), 4W Δ=+0.2136
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.841
- **상세**: VIX3M=17.61, VIX/VIX3M=0.8410 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.95
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 10.67
- **상세**: XLK 4W=+9.14%, XLE 4W=-1.53%, XLK-XLE=+10.67%p, XLP 4W=-4.78%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.748596
- **상세**: HYG/LQD=0.7486 (Ratio, OAS 아님), 4W Δ=-0.0011
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*