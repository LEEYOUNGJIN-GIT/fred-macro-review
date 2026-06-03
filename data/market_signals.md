# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-06-04 (oldest: 2026-06-02 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-06-03 23:00:27 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 140.8400 | KOSPI YoY=+238.28%, KOSDAQ YoY=+43.39%, KOSPI 4W=+33.38% |
| 2 | Breadth | 🔵 중립 | 0.2774 | RSP/SPY=0.2774 (Ratio, 무차원), 4W Δ=-0.0034 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.1223 | SPHB/SPLV=2.1223 (Ratio, 무차원), 4W Δ=+0.2500 |
| 4 | VIX Term | 🟢 contango | 0.8122 | VIX3M=19.76, VIX/VIX3M=0.8122 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.06 |
| 5 | 섹터 로테이션 | 🟢 확장 | 19.7100 | XLK 4W=+18.47%, XLE 4W=-1.24%, XLK-XLE=+19.71%p, XLP 4W=-2.26% |
| 6 | 신용 방향 | 🔵 중립 | 0.7336 | HYG/LQD=0.7336 (Ratio, OAS 아님), 4W Δ=-0.0010 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 140.84
- **상세**: KOSPI YoY=+238.28%, KOSDAQ YoY=+43.39%, KOSPI 4W=+33.38%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.277432
- **상세**: RSP/SPY=0.2774 (Ratio, 무차원), 4W Δ=-0.0034
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.122315
- **상세**: SPHB/SPLV=2.1223 (Ratio, 무차원), 4W Δ=+0.2500
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8122
- **상세**: VIX3M=19.76, VIX/VIX3M=0.8122 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.06
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 19.71
- **상세**: XLK 4W=+18.47%, XLE 4W=-1.24%, XLK-XLE=+19.71%p, XLP 4W=-2.26%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.733567
- **상세**: HYG/LQD=0.7336 (Ratio, OAS 아님), 4W Δ=-0.0010
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*