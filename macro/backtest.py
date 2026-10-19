#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
backtest.py - 워크포워드 백테스트: "이 절차가 과거에 실제로 기저율보다 나았는가"

매월 말 T마다, T까지 알 수 있었던 정보만으로 조건부 분포 분석을 다시 수행하고(상태 규칙·검정·
수축 전부 동일), 산출한 하락/횡보/상승 확률을 이후 실현 결과로 채점한다.

비교 기준(벤치마크)은 같은 시점에 계산한 기저율(전체 표본 3분위 = 약 1/3씩)이다.
  Brier = sum_k (p_k - o_k)^2        (낮을수록 좋다)
  BSS   = 1 - mean(Brier_모형) / mean(Brier_기저율)     (0보다 커야 기저율을 이긴 것)

한계 (결과 해석 전에 읽을 것)
  - 상태 규칙(states.yaml)은 이 데이터 전체를 본 뒤 고정한 것이 아니지만, 규칙 설계 시 2008~2026의
    일반적 지식(VIX 평균회귀 등)이 영향을 줬을 수 있다. 이 백테스트도 완전한 표본 외 검증은 아니다.
  - 월 단위로 표본을 뽑아도 지평 63영업일 결과는 3개월 겹친다 -> n_eff = n / ceil(지평/21)
  - 첫 평가 시점은 공통 표본 500일 이상이 쌓인 뒤(대략 2012년)다.
  - 한국 원화·금리 방향처럼 신호가 없는 대상에서 BSS가 0 근처로 나오는 것이 정상이다.
    BSS가 크게 음수면 수축 계수(shrink_k)나 검정 기준이 과신을 만든다는 뜻이다.

사용법
    python macro/backtest.py [--n-perm 300] [--start 2012-01-01]
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import macro_lib as L  # noqa: E402
import conditional_dist as C  # noqa: E402


def month_end_dates(cal: pd.DatetimeIndex, start: str) -> list[pd.Timestamp]:
    s = pd.Series(cal, index=cal)
    me = s.groupby([cal.year, cal.month]).max()
    return [d for d in me.tolist() if d >= pd.Timestamp(start)]


def bin_index(x: float, lo: float, hi: float) -> int:
    return 0 if x < lo else (2 if x > hi else 1)


def run(n_perm: int = 300, start: str = "2012-01-01", panel: dict | None = None, quiet: bool = False) -> pd.DataFrame:
    pan = panel or L.build_panel()
    cat, cfg = pan["cat"], pan["cfg"]
    rows = []
    dates = month_end_dates(pan["cal"], start)
    for sid in cfg["targets"]:
        for h in cfg["horizons_bdays"]:
            full_fwd = L.forward_change(pan["known"][sid], cat.loc[sid, "chg"], h)
            for T in dates:
                real = full_fwd.get(T, np.nan)
                if pd.isna(real):
                    continue                              # 결과가 아직 확정되지 않음
                r = C.analyze_target(pan, sid, h, n_perm=n_perm, seed=7, asof=T)
                if "error" in r:
                    continue
                lo, hi = r["edges"]
                o = np.zeros(3)
                o[bin_index(real, lo, hi)] = 1.0
                p, b = np.array(r["prob"]), np.array(r["base"])
                rows.append({"series": sid, "h": h, "T": T, "adopted": r["adopted"]["name"] if r["adopted"] else "",
                             "brier": float(((p - o) ** 2).sum()), "brier_base": float(((b - o) ** 2).sum()),
                             "hit": int(np.argmax(p) == np.argmax(o)),
                             "p_down": p[0], "p_flat": p[1], "p_up": p[2], "outcome": int(np.argmax(o))})
        if not quiet:
            print(f"  {sid} 완료", flush=True)
    return pd.DataFrame(rows)


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    out = []
    for (sid, h), g in df.groupby(["series", "h"]):
        n = len(g)
        n_eff = n / math.ceil(h / 21)
        d = g["brier_base"] - g["brier"]                     # 양수면 모형이 낫다
        se = d.std(ddof=1) / math.sqrt(max(n_eff, 1.0)) if n > 2 else float("nan")
        adopted = g[g["adopted"] != ""]
        bss_adopt = (1 - adopted["brier"].mean() / adopted["brier_base"].mean()) if len(adopted) else float("nan")
        out.append({"series": sid, "h": h, "n": n, "n_eff": round(n_eff, 1),
                    "신호채택비율": round(len(adopted) / n, 2),
                    "BSS_전체": round(1 - g["brier"].mean() / g["brier_base"].mean(), 4),
                    "평균Brier차(기저율-모형)": round(float(d.mean()), 4),
                    "z(차/표준오차)": round(float(d.mean() / se), 2) if se and se == se and se > 0 else float("nan"),
                    "BSS_채택시점만": round(float(bss_adopt), 4) if bss_adopt == bss_adopt else float("nan"),
                    "채택시점수": len(adopted)})
    return pd.DataFrame(out)


def load_validation(cfg: dict | None = None, root: Path | None = None) -> dict:
    """{(series, h): {'validated': bool, 'bss': float, 'z': float, 'note': str}}.
    요약 파일이 없거나 규칙 해시가 현재와 다르면 전부 미검증으로 취급한다(규칙이 바뀌면 재검증)."""
    cfg = cfg or L.load_config()
    path = (root or L.ROOT) / cfg["validation"]["summary_file"]
    if not path.exists():
        return {}
    df = pd.read_csv(path, dtype={"config_hash": str})
    cur = L.config_hash()
    out = {}
    for r in df.itertuples():
        ok = (r.config_hash == cur) and (r.z == r.z) and (r.z >= cfg["validation"]["min_z"]) and (r.bss > 0)
        note = "" if r.config_hash == cur else "규칙 변경 후 재검증 필요"
        out[(r.series, int(r.h))] = {"validated": bool(ok), "bss": float(r.bss), "z": float(r.z), "note": note,
                                     "end": r.sample_end, "n": int(r.n), "n_eff": float(r.n_eff)}
    return out


def save_summary(s: pd.DataFrame, df: pd.DataFrame, path: Path, n_perm: int) -> None:
    out = pd.DataFrame({
        "series": s["series"], "h": s["h"], "n": s["n"], "n_eff": s["n_eff"],
        "bss": s["BSS_전체"], "z": s["z(차/표준오차)"],
        "sample_end": str(df["T"].max().date()), "n_perm": n_perm, "config_hash": L.config_hash()})
    path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(path, index=False)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-perm", type=int, default=300)
    ap.add_argument("--start", default="2012-01-01")
    ap.add_argument("--csv", help="월별 채점 결과 저장 경로")
    ap.add_argument("--save-summary", action="store_true", help="검증 게이트용 요약 파일 갱신")
    a = ap.parse_args()
    df = run(a.n_perm, a.start)
    if df.empty:
        print("채점할 시점이 없다")
        return 1
    if a.csv:
        df.to_csv(a.csv, index=False)
    s = summarize(df)
    if a.save_summary:
        cfg = L.load_config()
        save_summary(s, df, L.ROOT / cfg["validation"]["summary_file"], a.n_perm)
        print(f"요약 저장: {cfg['validation']['summary_file']}")
    pd.set_option("display.width", 200, "display.max_columns", 20)
    print(s.to_string(index=False))
    tot = 1 - df["brier"].mean() / df["brier_base"].mean()
    print(f"\n전체 BSS {tot:.4f}  (표본 {len(df)}건, 대상 {df['series'].nunique()}개)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
