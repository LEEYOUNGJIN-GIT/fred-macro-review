#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data/series/ 무결성 검사 (CI 용)
──────────────────────────────────────────────────────────
검사 항목
• fred/{ID}.csv      헤더 == date,value / ISO 날짜 / 오름차순·중복 없음 /
                     값은 float 또는 빈칸 / 월·분기·연 시리즈는 기간 첫날
• fred_meta.csv      필수 열 / series_type 허용값 / vintage Y|N /
                     seasonal_adjustment 비어있지 않음 / 시리즈 파일과 1:1
• _revisions.csv     헤더 / 날짜 형식
• fred_vintage/*.csv 헤더 / 정렬·중복 없음 / realtime_start <= realtime_end

사용법:
    python scripts/validate_series.py [--root data/series] [--short-report]
종료코드: 0=통과, 1=오류 존재
"""

import argparse
import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fred_series_collect import (  # noqa: E402
    DEFAULT_OUT, META_COLUMNS, REVISION_COLUMNS, SERIES_COLUMNS, SERIES_TYPES,
    VINTAGE_COLUMNS,
)


def _read_raw(path):
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def _iso_ok(s):
    try:
        return date.fromisoformat(s).isoformat() == s
    except (TypeError, ValueError):
        return False


def _float_ok(s):
    if s == "":
        return True
    try:
        float(s)
        return s.strip().lower() not in ("nan", "inf", "-inf", ".")
    except ValueError:
        return False


def check_series_file(path, freq=None):
    errs = []
    df = _read_raw(path)
    name = Path(path).name
    if list(df.columns) != SERIES_COLUMNS:
        return [f"{name}: 헤더 {list(df.columns)} != {SERIES_COLUMNS}"]
    if df.empty:
        errs.append(f"{name}: 관측 0행")
    bad_dates = [d for d in df["date"] if not _iso_ok(d)]
    if bad_dates:
        errs.append(f"{name}: ISO 아닌 날짜 {len(bad_dates)}건 (예: {bad_dates[0]})")
        return errs
    if df["date"].duplicated().any():
        errs.append(f"{name}: 중복 날짜 {int(df['date'].duplicated().sum())}건")
    if list(df["date"]) != sorted(df["date"]):
        errs.append(f"{name}: 날짜 오름차순 아님")
    bad_vals = [v for v in df["value"] if not _float_ok(v)]
    if bad_vals:
        errs.append(f"{name}: 숫자 아닌 값 {len(bad_vals)}건 (예: {bad_vals[0]!r})")
    if freq in ("M", "Q", "SA", "A"):
        ds = [date.fromisoformat(d) for d in df["date"]]
        months = {"M": range(1, 13), "Q": (1, 4, 7, 10), "SA": (1, 7), "A": (1,)}[freq]
        off = [d for d in ds if d.day != 1 or d.month not in months]
        if off:
            errs.append(f"{name}: {freq} 시리즈인데 기간 첫날이 아닌 날짜 {len(off)}건 "
                        f"(예: {off[0]})")
    return errs


def check_meta(path, series_ids):
    errs = []
    df = _read_raw(path)
    missing = [c for c in META_COLUMNS if c not in df.columns]
    if missing:
        return [f"fred_meta.csv: 필수 열 누락 {missing}"], df
    if df["series_id"].duplicated().any():
        errs.append("fred_meta.csv: series_id 중복")
    bad_type = df[~df["series_type"].isin(SERIES_TYPES)]
    for sid, t in zip(bad_type["series_id"], bad_type["series_type"]):
        errs.append(f"fred_meta.csv: {sid} series_type={t!r} 허용값 아님")
    bad_v = df[~df["vintage"].isin(["Y", "N"])]
    for sid in bad_v["series_id"]:
        errs.append(f"fred_meta.csv: {sid} vintage 값 Y|N 아님")
    for sid in df[df["seasonal_adjustment"] == ""]["series_id"]:
        errs.append(f"fred_meta.csv: {sid} seasonal_adjustment 비어 있음")
    for sid, y in zip(df["series_id"], df["years_available"]):
        if not _float_ok(y) or y == "":
            errs.append(f"fred_meta.csv: {sid} years_available={y!r} 숫자 아님")
    meta_ids = set(df["series_id"])
    for sid in sorted(set(series_ids) - meta_ids):
        errs.append(f"fred_meta.csv: {sid} 시리즈 파일은 있으나 메타 행 없음")
    for sid in sorted(meta_ids - set(series_ids)):
        errs.append(f"fred_meta.csv: {sid} 메타 행은 있으나 시리즈 파일 없음")
    return errs, df


def check_revisions(path):
    df = _read_raw(path)
    if list(df.columns) != REVISION_COLUMNS:
        return [f"_revisions.csv: 헤더 {list(df.columns)} != {REVISION_COLUMNS}"]
    bad = [d for d in df["date"] if not _iso_ok(d)]
    return [f"_revisions.csv: ISO 아닌 날짜 {len(bad)}건"] if bad else []


def check_vintage_file(path):
    errs = []
    name = f"fred_vintage/{Path(path).name}"
    df = _read_raw(path)
    if list(df.columns) != VINTAGE_COLUMNS:
        return [f"{name}: 헤더 {list(df.columns)} != {VINTAGE_COLUMNS}"]
    key = df[["date", "realtime_start"]]
    if key.duplicated().any():
        errs.append(f"{name}: (date, realtime_start) 중복")
    if list(map(tuple, key.values)) != sorted(map(tuple, key.values)):
        errs.append(f"{name}: 정렬 아님")
    if (df["realtime_start"] > df["realtime_end"]).any():
        errs.append(f"{name}: realtime_start > realtime_end")
    bad_vals = [v for v in df["value"] if not _float_ok(v)]
    if bad_vals:
        errs.append(f"{name}: 숫자 아닌 값 {len(bad_vals)}건")
    return errs


def validate(root):
    root = Path(root)
    errs = []
    series_dir = root / "fred"
    files = sorted(series_dir.glob("*.csv")) if series_dir.exists() else []
    ids = [f.stem for f in files]
    meta_path = root / "fred_meta.csv"
    freq = {}
    if meta_path.exists():
        e, mdf = check_meta(meta_path, ids)
        errs += e
        if "frequency" in mdf.columns:
            freq = dict(zip(mdf["series_id"], mdf["frequency"]))
    elif files:
        errs.append("fred_meta.csv 없음 (시리즈 파일은 존재)")
    for f in files:
        errs += check_series_file(f, freq.get(f.stem))
    if (root / "_revisions.csv").exists():
        errs += check_revisions(root / "_revisions.csv")
    vdir = root / "fred_vintage"
    if vdir.exists():
        for f in sorted(vdir.glob("*.csv")):
            errs += check_vintage_file(f)
    return errs, len(files)


def short_history_report(root):
    meta_path = Path(root) / "fred_meta.csv"
    if not meta_path.exists():
        return "fred_meta.csv 없음"
    df = _read_raw(meta_path)
    df = df[df["short_history"] == "True"]
    lines = ["| series_id | years_available | observation_start(FRED) | frequency |",
             "| --- | --- | --- | --- |"]
    for r in df.sort_values("years_available").to_dict("records"):
        lines.append(f"| {r['series_id']} | {r['years_available']} | "
                     f"{r['observation_start']} | {r['frequency']} |")
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description="data/series 무결성 검사")
    p.add_argument("--root", default=str(DEFAULT_OUT))
    p.add_argument("--short-report", action="store_true",
                   help="years_available < 10 시리즈 표 출력")
    args = p.parse_args(argv)
    errs, n = validate(args.root)
    print(f"검사 대상 시리즈 파일: {n}개")
    if args.short_report:
        print(short_history_report(args.root))
    if errs:
        print(f"오류 {len(errs)}건")
        for e in errs:
            print(f"  - {e}")
        return 1
    print("통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
