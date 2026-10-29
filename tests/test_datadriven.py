# -*- coding: utf-8 -*-
"""数据驱动测试：从 framework/data/cases.json 读取场景矩阵，单用例覆盖多分支。"""
import json, os
import pytest
from framework.client import ApiClient

_HERE = os.path.dirname(__file__)
with open(os.path.join(_HERE, "..", "framework", "data", "cases.json"),
          encoding="utf-8") as _f:
    CASES = json.load(_f)


@pytest.fixture(scope="module")
def client():
    return ApiClient()


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_scenario(client, case):
    t, p, expect = case["type"], case["payload"], case["expect"]
    if t == "login":
        r = client.login(p.get("username"), p.get("password"))
    elif t == "create_order":
        r = client.create_order(p.get("user_id"), p.get("item", ""), p.get("qty", 0))
    elif t == "get_user":
        r = client.get_user(p["id"])
    else:
        pytest.fail(f"unknown scenario type: {t}")
    assert r.status_code == expect, f"期望 {expect}，实际 {r.status_code}"
