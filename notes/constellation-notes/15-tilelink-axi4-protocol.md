# 15｜TileLink / AXI4 协议支持

> 更新：2026-10-22。源码基线：[`c1b42cd`](https://github.com/ucb-bar/constellation/tree/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510)。本文按原定章节顺序展开；源码节选、教学示例与实验计划分别标明。运行版本、工具链及本次四项代表性验证见[实验复现附录](appendix-reproduction.md)；教学示意与未执行的扩展实验另行标明。

## 1. 从 flit 网络到协议传输层

核心 NoC 负责传输报文，不直接理解 CPU load/store 的完整协议语义。TileLink 和 AXI4 adapter 负责把协议通道编码成 packet，并在另一端恢复，同时保留地址、事务标识、数据、控制和顺序要求。

对于 TileLink，应先区分 A / D 请求响应与支持一致性时的 B / C / E 通道；AXI4 则有 AR / R 与 AW / W / B。实际生成哪些类别由端点能力决定，不能把所有配置都强行当成相同通道数。

## 2. 协议配置怎样重写基础 NoC

以下为固定版本的源码节选，省略外围上下文：[查看 src/main/scala/protocol/Protocol.scala 第 85–94 行](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/protocol/Protocol.scala#L85-L94)。

```scala
  val ingressOffsets  = protocolParams.map(_.ingressNodes.size).scanLeft(0)(_+_)
  val egressOffsets   = protocolParams.map(_.egressNodes.size).scanLeft(0)(_+_)
  val vNetOffsets     = protocolParams.map(_.nVirtualNetworks).scanLeft(0)(_+_)

  val nocParams = params.nocParams.copy(
    ingresses = protocolParams.map(_.ingressNodes).flatten.map(i =>
      UserIngressParams(i, payloadBits=terminalPayloadWidth)),
    egresses = protocolParams.map(_.egressNodes).flatten.map(i =>
      UserEgressParams(i, payloadBits=terminalPayloadWidth)),
    routerParams = (i) => params.nocParams.routerParams(i).copy(payloadBits=nocPayloadWidth),
```

`ProtocolNoC` 对多个 protocol 计算 ingress、egress、vNet 的累计 offset，并用 `nocParams.copy(...)` 重新生成终端与 flow。`scanLeft(0)(_+_)` 是 Scala 前缀和：例如两个协议分别有 2、3 个入口，offset 为 0、2、5，第二组入口的全局下标从 2 开始。

因此不能仅看传入的基础 `NoCParams.flows` 就断言最终协议网络支持哪些通信；要看 adapter 最后生成的规格。widthDivision 还会影响网络 payload 宽度、终端宽度和串并转换，须联合看 `WidthWidget.scala`。

## 3. 协议依赖如何进入 vNet

`ProtocolParams` 提供 `nVirtualNetworks`、`vNetBlocking` 与 flows。Tilelink.scala 和 AXI4.scala 在各自参数中定义阻塞关系；不要仅凭 vNet 编号猜某一类消息的优先级。应先在 adapter 找到消息到 vNet / terminal 的映射，再验证第 8 章的前进性契约。

路由无死锁与协议顺序是两类约束。例如 AXI 事务 ID、读写返回及写地址 / 写数据配对不能被 generic packet 传输随意改变；TileLink source / sink 和 coherence 消息也有各自生命周期。普通 NoC 数据正确测试不会覆盖全部协议约束。

## 4. 源码阅读和验证顺序

先读 Protocol.scala 的公共接口，再读 Tilelink.scala / AXI4.scala 的端点映射与 packet 格式，最后看 TLTestHarness / AXI4TestHarness 的产生器和检查器。Chisel `MixedVec(protocolParams.map(_.genIO()))` 说明不同协议 IO 可以在同一模块中具有不同类型；这不是在一个均匀 Vec 中运行时切换类型。

练习：手工展开两个协议实例的 terminal / vNet offset；再选择一次读事务，从协议输入握手开始，跟踪打包、注入、egress 和返回完成。增加 backpressure、多 outstanding、不同 ID、长 packet，验证数据、去重和允许的顺序。本轮已通过 `NoCTestTL00` 与 `NoCTestAXI400` 两项代表性验证；这不等于新增用例或全部协议回归均已执行。

## 源码与延伸阅读

以下链接均固定到本章使用的源码版本：

- [src/main/scala/protocol/Protocol.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/protocol/Protocol.scala)
- [src/main/scala/protocol/Tilelink.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/protocol/Tilelink.scala)
- [src/main/scala/protocol/AXI4.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/protocol/AXI4.scala)
- [src/main/scala/test/TLTestHarness.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/test/TLTestHarness.scala)
- [src/main/scala/test/AXI4TestHarness.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/test/AXI4TestHarness.scala)

源码节选版权归 The Regents of the University of California，遵循 [BSD-3-Clause 许可及免责声明](/notes/constellation-notes/source-license.txt)。文字解读与教学图为专栏整理内容。

---

[上一篇](14-vc-allocation-arbitration-pipeline.md) · [专栏导读](00-series-guide.md)

[下一篇：16｜Chipyard / RocketChip 集成](16-chipyard-integration.md)
