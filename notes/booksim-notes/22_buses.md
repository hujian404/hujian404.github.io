# Chapter 22｜Buses｜共享介质与交换网络的比较边界

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. Bus 的核心限制是共享服务机会

在一次只允许一个发送者占用的理想 bus 中，所有端点共享总带宽。若每个节点都以 λ flit/cycle 注入、共 N 个节点且每 flit 一次占用总线，则必要条件为 `Nλ≤C_bus`。实际还需考虑仲裁、地址阶段、转向、广播、响应和占用粒度。

对交换网络，互不冲突的源宿通信可能同时使用不同链路；但它支付更多 switch、buffer 与连接成本。是否选 bus 应由规模、流量和物理成本决定，而不是仅靠“并行更多”判断。

## 2. Crossbar 不是 bus 的同义词

单级 crossbar 可以同时支持多组互不冲突的输入输出，广播 bus 则通常只有共享介质服务机会。将 BookSim 的 n=1 fly 设成单级交换机，并不能自动复现共享 bus 的互斥约束。

## 3. 该版本工厂没有通用 topology=bus

Network::New 枚举 mesh、torus、fly、fattree 等实现，不含可以直接指定的通用 bus 模型。因此本章把 bus 作为理论比较对象，并说明扩展方向，不给一个实际无法运行的配置示例。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/networks/network.cpp 第 93–100 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/network.cpp#L93-L100)。

```cpp
  } else if ( topo == "fly" ) {
    KNFly::RegisterRoutingFunctions() ;
    n = new KNFly( config, name );
  } else if ( topo == "qtree" ) {
    QTree::RegisterRoutingFunctions() ;
    n = new QTree( config, name );
  } else if ( topo == "tree4" ) {
    Tree4::RegisterRoutingFunctions() ;
```

factory 是核对网络模型支持范围的入口。若实现 bus，应把每个时隙 / 事务可获得的全局服务许可、占用时间与端点队列显式建模，而不是只把不同端点接到同一 router。还要定义广播复制是否消耗额外服务机会。

## 5. 学习练习与实验边界

以4个节点、每报文4 flit为例，分别按 flit 级仲裁和 packet 级锁定手算服务次序。与单级 crossbar 对比时给相同的总带宽 / 成本预算；如需仿真 bus，先新增独立模型并做容量守恒测试。

## 源码与阅读导航

- [src/networks/network.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/network.cpp)
- [src/examples/singleconfig](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/examples/singleconfig)
- [src/networks/fly.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/fly.cpp)
- [src/routers/iq_router.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routers/iq_router.cpp)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](21_error_control.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 23 — Performance Analysis｜先定义事件，再解释曲线](23_performance_analysis.md)
