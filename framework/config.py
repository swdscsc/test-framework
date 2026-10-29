# -*- coding: utf-8 -*-
"""测试配置：支持环境变量切换测试 / 预发 / 生产环境。"""
import os

BASE_URL = os.environ.get("TEST_BASE_URL", "http://127.0.0.1:8765")
TIMEOUT = float(os.environ.get("TEST_TIMEOUT", "5"))
ENV = os.environ.get("TEST_ENV", "test")
