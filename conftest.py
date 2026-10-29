# -*- coding: utf-8 -*-
"""根配置：注入项目根到 sys.path，并在会话结束时生成 HTML 报告。"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))

from report import generate_report

_COLLECTED = []


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return
    err = getattr(report, "longreprtext", "") or "" if report.outcome == "failed" else ""
    _COLLECTED.append({
        "nodeid": report.nodeid,
        "name": item.name,
        "outcome": report.outcome,
        "duration": report.duration,
        "error": err,
    })


def pytest_sessionfinish(session):
    suites = {}
    for r in _COLLECTED:
        s = r["nodeid"].split("::")[0].replace("tests/", "").replace(".py", "")
        d = suites.setdefault(s, {"passed": 0, "failed": 0, "total": 0})
        d["total"] += 1
        d[r["outcome"]] += 1
    total = len(_COLLECTED)
    passed = sum(1 for r in _COLLECTED if r["outcome"] == "passed")
    failed = sum(1 for r in _COLLECTED if r["outcome"] == "failed")
    generate_report(total, passed, failed, suites, _COLLECTED, "output/report.html")
