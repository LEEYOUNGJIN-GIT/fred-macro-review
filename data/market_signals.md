# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-06-04 (oldest: 2026-06-02 ^KS11)
> Freshness: OK (oldest 2d ≤ 5d)
> Generated: 2026-06-04 22:17:18 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 140.8400 | KOSPI YoY=+238.28%, KOSDAQ YoY=+43.39%, KOSPI 4W=+33.38% |
| 2 | Breadth | 🔵 중립 | 0.2785 | RSP/SPY=0.2785 (Ratio, 무차원), 4W Δ=-0.0007 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.0967 | SPHB/SPLV=2.0967 (Ratio, 무차원), 4W Δ=+0.1724 |
| 4 | VIX Term | 🟢 contango | 0.8201 | VIX3M=19.23, VIX/VIX3M=0.8201 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.34 |
| 5 | 섹터 로테이션 | 🟢 확장 | 10.5400 | XLK 4W=+13.61%, XLE 4W=+3.07%, XLK-XLE=+10.54%p, XLP 4W=-2.61% |
| 6 | 신용 방향 | 🔵 중립 | 0.7334 | HYG/LQD=0.7334 (Ratio, OAS 아님), 4W Δ=+0.0002 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 140.84
- **상세**: KOSPI YoY=+238.28%, KOSDAQ YoY=+43.39%, KOSPI 4W=+33.38%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.278474
- **상세**: RSP/SPY=0.2785 (Ratio, 무차원), 4W Δ=-0.0007
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.096658
- **상세**: SPHB/SPLV=2.0967 (Ratio, 무차원), 4W Δ=+0.1724
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8201
- **상세**: VIX3M=19.23, VIX/VIX3M=0.8201 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.34
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 10.54
- **상세**: XLK 4W=+13.61%, XLE 4W=+3.07%, XLK-XLE=+10.54%p, XLP 4W=-2.61%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.733395
- **상세**: HYG/LQD=0.7334 (Ratio, OAS 아님), 4W Δ=+0.0002
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*