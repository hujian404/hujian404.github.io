# 23｜VC、Buffer 与 Flow Control 实验

> 更新：2026-10-22。源码基线：[`c1b42cd`](https://github.com/ucb-bar/constellation/tree/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510)。本文按原定章节顺序展开；源码节选、教学示例与实验计划分别标明。运行版本、工具链及本次四项代表性验证见[实验复现附录](appendix-reproduction.md)；教学示意与未执行的扩展实验另行标明。

## 1. 先把“更多 VC”和“更多存储”分离

增加 VC 数会增加独立报文上下文、仲裁候选和可能的隔离能力；增加单 VC 深度主要增加在途 flit 容量和覆盖 credit 往返的空间。二者都可能改善性能，但对应机制不同。

采用第 20 章的 2×8、4×4、4×8 三组。前两组总逻辑槽位相同，可用于分析切分方式；第三组用于分析容量增加。比较仍需报告控制成本与 pipeline 时序，不能把相同 payload 槽数称为完全同面积。

## 2. Buffer 实现也会随条件变化

以下为固定版本的源码节选，省略外围上下文：[查看 src/main/scala/router/InputUnit.scala 第 72–76 行](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/router/InputUnit.scala#L72-L76)。

```scala
  // Ugly case. Use multiple queues
  if ((cParam.srcSpeedup > 1 || cParam.destSpeedup > 1 || fullSize <= 1) || !cParam.unifiedBuffer) {
    require(useOutputQueues)
    val qs = cParam.virtualChannelParams.map(v => Module(new Queue(new BaseFlit(cParam.payloadBits), v.bufferSize)))
    qs.zipWithIndex.foreach { case (q,i) =>
```

InputBuffer 在特定 speedup、小容量或 `unifiedBuffer=false` 时采用每 VC Queue；另一分支使用 Mem、指针和输出队列。改变参数可能跨越实现分支，因此性能变化未必只来自“多了一个槽”。`Module(new Queue(...))` 创建硬件队列，`map` 按 VC 展开实例，`<>` 连接握手。

采用 unifiedBuffer 时还需看 delims / starts / ends。该实现按 VC 建立区段，不能直接宣称启用它就实现了无约束的动态共享 buffer。

## 3. 四种负载用于区分机制

| 负载 | 主要观察 |
| --- | --- |
| 单 flow 低负载 | 流水线与序列化基础时延 |
| 单 flow 持续发送 | credit 往返与槽位深度 |
| 多输入共享输出 | 仲裁与输出带宽上限 |
| 一个目标持续阻塞、其他目标可用 | HOL 阻塞和 VC 隔离效果 |

若所有 flow 都争同一个单 lane 输出，增加 VC 不会突破该输出的物理速率上限。若 depth 已覆盖 credit 周期，再加深也可能只增加拥塞下的积压。

## 4. 正确性先于吞吐

检查每个 VC credit 在合法范围内、返回不重复、reset 容量一致、所有 flit 最终只接收一次。故意让 egress 阻塞后恢复，核对 tail 释放与后续 head 进展。如果改了链路回传延迟，应重新确定覆盖其往返所需的深度。

练习：写下“更多 VC 降低特定阻塞传播”的假设，并用每流 latency、VA stall、SA stall、credit stall 和输出利用率区分原因。若只得到整体平均值下降，证据还不足以说明具体改善机制。这里给出的是实验计划，没有新增测量数据。

## 源码与延伸阅读

以下链接均固定到本章使用的源码版本：

- [src/main/scala/router/InputUnit.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/router/InputUnit.scala)
- [src/main/scala/router/OutputUnit.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/router/OutputUnit.scala)
- [src/main/scala/channel/Parameters.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/channel/Parameters.scala)

源码节选版权归 The Regents of the University of California，遵循 [BSD-3-Clause 许可及免责声明](/notes/constellation-notes/source-license.txt)。文字解读与教学图为专栏整理内容。

---

[上一篇](22-custom-routing.md) · [专栏导读](00-series-guide.md)

[下一篇：24｜Router Microarchitecture 优化](24-router-microarchitecture-optimization.md)
