# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-06-11 (oldest: 2026-06-10 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-06-11 22:48:06 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 112.0100 | KOSPI YoY=+193.14%, KOSDAQ YoY=+30.88%, KOSPI 4W=-1.17% |
| 2 | Breadth | 🔵 중립 | 0.2843 | RSP/SPY=0.2843 (Ratio, 무차원), 4W Δ=+0.0109, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9846 | SPHB/SPLV=1.9846 (Ratio, 무차원), 4W Δ=+0.0537 |
| 4 | VIX Term | 🟢 contango | 0.9276 | VIX3M=21.42, VIX/VIX3M=0.9276 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.24 |
| 5 | 섹터 로테이션 | 🟢 확장 | 4.4800 | XLK 4W=+3.60%, XLE 4W=-0.88%, XLK-XLE=+4.48%p, XLP 4W=+0.65% |
| 6 | 신용 방향 | 🔵 중립 | 0.7329 | HYG/LQD=0.7329 (Ratio, OAS 아님), 4W Δ=-0.0019 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 112.01
- **상세**: KOSPI YoY=+193.14%, KOSDAQ YoY=+30.88%, KOSPI 4W=-1.17%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.284307
- **상세**: RSP/SPY=0.2843 (Ratio, 무차원), 4W Δ=+0.0109, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.984561
- **상세**: SPHB/SPLV=1.9846 (Ratio, 무차원), 4W Δ=+0.0537
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.9276
- **상세**: VIX3M=21.42, VIX/VIX3M=0.9276 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.24
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 4.48
- **상세**: XLK 4W=+3.60%, XLE 4W=-0.88%, XLK-XLE=+4.48%p, XLP 4W=+0.65%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.732857
- **상세**: HYG/LQD=0.7329 (Ratio, OAS 아님), 4W Δ=-0.0019
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*