# Chapter 25｜Simulation Examples

> 原书：William J. Dally、Brian Towles，*Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004），第 25 章，印刷页 495–510。本地参考 PDF 的页序为印刷页 +27。以下为中文学习整理，保留原书全部目录小节的编号与标题，不是逐句翻译。BookSim2 对照版本固定为 [`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

[专栏导读](00_Introduction.md) · [原书目录与页码对照](appendix-reading-map.md)

## 25.1 Routing

*原书印刷页 495。*

原书先用仿真比较路由的 latency 和 throughput distribution，而不是给一份通用 smoke 配置。复读图表应记录拓扑、路由、traffic、资源和测量边界；相同算法在不同模式下会有不同排序。

### 25.1.1 Latency

*原书印刷页 496。*

比较零负载基线与随负载增长的排队开销。非最短路由可能低负载更慢却高负载更稳，因此不能只抽曲线上的一个点下结论。

### 25.1.2 Throughput Distributions

*原书印刷页 499。*

吞吐分布揭示算法在多种通信模式中的鲁棒性；均匀流量的一个峰值不能代替最坏模式和分布尾部。重新实验时应保存每种模式的结果而非只存总平均。

## 25.2 Flow Control Performance

*原书印刷页 500。*

本节按 VC、规模、注入过程、优先策略和稳定性依次控制变量。原书曲线属于其当时模型和参数，当前 BookSim2 实验应作为重新建模，不能声称逐值复现。

| 控制变量 | 应固定或额外报告 | 本专栏状态 |
|---|---|---|
| VC 数 | 总缓冲 / 每 VC 深度两种口径 | 后续对照方案，未声称测量 |
| 规模 | 终端数、总/每节点负载、链路延迟 | 后续对照方案 |
| 注入过程 | 平均速率、突发、包长、seed | 现有 smoke 只覆盖固定配置 |
| 优先策略 | 服务单位、分类吞吐和等待 | 后续对照方案 |
| 稳定性 | 长期积压、时间序列、重复实验 | 短 smoke 不证明稳态 |

已执行的 2×2 Mesh 校验见[补充实验与实际结果](appendix-simulation-results.md)，其用途是验证构建、配置与统计口径；它不是本章原书曲线的重现。

### 25.2.1 Virtual Channels

*原书印刷页 500。*

增加 VC 既可能减少队头阻塞，也改变缓冲总量。比较时分别设计“固定每 VC 深度”和“固定总 flit 容量”两组实验，区分机制与额外资源。

### 25.2.2 Network Size

*原书印刷页 502。*

增大网络改变路径长度、总资源与 traffic 空间。需要声明保持每节点负载还是保持全系统总流量，否则规模效应难以解释。

### 25.2.3 Injection Processes

*原书印刷页 503。*

Bernoulli、突发和相关注入即使平均速率相同，也可能产生不同队列尾部。应保持包长分布一致，并明确到达过程参数。

### 25.2.4 Prioritization

*原书印刷页 505。*

优先策略改变哪些消息先完成，可能改善某类延迟而恶化另一类。必须同时观察各类吞吐、源队列与低优先级饥饿。

### 25.2.5 Stability

*原书印刷页 507。*

系统稳定意味着长期队列与交付过程能维持受控状态，短时间完成和打印平均值都不足以证明稳定。对疑似饱和点延长运行、看积压趋势并做独立重复。

## 25.3 Fault Tolerance

*原书印刷页 508。*

故障实验应指定位置、模式、恢复协议和成功判据。固定版本 BookSim2 的常规 IQRouter/Channel 路径没有自动提供 CRC、ARQ 和物理 BER 模型；本专栏现有无故障 smoke 不构成原书故障容错实验复现。

## BookSim2 源码对照与适用边界

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/trafficmanager.cpp 第 209–212 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.cpp#L209-L212)。

```cpp
    if(config.GetInt("injection_rate_uses_flits")) {
        for(int c = 0; c < _classes; ++c)
            _load[c] /= _GetAveragePacketSize(c);
    }
```

_load 除以平均 packet size 后交给注入过程。保持 flit 负载不变、改 packet_size，会同时改变 packet 生成频率和序列化；保持 packet/cycle 不变则改变总 flit 需求。两类对照实验回答不同问题，不能混在一张横轴不明的图里。

## 来源与继续阅读

- 原书第 25 章，pp. 495–510；各节页码已逐项列出。案例与原书公式均以本地参考书为依据。
- [BookSim2 固定版本源码](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)，节选保留[上游许可](/notes/booksim-notes/source-license.txt)。
- [全书章节/源码路线与图片来源](appendix-reading-map.md)。新增图均附 `.drawio` 源文件，插图是结构说明，不是测量波形。

[上一篇](24_simulation.md) · [下一篇](appendix-simulation-results.md) · [专栏目录](/booksim-series.html)
