# -*- coding: utf-8 -*-
"""用户接口测试：正向 + 负向 + 数据驱动登录矩阵。"""
import pytest
from framework.client import ApiClient


@pytest.fixture(scope="module")
def client():
    return ApiClient()


def test_get_users_returns_list(client):
    r = client.get_users()
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 2


def test_get_user_by_id(client):
    r = client.get_user(1)
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == 1
    assert "username" in body


def test_get_user_not_found(client):
    r = client.get_user(99999)
    assert r.status_code == 404


@pytest.mark.parametrize("username,password,expect", [
    ("alice", "secret123", 200),
    ("bob", "hunter2", 200),
    ("alice", "wrong", 401),
    ("ghost", "nope", 401),
])
def test_login_matrix(client, username, password, expect):
    r = client.login(username, password)
    assert r.status_code == expect
    if expect == 200:
        assert "token" in r.json()
