# Chapter 4｜Butterfly Networks

> 原书：William J. Dally、Brian Towles，*Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004），第 4 章，印刷页 75–88。本地参考 PDF 的页序为印刷页 +27。以下为中文学习整理，保留原书全部目录小节的编号与标题，不是逐句翻译。BookSim2 对照版本固定为 [`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

[专栏导读](00_Introduction.md) · [原书目录与页码对照](appendix-reading-map.md)

## 4.1 The Structure of Butterfly Networks

*原书印刷页 75。*

k-ary n-fly 有 k^n 个输入和输出、n 级、每级 k^(n−1) 个 k×k switch，总 switch 数为 n·k^(n−1)。目的地址逐级选端口，使规则连线和简单路由配合；标准 butterfly 每对源宿只有一条路径。

## 4.2 Isomorphic Butterflies

*原书印刷页 77。*

调整节点编号、级次画法或连线排列可得到同构表示。判断是否同构要找保持邻接关系的映射，不能因为图中交叉线少就认为 hop 或连通性改变了。

## 4.3 Performance and Packaging Cost

*原书印刷页 78。*

路径长度规则且较短，但不同源宿对会争用内部 channel。比较成本时同时数 switch、级间连接和跨封装边界的线，而不是只与大 crossbar 比门数。

## 4.4 Path Diversity and Extra Stages

*原书印刷页 81。*

额外交换级可增加可选路径，并减小某些内部阻塞；代价是更多交换和布线。多路径还需要对应路由与调度策略，新增级数本身不会保证无阻塞。

## 4.5 Case Study: The BBN Butterfly

*原书印刷页 84。*

BBN Butterfly 案例展示多级网络在并行机器中的使用。对照它的处理器连接、逐级转发和物理实现，再回到本章抽象结构；避免把原书机器参数与 BookSim 默认 fly 参数混为一谈。

64 节点示例使用四级 radix-4 switch，比基本三级 butterfly 多一级；新增级提供四条边不相交路径，发送时随机选择，并可用路径 mask 排除故障路径。这里路径多样性来自实际增添结构，而非给唯一最短路径换一个 routing function。原机是远程可访问内存的共享存储机器，但并不提供一般的 cache coherence。

## 4.6 Bibliographic Notes

*原书印刷页 86。*

本节对应原书 p. 86 的文献脉络。继续查阅时应回到原书该节和书末 Bibliography，区分最初提出的方法、后续实现与本文使用的 BookSim2 版本。本文末尾源码链接是实现对照，不作为原书历史论述的替代依据。

## 4.7 Exercises

*原书印刷页 86。*

自拟练习（不复制原书习题）：手算 k=2、n=3 的每级 switch 数和内部 channel 数，追踪两个不同目的请求的路径，寻找一组内部争用。先用 `src/examples/singleconfig` 理解 n=1 如何退化为单级交换，再尝试多级；示例不是所有置换都无阻塞的证明。

## BookSim2 源码对照与适用边界

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

## 来源与继续阅读

- 原书第 4 章，pp. 75–88；各节页码已逐项列出。案例与原书公式均以本地参考书为依据。
- [BookSim2 固定版本源码](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)，节选保留[上游许可](/notes/booksim-notes/source-license.txt)。
- [全书章节/源码路线与图片来源](appendix-reading-map.md)。新增图均附 `.drawio` 源文件，插图是结构说明，不是测量波形。

[上一篇](03_topology_basics.md) · [下一篇](05_torus_networks.md) · [专栏目录](/booksim-series.html)
