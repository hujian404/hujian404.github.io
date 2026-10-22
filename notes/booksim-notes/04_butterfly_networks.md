# Chapter 4｜Butterfly Networks｜用目的地址选择逐级路径

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. 从单级大交换机到多级小交换机

Butterfly 将大规模连接分解为多级小 radix 交换机。k-ary n-fly 有 k^n 个输入与输出端点、n 级交换；每级有 k^(n−1) 个 k×k switch，总数为 `n*k^(n−1)`。这里 n 表示级数，而不是 Mesh 中的物理维度含义。

例如二进制 3-fly 连接8个输入和8个输出，包含3级、每级4个 switch。它减少了单个交换机的端口压力，却带来级间共享路径与阻塞。

## 2. Destination tag 的含义

将目的编号展开为 k 进制数字，每一级用相应数字选择输出，便可在规则级间布线中到达目的端。端口编号、地址数字顺序与级间排列必须一致。一个源宿对只有一条路径并不意味着不同源宿对不会共享中间资源。

Butterfly 中可能存在输出端互不冲突、却在内部 channel 上冲突的请求。因此“最终目的不同”和“可同时通过”不是等价命题。

## 3. 把路径唯一与无死锁分开

逐级向前且不回到先前级的网络，可以按级数建立资源顺序；但端点协议依赖、队列和反向响应网络仍需单独考虑。不要从单向数据平面无环推导出完整系统永远不会停住。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/networks/fly.cpp 第 45–58 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/fly.cpp#L45-L58)。

```cpp
void KNFly::_ComputeSize( const Configuration &config )
{
  _k = config.GetInt( "k" );
  _n = config.GetInt( "n" );

  gK = _k; gN = _n;

  _nodes = powi( _k, _n );

  // n stages of k^(n-1) k x k switches
  _size     = _n*powi( _k, _n-1 );

  // n-1 sets of wiring between the stages
  _channels = (_n-1)*_nodes;
```

源码的 `_nodes`、`_size`、`_channels` 与上述级数公式对应，内部有向 channel 数为 `(n−1)*k^n`，不包括终端连接。`dest_tag_fly` 在 routefunc.cpp 中决定逐级输出；`topology=fly` 与 `routing_function=dest_tag` 组合形成注册键。

## 5. 学习练习与实验边界

手算 k=2、n=3 的每级 switch 数和内部 channel 数，追踪两个不同目的请求的路径，寻找一组内部争用。先用 `src/examples/singleconfig` 理解 n=1 如何退化为单级交换，再尝试多级；示例不是所有置换都无阻塞的证明。

## 源码与阅读导航

- [src/networks/fly.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/fly.cpp)
- [src/routefunc.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routefunc.cpp)
- [src/examples/singleconfig](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/examples/singleconfig)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](03_topology_basics.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 5 — Torus Networks｜回绕连接与资源依赖](05_torus_networks.md)
