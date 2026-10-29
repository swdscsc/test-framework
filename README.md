# 自动化测试框架（Software Testing Automation Framework）

> 面向校招测试开发 / 软件测试岗的实战项目：用 pytest 从零搭建一套**分层、可数据驱动、带自研可视化报告**的自动化测试框架，并配套一个合成被测 REST 服务，覆盖正向与负向断言。

## 为什么做这个项目
目标岗位（OPPO / vivo / 比亚迪 / 宇瞳 等）的软件测试 / 测试开发岗，普遍要求：会写自动化用例、能做接口测试、懂数据驱动、能出报告。本项目把这几项能力用**可运行、可演示、可讲清**的方式落地，面试时能逐句说明框架设计与排障思路。

## 技术栈
- **Python 3.12**（Anaconda）+ pytest 7.x + requests
- 被测服务：`http.server`（标准库，零依赖）模拟用户 / 订单 / 登录 CRUD
- 报告：自研 HTML 插件（内联 SVG 环形图 + 分套件条形 + 用例明细），并导出 JUnit XML 兼容 CI

## 架构
```
test-framework/
├── demo_app.py            # 合成被测 REST 服务（GET/POST/PUT/DELETE + 校验分支）
├── report.py              # 自含 HTML 报告生成（SVG 图表）
├── conftest.py            # pytest 钩子：收集结果 + 会话结束生成报告
├── run.py                 # 一键运行：启服务 → 跑套件 → 出报告
├── framework/
│   ├── config.py          # 环境配置（test/prod 可切，读环境变量）
│   ├── client.py          # API 客户端封装（语义化方法）
│   └── data/cases.json    # 数据驱动场景矩阵
├── tests/
│   ├── test_api_users.py   # 用户接口：正向 + 负向 + 登录矩阵
│   ├── test_api_orders.py  # 订单接口：增改删全流程 + 参数校验
│   ├── test_datadriven.py  # 数据驱动：从 JSON 读取 11 组场景参数化执行
│   └── test_ui_smoke.py    # 页面级冒烟：校验返回 HTML 关键元素
└── output/
    ├── report.html         # 可视化报告（截图可发 HR / 放作品集）
    └── junit.xml           # CI 兼容结果
```

## 测试设计亮点
- **接口自动化**：覆盖 users / orders / login 全链路，含状态码、响应体字段、业务规则断言。
- **数据驱动**：`pytest.mark.parametrize` 读取 `cases.json`，单用例覆盖多分支（合法 / 越权 / 缺参 / 非法参数 / 不存在资源）。
- **负向用例**：显式验证 400 / 401 / 404 等错误分支，体现边界与异常思维。
- **页面冒烟**：无需浏览器，直接校验返回 HTML 含关键表单元素。
- **可视化报告**：会话结束自动生成 HTML 报告（通过率环形图、分套件条形、用例明细表），并导出 JUnit XML 接入 CI。

## 运行方法
```bash
# 一条命令：启动被测服务 + 执行全部用例 + 生成报告
python run.py
# 或分步：
python demo_app.py &          # 启动被测服务（端口 8765）
pytest -q --junitxml=output/junit.xml tests/
```

## 量化结果（固定种子可复现）
| 指标 | 结果 |
|---|---|
| 用例总数 | **26** |
| 通过 | **26** |
| 失败 | **0** |
| 通过率 | **100%** |
| 业务套件 | 4 类（用户 / 订单 / 数据驱动 / 页面冒烟） |
| 参数化场景 | 11 组 |

> 本项目与「工业缺陷视觉检测」「网络入侵检测」共同构成候选人的三个旗舰实战项目，分别补强机器视觉、网络安全、软件测试三条目标岗主线。
