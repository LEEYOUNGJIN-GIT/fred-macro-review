# -*- coding: utf-8 -*-
"""결정적(deterministic) 합성 FRED 응답 생성기.

주의: 여기서 만드는 값은 모두 **합성값**이다. 실제 FRED 관측값이 아니다.
FRED 응답 형식(series / series/observations JSON)만 흉내 낸다.
"""
import math
from datetime import date, timedelta

HOLIDAYS_MD = {(1, 1), (7, 4), (12, 25)}   # 결측(".") 위치 재현용


def _business_days(start, end):
    d = start
    while d <= end:
        if d.weekday() < 5:
            yield d
        d += timedelta(days=1)


def _months(start, end):
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        yield date(y, m, 1)
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def _daily_obs(start, end, base, amp, period, decimals=2):
    out = []
    for i, d in enumerate(_business_days(start, end)):
        if (d.month, d.day) in HOLIDAYS_MD:
            v = "."
        else:
            v = f"{base + amp * math.sin(i / period):.{decimals}f}"
        out.append({"date": d.isoformat(), "value": v})
    return out


def _monthly_obs(start, end, base, growth, seasonal=0.0):
    out = []
    for i, d in enumerate(_months(start, end)):
        v = base * (1 + growth) ** i + seasonal * math.sin(2 * math.pi * (d.month - 1) / 12)
        out.append({"date": d.isoformat(), "value": f"{v:.3f}"})
    return out


def _meta(sid, title, units, freq, sa, obs_start, obs_end):
    return {"id": sid, "title": title, "units": units, "frequency_short": freq,
            "frequency": {"D": "Daily", "M": "Monthly"}[freq],
            "seasonal_adjustment_short": sa,
            "seasonal_adjustment": {"SA": "Seasonally Adjusted",
                                    "NSA": "Not Seasonally Adjusted"}[sa],
            "observation_start": obs_start, "observation_end": obs_end,
            "last_updated": "2026-10-09 15:16:02-05"}


def _unrate_vintage():
    """UNRATE 합성 vintage: 월별 관측이 1개월 후 최초 발표, 2개월 후 1회 개정."""
    rows = []
    for i, d in enumerate(_months(date(2024, 1, 1), date(2026, 8, 1))):
        first = 4.0 + 0.1 * math.sin(i / 3)
        rel1 = date(d.year + (d.month // 12), d.month % 12 + 1, 5)
        rel2 = date(rel1.year + (rel1.month // 12), rel1.month % 12 + 1, 5)
        rows.append({"realtime_start": rel1.isoformat(),
                     "realtime_end": (rel2 - timedelta(days=1)).isoformat(),
                     "date": d.isoformat(), "value": f"{first:.1f}"})
        rows.append({"realtime_start": rel2.isoformat(), "realtime_end": "9999-12-31",
                     "date": d.isoformat(), "value": f"{first + 0.1:.1f}"})
    return rows


def build_series():
    end_d = date(2026, 10, 8)
    s = {
        "DFII10": {
            "meta": _meta("DFII10", "Market Yield on U.S. Treasury Securities at 10-Year "
                          "Constant Maturity, Quoted on an Investment Basis, Inflation-Indexed",
                          "Percent", "D", "NSA", "2003-01-02", "2026-10-08"),
            "observations": _daily_obs(date(2015, 1, 1), end_d, 1.5, 1.2, 90),
        },
        "DEXKOUS": {
            "meta": _meta("DEXKOUS", "South Korean Won to U.S. Dollar Spot Exchange Rate",
                          "South Korean Won to One U.S. Dollar", "D", "NSA",
                          "1981-04-13", "2026-10-02"),
            "observations": _daily_obs(date(2015, 1, 1), date(2026, 10, 2), 1250, 120, 70),
        },
        "CPIAUCSL": {
            "meta": _meta("CPIAUCSL", "Consumer Price Index for All Urban Consumers: "
                          "All Items in U.S. City Average", "Index 1982-1984=100",
                          "M", "SA", "1947-01-01", "2026-08-01"),
            "observations": _monthly_obs(date(2000, 1, 1), date(2026, 8, 1), 169.3, 0.0021),
        },
        "CPIAUCNS": {
            "meta": _meta("CPIAUCNS", "Consumer Price Index for All Urban Consumers: "
                          "All Items in U.S. City Average", "Index 1982-1984=100",
                          "M", "NSA", "1913-01-01", "2026-08-01"),
            "observations": _monthly_obs(date(2000, 1, 1), date(2026, 8, 1), 168.8, 0.0021,
                                         seasonal=0.6),
        },
        # 가정 시나리오: FRED 메타상 시작일은 1996 이지만 API 가 최근 3년만 반환하는 경우
        "BAMLH0A0HYM2": {
            "meta": _meta("BAMLH0A0HYM2", "ICE BofA US High Yield Index Option-Adjusted Spread",
                          "Percent", "D", "NSA", "1996-12-31", "2026-10-08"),
            "observations": _daily_obs(date(2023, 10, 9), end_d, 3.3, 0.4, 40),
        },
        "UNRATE": {
            "meta": _meta("UNRATE", "Unemployment Rate", "Percent", "M", "SA",
                          "1948-01-01", "2026-09-01"),
            "observations": [{"date": d.isoformat(),
                              "value": f"{4.0 + 0.1 * math.sin(i / 3) + 0.1:.1f}"}
                             for i, d in enumerate(_months(date(2016, 1, 1),
                                                           date(2026, 8, 1)))],
            "vintage": _unrate_vintage(),
        },
    }
    return s


# ── fred_fetch.py 골든 회귀용: REG 전체에 대한 desc 정렬 관측값 ──

_N_BY_FREQ = {"D": 800, "W": 170, "M": 40, "Q": 14, "A": 5}


def golden_observations(series_id, freq, k):
    """fred_fetch.fetch_fred_series 가 받는 FRED 원 응답(observations, desc)."""
    n = _N_BY_FREQ[freq]
    end = date(2026, 10, 9)
    out = []
    for i in range(n):
        if freq == "D":
            d = end - timedelta(days=i)
        elif freq == "W":
            d = end - timedelta(weeks=i)
        elif freq == "M":
            y, m = divmod((2026 * 12 + 8) - i, 12)
            d = date(y, m + 1, 1)
        elif freq == "Q":
            y, q = divmod((2026 * 4 + 2) - i, 4)
            d = date(y, q * 3 + 1, 1)
        else:
            d = date(2025 - i, 1, 1)
        base = 10 ** (k % 5)
        if freq == "D" and i % 23 == 7:
            v = "."
        else:
            v = f"{base * (1 + 0.3 * math.sin(i / (3 + k % 7) + k)):.4f}"
            if k % 11 == 0 and i == 2:
                v = "0"        # 0 값 보존 경로
        out.append({"realtime_start": "2026-10-12", "realtime_end": "2026-10-12",
                    "date": d.isoformat(), "value": v})
    return out
