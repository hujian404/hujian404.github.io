# Chapter 2｜A Simple Interconnection Network｜从四个节点开始

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. 把最小网络分成五个决定

先考虑四个计算节点，各能向其他节点发送报文。最简单的实现可以是一个四端口交换结构，也可以是 2×2 Mesh。端点数相同并不代表路径、竞争和延迟相同：前者把竞争集中在交换结构，后者把通信分散到多个 router 和 link。

描述一个网络至少要说明 topology、routing、flow control、router architecture 和 workload。只写“2×2 Mesh”不足以复现实验，因为包长、VC 数和流水线延迟还没有确定。

## 2. Packet、flit 与两种排队

Packet 是协议或流量层的消息；flit 是模型中传输、缓存和调度的基本单位。一个 4-flit packet 的 head 建立路由与 VC 绑定，tail 标出报文结束。源端等待注入和进入 router 后等待转发应分别看待，后面会映射为 packet latency 与 network latency 的差别。

对一条每拍可发送 1 flit 的链路，F-flit 报文仅序列化就需要 F 拍传输机会。无竞争、流水转发时，可用 `head 路径开销 + (F−1)×每 flit 间隔` 理解 tail 到达时间；这不是对任意 BookSim 配置的精确公式。

## 3. 用一个固定配置串起全书

后续 smoke 示例使用 2×2 Mesh、DOR、4 VC、每 VC 4 flit、4-flit packet 和单 lane。`injection_rate_uses_flits=1` 明确将负载写成 flit/node/cycle，避免把 packet/cycle 的 0.1 与 flit/cycle 的 0.1 混比。

![BookSim 仿真对象与周期推进](pic/02-model/simulation-model.svg)

上图表示软件模型的职责，不是 Verilog 生成流程。BookSim 是周期级性能模拟器，不直接生成可综合 NoC RTL。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/networks/network.cpp 第 80–91 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/network.cpp#L80-L91)。

```cpp
Network * Network::New(const Configuration & config, const string & name)
{
  const string topo = config.GetStr( "topology" );
  Network * n = NULL;
  if ( topo == "torus" ) {
    KNCube::RegisterRoutingFunctions() ;
    n = new KNCube( config, name, false );
  } else if ( topo == "mesh" ) {
    KNCube::RegisterRoutingFunctions() ;
    n = new KNCube( config, name, true );
  } else if ( topo == "cmesh" ) {
    CMesh::RegisterRoutingFunctions() ;
```

工厂读取 `topology` 字符串，选择 KNCube、KNFly 等具体网络类；router 的实现选择还在 Router 工厂中。`mesh` 与 `torus` 都使用 KNCube，但构造时的模式参数不同。先从 main → Network::New → TrafficManager 追踪对象，再进入单个 router，能避免一开始被流水线细节淹没。

## 5. 学习练习与实验边界

打开本专栏的 `experiments/mesh2x2-flit002.cfg`，逐项标注五个设计决定。手画节点 0→3 的 DOR 路径，标出两次 router 间传输和终端边界。第 25 章给出这份配置的运行方法与验证结果；这里不把小规模 smoke 当成完整网络性能评估。

## 源码与阅读导航

- [src/networks/network.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/network.cpp)
- [src/main.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/main.cpp)
- [src/trafficmanager.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.cpp)
- [src/routers/router.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routers/router.cpp)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](01_introduction_to_interconnection_networks.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 3 — Topology Basics｜度数、距离与割集](03_topology_basics.md)
