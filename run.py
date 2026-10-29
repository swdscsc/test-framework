# -*- coding: utf-8 -*-
"""一键运行：启动被测服务 -> 执行 pytest 自动化套件 -> 自动生成 HTML 报告。"""
import threading
import time
import sys

import pytest
from demo_app import run_server


def main():
    srv = threading.Thread(target=run_server, daemon=True)
    srv.start()
    time.sleep(1.0)  # 等待服务就绪
    rc = pytest.main(["-q", "--junitxml=output/junit.xml", "tests/"])
    print(f"\npytest 退出码: {rc}  (报告已生成 -> output/report.html)")
    return rc


if __name__ == "__main__":
    sys.exit(main())
