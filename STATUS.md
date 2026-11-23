# Benchmark Demo 交件回执

工单编号 WO-GPT-BENCHMARK-DEMO。交件目录为 Drive 的 `AI-Office/outbox/chatgpt/Benchmark-Demo/`。

## 交件清单

- `README.md` — 英文作品集入口，含运行命令、评分节录、设计说明和限制。
- `challenges/` — 原创编程题 12 道，算法、修 bug、真实小任务各 4 道。各题有题面、类别／难度及 4 个 pytest 用例。
- `solutions/` 和 `mock_submissions/` — 12 个参考解和 5 个带缺陷的 mock 提交。
- `runner.py`、`Dockerfile` — 本地 mock、参考解验证，以及 OpenAI 兼容端点和 Docker 判题路径。
- `report.py`、`reports/report.md`、`reports/report.json` — 报告生成器和本次实跑产生的 mock 评分报告。
- `harness_tests/`、`requirements.txt`、`pytest.ini` — runner 自测及依赖配置。

## 自测结果

| 检查 | 结果 |
| --- | --- |
| `python -m pytest -q` | 12 项通过，覆盖本地 HTTP stub、判题、超时、Docker 参数与报告聚合。 |
| `python runner.py --reference` | 12/12 个参考解通过。 |
| `python runner.py --mock` | 两次逐题判定与评分分组一致，总分均为 7/12（58.3%）。 |
| Mock 分类 | 算法 2/4，修 bug 2/4，真实小任务 3/4。 |

报告标明 **Mock run**，本次分数来自本地合成提交。实测环境为 Windows、Python 3.11.9、pytest 8.4.2。真实模型端点与 Docker 容器联跑未验证，本机缺少 Docker Linux 容器引擎。
