# 09｜Routing Relation 与 Routing Table

> 更新：2026-10-22。源码基线：[`c1b42cd`](https://github.com/ucb-bar/constellation/tree/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510)。本文按原定章节顺序展开；源码节选、教学示例与实验计划分别标明。运行版本、工具链及本次四项代表性验证见[实验复现附录](appendix-reproduction.md)；教学示意与未执行的扩展实验另行标明。

## 1. 路由关系判定一次合法资源转移

`RoutingRelation.rel(srcC,nxtC,flow): Boolean` 接收当前 channel、候选下一 channel 和通信信息。返回 true 表示该 flow 可以从当前 VC 申请下一 VC。它输出合法候选集合，最终选择还要经过资源状态与仲裁。

以下为固定版本的源码节选，省略外围上下文：[查看 src/main/scala/routing/RoutingRelations.scala 第 22–29 行](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/routing/RoutingRelations.scala#L22-L29)。

```scala
abstract class RoutingRelation(topo: PhysicalTopology) {
  // Child classes must implement these
  def rel       (srcC: ChannelRoutingInfo,
                 nxtC: ChannelRoutingInfo,
                 flow: FlowRoutingInfo): Boolean

  def isEscape  (c: ChannelRoutingInfo,
                 vNetId: Int): Boolean = true
```

`ChannelRoutingInfo` 用 `(src,dst,vc,n_vc)` 标识一个逻辑 channel。`RoutingRelation.apply` 还要求 `srcC.dst==nxtC.src`，保证两段连接相接，并用 Scala HashMap 缓存判定结果。它不是在 RTL 中实例化 HashMap。

## 2. 跟一个三节点例子手算

单向链 `0→1→2` 加上 `0→2` 捷径，flow 的目标节点为 1。`UnidirectionalLineRouting` 判断 `nxtC.dst<=flow.egressNode`，所以允许 0→1，不允许直接跨到 2。若目标是 2，两条前向选择都可能合法。

这解释了为何 routing relation 需要当前 channel 与 flow，而不只是目标地址；涉及 dateline、转向限制、escape VC 时，已有路径所在的 VC 类别也会影响下一步。

## 3. 从 Scala 判定到 Chisel 译码

`RouteComputer.scala` 枚举某输入可能承载的 flow 和 VC，再对每个输出 VC 调用 relation，得到由 0/1 组成的 mask。随后构造 `TruthTable`，用 `decoder(addr,truthTable)` 生成硬件译码。结果被拆回 `resp.vc_sel(output)(vc)`。

这里有三种不同的数据：Scala `Boolean` 是生成时的可达性；Scala `String` 保存真值表文本；Chisel `UInt` / `Bool` 是运行时的地址和候选信号。路由算法的复杂 Scala 控制流不会原样作为软件在芯片上运行。

## 4. 到达目的节点与非法输入

该实现把到达目的物理节点的包导向对应 egress；不能直接将 relation 改成 deflection routing 并假定端点可以继续转发。另一个边界是 `TruthTable` 对未列入的项可能使用 don't-care，因此运行时必须遵守已声明 flow / 编码约束，不能依赖默认项替自己报告非法流量。

路由表增大也可能增加译码面积、生成时间和关键路径。减少 flow 数不是无条件优化：必须先保证真实协议通信没有被遗漏。

## 5. 阅读和验证练习

手列一个输入、两个候选输出、各两个 VC 的四位 mask，分别对目标 1 和目标 2 求值。再在 RouteComputer 中核对 table 行如何形成以及 `Reverse` 后位序如何分配。修改 relation 后先运行结构检查，再做报文和顺序检查，最后评估性能。不能用“找到了最短路径”替代无死锁检查。

## 源码与延伸阅读

以下链接均固定到本章使用的源码版本：

- [src/main/scala/routing/RoutingRelations.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/routing/RoutingRelations.scala)
- [src/main/scala/routing/Types.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/routing/Types.scala)
- [src/main/scala/router/RouteComputer.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/router/RouteComputer.scala)

源码节选版权归 The Regents of the University of California，遵循 [BSD-3-Clause 许可及免责声明](/notes/constellation-notes/source-license.txt)。文字解读与教学图为专栏整理内容。

---

[上一篇](08-flow-virtual-subnetwork.md) · [专栏导读](00-series-guide.md)

[下一篇：10｜从 Scala Configuration 到 Verilog RTL](10-configuration-to-rtl.md)
