# 02｜论文精读：设计目标与核心思想

> 更新：2026-10-22。源码基线：[`c1b42cd`](https://github.com/ucb-bar/constellation/tree/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510)。本文按原定章节顺序展开；源码节选、教学示例与实验计划分别标明。运行版本、工具链及本次四项代表性验证见[实验复现附录](appendix-reproduction.md)；教学示意与未执行的扩展实验另行标明。

## 1. 带着三个问题读论文

论文 [Constellation: An Open-Source SoC-Capable NoC Generator](https://doi.org/10.1109/NoCArc57472.2022.9911299) 提供了专栏的设计背景。本章按“设计目标—工程对应—适用边界”整理阅读线索；不转述未经本次复现的论文性能数字。项目的功能范围以固定版本 README 和源码为依据。

首先问：为何面向 SoC，而不只面向规则多核阵列？异构模块的物理位置、端口数和带宽不均匀，协议又有多种消息类型。其次问：如何把一个抽象路由算法变为可综合电路？第三问：网络路由无环以后，协议是否仍可能互相等待？这三个问题分别引向 topology、路由编译和 virtual subnetwork。

## 2. 将设计目标落实到源码

| 学习线索 | 固定版本中的落点 | 要核对的约束 |
| --- | --- | --- |
| 不规则和层次化网络 | `PhysicalTopology`、`HierarchicalTopology` | 有向连通、节点编号 |
| 解耦描述 | `NoCParams` | topology、flow、routing 的一致性 |
| 路由验证与编译 | `InternalNoCParams`、`RouteComputer` | 可达性、escape 依赖、译码输入 |
| 协议无关传输 | `ProtocolNoC`、TileLink / AXI4 adapter | 消息依赖、顺序、ID |
| 可配置微架构 | `UserRouterParams`、`UserChannelParams` | 时序、存储、credit 往返 |

解耦的收益在于能复用，但不是消除约束。相同 topology 下，flow 集不同会改变实际可遍历资源；相同路由规则下，VC 数和协议依赖不匹配也会使构建失败。

## 3. 用类型判断“描述”与“硬件”

以下为固定版本的源码节选，省略外围上下文：[查看 src/main/scala/noc/Parameters.scala 第 15–31 行](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/noc/Parameters.scala#L15-L31)。

```scala
case class NoCParams(
  // Physical specifications
  topology: PhysicalTopology = UnidirectionalLine(1),
  channelParamGen: (Int, Int) => UserChannelParams = (_, _) => UserChannelParams(),
  ingresses: Seq[UserIngressParams] = Nil,
  egresses: Seq[UserEgressParams] = Nil,
  routerParams: Int => UserRouterParams = (i: Int) => UserRouterParams(),

  // Flow specification
  // (blocker, blockee) => bool
  // If true, then blocker must be able to proceed when blockee is blocked
  vNetBlocking: (Int, Int) => Boolean = (_, _) => true,
  flows: Seq[FlowParams] = Nil,

  // Routing specification
  routingRelation: PhysicalTopology => RoutingRelation = AllLegalRouting(),

```

这段 `case class` 的字段是 Scala 值和函数：`Int`、`Boolean`、`Seq` 与 `PhysicalTopology => RoutingRelation` 都在 elaboration 期间使用。它们没有时钟；只有后续 `Module`、`Reg`、`Wire` 等 Chisel 构造才描述硬件。参数化 NoC 的关键是先计算合法结构，再生成所需电路。

阅读时可以在纸上标两个颜色：Scala 求值负责“建立哪些实例和连接”；Chisel 信号负责“芯片运行时每拍做什么”。这种区分比逐行翻译语法更有帮助。

## 4. 不要把验证范围扩展成万能保证

源码中的静态检查基于已声明 flow、routing relation 与 escape 资源，不能代替终端消费约束、仲裁公平性、CDC 正确性或协议回归。有限次数随机测试也不是无死锁的数学证明。后续应同时保留结构检查、功能仿真与性能评估三个证据层次。

练习：选择一个目标，例如“给 DMA 加一条捷径”，列出需要变化的参数、应当重新执行的检查，以及什么证据才能说明它有价值。若只是低负载少了一跳，还不能推出满负载更好。

## 源码与延伸阅读

以下链接均固定到本章使用的源码版本：

- [README.md](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/README.md)
- [src/main/scala/noc/Parameters.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/noc/Parameters.scala)
- [src/main/scala/router/RouteComputer.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/router/RouteComputer.scala)

源码节选版权归 The Regents of the University of California，遵循 [BSD-3-Clause 许可及免责声明](/notes/constellation-notes/source-license.txt)。文字解读与教学图为专栏整理内容。

---

[上一篇](01-why-constellation.md) · [专栏导读](00-series-guide.md)

[下一篇：03｜Constellation 整体架构](03-constellation-architecture.md)
