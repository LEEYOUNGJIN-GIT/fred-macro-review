# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-11-27 (oldest: 2026-11-27 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-11-28 03:01:06 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟡 둔화 | -0.6200 | KOSPI YoY=+20.21%, KOSDAQ YoY=-21.46%, KOSPI 4W=-14.22% |
| 2 | Breadth | 🔵 중립 | 0.2998 | RSP/SPY=0.2998 (Ratio, 무차원), 4W Δ=+0.0138, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🔵 중립 | 1.6094 | SPHB/SPLV=1.6094 (Ratio, 무차원), 4W Δ=-0.2881 |
| 4 | VIX Term | 🟡 backwardation | 1.1251 | VIX3M=23.82, VIX/VIX3M=1.1251 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+4.45 |
| 5 | 섹터 로테이션 | 🟠 경계 | -4.9000 | XLK 4W=-15.15%, XLE 4W=-10.25%, XLK-XLE=-4.90%p, XLP 4W=+5.10%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟠 긴축 | 0.7366 | HYG/LQD=0.7366 (Ratio, OAS 아님), 4W Δ=-0.0067 |

## 신호 상세

### 🟡 한국 주식 — 둔화
- **값**: -0.62
- **상세**: KOSPI YoY=+20.21%, KOSDAQ YoY=-21.46%, KOSPI 4W=-14.22%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.299841
- **상세**: RSP/SPY=0.2998 (Ratio, 무차원), 4W Δ=+0.0138, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🔵 Risk-on/off — 중립
- **값**: 1.609389
- **상세**: SPHB/SPLV=1.6094 (Ratio, 무차원), 4W Δ=-0.2881
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟡 VIX Term — backwardation
- **값**: 1.1251
- **상세**: VIX3M=23.82, VIX/VIX3M=1.1251 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+4.45
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -4.9
- **상세**: XLK 4W=-15.15%, XLE 4W=-10.25%, XLK-XLE=-4.90%p, XLP 4W=+5.10%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟠 신용 방향 — 긴축
- **값**: 0.736635
- **상세**: HYG/LQD=0.7366 (Ratio, OAS 아님), 4W Δ=-0.0067
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*