# -*- coding: utf-8 -*-
"""API 客户端封装：统一 base url、语义化方法。
不使用 requests.Session，每次新建连接，规避与本机 http.server 的 keep-alive 复用抖动。
"""
import requests
from framework.config import BASE_URL, TIMEOUT


class ApiClient:
    def __init__(self, base=BASE_URL):
        self.base = base.rstrip("/")

    def get_users(self):
        return requests.get(f"{self.base}/api/users", timeout=TIMEOUT)

    def get_user(self, uid):
        return requests.get(f"{self.base}/api/users/{uid}", timeout=TIMEOUT)

    def login(self, username, password):
        return requests.post(f"{self.base}/api/login",
                             json={"username": username, "password": password},
                             timeout=TIMEOUT)

    def create_order(self, user_id, item, qty):
        return requests.post(f"{self.base}/api/orders",
                             json={"user_id": user_id, "item": item, "qty": qty},
                             timeout=TIMEOUT)

    def update_order(self, oid, status):
        return requests.put(f"{self.base}/api/orders/{oid}",
                            json={"status": status}, timeout=TIMEOUT)

    def delete_order(self, oid):
        return requests.delete(f"{self.base}/api/orders/{oid}", timeout=TIMEOUT)

    def get_order(self, oid):
        return requests.get(f"{self.base}/api/orders/{oid}", timeout=TIMEOUT)

    def get_page(self, path="/"):
        return requests.get(f"{self.base}{path}", timeout=TIMEOUT)
