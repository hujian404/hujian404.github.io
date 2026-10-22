# 19｜NoC 性能评价方法

> 更新：2026-10-22。源码基线：[`c1b42cd`](https://github.com/ucb-bar/constellation/tree/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510)。本文按原定章节顺序展开；源码节选、教学示例与实验计划分别标明。运行版本、工具链及本次四项代表性验证见[实验复现附录](appendix-reproduction.md)；教学示意与未执行的扩展实验另行标明。

## 1. 先定义采样事件，再画曲线

offered load 是流量模型期望产生的负载；accepted injection 是入口实际接纳的负载；delivered throughput 是出口实际完成接收的速率。拥塞时这三者可以明显不同。只看接收 / 产生比例，可能把低 offered load 下的 100% 接收误称为很高的带宽。

## 2. 固定版本的 latency 包含入口排队

以下为固定版本的源码节选，省略外围上下文：[查看 src/main/resources/csrc/TrafficEval.cpp 第 392–396 行](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/resources/csrc/TrafficEval.cpp#L392-L396)。

```cpp
    uint64_t latency = current_cycle - f->creation_cycle;
    this->flits_received[ingress_id][egress_id]++;
    this->total_flits_received++;
    this->latencies_by_flow[ingress_id][egress_id][latency]++;
    this->latencies[latency]++;
```

flit 在 `inject_flits_for_packet` 中创建时记录 creation_cycle，并进入 C++ ingress queue；`eject_flits` 用接收周期减 creation_cycle。因此统计是逐 flit 延迟，且包含模型入口队列等待，不是仅从 RTL 接受 head 到 tail 离开之间的 packet latency。

若要测纯网络延迟，需要在真实注入握手时额外记录时间戳。若要测 packet 延迟，要明确 head-to-head、head-to-tail 或 creation-to-tail，并修改统计事件。不能只是把日志中的 median 改名为平均 packet latency。

## 3. 上游 throughput 输出也要核对分母

该版本 TrafficEval.cpp 的报告路径用 `received/sent` 得到每流 throughput，并输出最小 flow 比例。它更接近统计窗口定义下的完成比例，不是直接的 flit/cycle。研究报告应另按统一窗口计算 `delivered_flits / measurement_cycles`，并明确是否包含 drain 接收和 warmup 残留。

| 指标 | 推荐写法 | 必须交代 |
| --- | --- | --- |
| 接收速率 | flit/cycle/port 或全网 flit/cycle | 端口归一化方式 |
| 有效带宽 | payload bit/cycle，必要时换 bit/s | 编码开销与频率 |
| 延迟 | cycles，median / p95 / max 分开 | flit / packet、起止事件 |
| 公平性 | per-flow 速率与最差流 | 不只报告总体平均 |
| 在途量 | 注入−接收 | 是否已 drain |

## 4. Warmup、measurement、drain 要分开

Warmup 用于接近稳态；measurement 定义统计窗口；drain 停止产生新流量并观察在途请求是否完成。必须阅读 TrafficEval.cpp / .h 中对应的边界和计数使能，不能默认三阶段所有统计都采用相同样本集合。无法排空可能来自过载积压、依赖问题或实际错误，需进一步定位。

## 5. 从曲线解释瓶颈

先做低负载基线，再逐步提高 offered load。记录实际入口接纳率、出口速率、延迟和积压；接近饱和时延迟通常上升，但有限窗口不能直接证明长期稳定。用每链路利用率和 VA / SA stall 解释瓶颈，避免仅凭一条总体曲线归因。

练习：手写一份 CSV schema：variant、seed、offered、accepted、delivered、window_cycles、median_flit_latency、max、drained。没有真实数据时保留 schema 和实验步骤，不填看似合理的“测量值”。

## 6. 用本次 Eval03 输出校准指标理解

本次实验 fork 的 Eval03 报告 median=28 cycles、max=225 cycles，最差流 2→6 的 received/sent 比例为 0.97619。上游 max 门槛 210 不满足，fork 改成 250 后满足；硬件时延没有因此降低。

若测量窗口内接收了 warmup 中已经产生的 flit，某些流的 received/sent 还可能超过 1。本次输出确实包含这类比例，说明它不能直接当作物理链路利用率或纯粹的 packet delivery probability。应追踪 `in_measurement` 使能、creation 时刻与接收时刻，而不是只给列标题改名字。证据与限制见[实验复现附录](appendix-reproduction.md)。

## 源码与延伸阅读

以下链接均固定到本章使用的源码版本：

- [src/main/resources/csrc/TrafficEval.cpp](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/resources/csrc/TrafficEval.cpp)
- [src/main/resources/csrc/TrafficEval.h](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/resources/csrc/TrafficEval.h)
- [src/main/scala/test/TrafficEvalHarness.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/test/TrafficEvalHarness.scala)

源码节选版权归 The Regents of the University of California，遵循 [BSD-3-Clause 许可及免责声明](/notes/constellation-notes/source-license.txt)。文字解读与教学图为专栏整理内容。

---

[上一篇](18-netrace-traffic-evaluation.md) · [专栏导读](00-series-guide.md)

[下一篇：20｜实验设计与 Design Space Exploration](20-design-space-exploration.md)
