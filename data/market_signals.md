# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-07-06 (oldest: 2026-07-03 ^KS11)
> Freshness: OK (oldest 3d ≤ 5d)
> Generated: 2026-07-06 22:09:26 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 89.4900 | KOSPI YoY=+168.32%, KOSDAQ YoY=+10.66%, KOSPI 4W=-0.89% |
| 2 | Breadth | 🔵 중립 | 0.2862 | RSP/SPY=0.2862 (Ratio, 무차원), 4W Δ=+0.0081, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9731 | SPHB/SPLV=1.9731 (Ratio, 무차원), 4W Δ=-0.1250 |
| 4 | VIX Term | 🟢 contango | 0.8834 | VIX3M=18.78, VIX/VIX3M=0.8834 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.45 |
| 5 | 섹터 로테이션 | 🟢 확장 | 4.0500 | XLK 4W=-4.86%, XLE 4W=-8.91%, XLK-XLE=+4.05%p, XLP 4W=+3.22%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🔵 중립 | 0.7350 | HYG/LQD=0.7350 (Ratio, OAS 아님), 4W Δ=+0.0024 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 89.49
- **상세**: KOSPI YoY=+168.32%, KOSDAQ YoY=+10.66%, KOSPI 4W=-0.89%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.286178
- **상세**: RSP/SPY=0.2862 (Ratio, 무차원), 4W Δ=+0.0081, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.973086
- **상세**: SPHB/SPLV=1.9731 (Ratio, 무차원), 4W Δ=-0.1250
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8834
- **상세**: VIX3M=18.78, VIX/VIX3M=0.8834 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.45
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 4.05
- **상세**: XLK 4W=-4.86%, XLE 4W=-8.91%, XLK-XLE=+4.05%p, XLP 4W=+3.22%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.734977
- **상세**: HYG/LQD=0.7350 (Ratio, OAS 아님), 4W Δ=+0.0024
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*