# 05｜NoC Specification 与 NoCParams

> 更新：2026-10-22。源码基线：[`c1b42cd`](https://github.com/ucb-bar/constellation/tree/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510)。本文按原定章节顺序展开；源码节选、教学示例与实验计划分别标明。运行版本、工具链及本次四项代表性验证见[实验复现附录](appendix-reproduction.md)；教学示意与未执行的扩展实验另行标明。

## 1. 一份规格到底包含什么

`NoCParams` 是 Scala `case class`，不是顶层硬件 IO。它把物理连接、资源大小、终端、允许的通信关系、路由规则和生成选项组合成一个值。内部参数再将这份简洁规格展开为每条实际 channel 和每个 router 所需的信息。

以下为固定版本的源码节选，省略外围上下文：[查看 src/main/scala/test/Configs.scala 第 29–36 行](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/test/Configs.scala#L29-L36)。

```scala
class TestConfig00 extends NoCTesterConfig(NoCTesterParams(NoCParams(
  topology        = UnidirectionalLine(2),
  channelParamGen = (a, b) => UserChannelParams(Seq.fill(3) { UserVirtualChannelParams(3) }),
  ingresses       = Seq(0).map { i => UserIngressParams(i) },
  egresses        = Seq(1).map { i => UserEgressParams(i) },
  flows           = Seq.tabulate(1, 1) { (s, d) => FlowParams(s, d, 0) }.flatten,
  routingRelation = UnidirectionalLineRouting()
)))
```

逐项拆解这个真实的两节点配置：

1. `UnidirectionalLine(2)` 有节点 0、1，只有 0→1 的前向边。
2. `channelParamGen(a,b)` 按有向边返回 channel 参数；这里忽略 a、b，所有物理边都配置三个深度为 3 的 VC。
3. `ingresses(0).destId = 0`，`egresses(0).srcId = 1`，表示网络入口挂在节点 0，出口挂在节点 1。
4. `Seq.tabulate(1,1)` 产生一个二维 Scala 序列，`flatten` 后只有 `FlowParams(0,0,0)`。
5. `UnidirectionalLineRouting()` 返回一个接受 topology 的函数，生成与拓扑关联的路由对象。

## 2. 两套编号必须分开

例如增加第二个 ingress 并仍挂在 router 0，则 `ingresses = Seq(UserIngressParams(0), UserIngressParams(0))`。来自第二个入口的 flow 应写 `FlowParams(1,0,0)`。这里 ingress ID 为 1，物理节点仍为 0。内部还会给同节点端口分配局部序号 `ingressNodeId`，供路由 bundle 表示使用。

| 名称 | 例子 | 含义 |
| --- | --- | --- |
| ingressId | 1 | 入口列表中的第二项 |
| ingressNode | 0 | 这个入口挂接的 router |
| ingressNodeId | 1 | 同一个 router 上的第二个入口 |
| vNetId | 0 | 所属虚拟子网 |

不能用物理节点号直接替代 terminal ID；在“每节点恰好一个终端且顺序相同”的配置里二者恰巧相等，最容易掩盖这个错误。

## 3. 从 User 参数变为 Internal 参数

`InternalNoCParams.apply` 枚举全部 `(i,j)`，只对 `topology.topo(i,j)` 为真的边生成 ChannelParams；flow 则通过 terminal 列表补齐物理位置。随后运行可达性和依赖检查，收集每个 VC 的 `possibleFlows`，过滤不可遍历的物理 channel。因而配置中的资源上限不一定等于最终 RTL 中保留的资源。

Chisel 学习点是先用 Scala 数据结构表达结构，再由结构决定 `Vec` 大小、位宽和 `Module` 数量。`case class.copy` 创建新参数值，不是把运行中的寄存器改写；`require` 失败也发生在生成阶段。

## 4. 最小修改实验

以原始 `TestConfig00` 为基线，一次只修改 VC 数或单 VC 深度。先手算原始链路的逻辑容量为 `3 × 3 = 9 flit slots`，然后检查 elaboration 日志中是否有不可遍历资源被剔除。容量估算不包含终端缓冲、实现额外队列和控制位。

另做一个故障注入：把唯一 flow 的 egress ID 改为不存在的 1。预期在构建检查中失败，而不是等仿真丢包。这是验证规格检查路径的练习，不能把“编译成功”当作性能结论。

## 源码与延伸阅读

以下链接均固定到本章使用的源码版本：

- [src/main/scala/test/Configs.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/test/Configs.scala)
- [src/main/scala/noc/Parameters.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/noc/Parameters.scala)
- [src/main/scala/routing/Types.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/routing/Types.scala)

源码节选版权归 The Regents of the University of California，遵循 [BSD-3-Clause 许可及免责声明](/notes/constellation-notes/source-license.txt)。文字解读与教学图为专栏整理内容。

---

[上一篇](04-github-source-code-guide.md) · [专栏导读](00-series-guide.md)

[下一篇：06｜Topology：从 Mesh 到任意有向图](06-topology.md)
