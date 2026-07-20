# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-07-20 (oldest: 2026-07-16 ^KS11)
> Freshness: OK (oldest 4d ≤ 5d)
> Generated: 2026-07-20 21:56:28 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 62.6900 | KOSPI YoY=+123.31%, KOSDAQ YoY=+2.07%, KOSPI 4W=-24.75% |
| 2 | Breadth | 🔵 중립 | 0.2862 | RSP/SPY=0.2862 (Ratio, 무차원), 4W Δ=+0.0062, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 risk-on | 1.8479 | SPHB/SPLV=1.8479 (Ratio, 무차원), 4W Δ=-0.2747 |
| 4 | VIX Term | 🟢 contango | 0.8201 | VIX3M=20.40, VIX/VIX3M=0.8201 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.83 |
| 5 | 섹터 로테이션 | 🟠 경계 | -16.6400 | XLK 4W=-8.11%, XLE 4W=+8.53%, XLK-XLE=-16.64%p, XLP 4W=+2.58%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟢 완화 | 0.7436 | HYG/LQD=0.7436 (Ratio, OAS 아님), 4W Δ=+0.0109 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 62.69
- **상세**: KOSPI YoY=+123.31%, KOSDAQ YoY=+2.07%, KOSPI 4W=-24.75%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.286246
- **상세**: RSP/SPY=0.2862 (Ratio, 무차원), 4W Δ=+0.0062, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.847943
- **상세**: SPHB/SPLV=1.8479 (Ratio, 무차원), 4W Δ=-0.2747
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8201
- **상세**: VIX3M=20.40, VIX/VIX3M=0.8201 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.83
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -16.64
- **상세**: XLK 4W=-8.11%, XLE 4W=+8.53%, XLK-XLE=-16.64%p, XLP 4W=+2.58%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.74363
- **상세**: HYG/LQD=0.7436 (Ratio, OAS 아님), 4W Δ=+0.0109
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*