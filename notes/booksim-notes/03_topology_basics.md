# Chapter 3｜Topology Basics｜度数、距离与割集

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. 三个数量不要混为一谈

网络的端点数、router 数和有向 channel 数可能各不相同。集中式网络允许多个端点挂在一个 router；多级网络还可能用许多内部交换机连接较少端点。讨论 radix 时要说明是否包括本地注入 / 接收端口，讨论链路数时要说明双向连接算一条还是两个方向。

## 2. 先算能独立核对的图指标

对每维 k 个节点、n 维、每 router 一个 terminal 的 Mesh，节点数是 `N=k^n`，网络直径为 `n(k−1)`。当源宿在全部 N 个节点中独立均匀选择、允许自发送时，平均 Manhattan 距离为 `n(k²−1)/(3k)`。若明确排除自发送，应再按条件概率归一化，不能照搬该平均值。

对 4×4 Mesh，N=16、直径6，独立均匀源宿的平均 router 间距离是2.5跳。它不包含注入 / 接收链路，也不是网络延迟。

BookSim 的 Hops average 还需按事件定义理解：IQRouter 在发出 flit 时递增 hops，最终 ejection 也经过 router，因而不宜直接将这个统计与数学上的 router 间链路数逐值等同。

## 3. 跳数之外，还要看割集和布线

某个 cut 两侧的通信需要穿过割集中的 channel。若这些有向 channel 的总容量为 B flit/cycle，给定 traffic matrix 跨过该 cut 的期望 flit 量为 L，则负载缩放因子受 `B/L` 限制。这只是必要上界，实际路由和争用可能更早饱和。

低直径通常需要更高 radix 或更长导线，物理实现中面积、时钟和线延迟也会变化。公平比较应说明固定了端点、端口带宽、总布线还是面积预算。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/networks/kncube.cpp 第 55–65 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/kncube.cpp#L55-L65)。

```cpp
void KNCube::_ComputeSize( const Configuration &config )
{
  _k = config.GetInt( "k" );
  _n = config.GetInt( "n" );

  gK = _k; gN = _n;
  _size     = powi( _k, _n );
  _channels = 2*_n*_size;

  _nodes = _size;
}
```

`_size` 和 `_nodes` 在这里都等于 k^n，`_channels=2*n*_size` 是该实现分配的 channel 对象规模。尤其要注意：固定版本 KNCube 对 mesh / torus 共享邻接和端口组织，边界方向仍分配对象；Mesh 的 DOR 不使用跨边界的 wrap 方向。不能将 `_channels` 直接当成教科书有限 Mesh 中有效内部边的计数。

## 5. 学习练习与实验边界

分别手算 2×2、4×4、8×8 Mesh 的节点数、直径和平均距离，再比较模型分配的 channel 对象数与数学上有效有向边数 `2*n*(k−1)*k^(n−1)`。解释两者不相等为何不必立即判定仿真器接错线。

## 源码与阅读导航

- [src/networks/kncube.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/kncube.cpp)
- [src/networks/kncube.hpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/kncube.hpp)
- [src/routefunc.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routefunc.cpp)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](02_a_simple_interconnection_network.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 4 — Butterfly Networks｜用目的地址选择逐级路径](04_butterfly_networks.md)
