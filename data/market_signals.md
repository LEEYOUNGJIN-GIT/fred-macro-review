# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-11-13 (oldest: 2026-11-11 RSP)
> Freshness: OK (oldest 2d ≤ 5d)
> Generated: 2026-11-13 01:37:11 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🔵 중립 | 6.5900 | KOSPI YoY=+33.02%, KOSDAQ YoY=-19.84%, KOSPI 4W=-1.63% |
| 2 | Breadth | 🔵 중립 | 0.2930 | RSP/SPY=0.2930 (Ratio, 무차원), 4W Δ=+0.0174, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 risk-on | 1.7662 | SPHB/SPLV=1.7662 (Ratio, 무차원), 4W Δ=-0.2046 |
| 4 | VIX Term | 🟢 contango | 0.8719 | VIX3M=20.06, VIX/VIX3M=0.8719 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+1.57 |
| 5 | 섹터 로테이션 | 🟡 둔화 | -2.1400 | XLK 4W=-8.44%, XLE 4W=-6.30%, XLK-XLE=-2.14%p, XLP 4W=+6.26%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🔵 중립 | 0.7440 | HYG/LQD=0.7440 (Ratio, OAS 아님), 4W Δ=-0.0032 |

## 신호 상세

### 🔵 한국 주식 — 중립
- **값**: 6.59
- **상세**: KOSPI YoY=+33.02%, KOSDAQ YoY=-19.84%, KOSPI 4W=-1.63%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.293034
- **상세**: RSP/SPY=0.2930 (Ratio, 무차원), 4W Δ=+0.0174, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.76624
- **상세**: SPHB/SPLV=1.7662 (Ratio, 무차원), 4W Δ=-0.2046
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8719
- **상세**: VIX3M=20.06, VIX/VIX3M=0.8719 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+1.57
- **시리즈**: ^VIX3M, VIXCLS

### 🟡 섹터 로테이션 — 둔화
- **값**: -2.14
- **상세**: XLK 4W=-8.44%, XLE 4W=-6.30%, XLK-XLE=-2.14%p, XLP 4W=+6.26%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.744036
- **상세**: HYG/LQD=0.7440 (Ratio, OAS 아님), 4W Δ=-0.0032
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*