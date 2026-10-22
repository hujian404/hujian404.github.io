# Chapter 5｜Torus Networks｜回绕连接与资源依赖

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. 回绕缩短距离，但改变了等待关系

Torus 在每个维度加入回绕方向，使边界节点也连接到另一端。对双向规则 k-ary n-cube，最短路径直径是 `n*floor(k/2)`，而 Mesh 为 `n*(k−1)`。是否真正减小延迟，还取决于回绕导线、router pipeline 与路径竞争。

最短方向有时存在平局；相同源宿可以走正向或负向。算法如何处理平局会改变负载，实验应固定路由函数和 seed。

## 2. 物理环不等于一定死锁

一个 packet 保持当前 VC 并等待下一 VC，可能沿环形成循环依赖。dateline 等规则通过 VC 类别和阶段限制打断资源依赖；关键不是“多加几个 VC”，而是保证允许转移遵守预定次序。

Mesh 中可用的 VC 分区不能不加检查地移植到 Torus。运行没有超时也不是对所有流量无死锁的证明，第14章会专门分析。

## 3. 比较 Mesh 与 Torus 的时延假设

固定版本 KNCube 在 `use_noc_latency=1` 时，把 mesh 方向链路延迟设为1、torus 设为2；这是模型假设，不是某工艺的物理测量。若只改 topology 而不说明该默认，比较中就同时改变了连通性和时延。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/networks/kncube.cpp 第 118–121 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/kncube.cpp#L118-L121)。

```cpp
      // torus channel is longer due to wrap around
      int latency = _mesh ? 1 : 2 ;

      //get the input channel number
```

`_mesh` 控制默认 latency；`SetLatency` 同时作用于数据和 credit channel。该实现分配的邻接对象带有 wrap 组织，Mesh 靠路由约束避免使用边界回绕，不能只数指针就判断某条路径会被选中。Torus 的 `dim_order_torus` 还会对 VC 区间进行分割。

## 5. 学习练习与实验边界

先用 n=1、k=8 手画0→7和0→4，分别记录 Mesh、Torus 的跳数和平局选择。随后阅读 `dor_next_torus` 的边界与 partition 更新；比较时分别报告链路周期假设和 hop 数，不能只给总体平均延迟。

## 源码与阅读导航

- [src/networks/kncube.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/kncube.cpp)
- [src/routefunc.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routefunc.cpp)
- [src/examples/torus88](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/examples/torus88)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](04_butterfly_networks.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 6 — Non-Blocking Networks｜可路由不等于可同时接通](06_non_blocking_networks.md)
