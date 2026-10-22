# Chapter 6｜Non-Blocking Networks｜可路由不等于可同时接通

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. 三种不同的无阻塞要求

严格无阻塞要求在不移动既有连接的条件下，为任意空闲输入和空闲输出建立新连接；可重排无阻塞允许调整已有路径；宽义无阻塞依赖特定的连接选择算法。讨论时必须明确连接模型、端口占用和路径是否允许重排。

这些概念通常针对电路连接或置换映射。Packet 网络中队列、分配器效率和时隙冲突又会影响持续吞吐，因此“拓扑可承载某置换”不能推出“每拍所有包都能传完”。

## 2. Clos 的条件依赖于模型

经典三阶段 Clos C(n,m,r) 中，输入级有 r 个 n×m switch，输出级对称；在单速率、单播电路连接等经典假设下，`m≥2n−1` 是严格无阻塞的充分条件，`m≥n` 对应可重排无阻塞。改变多播、速率或连接规则后，不能直接套用这个结论。

条件描述的是内部通路供给；实际实现仍要支付中间级交换机、连线和路由控制的成本。

## 3. BookSim 的 FatTree 不能直接当成 Clos 证明器

该版本提供 fattree 网络和相应路由，但没有一个通用的 Clos 连接重排验证流程。应按实际端口、级间边和流量检查它，而不是把 `topology=fattree` 当成严格无阻塞的认证。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/networks/fattree.cpp 第 79–83 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/fattree.cpp#L79-L83)。

```cpp
  //levels * routers_per_level
  _size = _n * powi( _k , _n - 1 );

  //(channels per level = k*routers_per_level* up/down) * (levels-1)
  _channels = (2*_k * powi( _k , _n-1 ))*(_n-1);
```

源码根据 k、n 计算级数和 switch 数，随后在 `_BuildNet` 中按 level 建立端口。顶层和其他层的 radix 不同。选择 FatTree 路由时要读实际 upward / downward 选择策略，以及内部链路是否为目标流量提供足够容量。

## 5. 学习练习与实验边界

画一个小型三阶段网络，给两组端点不冲突的连接找内部路径，分别尝试“不移动既有路径”和“允许重新分配”。在仿真层面则检查实际流量置换和每链路负载，避免把随机 uniform 的好结果解释为所有置换的无阻塞保证。

## 源码与阅读导航

- [src/networks/fattree.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/fattree.cpp)
- [src/networks/network.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/network.cpp)
- [src/routefunc.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routefunc.cpp)
- [src/examples/fattree_config](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/examples/fattree_config)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](05_torus_networks.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 7 — Slicing and Dicing｜带宽、radix 与物理代价](07_slicing_and_dicing.md)
