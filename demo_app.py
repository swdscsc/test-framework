# -*- coding: utf-8 -*-
"""合成被测 REST 应用（仅用标准库，无需任何第三方依赖）。
提供 users / orders / login 的 CRUD 与若干校验分支，专供自动化测试做正向 / 负向断言。
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json, re, threading

# ---------------- 内存数据 ----------------
USERS = {
    1: {"id": 1, "username": "alice", "email": "alice@demo.io", "role": "admin"},
    2: {"id": 2, "username": "bob", "email": "bob@demo.io", "role": "user"},
}
CREDENTIALS = {"alice": "secret123", "bob": "hunter2"}
ORDERS = {}
_ORDER_SEQ = [100]
LOCK = threading.Lock()


def _send(handler, code, payload=None):
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    if payload is not None:
        handler.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))


def _body(handler):
    length = int(handler.headers.get("Content-Length", "0") or 0)
    if not length:
        return {}
    try:
        return json.loads(handler.rfile.read(length).decode("utf-8"))
    except Exception:
        return {}


USER_RE = re.compile(r"^/api/users/(\d+)$")
ORDER_RE = re.compile(r"^/api/orders/(\d+)$")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # 静默日志
        pass

    # ---------------- GET ----------------
    def do_GET(self):
        if self.path == "/api/users":
            _send(self, 200, list(USERS.values())); return
        m = USER_RE.match(self.path)
        if m:
            uid = int(m.group(1))
            if uid in USERS:
                _send(self, 200, USERS[uid])
            else:
                _send(self, 404, {"error": "user not found"})
            return
        if self.path == "/api/orders":
            _send(self, 200, list(ORDERS.values())); return
        m = ORDER_RE.match(self.path)
        if m:
            oid = int(m.group(1))
            if oid in ORDERS:
                _send(self, 200, ORDERS[oid])
            else:
                _send(self, 404, {"error": "order not found"})
            return
        if self.path == "/":
            self._serve_page(); return
        _send(self, 404, {"error": "not found"})

    # ---------------- POST ----------------
    def do_POST(self):
        if self.path == "/api/login":
            d = _body(self)
            u, p = d.get("username"), d.get("password")
            if not u or not p:
                _send(self, 400, {"error": "missing field"}); return
            if CREDENTIALS.get(u) == p:
                _send(self, 200, {"token": "tok-" + u, "username": u}); return
            _send(self, 401, {"error": "unauthorized"}); return
        if self.path == "/api/orders":
            d = _body(self)
            uid, item, qty = d.get("user_id"), d.get("item", ""), d.get("qty", 0)
            if uid not in USERS:
                _send(self, 404, {"error": "unknown user"}); return
            if not item or not isinstance(qty, (int, float)) or qty <= 0:
                _send(self, 400, {"error": "invalid order"}); return
            with LOCK:
                oid = _ORDER_SEQ[0]; _ORDER_SEQ[0] += 1
                ORDERS[oid] = {"id": oid, "user_id": uid, "item": item,
                               "qty": qty, "status": "created"}
            _send(self, 201, ORDERS[oid]); return
        _send(self, 404, {"error": "not found"})

    # ---------------- PUT ----------------
    def do_PUT(self):
        m = ORDER_RE.match(self.path)
        if m:
            oid = int(m.group(1))
            if oid not in ORDERS:
                _send(self, 404, {"error": "order not found"}); return
            d = _body(self)
            if d.get("status"):
                ORDERS[oid]["status"] = d["status"]
            _send(self, 200, ORDERS[oid]); return
        _send(self, 404, {"error": "not found"})

    # ---------------- DELETE ----------------
    def do_DELETE(self):
        m = ORDER_RE.match(self.path)
        if m:
            oid = int(m.group(1))
            if oid in ORDERS:
                del ORDERS[oid]
                _send(self, 200, {"deleted": oid}); return
            _send(self, 404, {"error": "order not found"}); return
        _send(self, 404, {"error": "not found"})

    def _serve_page(self):
        html = (
            "<html><head><title>Demo Shop</title></head><body>"
            "<form action=\"/api/login\" method=\"post\">"
            "<input name=\"username\" placeholder=\"username\"/>"
            "<input name=\"password\" type=\"password\" placeholder=\"password\"/>"
            "<button type=\"submit\">Login</button>"
            "</form></body></html>"
        )
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


def run_server(host="127.0.0.1", port=8765):
    server = ThreadingHTTPServer((host, port), Handler)
    server.serve_forever()


if __name__ == "__main__":
    run_server()
