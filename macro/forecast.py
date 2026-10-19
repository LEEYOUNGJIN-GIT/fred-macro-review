#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
forecast.py - 사전등록 예측 (append-only) · 자동 채점 · 점수 요약

"예측이 맞았는가"를 나중에 따질 수 있으려면 예측을 하기 전에 기록해 둬야 한다.
ISO 주마다 첫 실행에서 (대상 x 지평) 전부를 forecast_log.csv에 등록한다.

기록 항목
  공식 확률(p_*)   검증 게이트를 통과한 (대상, 지평)만 신호를 반영, 나머지는 기저율
  모형 확률(m_*)   게이트와 무관하게 조건부 분포가 낸 확률 (게이트가 옳았는지 채점하기 위해)
  기저율(base_*)   전체 표본 3분위
  3분위 경계·기산값·해소일·설정 해시 -> row_hash로 사후 수정을 감지한다

채점: 해소일이 지나면 같은 규칙('알려진 값')으로 실현 변화를 계산해 Brier를 기록한다.
점수: BSS = 1 - mean(Brier)/mean(Brier_기저율). 공식·모형 둘 다 기저율과 비교한다.
      겹치는 등록(주 1회 x 지평 21·63일)이므로 유효 표본 n_eff = n / ceil(지평/5)

사용법
    python macro/forecast.py register | grade | score | verify
"""
from __future__ import annotations

import argparse
import hashlib
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import macro_lib as L  # noqa: E402
import conditional_dist as C  # noqa: E402
import backtest as B  # noqa: E402

REG_FIELDS = ["registered_on", "series", "horizon", "resolve_on", "start_value", "edge_lo", "edge_hi",
              "base_down", "base_flat", "base_up", "p_down", "p_flat", "p_up",
              "m_down", "m_flat", "m_up", "config_hash"]
COLS = ["id", "iso_week"] + REG_FIELDS + [
    "adopted", "validated", "n_eff", "p_perm", "row_hash",
    "status", "resolved_on", "realized_value", "realized_change", "outcome_bin",
    "brier", "brier_base", "brier_model"]


def log_path(cfg: dict, root: Path | None = None) -> Path:
    return (root or L.ROOT) / cfg["forecast"]["log_file"]


def row_hash(row: dict) -> str:
    s = "|".join(f"{row[k]:.8g}" if isinstance(row[k], float) else str(row[k]) for k in REG_FIELDS)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


STR_COLS = ["iso_week", "registered_on", "series", "resolve_on", "config_hash", "adopted", "row_hash",
            "status", "resolved_on"]


def load_log(path: Path) -> pd.DataFrame:
    """문자열 열은 반드시 str로 읽는다 (해시가 '1e5...' 꼴이면 부동소수로 오인되어 해시 검증이 깨진다)."""
    if not path.exists():
        return pd.DataFrame(columns=COLS)
    return pd.read_csv(path, dtype={c: str for c in STR_COLS}).reindex(columns=COLS)


def save_log(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".csv.tmp")
    df.reindex(columns=COLS).to_csv(tmp, index=False, float_format="%.10g")
    tmp.replace(path)


def register(today=None, panel: dict | None = None, root: Path | None = None, n_perm: int | None = None,
             validation: dict | None = None) -> int:
    pan = panel or L.build_panel(end=today)
    cfg = pan["cfg"]
    today = pd.Timestamp(today) if today is not None else pan["cal"][-1]
    path = log_path(cfg, root)
    log = load_log(path)
    iso = today.isocalendar()
    week = f"{iso.year}-W{iso.week:02d}"
    if (log["iso_week"] == week).any():
        print(f"[등록 건너뜀] {week}에 이미 등록됨")
        return 0
    val = validation if validation is not None else B.load_validation(cfg, root)
    chash = L.config_hash()
    new = []
    next_id = int(log["id"].max()) + 1 if len(log) else 1
    for sid in cfg["targets"]:
        for h in cfg["horizons_bdays"]:
            r = C.analyze_target(pan, sid, h, n_perm=n_perm)
            if "error" in r:
                print(f"  {sid} h={h}: {r['error']} (등록 안 함)")
                continue
            v = val.get((sid, h), {})
            validated = bool(v.get("validated", False))
            base, model = r["base"], r["prob"]
            official = model if validated else base
            row = {
                "registered_on": str(today.date()), "series": sid, "horizon": h,
                "resolve_on": str(pd.Timestamp(np.busday_offset(today.date(), h, roll="forward")).date()),
                "start_value": float(pan["known"][sid].iloc[-1]),
                "edge_lo": r["edges"][0], "edge_hi": r["edges"][1],
                "base_down": base[0], "base_flat": base[1], "base_up": base[2],
                "p_down": official[0], "p_flat": official[1], "p_up": official[2],
                "m_down": model[0], "m_flat": model[1], "m_up": model[2],
                "config_hash": chash,
            }
            adopted_tests = [t for t in r["tests"] if t.get("passes")]
            row.update({
                "id": next_id, "iso_week": week,
                "adopted": r["adopted"]["name"] if r["adopted"] else "",
                "validated": validated,
                "n_eff": min((t["n_eff"] for t in adopted_tests), default=float("nan")),
                "p_perm": min((t["p_perm"] for t in adopted_tests), default=float("nan")),
                "row_hash": row_hash(row), "status": "pending"})
            next_id += 1
            new.append(row)
    if not new:
        print("[등록할 예측이 없다]")
        return 1
    out = pd.DataFrame(new) if log.empty else pd.concat([log, pd.DataFrame(new)], ignore_index=True)
    save_log(out, path)
    print(f"[등록] {week} {len(new)}건 (검증 통과 {sum(r['validated'] for r in new)}건)")
    return 0


def grade(today=None, panel: dict | None = None, root: Path | None = None) -> int:
    pan = panel or L.build_panel(end=today)
    cfg, cat = pan["cfg"], pan["cat"]
    path = log_path(cfg, root)
    log = load_log(path)
    if log.empty:
        print("[채점] 로그 없음")
        return 0
    n_done = 0
    for i, r in log[log["status"] == "pending"].iterrows():
        sid, res = r["series"], pd.Timestamp(r["resolve_on"])
        raw = pan["raw"][sid]
        lag = int(cat.loc[sid, "lag_days"])
        if res > pan["cal"][-1] or raw.empty or raw.index.max() + pd.Timedelta(days=lag) < res:
            continue                                                        # 아직 데이터가 해소일에 도달하지 못함
        val = float(pan["known"][sid].get(res, np.nan))
        if np.isnan(val):
            continue
        start = float(r["start_value"])
        chg = (np.log(val / start) * 100.0) if cat.loc[sid, "chg"] == "pct" else (val - start)
        o = np.zeros(3)
        o[B.bin_index(chg, r["edge_lo"], r["edge_hi"])] = 1.0
        brier = lambda p: float(((np.array(p) - o) ** 2).sum())             # noqa: E731
        for col, v in (("status", "resolved"), ("resolved_on", str(pan["cal"][-1].date())),
                       ("realized_value", val), ("realized_change", chg), ("outcome_bin", float(np.argmax(o))),
                       ("brier", brier([r["p_down"], r["p_flat"], r["p_up"]])),
                       ("brier_base", brier([r["base_down"], r["base_flat"], r["base_up"]])),
                       ("brier_model", brier([r["m_down"], r["m_flat"], r["m_up"]]))):
            log.at[i, col] = v
        n_done += 1
    if n_done:
        save_log(log, path)
    print(f"[채점] 신규 해소 {n_done}건 / 대기 {int((log['status'] == 'pending').sum())}건")
    return 0


def score(root: Path | None = None, cfg: dict | None = None) -> pd.DataFrame:
    cfg = cfg or L.load_config()
    log = load_log(log_path(cfg, root))
    res = log[log["status"] == "resolved"]
    rows = []
    for (sid, h), g in res.groupby(["series", "horizon"]):
        n = len(g)
        n_eff = n / math.ceil(h / 5)
        mb = g["brier_base"].mean()
        rows.append({"series": sid, "h": int(h), "n": n, "n_eff": round(n_eff, 1),
                     "BSS_공식": round(1 - g["brier"].mean() / mb, 4),
                     "BSS_모형": round(1 - g["brier_model"].mean() / mb, 4)})
    return pd.DataFrame(rows)


def verify(root: Path | None = None, cfg: dict | None = None) -> list[str]:
    """등록 시점 필드가 사후에 바뀌지 않았는지, id·주차 중복이 없는지 확인한다."""
    cfg = cfg or L.load_config()
    log = load_log(log_path(cfg, root))
    probs = []
    if log.empty:
        return probs
    if log["id"].duplicated().any():
        probs.append("id 중복")
    if log.duplicated(["iso_week", "series", "horizon"]).any():
        probs.append("같은 주차에 같은 (대상, 지평)이 중복 등록됨")
    for _, r in log.iterrows():
        d = {k: (float(r[k]) if isinstance(r[k], (np.floating, float)) else r[k]) for k in REG_FIELDS}
        for k in ("horizon",):
            d[k] = int(d[k])
        if row_hash(d) != r["row_hash"]:
            probs.append(f"id {int(r['id'])}: 등록 필드가 변경됨(해시 불일치)")
    return probs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["register", "grade", "score", "verify"])
    a = ap.parse_args()
    if a.cmd == "register":
        return register()
    if a.cmd == "grade":
        return grade()
    if a.cmd == "score":
        s = score()
        print(s.to_string(index=False) if len(s) else "해소된 예측 없음")
        return 0
    probs = verify()
    for p in probs:
        print("[결함]", p)
    print("무결성 검사:", "통과" if not probs else f"{len(probs)}건 결함")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
