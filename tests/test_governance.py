#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""governance/v9.3/apply_v93.py 검증 - 실제 문서에서 복사한 앵커 줄로 만든 최소 픽스처를 쓴다.
(실제 문서 전체와의 일치는 사용자 환경에서 스크립트가 앵커 1회 검사로 다시 확인한다.)"""
import importlib.util
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("apply_v93", ROOT / "governance/v9.3/apply_v93.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

CORE = """# guideline_core.md

**버전**: 9.2 | **작성일**: 2026-08-27 | **개정일**: 2026-09-16 | **로드 범위**: Quick·Standard·Full 전 티어

**v9.2 개정 성격 (2026-09-16, Review — 구조 개편 세션, `restructure_plan_agenda.md` §0-1 배치)**:
본문.

| Quick | 단일 지표 질의 | 해당 latest + 실시간 검증 | 인라인 5줄 | 없음 |

### 1-2. 호출 주기 — 상태 기반 발동 (v9.0)

| **snapshot.md** | 포트폴리오 종합잔고 | 간헐 갱신. 기준일자 확인 + 3-1 신선도 판정(주기 M) |
참조 P-34 P-98
"""
DIGEST = """# core_digest.md
**생성**: 2026-09-14. **갱신 2026-09-16 (Review — 구조 개편 세션, decision 082)**: 반영. 원문 버전 — IPS.md 1.1 · guideline_core.md 9.2 · guideline_standard.md 9.2.
---
## M. guideline_core.md (전 티어 로드) — v9.2
| Quick | 단일지표질의 | 인라인 5줄 | 없음 |
### Watch 게이트 8개
"""
AGENDA = """# agenda_pending.md
**최종 갱신**: 2026-09-16 (Review — 구조 개편 세션: K절 신설, P-80·P-82 상태 갱신)
| P-34 | x |
| P-38 | x |
| P-98 | x |
| P-100 | x |
## 배치 진행 현황
"""


def build(d, core=CORE, digest=DIGEST, agenda=AGENDA):
    (d / "claude").mkdir(parents=True, exist_ok=True)
    (d / "guideline_core.md").write_text(core, encoding="utf-8")
    (d / "claude" / "core_digest.md").write_text(digest, encoding="utf-8")   # 프로젝트에서의 실제 경로
    (d / "agenda_pending.md").write_text(agenda, encoding="utf-8")


def test_applies_and_passes_crosscheck_rules():
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        build(d)
        assert M.main.__call__ is not None
        out, errs = M.plan(str(d))
        assert not errs, errs
        assert not M.post_checks(out), M.post_checks(out)
        core = out["guideline_core.md"][1]
        assert re.search(r"\*\*버전\*\*:\s*9\.3\b", core)
        assert core.count("### 1-1a. Macro 티어") == 1 and core.count("| **Macro** ★v9.3 |") == 1
        assert "macro_outlook.md" in core                                    # crosscheck [3] 등재
        assert "guideline_core.md 9.3 ·" in out["core_digest.md"][1]
        # crosscheck [1] 규칙 재현: 본문 마커가 헤더보다 높으면 실패
        marks = {tuple(map(int, m)) for m in re.findall(r"★\s*v(\d+)\.(\d+)", core)}
        assert max(marks) <= (9, 3)
        # [7] 규칙 재현
        assert not re.findall(r"\b[a-z_]+\.py\b", M.CORE_SEC_1_1A + M.CORE_DATA_ROW + M.DIGEST_MACRO + M.AGENDA_SEC)


def test_aborts_without_writing_when_anchor_missing_or_duplicated():
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        build(d, agenda=AGENDA.replace("## 배치 진행 현황", "## 다른 제목"))
        before = {p: p.read_text(encoding="utf-8") for p in d.rglob("*.md")}
        rc = M.sys.argv and None
        sys.argv = ["apply_v93.py", "--dir", str(d), "--inplace"]
        assert M.main() == 1
        assert {p: p.read_text(encoding="utf-8") for p in d.rglob("*.md")} == before      # 아무 파일도 안 바뀜
        assert not list(d.rglob("*.bak")) and not list(d.rglob("*.v93"))
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        build(d, core=CORE + "\n" + CORE.split("\n\n")[1])                   # 헤더 줄이 2회
        out, errs = M.plan(str(d))
        assert any("2회" in e for e in errs)


def test_double_apply_is_rejected():
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        build(d)
        sys.argv = ["apply_v93.py", "--dir", str(d), "--inplace"]
        assert M.main() == 0
        assert M.main() == 1                                                  # 두 번째는 앵커가 사라져 중단


def main():
    fails = 0
    for n, f in list(globals().items()):
        if n.startswith("test_"):
            try:
                f(); print("  통과", n)
            except Exception as e:                                          # noqa: BLE001
                fails += 1; print("  실패", n, repr(e))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
