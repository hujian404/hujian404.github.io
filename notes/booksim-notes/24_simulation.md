# Chapter 24｜Simulation

> 原书：William J. Dally、Brian Towles，*Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004），第 24 章，印刷页 473–494。本地参考 PDF 的页序为印刷页 +27。以下为中文学习整理，保留原书全部目录小节的编号与标题，不是逐句翻译。BookSim2 对照版本固定为 [`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

[专栏导读](00_Introduction.md) · [原书目录与页码对照](appendix-reading-map.md)

## 24.1 Levels of Detail

*原书印刷页 473。*

抽象层次决定可以回答的问题：解析/事务/packet/flit/周期/电路级各有成本。BookSim2 是性能模拟器，适于研究配置下的网络行为，不生成可综合 RTL，也不直接证明时序收敛或功耗。

## 24.2 Network Workloads

*原书印刷页 475。*

workload 既包含源宿选择，也包含到达过程、包长和因果依赖。只配置 uniform 不足以完整定义实验。

### 24.2.1 Application-Driven Workloads

*原书印刷页 475。*

application-driven 来自执行或 trace，保留真实程序的部分结构，但 trace 重放是否反馈网络延迟会改变闭环行为。

### 24.2.2 Synthetic Workloads

*原书印刷页 476。*

synthetic 便于控制均匀、置换、热点和突发，适合隔离机制；应覆盖能暴露目标算法弱点的模式。

## 24.3 Simulation Measurements

*原书印刷页 478。*

统计方法需与研究问题配套：先排除初始化偏差，再收集足够的稳态样本，最后估计不确定性。一次短跑不能支持普遍结论。

### 24.3.1 Simulator Warm-Up

*原书印刷页 479。*

warm-up 让队列和利用率离开全空初态。高负载时所需时间可能更长，应观察时间序列而不是机械复用同一拍数。

### 24.3.2 Steady-State Sampling

*原书印刷页 481。*

steady-state sampling 需检查均值、吞吐及队列趋势。达到 max_samples 只是一个结束条件，不自动等于统计收敛。

### 24.3.3 Confidence Intervals

*原书印刷页 482。*

网络样本通常有相关性，不能把每个 flit 都当独立样本套置信区间。可采用独立重复和合适批均值，并报告种子与方法。

## 24.4 Simulator Design

*原书印刷页 484。*

simulator design 应保证因果、资源守恒和统计边界一致。执行速度优化必须保持模型的事件顺序。

### 24.4.1 Simulation Approaches

*原书印刷页 485。*

time-stepped 逐周期推进，event-driven 跳到下一事件；二者都必须处理同一时刻的更新语义，不能让后执行节点偷看不该同拍可见的状态。

### 24.4.2 Modeling Source Queues

*原书印刷页 488。*

source queue 保存尚未获准注入的流量。忽略它会让网络看起来 latency 低，却把拥塞推到测量边界以外。

### 24.4.3 Random Number Generation

*原书印刷页 490。*

固定并记录 seed 有助复现；多 seed 用于估计变异。相同 seed 在不同算法中未必产生相同通信事件序列，要核对随机数消费路径。

### 24.4.4 Troubleshooting

*原书印刷页 491。*

从单消息、单流、低负载和守恒计数逐步排查；再检查 VC 依赖、credit 和事件时间。遇到异常退出同时看日志，不能只信 exit code。

## 24.5 Bibliographic Notes

*原书印刷页 491。*

本节对应原书 p. 491 的文献脉络。继续查阅时应回到原书该节和书末 Bibliography，区分最初提出的方法、后续实现与本文使用的 BookSim2 版本。本文末尾源码链接是实现对照，不作为原书历史论述的替代依据。

## 24.6 Exercises

*原书印刷页 492。*

自拟练习（不复制原书习题）：先执行第25章的最小配置并保存 stdout 和退出码，再重复相同 seed 检查可重复性。多seed统计时显式改 seed，不把确定性重跑当成独立样本。保存异常结果和收敛状态，避免在图表中悄悄丢弃过载点。

## BookSim2 源码对照与适用边界

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/trafficmanager.cpp 第 954–961 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.cpp#L954-L961)。

```cpp
void TrafficManager::_Step( )
{
    bool flits_in_flight = false;
    for(int c = 0; c < _classes; ++c) {
        flits_in_flight |= !_total_in_flight_flits[c].empty();
    }
    if(flits_in_flight && (_deadlock_timer++ >= _deadlock_warn_timeout)){
        _deadlock_timer = 0;
```

_Step 推进一个网络周期，先组织接收 / credit，再处理生成和注入，以及网络对象的周期操作。读取时沿实际函数完整跟踪，不要把主循环里的一个 C++ statement 当成硬件的一个 stage。Run 管理仿真重复与结束，BatchTrafficManager 又具有不同的测量目标。

运行方法、工具链版本、退出码解释和现有 smoke 数据统一见[补充实验](appendix-simulation-results.md)。`max_samples` 触发结束与统计意义的收敛不同，复现实验必须同时保留配置、日志和判定规则。

## 来源与继续阅读

- 原书第 24 章，pp. 473–494；各节页码已逐项列出。案例与原书公式均以本地参考书为依据。
- [BookSim2 固定版本源码](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)，节选保留[上游许可](/notes/booksim-notes/source-license.txt)。
- [全书章节/源码路线与图片来源](appendix-reading-map.md)。新增图均附 `.drawio` 源文件，插图是结构说明，不是测量波形。

[上一篇](23_performance_analysis.md) · [下一篇](25_simulation_examples.md) · [专栏目录](/booksim-series.html)
