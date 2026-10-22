# 13｜Virtual Channel 与 Deadlock Avoidance

> 更新：2026-10-22。源码基线：[`c1b42cd`](https://github.com/ucb-bar/constellation/tree/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510)。本文按原定章节顺序展开；源码节选、教学示例与实验计划分别标明。运行版本、工具链及本次四项代表性验证见[实验复现附录](appendix-reproduction.md)；教学示意与未执行的扩展实验另行标明。

## 1. 先分清三种停止前进

死锁是资源等待形成循环且无法解除；饥饿是有机会前进却长期得不到仲裁；活锁是持续活动却无法到达目的。增加 VC 数有时改善阻塞，但没有配套路由与仲裁约束时，不能自动解决以上问题。

构建 channel dependency graph 时，顶点应是具体的 `(src,dst,vc)` 资源；若 packet 占着资源 A 还可能申请资源 B，就建立 A→B。它不同于以 router 为顶点的物理拓扑图。

## 2. Escape channel 的源码落点

以下为固定版本的源码节选，省略外围上下文：[查看 src/main/scala/noc/Parameters.scala 第 266–272 行](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/noc/Parameters.scala#L266-L272)。

```scala
    val acyclicPath = checkAcyclic(new RoutingRelation(nocParams.topology) {
      def rel(srcC: ChannelRoutingInfo, nxtC: ChannelRoutingInfo, flow: FlowRoutingInfo) = {
        val escape = routingRelation.isEscape(nxtC, flow.vNetId)
        routingRelation(srcC, nxtC, flow) && escape
      }
    })
    require(acyclicPath.isEmpty, s"Cyclic path may cause deadlock: ${acyclicPath.get}")
```

`checkAcyclic` 遍历可能 flow 引起的资源依赖，示例 wrapper 只保留 `routingRelation.isEscape(nxtC, flow.vNetId)` 对应的下一资源。默认 `isEscape=true` 时所有资源都属于被检查集合；使用 escape 包装时，需要同时保证进入 escape、沿 escape 前进及资源划分契约。

这项检查证明的是该规格模型中的结构性质；它不替代公平仲裁、终端最终消费以及协议依赖满足等运行条件。关闭 `skipValidationChecks` 所控制的虚拟子网检查也不能作为解决非法路由的方式。

## 3. 用 dateline 理解 VC 为什么参与路由

环形网络里，如果每条边都能等下一条边，资源依赖可能绕环。dateline 将不同阶段的路径放入不同 VC 类，并限制跨界后的资源转移。`UnidirectionalTorus1DDatelineRouting` 中对 `srcC.vc`、`nxtC.vc` 和边界节点分别判断，就是为了切断允许依赖中的循环。

数字上“有两个 VC”并不够，还要保证 relation 按阶段使用它们，不能允许跨界后返回原阶段并重建环。应逐项核对 n_vc 与 vc 重编号，尤其在 `EscapeChannelRouting`、`NonblockingVirtualSubnetworksRouting` 组合后。

## 4. 协议层还需要第二张依赖图

请求可能等待响应，响应又需要网络资源。如果请求占满响应所必需的资源，就可能协议死锁。这时 router 路由无环仍不足够，需要 `vNetBlocking` 与相应可独立前进的 VC 路径。第 15 章从协议 adapter 的生成参数继续阅读。

练习：手画一个四节点单向环的资源依赖，再把每条物理边拆为两个 VC 顶点，依据实际 dateline 规则画允许转移。最后制造一个违反规则的 relation，检查 elaboration 是否拒绝。仿真超时只能说明观察到未完成，不能仅凭超时给它定性为死锁；还应检查注入过载、终端 backpressure 和测试结束条件。

## 源码与延伸阅读

以下链接均固定到本章使用的源码版本：

- [src/main/scala/noc/Parameters.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/noc/Parameters.scala)
- [src/main/scala/routing/RoutingRelations.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/routing/RoutingRelations.scala)
- [docs/source/Configuration/RoutingSpec.rst](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/docs/source/Configuration/RoutingSpec.rst)

源码节选版权归 The Regents of the University of California，遵循 [BSD-3-Clause 许可及免责声明](/notes/constellation-notes/source-license.txt)。文字解读与教学图为专栏整理内容。

---

[上一篇](12-wormhole-credit-flow-control.md) · [专栏导读](00-series-guide.md)

[下一篇：14｜VC Allocation、Arbitration 与 Pipeline](14-vc-allocation-arbitration-pipeline.md)
