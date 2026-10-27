# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-10-27 (oldest: 2026-10-23 ^KS11)
> Freshness: OK (oldest 4d ≤ 5d)
> Generated: 2026-10-27 00:09:11 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 21.1000 | KOSPI YoY=+54.84%, KOSDAQ YoY=-12.64%, KOSPI 4W=-20.80% |
| 2 | Breadth | 🔵 중립 | 0.2849 | RSP/SPY=0.2849 (Ratio, 무차원), 4W Δ=+0.0112, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 risk-on | 1.8032 | SPHB/SPLV=1.8032 (Ratio, 무차원), 4W Δ=-0.3482 |
| 4 | VIX Term | 🔵 중립 | 0.9544 | VIX3M=19.94, VIX/VIX3M=0.9544 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+1.71 |
| 5 | 섹터 로테이션 | 🟠 경계 | -18.3900 | XLK 4W=-6.64%, XLE 4W=+11.75%, XLK-XLE=-18.39%p, XLP 4W=+7.56%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟠 긴축 | 0.7419 | HYG/LQD=0.7419 (Ratio, OAS 아님), 4W Δ=-0.0123 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 21.1
- **상세**: KOSPI YoY=+54.84%, KOSDAQ YoY=-12.64%, KOSPI 4W=-20.80%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.284932
- **상세**: RSP/SPY=0.2849 (Ratio, 무차원), 4W Δ=+0.0112, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.803235
- **상세**: SPHB/SPLV=1.8032 (Ratio, 무차원), 4W Δ=-0.3482
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🔵 VIX Term — 중립
- **값**: 0.9544
- **상세**: VIX3M=19.94, VIX/VIX3M=0.9544 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+1.71
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -18.39
- **상세**: XLK 4W=-6.64%, XLE 4W=+11.75%, XLK-XLE=-18.39%p, XLP 4W=+7.56%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟠 신용 방향 — 긴축
- **값**: 0.741936
- **상세**: HYG/LQD=0.7419 (Ratio, OAS 아님), 4W Δ=-0.0123
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*