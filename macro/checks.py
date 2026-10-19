#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
checks.py - 수집 데이터 결함 검사 (조용한 실패를 큰 소리로 바꾸는 파일)

검사 항목
  빈 파일·행 수 미달      수집이 조용히 실패해도 파일은 남는다
  이력 절단               첫 관측일이 expected_start보다 한참 늦다 (예: 라이선스로 이력이 잘린 경우)
  날짜 중복·역순          병합 오류
  갱신 지연               마지막 관측일이 (발표 시차 + 주기별 허용치)를 넘음. 2배 초과는 오류
  급변                    최근 30개 변화량이 과거 변화량 MAD의 12배 초과 (단위 변경·오입력 의심)
  값 고정                 최근 10개 값이 전부 같음 (피드 정지 의심)

사용법
    python macro/checks.py            # 결함 있으면 종료코드 1
    python macro/checks.py --quiet
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import macro_lib as L  # noqa: E402

FREQ_TOL = {"D": 6, "W": 12, "M": 50, "Q": 110}     # 마지막 관측일 허용 지연(발표 시차 외 추가 일수)
START_TOL_DAYS = 45


def run_checks(today=None, obs_dir: Path | None = None, catalog: pd.DataFrame | None = None) -> list[dict]:
    cat = catalog if catalog is not None else L.load_catalog()
    obs_dir = obs_dir or L.OBS_DIR
    today = pd.Timestamp(today) if today is not None else pd.Timestamp.now("UTC").tz_localize(None).normalize()
    out = []

    def add(sid, level, msg, **extra):
        out.append({"series": sid, "level": level, "msg": msg, **extra})

    for sid, row in cat.iterrows():
        p = obs_dir / f"{sid}.csv"
        if not p.exists() or p.stat().st_size == 0:
            add(sid, "ERROR", "파일이 없거나 비어 있다")
            continue
        raw = pd.read_csv(p)
        if raw.empty or "date" not in raw or "value" not in raw:
            add(sid, "ERROR", "행이 없거나 열 구성이 다르다")
            continue
        dates = pd.to_datetime(raw["date"], errors="coerce")
        if dates.isna().any():
            add(sid, "ERROR", "날짜 파싱 실패 행이 있다")
            continue
        if dates.duplicated().any():
            add(sid, "ERROR", f"날짜 중복 {int(dates.duplicated().sum())}건")
        if not dates.is_monotonic_increasing:
            add(sid, "ERROR", "날짜가 오름차순이 아니다")
        s = pd.Series(pd.to_numeric(raw["value"], errors="coerce").to_numpy(), index=pd.DatetimeIndex(dates))
        if s.isna().any():
            add(sid, "ERROR", f"숫자가 아닌 값 {int(s.isna().sum())}건")
            s = s.dropna()
        n, first, last = len(s), s.index.min(), s.index.max()

        if n < int(row["min_rows"]):
            add(sid, "ERROR", f"행 수 {n} < 하한 {row['min_rows']}")
        exp = pd.Timestamp(row["expected_start"])
        if first > exp + pd.Timedelta(days=START_TOL_DAYS):
            add(sid, "ERROR", f"이력 절단: 첫 관측일 {first.date()} > 기대 {exp.date()}")

        age = (today - last).days
        allowed = int(row["lag_days"]) + FREQ_TOL.get(row["freq"], 10)
        if age > 2 * allowed:
            add(sid, "ERROR", f"갱신 지연 {age}일 (허용 {allowed}일의 2배 초과)", last=str(last.date()), age=age)
        elif age > allowed:
            add(sid, "WARN", f"갱신 지연 {age}일 (허용 {allowed}일)", last=str(last.date()), age=age)

        d = s.diff().dropna()
        if len(d) > 100:
            mad = float(np.median(np.abs(d - d.median())) * 1.4826)
            if mad > 0:
                recent = d.iloc[-30:]
                big = recent[np.abs(recent - d.median()) > 12 * mad]
                if len(big):
                    add(sid, "WARN", f"최근 급변 {len(big)}건 (최대 {big.abs().max():.4g}, MAD {mad:.4g})")
        if n >= 10 and s.iloc[-10:].nunique() == 1:
            add(sid, "WARN", "최근 10개 값이 동일하다 (피드 정지 의심)")

        if not any(o["series"] == sid and o["level"] in ("ERROR", "WARN") for o in out):
            add(sid, "OK", f"{n}행 {first.date()}~{last.date()}", last=str(last.date()), age=age)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    res = run_checks()
    bad = [r for r in res if r["level"] == "ERROR"]
    warn = [r for r in res if r["level"] == "WARN"]
    if not a.quiet:
        for r in res:
            print(f"[{r['level']:<5}] {r['series']:<14} {r['msg']}")
    print(f"검사 {len(res)}건: 오류 {len(bad)} / 경고 {len(warn)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
