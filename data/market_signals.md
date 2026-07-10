# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-07-10 (oldest: 2026-07-09 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-07-10 21:55:21 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 70.1000 | KOSPI YoY=+138.61%, KOSDAQ YoY=+1.59%, KOSPI 4W=-6.08% |
| 2 | Breadth | 🔵 중립 | 0.2839 | RSP/SPY=0.2839 (Ratio, 무차원), 4W Δ=-0.0005 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9706 | SPHB/SPLV=1.9706 (Ratio, 무차원), 4W Δ=+0.0787 |
| 4 | VIX Term | 🟢 contango | 0.9101 | VIX3M=18.57, VIX/VIX3M=0.9101 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.66 |
| 5 | 섹터 로테이션 | 🟢 확장 | 10.0700 | XLK 4W=+5.31%, XLE 4W=-4.76%, XLK-XLE=+10.07%p, XLP 4W=-0.92% |
| 6 | 신용 방향 | 🟢 완화 | 0.7418 | HYG/LQD=0.7418 (Ratio, OAS 아님), 4W Δ=+0.0078 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 70.1
- **상세**: KOSPI YoY=+138.61%, KOSDAQ YoY=+1.59%, KOSPI 4W=-6.08%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.28386
- **상세**: RSP/SPY=0.2839 (Ratio, 무차원), 4W Δ=-0.0005
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.970596
- **상세**: SPHB/SPLV=1.9706 (Ratio, 무차원), 4W Δ=+0.0787
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.9101
- **상세**: VIX3M=18.57, VIX/VIX3M=0.9101 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.66
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 10.07
- **상세**: XLK 4W=+5.31%, XLE 4W=-4.76%, XLK-XLE=+10.07%p, XLP 4W=-0.92%
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.741764
- **상세**: HYG/LQD=0.7418 (Ratio, OAS 아님), 4W Δ=+0.0078
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*