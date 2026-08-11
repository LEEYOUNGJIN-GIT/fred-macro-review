# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-08-11 (oldest: 2026-08-10 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-08-11 21:38:30 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 51.2500 | KOSPI YoY=+96.28%, KOSDAQ YoY=+6.22%, KOSPI 4W=-15.73% |
| 2 | Breadth | 🔵 중립 | 0.2864 | RSP/SPY=0.2864 (Ratio, 무차원), 4W Δ=+0.0025 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9506 | SPHB/SPLV=1.9506 (Ratio, 무차원), 4W Δ=-0.0001 |
| 4 | VIX Term | 🟢 contango | 0.7879 | VIX3M=18.91, VIX/VIX3M=0.7879 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.66 |
| 5 | 섹터 로테이션 | 🟠 경계 | -5.6400 | XLK 4W=+1.35%, XLE 4W=+6.99%, XLK-XLE=-5.64%p, XLP 4W=+1.52%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟢 완화 | 0.7502 | HYG/LQD=0.7502 (Ratio, OAS 아님), 4W Δ=+0.0073 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 51.25
- **상세**: KOSPI YoY=+96.28%, KOSDAQ YoY=+6.22%, KOSPI 4W=-15.73%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.286402
- **상세**: RSP/SPY=0.2864 (Ratio, 무차원), 4W Δ=+0.0025
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.950562
- **상세**: SPHB/SPLV=1.9506 (Ratio, 무차원), 4W Δ=-0.0001
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.7879
- **상세**: VIX3M=18.91, VIX/VIX3M=0.7879 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.66
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -5.64
- **상세**: XLK 4W=+1.35%, XLE 4W=+6.99%, XLK-XLE=-5.64%p, XLP 4W=+1.52%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.750165
- **상세**: HYG/LQD=0.7502 (Ratio, OAS 아님), 4W Δ=+0.0073
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*