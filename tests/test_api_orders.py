# -*- coding: utf-8 -*-
"""订单接口测试：创建 / 更新 / 删除全流程 + 参数校验分支。"""
import pytest
from framework.client import ApiClient


@pytest.fixture(scope="module")
def client():
    return ApiClient()


def test_create_order_success(client):
    r = client.create_order(user_id=1, item="Keyboard", qty=2)
    assert r.status_code == 201
    body = r.json()
    assert body["id"]
    assert body["status"] == "created"


def test_create_order_unknown_user(client):
    r = client.create_order(user_id=99999, item="Mouse", qty=1)
    assert r.status_code == 404


def test_create_order_qty_nonpositive(client):
    r = client.create_order(user_id=1, item="Mouse", qty=0)
    assert r.status_code == 400


def test_create_order_empty_item(client):
    r = client.create_order(user_id=1, item="", qty=1)
    assert r.status_code == 400


def test_update_order_status(client):
    created = client.create_order(user_id=1, item="Cable", qty=5)
    oid = created.json()["id"]
    r = client.update_order(oid, status="shipped")
    assert r.status_code == 200
    assert r.json()["status"] == "shipped"


def test_update_order_not_found(client):
    r = client.update_order(99999, status="shipped")
    assert r.status_code == 404


def test_delete_order_flow(client):
    created = client.create_order(user_id=1, item="Pad", qty=1)
    oid = created.json()["id"]
    r = client.delete_order(oid)
    assert r.status_code == 200
    assert client.get_order(oid).status_code == 404
