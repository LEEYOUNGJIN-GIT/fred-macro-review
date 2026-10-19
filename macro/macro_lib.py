#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macro_lib.py - 거시 시계열 공용 로더와 상태 계산

룩어헤드(미래 정보 혼입) 방지 규칙은 이 파일에만 둔다.
  1. 모든 시리즈는 '알려진 시점' 기준으로 달력에 올린다:
       known(t) = (관측일 + lag_days) <= t 인 마지막 관측값
  2. 백분위는 시점 t까지의 후행 창(10년)만으로 계산한다 (전체 표본 백분위는 쓰지 않는다)
  3. 상태는 히스테리시스(60/40)로 전환해 경계 부근의 잦은 뒤집힘을 줄인다

검증: tests/test_macro.py의 '절단 불변성' 테스트가 "미래 데이터를 지워도 과거 시점의
상태가 변하지 않는다"를 확인한다.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

MACRO_DIR = Path(__file__).resolve().parent
ROOT = MACRO_DIR.parent
DATA_DIR = ROOT / "data"
OBS_DIR = DATA_DIR / "macro" / "obs"
CAL_START = "1990-01-01"          # 달력 시작을 고정해 절단 비교가 결정적이도록 한다


# ───────────────────────── 설정 로드 ─────────────────────────

def load_catalog(path: Path | None = None) -> pd.DataFrame:
    df = pd.read_csv(path or MACRO_DIR / "series_catalog.csv", dtype=str).fillna("")
    for c in ("lag_days", "min_rows", "max_ffill"):
        df[c] = pd.to_numeric(df[c]).astype(int)
    return df.set_index("series_id", drop=False)


def load_config(path: Path | None = None) -> dict:
    with open(path or MACRO_DIR / "states.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


MODEL_KEYS = ("percentile", "axes", "targets", "horizons_bdays", "test", "probability")


def config_hash() -> str:
    """모형을 정의하는 설정의 해시(카탈로그 + states.yaml의 MODEL_KEYS 파싱 결과).
    주석·검증 게이트·로그 경로 변경은 해시를 바꾸지 않는다. 모형이 바뀌면 사전등록 예측과 검증 요약이
    서로 다른 가설로 구분된다."""
    cfg = load_config()
    payload = json.dumps({k: cfg[k] for k in MODEL_KEYS}, sort_keys=True, ensure_ascii=False)
    cat = (MACRO_DIR / "series_catalog.csv").read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(payload.encode("utf-8") + cat).hexdigest()[:10]


def roles_of(cat: pd.DataFrame, sid: str) -> set[str]:
    return set(cat.loc[sid, "roles"].split("|"))


# ───────────────────────── 관측치 입출력 ─────────────────────────

def read_obs(sid: str, asof=None, obs_dir: Path | None = None) -> pd.Series:
    p = (obs_dir or OBS_DIR) / f"{sid}.csv"
    empty = pd.Series(dtype=float, index=pd.DatetimeIndex([]), name=sid)
    if not p.exists() or p.stat().st_size == 0:
        return empty
    df = pd.read_csv(p)
    if df.empty:
        return empty
    idx = pd.DatetimeIndex(pd.to_datetime(df["date"]))
    s = pd.Series(pd.to_numeric(df["value"], errors="coerce").to_numpy(), index=idx, name=sid)
    s = s.dropna().sort_index()
    s = s[~s.index.duplicated(keep="last")]
    if asof is not None:
        s = s[s.index <= pd.Timestamp(asof)]
    return s


# ───────────────────────── 시점 정합 변환 ─────────────────────────

def known_series(obs: pd.Series, lag_days: int, cal: pd.DatetimeIndex, max_ffill: int) -> pd.Series:
    """관측값을 '알려진 날짜'(관측일 + 발표 시차)에 올려 영업일 달력으로 ffill."""
    if obs.empty:
        return pd.Series(np.nan, index=cal, name=obs.name)
    k = obs.copy()
    k.index = k.index + pd.Timedelta(days=int(lag_days))
    k = k[~k.index.duplicated(keep="last")].sort_index()
    out = k.reindex(cal, method="ffill", limit=int(max_ffill))
    out.name = obs.name
    return out


def trailing_pct(x: pd.Series, window: int, min_periods: int) -> pd.Series:
    """시점 t의 값이 직전 window 영업일(자기 포함) 분포에서 차지하는 백분위(0~1)."""
    v = x.to_numpy(dtype=float)
    out = np.full(len(v), np.nan)
    for i in range(len(v)):
        if np.isnan(v[i]):
            continue
        w = v[max(0, i - window + 1): i + 1]
        w = w[~np.isnan(w)]
        if len(w) >= min_periods:
            out[i] = float((w <= v[i]).mean())
    return pd.Series(out, index=x.index, name=x.name)


def hysteresis(p: pd.Series, lo: float, hi: float) -> pd.Series:
    """백분위 -> 0/1 상태. hi 이상이면 1, lo 이하면 0, 사이는 직전 상태 유지."""
    out = np.full(len(p), np.nan)
    st = np.nan
    for i, v in enumerate(p.to_numpy(dtype=float)):
        if np.isnan(v):
            continue                      # 미정 구간: 상태 출력은 NaN, 직전 상태는 보존
        if np.isnan(st):
            st = 1.0 if v >= 0.5 else 0.0
        elif v >= hi:
            st = 1.0
        elif v <= lo:
            st = 0.0
        out[i] = st
    return pd.Series(out, index=p.index, name=p.name)


def level_at_pct(x: pd.Series, q: float, window: int) -> float:
    """현재 창에서 백분위 q에 해당하는 값 (상태가 뒤집히는 지표 수준 계산용)."""
    w = x.dropna().to_numpy()[-window:]
    return float(np.quantile(w, q)) if len(w) else float("nan")


# ───────────────────────── 패널 ─────────────────────────

def build_panel(end=None, asof=None, obs_dir: Path | None = None,
                catalog: pd.DataFrame | None = None, cfg: dict | None = None) -> dict:
    """알려진 값·후행 백분위·상태 축을 담은 패널.

    end : 달력 마지막 날(기본 오늘 UTC). asof : 이 날짜 이후 관측은 존재하지 않는 것으로 취급.
    """
    cat = catalog if catalog is not None else load_catalog()
    cfg = cfg or load_config()
    pc = cfg["percentile"]
    end = pd.Timestamp(end) if end is not None else pd.Timestamp.now("UTC").tz_localize(None).normalize()
    if asof is not None:
        end = min(end, pd.Timestamp(asof))
    cal = pd.bdate_range(CAL_START, end)

    raw, known, pct = {}, {}, {}
    for sid in cat.index:
        o = read_obs(sid, asof=asof, obs_dir=obs_dir)
        raw[sid] = o
        k = known_series(o, int(cat.loc[sid, "lag_days"]), cal, int(cat.loc[sid, "max_ffill"]))
        known[sid] = k
        if not o.empty:
            pct[sid] = trailing_pct(k, pc["window_bdays"], pc["min_bdays"])
        else:
            pct[sid] = pd.Series(np.nan, index=cal, name=sid)
    known_df, pct_df = pd.DataFrame(known), pd.DataFrame(pct)

    axis_pct, axis_state = {}, {}
    for ax, spec in cfg["axes"].items():
        comp = pct_df[spec["series"]]
        ap = comp.mean(axis=1, skipna=False)          # 구성 시리즈 중 하나라도 미정이면 미정
        axis_pct[ax] = ap
        axis_state[ax] = hysteresis(ap, pc["hysteresis_lo"], pc["hysteresis_hi"])
    return {
        "cal": cal, "cat": cat, "cfg": cfg, "raw": raw, "known": known_df, "pct": pct_df,
        "axis_pct": pd.DataFrame(axis_pct), "axis_state": pd.DataFrame(axis_state),
    }


def forward_change(known: pd.Series, kind: str, h: int) -> pd.Series:
    """t 시점에 알려진 값 대비 t+h 영업일 시점에 알려진 값의 변화. kind: diff(차이) | pct(로그수익률 %)."""
    f = known.shift(-h)
    if kind == "pct":
        return np.log(f / known) * 100.0
    return f - known


def cell_code(axis_state: pd.DataFrame, order: list[str]) -> pd.Series:
    """3축 이진 상태를 0~7 셀 번호로 결합. 하나라도 미정이면 NaN."""
    code = pd.Series(0.0, index=axis_state.index)
    for i, ax in enumerate(order):
        code = code + axis_state[ax] * (2 ** (len(order) - 1 - i))
    return code
