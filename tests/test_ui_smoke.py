# -*- coding: utf-8 -*-
"""页面级冒烟测试：无需浏览器，直接校验返回 HTML 含关键元素。"""
import pytest
from framework.client import ApiClient


@pytest.fixture(scope="module")
def client():
    return ApiClient()


def test_homepage_loads(client):
    r = client.get_page("/")
    assert r.status_code == 200
    html = r.text.lower()
    assert "<form" in html
    assert "username" in html
    assert "password" in html
