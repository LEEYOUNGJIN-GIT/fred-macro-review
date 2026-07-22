# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-07-23 (oldest: 2026-07-21 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-07-22 22:00:16 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 56.3400 | KOSPI YoY=+116.63%, KOSDAQ YoY=-3.94%, KOSPI 4W=-25.97% |
| 2 | Breadth | 🔵 중립 | 0.2846 | RSP/SPY=0.2846 (Ratio, 무차원), 4W Δ=-0.0002 |
| 3 | Risk-on/off | 🟢 risk-on | 1.8991 | SPHB/SPLV=1.8991 (Ratio, 무차원), 4W Δ=-0.1321 |
| 4 | VIX Term | 🔵 중립 | 0.9545 | VIX3M=19.54, VIX/VIX3M=0.9545 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.03 |
| 5 | 섹터 로테이션 | 🟠 경계 | -10.8300 | XLK 4W=-2.13%, XLE 4W=+8.70%, XLK-XLE=-10.83%p, XLP 4W=+0.79%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟢 완화 | 0.7455 | HYG/LQD=0.7455 (Ratio, OAS 아님), 4W Δ=+0.0129 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 56.34
- **상세**: KOSPI YoY=+116.63%, KOSDAQ YoY=-3.94%, KOSPI 4W=-25.97%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.284583
- **상세**: RSP/SPY=0.2846 (Ratio, 무차원), 4W Δ=-0.0002
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.899082
- **상세**: SPHB/SPLV=1.8991 (Ratio, 무차원), 4W Δ=-0.1321
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🔵 VIX Term — 중립
- **값**: 0.9545
- **상세**: VIX3M=19.54, VIX/VIX3M=0.9545 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.03
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -10.83
- **상세**: XLK 4W=-2.13%, XLE 4W=+8.70%, XLK-XLE=-10.83%p, XLP 4W=+0.79%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.745477
- **상세**: HYG/LQD=0.7455 (Ratio, OAS 아님), 4W Δ=+0.0129
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*