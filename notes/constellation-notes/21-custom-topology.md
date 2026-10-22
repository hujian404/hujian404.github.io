# 21｜自定义 Topology

> 更新：2026-10-22。源码基线：[`c1b42cd`](https://github.com/ucb-bar/constellation/tree/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510)。本文按原定章节顺序展开；源码节选、教学示例与实验计划分别标明。运行版本、工具链及本次四项代表性验证见[实验复现附录](appendix-reproduction.md)；教学示意与未执行的扩展实验另行标明。

## 1. 先用显式边表表达一张小图

固定版本提供 `TopologyEdge` 和 `CustomTopology`，无需为了增加几条边重写整个 NoC。先从四节点双向链开始，再考虑捷径与层次化。

以下为固定版本的源码节选，省略外围上下文：[查看 src/main/scala/topology/Topologies.scala 第 208–218 行](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/topology/Topologies.scala#L208-L218)。

```scala
case class TopologyEdge(src: Int, dst: Int)
case class CustomTopology(n: Int, edgeList: Seq[TopologyEdge]) extends PhysicalTopology {
  val nNodes = n

  println(s"[CustomTopology] nNodes = $nNodes")
  println("[CustomTopology] Edges:")
  edgeList.foreach { e => println(s"  ${e.src} -> ${e.dst}") }

  def topo(src: Int, dst: Int): Boolean = edgeList.contains(TopologyEdge(src, dst))
  val plotter = new LinePlotter(this)
}
```

`edgeList.contains(TopologyEdge(src,dst))` 是 Scala 生成阶段查询。给出一条 0→1 并不会自动产生 1→0；节点越界、重复、自环和无用边应在自己的输入准备阶段检查，不能假定这个简短构造器已经完整验证了它们。

## 2. 可嵌入配置的教学示例

```scala
// 教学示例：替换 NoCParams.topology 字段，非独立可运行工程
import constellation.topology._
val edges = Seq((0,1),(1,0),(1,2),(2,1),(2,3),(3,2))
val graph = CustomTopology(4, edges.map { case (s,d) => TopologyEdge(s,d) })
```

此时图与 `BidirectionalLine(4)` 的边相同，可以使用对应 line relation 做第一步回归。一旦加入 0↔3 等回绕捷径，原来的 line relation 并不会自动获得安全而高效的新路径，应换用与新拓扑匹配的 routing，再做依赖检查。

## 3. 三张表先于 RTL 修改

先列节点表、边表和 terminal 映射表。对每条 edge 记录方向、宽度、VC 深度、预期延迟；对每个 flow 检查可达性。新增高阶节点还会增加 Switch 和 allocator 的规模；跨很远的捷径可能需要流水，因此“跳数少”不必然意味着“时间短”。

该版本 CustomTopology 使用 LinePlotter。自动可视化未必反映你想表达的物理布局，所以另存 draw.io 图有助于展示 floorplan 意图；图像不应被误当作实际布线或后端时序证据。

## 4. 渐进验收

第一步用等价边表复现已有拓扑，保持 terminal、flow 与路由不变；第二步只增加一条有向捷径，验证它是否被 relation 使用；第三步做冲突与高负载测试。日志中应区分“物理边存在”“VC 可遍历”“运行中有实际流量”三种状态。

练习：为新增 0→3 捷径手算端口数变化，检查是否需要反向响应路径，并列出每一类 flow 的候选路径。第 22 章进一步讨论如何定义与该图一致的 routing relation。

## 源码与延伸阅读

以下链接均固定到本章使用的源码版本：

- [src/main/scala/topology/Topologies.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/topology/Topologies.scala)
- [src/main/scala/test/CustomConfigs.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/test/CustomConfigs.scala)
- [src/main/scala/noc/Parameters.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/noc/Parameters.scala)

源码节选版权归 The Regents of the University of California，遵循 [BSD-3-Clause 许可及免责声明](/notes/constellation-notes/source-license.txt)。文字解读与教学图为专栏整理内容。

---

[上一篇](20-design-space-exploration.md) · [专栏导读](00-series-guide.md)

[下一篇：22｜自定义 Routing](22-custom-routing.md)
