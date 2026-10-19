#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_v93.py - Macro 티어(v9.3) 개정을 프로젝트 문서 3종에 적용한다.

대상: guideline_core.md / core_digest.md / agenda_pending.md
방식: 앵커 문자열이 파일에 정확히 1회 있을 때만 치환한다. 하나라도 어긋나면 아무 파일도 쓰지 않고 중단한다.
      (프로젝트 문서는 단일 파일 통째 교체 방식이라, 부분 적용된 상태를 만들지 않는 것이 목적이다.)

사용: 프로젝트에서 위 3개 파일을 한 폴더로 내려받은 뒤
    python3 apply_v93.py --dir 폴더
    -> 같은 폴더에 *.v93 파일이 생성된다. 확인 후 원래 이름으로 프로젝트에 다시 올린다.
    (--inplace를 주면 .bak을 남기고 원본을 직접 덮어쓴다)
적용 후 새 세션에서 selftest / provenance / crosscheck 가 통과하는지 확인한다.
"""
import argparse
import os
import re
import sys

# ───────────────────────── 삽입 텍스트 ─────────────────────────

CORE_V93_PARA = """**v9.3 개정 성격 (2026-10-19, 사용자 승인 — agenda P-101~P-104)**: 거시 전망 중심의 **Macro 티어**를 신설한다(1-1a).
포트폴리오 입력 없이 `macro_outlook.md` 하나로 지표·상태·방향 확률·채점 현황을 답한다 ★v9.3.
배경: Full이 포트폴리오 갱신(snapshot)과 TIER 구조에 묶여 거시 질의에 형식·갱신 부담이 컸다. 이 티어는 배분 권한이 없으므로
IPS·SAA·8-5 확률 규율에는 영향이 없다. 한국 일별 4종(국고채 3Y·10Y, KOSPI, 원/달러 매매기준율)은 ECOS에서 수집해 같은 파일에 편입했다.
**조항 순증: 1개(1-1a)** — 1-2b 연 3개 상한 대상.

"""

CORE_TIER_ROW = """| Quick | 단일 지표 질의 | 해당 latest + 실시간 검증 | 인라인 5줄 | 없음 |
| **Macro** ★v9.3 | 거시 전망·지표 조합 질의, 포트폴리오 없이 시작하는 세션 | `macro_outlook.md` (1-1a) | 기본 답변 + 선택 추가(1-1a) | **없음** |"""

CORE_SEC_1_1A = """### 1-1a. Macro 티어 ★v9.3

**목적**: 적시에 정보를 파악하고, 지표 조합이 어느 방향으로 흘러갈 수 있는지를 확률 범위로 본다.
**입력**: `macro_outlook.md` (GitHub 자동 생성, 수동 편집 금지). 포트폴리오 파일·snapshot·보유 입력은 **필요 없다** — 사용자 갱신 부담을 지우는 것이 설계 목적이다.

**기본 답변 (항상, 이 순서)**
```
① 달라진 것 3개   지표 표(수준·1M·3M·가속·10년 위치)에서 변화가 큰 순
② 시장 내재 상태   3축(커브·물가기대·신용변동성)의 현재 상태와 전환 조건
③ 방향 확률        대상별 21·63영업일 하락/횡보/상승 범위(±10%p) + 근거 등급
④ 신뢰 1줄         데이터 결함·예측 로그 무결성·채점 현황
끝에 추가 답변 메뉴 1줄 (아래)
```
**추가 답변 (사용자가 고른 것만)**: A 지평 선택(21/63) · B 지표별 3차원 상세 · C 조건부 분포 표본(n·n_eff·p값) ·
D 검증 결과와 한계 · E 한국-미국 연계 · F 포트폴리오 영향(이때만 snapshot 로드).

**규칙**
```
1. 근거 등급을 반드시 병기한다 — [검증 통과] 신호 반영 / [기저율] 검증 미통과로 약 1/3씩.
   기저율 항목의 방향을 서사로 확대하지 않는다(사실상 정보 없음).
2. 확률은 범위(±10%p). 점추정·'확실' 표현 금지(원칙 7).
3. macro_outlook.md 섹션 0에 결함 또는 무결성 경고가 있으면 확률을 인용하기 전에 그 사실을 먼저 쓴다.
4. 사전등록 예측만 '예측'이라 부른다. 채점 표본이 쌓이기 전(n_eff 부족)에는 신호의 우위를 주장하지 않는다.
5. 이 확률은 S1~S4 시나리오 확률의 근거가 아니다 — 8-5 확률 변경 규율이 우선한다.
   시장 내재 확률과의 대조 참고용으로만 병기할 수 있다(agenda P-34).
6. 배분·종목 제안 금지. 포트폴리오 영향(F)을 요청받아도 방향·강도만, Full 절차로 승격한다.
7. 월간 한국 지표(CPI·기준금리·GDP 등)는 조건부 분포에 쓰지 않는다 — 개정·발표 시차·표본 수 때문. 표시용으로만 ecos_latest.md를 인용한다.
```
**한계 공개 의무**: 검증된 신호가 소수(작성 시점 VIX 평균회귀 1건)라는 사실, 게이트 선정이 표본 내 선택이라는 사실을 D 요청 시 숨기지 않는다.

"""

CORE_DATA_ROW = """| **snapshot.md** | 포트폴리오 종합잔고 | 간헐 갱신. 기준일자 확인 + 3-1 신선도 판정(주기 M) |
| **macro_outlook.md** ★v9.3 | 지표·시장 내재 상태·방향 확률·사전등록 채점 (자동 생성, 파생물) | **Macro 티어 입력(1-1a).** 원천 수치의 정본은 fred_latest.md·ecos_latest.md이며 이 파일의 확률은 규칙 기반 산출물이다. 산출 코드·예측 로그는 GitHub 저장소에 있고 프로젝트 문서함에는 없다 |"""

DIGEST_TIER_ROW = """| Quick | 단일지표질의 | 인라인 5줄 | 없음 |
| Macro(v9.3) | 거시전망·지표조합 질의 | 기본답변+선택추가 | 없음 |"""

DIGEST_MACRO = """### Macro 티어 (1-1a, v9.3 신설)
```
입력: macro_outlook.md 하나(포트폴리오 불필요). 기본답변: ①달라진 것3 ②3축 상태·전환조건 ③21·63영업일 방향 확률(±10%p, 근거등급 병기) ④신뢰1줄
추가(요청시만): 지평선택·3차원상세·조건부분포표본·검증한계·한미연계·포트폴리오영향(이때만 snapshot)
규칙: 기저율 항목 서사 확대 금지 / 섹션0 결함 선언 후 인용 / 사전등록만 '예측' / S1~S4 확률 근거 아님(8-5 우선) / 배분·종목 제안 금지 / 월간 한국지표는 조건부분포 제외
```

### Watch 게이트 8개"""

AGENDA_SEC = """## L. 2026-10-19 — Macro 티어(v9.3) 개정 접수

**사용자 승인 후 반영한 항목과 남은 결정 사항. 심의·확정은 Review 세션에서 한다.**

| # | 안건 | 대상 | 발견 회차 | 상태 |
|---|---|---|---|---|
| P-101 | Macro 티어 신설(guideline_core 1-1a) — 포트폴리오 입력 없이 macro_outlook.md로 거시 전망을 답한다. 조항 순증 1개(1-2b 연 3개 상한). P-34(시장 내재 확률 대조 절차 부재)를 부분 해소하는 도구이나 S1~S4 확률의 근거로는 쓰지 않는다 | guideline_core 1-1a·2-1 / core_digest | 2026-10-19 | **반영 (사용자 승인 2026-10-19)** — 프로젝트 지침(붙여넣기 본)의 반영은 별도(P-100과 함께 적용 가능) |
| P-102 | 한국 일별 4종 ECOS 편입 범위 — 국고채 3Y·10Y, KOSPI, 원/달러 매매기준율. 월간·분기 한국 지표는 조건부 분포에서 제외(개정·발표 시차·표본 수). FRED H.10(발표 시차 8일)과 ECOS 매매기준율(시차 1일)은 서로 다른 계열이라 병존한다 | macro 패키지(GitHub) | 2026-10-19 | 반영 — 한국 대상의 검증 통과 여부는 ECOS 이력 수집 후 백테스트로 확인 |
| P-103 | 검증 게이트·수축 계수의 한계 — 게이트 통과 선정이 백테스트 전체를 본 뒤의 표본 내 선택이고, 수축 계수 shrink_k=30과 상태 축 선택은 [주관 판단]이다. 작성 시점 검증 통과는 VIX 평균회귀 1건뿐 | macro 패키지 / assumptions 등재 검토 | 2026-10-19 | **결정 필요** — assumptions.csv 등재 여부(등재 시 이 항목과 A-id 연계) |
| P-104 | 사전등록 예측 로그의 존치·승격 기준 — 채점 표본 n_eff가 얼마 쌓였을 때 어떤 BSS·z 기준으로 신호를 공식 확률에 올리거나 내릴지. 현재는 백테스트 z≥2·BSS>0만 규칙화돼 있다. 고정 ±10%p 폭(P-38)과의 관계도 함께 | macro 패키지 / guideline_core 1-1a | 2026-10-19 | **결정 필요** (Review, 로그 3개월 이상 축적 후) |

---

## 배치 진행 현황"""

AGENDA_HEADER_OLD = "**최종 갱신**: 2026-09-16 (Review — 구조 개편 세션: K절 신설, P-80·P-82 상태 갱신)"
AGENDA_HEADER_NEW = "**최종 갱신**: 2026-10-19 (Macro 티어 v9.3: L절 신설, P-101~P-104 접수)"

# (파일 키, 앵커, 치환, 설명)
EDITS = {
    "guideline_core.md": [
        ("**버전**: 9.2 | **작성일**: 2026-08-27 | **개정일**: 2026-09-16 |",
         "**버전**: 9.3 | **작성일**: 2026-08-27 | **개정일**: 2026-10-19 |", "헤더 버전"),
        ("**v9.2 개정 성격 (2026-09-16, Review", CORE_V93_PARA + "**v9.2 개정 성격 (2026-09-16, Review", "v9.3 개정 성격"),
        ("| Quick | 단일 지표 질의 | 해당 latest + 실시간 검증 | 인라인 5줄 | 없음 |", CORE_TIER_ROW, "티어 표 Macro 행"),
        ("### 1-2. 호출 주기 — 상태 기반 발동 (v9.0)", CORE_SEC_1_1A + "### 1-2. 호출 주기 — 상태 기반 발동 (v9.0)", "1-1a 신설"),
        ("| **snapshot.md** | 포트폴리오 종합잔고 | 간헐 갱신. 기준일자 확인 + 3-1 신선도 판정(주기 M) |", CORE_DATA_ROW, "2-1 데이터 레이어 등재"),
    ],
    "core_digest.md": [
        ("guideline_core.md 9.2 ·", "guideline_core.md 9.3 ·", "다이제스트 원문 버전 줄"),
        ("**갱신 2026-09-16 (Review — 구조 개편 세션, decision 082)**:",
         "**갱신 2026-10-19 (Macro 티어 v9.3 — agenda P-101)**: guideline_core 1-1a·2-1 신설분 반영. 직전 갱신 2026-09-16 (Review — 구조 개편 세션, decision 082):",
         "다이제스트 갱신 문구"),
        ("## M. guideline_core.md (전 티어 로드) — v9.2", "## M. guideline_core.md (전 티어 로드) — v9.3", "다이제스트 M 헤딩"),
        ("| Quick | 단일지표질의 | 인라인 5줄 | 없음 |", DIGEST_TIER_ROW, "다이제스트 티어 행"),
        ("### Watch 게이트 8개", DIGEST_MACRO, "다이제스트 Macro 절"),
    ],
    "agenda_pending.md": [
        (AGENDA_HEADER_OLD, AGENDA_HEADER_NEW, "agenda 갱신일"),
        ("## 배치 진행 현황", AGENDA_SEC, "agenda L절"),
    ],
}


def locate(d, name):
    cands = [os.path.join(d, name), os.path.join(d, "claude", name)]
    for c in cands:
        if os.path.exists(c):
            return c
    return None


def plan(d):
    out, errs = {}, []
    for name, edits in EDITS.items():
        p = locate(d, name)
        if p is None:
            errs.append(f"{name}: 폴더에 없다")
            continue
        txt = open(p, encoding="utf-8").read()
        for old, new, why in edits:
            n = txt.count(old)
            if n != 1:
                errs.append(f"{name} / {why}: 앵커가 {n}회 발견됨(1회여야 한다) — 문서가 이미 바뀌었거나 앵커가 다르다")
                continue
            txt = txt.replace(old, new)
        out[name] = (p, txt)
    return out, errs


def post_checks(out):
    errs = []
    inserted = "\n".join([CORE_V93_PARA, CORE_SEC_1_1A, CORE_DATA_ROW, DIGEST_MACRO, AGENDA_SEC])
    # crosscheck [7]: 프로젝트 문서에 폴더에 없는 .py 이름을 쓰지 않는다
    for m in sorted(set(re.findall(r"\b([a-z_]+\.py)\b", inserted))):
        errs.append(f"삽입 텍스트에 스크립트 이름 '{m}' — crosscheck [7] 위반 위험")
    # crosscheck [1]/[2]: 헤더 버전과 다이제스트 기재 버전
    core = out["guideline_core.md"][1]
    dig = out["core_digest.md"][1]
    if not re.search(r"\*\*버전\*\*:\s*9\.3\b", core):
        errs.append("guideline_core 헤더가 9.3이 아니다")
    if "guideline_core.md 9.3 ·" not in dig:
        errs.append("다이제스트가 원문 9.3을 기재하지 않는다")
    # crosscheck [4]: 새로 참조한 P-번호가 agenda에 정의돼 있는가
    agenda = out["agenda_pending.md"][1]
    defined = set(re.findall(r"P-(\d{2,3})", agenda))
    for f in ("guideline_core.md", "core_digest.md"):
        for n in set(re.findall(r"P-(\d{2,3})\b", out[f][1])):
            if n not in defined:
                errs.append(f"{f}가 참조한 P-{n}이 agenda_pending.md에 없다")
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--inplace", action="store_true")
    a = ap.parse_args()
    out, errs = plan(a.dir)
    if not errs:
        errs = post_checks(out)
    if errs:
        print("[중단] 아무 파일도 쓰지 않았다")
        for e in errs:
            print("  -", e)
        return 1
    for name, (p, txt) in out.items():
        if a.inplace:
            os.replace(p, p + ".bak")
            open(p, "w", encoding="utf-8").write(txt)
            print(f"  갱신 {p} (백업 {p}.bak)")
        else:
            open(p + ".v93", "w", encoding="utf-8").write(txt)
            print(f"  생성 {p}.v93")
    print("완료. 새 세션에서 selftest / provenance / crosscheck 통과를 확인한다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
