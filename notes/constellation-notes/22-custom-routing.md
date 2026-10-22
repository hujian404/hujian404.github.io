# 22｜自定义 Routing

> 更新：2026-10-22。源码基线：[`c1b42cd`](https://github.com/ucb-bar/constellation/tree/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510)。本文按原定章节顺序展开；源码节选、教学示例与实验计划分别标明。运行版本、工具链及本次四项代表性验证见[实验复现附录](appendix-reproduction.md)；教学示意与未执行的扩展实验另行标明。

## 1. 先写约束，再写 rel

自定义路由的产物是“允许哪些资源转移”的规则，而不是手写一个软件 shortest-path 程序就结束。至少明确可用 topology、VC 类别、flow 目标、转向限制、escape 策略和 fifo 约束。路由应同时满足可达、终止及所需前进性。

## 2. 一个足够小的教学规则

```scala
// 教学示例：仅用于四节点普通双向链，不适用于加回绕边的环
import constellation.routing._
import constellation.topology._
val linePolicy: PhysicalTopology => RoutingRelation = topo => new RoutingRelation(topo) {
  def rel(cur: ChannelRoutingInfo, next: ChannelRoutingInfo,
          flow: FlowRoutingInfo): Boolean = {
    val here = cur.dst
    if (flow.egressNode > here) next.dst == here + 1
    else if (flow.egressNode < here) next.dst == here - 1
    else false // 目的节点的 egress 由终端路径处理
  }
}
```

这段是完整 relation 值的教学写法，需嵌入已有配置并保留足够资源；本次没有编译它。它限定单调前进，因此不能直接移植到任意不规则图。候选 channel 的相接条件由 apply 检查，物理边由 topology 提供。

## 3. 读上游已有规则对照自己的实现

以下为固定版本的源码节选，省略外围上下文：[查看 src/main/scala/routing/RoutingRelations.scala 第 125–131 行](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/routing/RoutingRelations.scala#L125-L131)。

```scala
object BidirectionalLineRouting {
  def apply() = (topo: PhysicalTopology) => new RoutingRelation(topo) {
    def rel(srcC: ChannelRoutingInfo, nxtC: ChannelRoutingInfo, flow: FlowRoutingInfo) = {
      if (nxtC.src < nxtC.dst) flow.egressNode >= nxtC.dst else flow.egressNode <= nxtC.dst
    }
  }
}
```

上游 line relation 使用目标与下一节点的位置关系约束方向。差别在于候选集合与拓扑共同限制路径：不能只看一行不等式就断言它适用于所有图。`getPrio` 可以在合法候选之间提供优先级信息，但不能让非法转移变合法；`isEscape` 也不自动生成 escape 路径。

对更复杂拓扑，可以从 CustomConfigs.scala 中已经组合好的 routing 示例入手，再回到具体实现研究 VC 重编号、dateline 或 escape。避免一开始把 AllLegalRouting 套到有资源环的网络。

## 4. 最小测试矩阵

枚举每个 flow、每个可能当前位置和候选 VC，检查是否会误过目的端、走回头路、进入死端或反复改变 VC 类。然后跑构建检查，补随机竞争与终端阻塞测试，最后才与基线路由比较吞吐。若 flow 声明为 fifo，合法路径不能造成不被支持的多下一节点选择。

练习：把上面规则应用到 0→3 和 3→0，列出依赖资源链；再给 topology 加一条回绕边，看规则是否使用它。这个实验说明“拓扑可连”与“策略可走”是两个不同的设计决定。

## 源码与延伸阅读

以下链接均固定到本章使用的源码版本：

- [src/main/scala/routing/RoutingRelations.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/routing/RoutingRelations.scala)
- [src/main/scala/router/RouteComputer.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/router/RouteComputer.scala)
- [src/main/scala/test/CustomConfigs.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/test/CustomConfigs.scala)

源码节选版权归 The Regents of the University of California，遵循 [BSD-3-Clause 许可及免责声明](/notes/constellation-notes/source-license.txt)。文字解读与教学图为专栏整理内容。

---

[上一篇](21-custom-topology.md) · [专栏导读](00-series-guide.md)

[下一篇：23｜VC、Buffer 与 Flow Control 实验](23-vc-buffer-flow-control-experiments.md)
