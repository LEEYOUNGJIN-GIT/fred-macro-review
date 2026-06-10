# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-06-10 (oldest: 2026-06-09 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-06-10 22:49:51 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 119.8100 | KOSPI YoY=+206.19%, KOSDAQ YoY=+33.44%, KOSPI 4W=+7.99% |
| 2 | Breadth | 🔵 중립 | 0.2847 | RSP/SPY=0.2847 (Ratio, 무차원), 4W Δ=+0.0086, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 risk-on | 1.8906 | SPHB/SPLV=1.8906 (Ratio, 무차원), 4W Δ=-0.0317 |
| 4 | VIX Term | 🟢 contango | 0.8266 | VIX3M=22.89, VIX/VIX3M=0.8266 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+1.85 |
| 5 | 섹터 로테이션 | 🟡 둔화 | -0.3600 | XLK 4W=+0.82%, XLE 4W=+1.18%, XLK-XLE=-0.36%p, XLP 4W=+1.24%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🔵 중립 | 0.7347 | HYG/LQD=0.7347 (Ratio, OAS 아님), 4W Δ=N/A |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 119.81
- **상세**: KOSPI YoY=+206.19%, KOSDAQ YoY=+33.44%, KOSPI 4W=+7.99%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.2847
- **상세**: RSP/SPY=0.2847 (Ratio, 무차원), 4W Δ=+0.0086, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.890648
- **상세**: SPHB/SPLV=1.8906 (Ratio, 무차원), 4W Δ=-0.0317
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8266
- **상세**: VIX3M=22.89, VIX/VIX3M=0.8266 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+1.85
- **시리즈**: ^VIX3M, VIXCLS

### 🟡 섹터 로테이션 — 둔화
- **값**: -0.36
- **상세**: XLK 4W=+0.82%, XLE 4W=+1.18%, XLK-XLE=-0.36%p, XLP 4W=+1.24%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.734745
- **상세**: HYG/LQD=0.7347 (Ratio, OAS 아님), 4W Δ=N/A
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*