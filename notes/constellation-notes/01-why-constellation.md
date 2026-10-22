# 01｜为什么需要 Constellation

> 更新：2026-10-22。源码基线：[`c1b42cd`](https://github.com/ucb-bar/constellation/tree/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510)。本文按原定章节顺序展开；源码节选、教学示例与实验计划分别标明。运行版本、工具链及本次四项代表性验证见[实验复现附录](appendix-reproduction.md)；教学示意与未执行的扩展实验另行标明。

## 1. 从通信需求开始，而不是先画 Mesh

假设一个教学 SoC 有 CPU、DMA、两个 SRAM bank 和一个加速器。CPU 常发短控制请求，DMA 搬运长数据块，加速器高频访问 SRAM。即使这些模块全都能接入同一个 Crossbar，它们的带宽、时延、突发长度和协议依赖也不相同。随着端点增加，全连接结构的端口、仲裁和布线成本会变大；规则 Mesh 又可能让相邻的高流量模块绕行。

选择 NoC 时首先需要写出通信矩阵：谁会向谁发送、峰值和平均流量是多少、哪类消息必须在另一类阻塞时继续前进。Constellation 的价值是把这些约束送进生成器，产出适合该 SoC 的网络，而非只提供一个固定尺寸的 Mesh。

## 2. 四种描述共同决定硬件

| 描述 | 回答的问题 | 修改后的硬件影响 |
| --- | --- | --- |
| Topology | 哪两个 router 之间有有向边？ | 端口、连线与交换结构 |
| Channel / Router 参数 | 链路宽度、VC 数量、深度、流水线是什么？ | 存储与控制逻辑 |
| Flow | 哪些 ingress–egress 通信被支持？ | 可达路径、路由项和可裁剪资源 |
| Routing relation | 某个 flow 能从当前 VC 进入哪个下一 VC？ | 路由译码与合法候选集合 |

这些描述可以分别修改，却不能独立保证正确性。加入一条捷径后，原路由可能不使用它；多开一个 VC 后，如果没有合法分配规则，也不会自动提高吞吐。

## 3. 从一个真实入口看 Chisel 生成器

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

`TestConfig00` 的 Scala 构造器嵌套顺序是 `Config → NoCTesterParams → NoCParams`。`Seq.fill(3)` 在生成阶段创建三个 VC 参数对象，每个深度为 3；它本身不是三个时钟周期。`Seq(0).map(...)` 把物理节点 0 映射为一个 ingress，egress 则挂在物理节点 1。`FlowParams(0, 0, 0)` 中前两个 0 是端口列表下标，因此其物理路径是 0→1。

学习的第一步应当能把这一小段代码手画为两个 router、一条有向物理链路和一对终端。到第 5–10 章再逐步追踪这些对象如何变为 Chisel 电路。

## 4. 关键取舍与练习

NoC 不是免费的带宽：每跳增加控制、缓存与链路开销，窄链路还会把一个消息切成更多 flit。先定义要改善的瓶颈，再选择网络。对上面的教学 SoC，画出 CPU→SRAM、DMA→SRAM、加速器→SRAM 的方向，并单独列出返回流；不要默认请求与响应使用同一资源就一定安全。

完成标准：能够解释“端点数、router 数、flow 数、VC 数”为什么是四个不同的量，并指出 `TestConfig00` 的实际取值。本次已在实验 fork 中通过对应的 `NoCTest00`；完整版本和结果见实验复现附录，不由这一次功能通过推导性能优势。

## 源码与延伸阅读

以下链接均固定到本章使用的源码版本：

- [src/main/scala/test/Configs.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/test/Configs.scala)
- [README.md](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/README.md)

源码节选版权归 The Regents of the University of California，遵循 [BSD-3-Clause 许可及免责声明](/notes/constellation-notes/source-license.txt)。文字解读与教学图为专栏整理内容。

---

[上一篇](00-series-guide.md) · [专栏导读](00-series-guide.md)

[下一篇：02｜论文精读：设计目标与核心思想](02-paper-design-goals.md)
