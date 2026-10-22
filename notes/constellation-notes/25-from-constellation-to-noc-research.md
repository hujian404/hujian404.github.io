# 25｜从 Constellation 到自己的 NoC 研究

> 更新：2026-10-22。源码基线：[`c1b42cd`](https://github.com/ucb-bar/constellation/tree/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510)。本文按原定章节顺序展开；源码节选、教学示例与实验计划分别标明。运行版本、工具链及本次四项代表性验证见[实验复现附录](appendix-reproduction.md)；教学示意与未执行的扩展实验另行标明。

## 1. 把学习主线变成可检验的研究问题

到这里应能沿 `NoCParams → InternalNoCParams → NoC → Router → RTL → harness → statistics` 追踪一个决定怎样改变电路与实验。研究问题应进一步明确目标 workload、比较约束和机制假设，而不只是“做一个更好的 NoC”。

例如：在相同总 buffer 容量下，面向局部加速器流量的不规则捷径能否降低某类流的尾延迟？需要固定 endpoint mapping、路由合法性、消息依赖、负载和物理频率假设，还应检查其他 flow 是否为此付出代价。

## 2. 三条可从现有代码出发的路线

| 方向 | 修改入口 | 首要反例 |
| --- | --- | --- |
| 应用感知 topology | CustomTopology、channelParamGen | 捷径长线、热点转移 |
| 路由与子网资源 | RoutingRelation、vNetBlocking | escape / 协议前进性破坏 |
| Router 资源分配 | vcAllocator、InputBuffer、pipeline | 公平性、关键路径与 credit 错误 |

每条路线都先建立未修改的 baseline，完成最小复现，再改变一个机制。功能失败的设计不能进入性能胜负比较。

## 3. 研究记录应足以重建一次实验

```text
experiment/
  manifest.json       # 所有依赖 SHA、工具版本、seed、设计/运行参数
  config/             # NoC 配置、noceval.cfg、端点与 flow 映射
  logs/               # 完整命令、stdout、失败原因
  results/            # 原始计数、窗口、单位、派生指标
  figures/            # 绘图脚本与图，标明数据来源
  checks/             # 结构检查、功能回归、综合与时序报告
```

该目录是建议，不是本仓库已经完成的一组实验。源数据与派生数据应区分；失败、超时和无法 drain 的点也应保留。多 seed 分析必须真正改变随机源，上游固定 seed 的重复运行并不是独立样本。

## 4. 用源码事件约束结论

以下为固定版本的源码节选，省略外围上下文：[查看 src/main/resources/csrc/TrafficEval.cpp 第 395–397 行](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/resources/csrc/TrafficEval.cpp#L395-L397)。

```cpp
    this->latencies_by_flow[ingress_id][egress_id][latency]++;
    this->latencies[latency]++;
  }
```

收到一个 flit 只是统计事件；若要得出应用完成时间或系统能耗结论，还需要更高层模型。即使网络延迟改善，也可能被 adapter 排队、memory 服务或频率下降抵消。每个图表标题应说明单位、样本、窗口和是否为仿真 / 综合结果。

研究叙述可按“观察到的瓶颈—机制假设—代码改动—正确性证据—控制变量实验—适用边界”展开。能清楚解释为什么某个反例没有收益，往往比只列出最佳点更有价值。

## 5. 学习完成度自查

尝试不看目录回答：flow ID 与 router ID 有何区别？为什么 route relation 是 Boolean 而响应是 Bool 向量？credit 与 occupied 分别表示什么？vNet 标签为何不自动提供资源隔离？减少一拍为何可能变慢？当前评估器 latency 的起始点在哪里？

若能用源码、图与一个最小波形回答这些问题，就具备继续修改生成器的基础。本轮已完成学习正文、源码核对，并在现有实验 fork 环境通过四项代表性验证；饱和性能曲线、实际捕获波形和新微架构结论仍需按实验设计补充。

## 源码与延伸阅读

以下链接均固定到本章使用的源码版本：

- [src/main/resources/csrc/TrafficEval.cpp](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/resources/csrc/TrafficEval.cpp)
- [src/main/scala/noc/Parameters.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/noc/Parameters.scala)
- [src/main/scala/test/CustomConfigs.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/test/CustomConfigs.scala)
- [src/main/scala/router/Router.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/router/Router.scala)

源码节选版权归 The Regents of the University of California，遵循 [BSD-3-Clause 许可及免责声明](/notes/constellation-notes/source-license.txt)。文字解读与教学图为专栏整理内容。

---

[上一篇](24-router-microarchitecture-optimization.md) · [专栏导读](00-series-guide.md)

[返回专栏目录](/constellation-series.html)
