# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-11-20 (oldest: 2026-11-18 RSP)
> Freshness: OK (oldest 2d ≤ 5d)
> Generated: 2026-11-20 01:58:27 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟡 둔화 | -0.3000 | KOSPI YoY=+24.53%, KOSDAQ YoY=-25.13%, KOSPI 4W=-11.03% |
| 2 | Breadth | 🔵 중립 | 0.2950 | RSP/SPY=0.2950 (Ratio, 무차원), 4W Δ=+0.0148, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🔵 중립 | 1.6513 | SPHB/SPLV=1.6513 (Ratio, 무차원), 4W Δ=-0.2804 |
| 4 | VIX Term | 🟢 contango | 0.9086 | VIX3M=27.03, VIX/VIX3M=0.9086 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+6.91 |
| 5 | 섹터 로테이션 | 🟠 경계 | -3.0400 | XLK 4W=-13.12%, XLE 4W=-10.08%, XLK-XLE=-3.04%p, XLP 4W=+4.67%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🔵 중립 | 0.7431 | HYG/LQD=0.7431 (Ratio, OAS 아님), 4W Δ=-0.0018 |

## 신호 상세

### 🟡 한국 주식 — 둔화
- **값**: -0.3
- **상세**: KOSPI YoY=+24.53%, KOSDAQ YoY=-25.13%, KOSPI 4W=-11.03%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.295029
- **상세**: RSP/SPY=0.2950 (Ratio, 무차원), 4W Δ=+0.0148, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🔵 Risk-on/off — 중립
- **값**: 1.651301
- **상세**: SPHB/SPLV=1.6513 (Ratio, 무차원), 4W Δ=-0.2804
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.9086
- **상세**: VIX3M=27.03, VIX/VIX3M=0.9086 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+6.91
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -3.04
- **상세**: XLK 4W=-13.12%, XLE 4W=-10.08%, XLK-XLE=-3.04%p, XLP 4W=+4.67%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.743093
- **상세**: HYG/LQD=0.7431 (Ratio, OAS 아님), 4W Δ=-0.0018
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*