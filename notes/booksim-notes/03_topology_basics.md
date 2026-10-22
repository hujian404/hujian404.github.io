# Chapter 3｜Topology Basics

> 原书：William J. Dally、Brian Towles，*Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004），第 3 章，印刷页 45–74。本地参考 PDF 的页序为印刷页 +27。以下为中文学习整理，保留原书全部目录小节的编号与标题，不是逐句翻译。BookSim2 对照版本固定为 [`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

[专栏导读](00_Introduction.md) · [原书目录与页码对照](appendix-reading-map.md)

## 3.1 Nomenclature

*原书印刷页 46。*

把网络抽象为图后，必须先固定计数约定。端点、router、端口和有向 channel 不是同一个数量；同样的图指标，也可能对应不同的板级布线成本。

### 3.1.1 Channels and Nodes

*原书印刷页 46。*

node 表示图顶点，channel 表示有方向和容量的连接。双向物理线可建模为两个方向的 channel；本地注入与接收是否计入 hop 要另行声明。

### 3.1.2 Direct and Indirect Networks

*原书印刷页 47。*

直接网络通常在连接终端的节点之间路由，间接网络通过额外交换级连接终端。多级 butterfly 的 switch 数一般不等于端点数。

### 3.1.3 Cuts and Bisections

*原书印刷页 48。*

cut 把节点集合分开，跨 cut 的容量给出相应通信的吞吐上界。bisection 要求两侧规模平衡，但最紧瓶颈未必发生在几何中线。

### 3.1.4 Paths

*原书印刷页 48。*

path 是有序 channel 序列；长度、最短距离和直径分别回答某条路径、某对节点及最坏节点对的问题。跳数不直接等于周期数。

### 3.1.5 Symmetry

*原书印刷页 49。*

节点对称、边对称等性质决定哪些节点或链路可以等价分析。终端映射和不均匀 traffic 会破坏性能上的对称性。

## 3.2 Traffic Patterns

*原书印刷页 50。*

traffic matrix 描述源宿之间的通信强度。uniform、permutation、transpose 等模式应分别分析；只用 uniform 测试容易遗漏特定映射造成的热点。

## 3.3 Performance

*原书印刷页 51。*

性能由拓扑、路由与流量共同决定。先做 channel-load 上界和距离估算，再用具体流控与 router 仿真检查排队损失。

### 3.3.1 Throughput and Maximum Channel Load

*原书印刷页 51。*

把单位终端注入下经过有向 channel c 的平均流量记为 load(c)，容量为 b(c)，则负载缩放受 `min_c b(c)/load(c)` 约束。超过它必然无法稳定交付，低于它也未必能达到上界。

### 3.3.2 Latency

*原书印刷页 55。*

零负载延迟包含路径上的 router/link 时间和消息序列化；负载增加后的排队另算。用平均最短距离估计时，需要说明源宿抽样是否允许自发送。

例如 k×k 二维 Mesh 在源宿独立均匀、允许自发送时，平均 Manhattan 距离为 `2(k²−1)/(3k)`。4×4 的结果为 2.5 hop，直径为 6；这不含终端链路。若排除自发送，平均值要除以 `1−1/16`，成为 8/3 hop。

### 3.3.3 Path Diversity

*原书印刷页 57。*

路径多样性提供绕开热点和故障的机会；若路由始终选同一条路径，结构上存在替代路径并不会自动转化成吞吐收益。

## 3.4 Packaging Cost

*原书印刷页 60。*

按 channel 数比较成本不够，还要计入线长、芯片引脚、板卡边界和连接器。相同 bisection bandwidth 可以由少量高速长线或较多低速短线实现，物理代价不同。

## 3.5 Case Study: The SGI Origin 2000

*原书印刷页 64。*

SGI Origin 2000 案例把拓扑和共享存储系统联系起来。阅读时对照端点连接、router radix 和封装限制，区分系统实际实现与理想规则图；BookSim 的一个 topology 名称并不代表复现整台机器。

具体看端口分配：SPIDER router 有六个双向 channel；terminal router 的两个端口连接两个处理节点，留下四个端口连接其他 router。系统扩容必须在固定器件 radix 下重新组织网络。因此“更多节点”不是把同一张图无代价放大，而是同时改变封装层级和可用于互连的端口。

## 3.6 Bibliographic Notes

*原书印刷页 69。*

本节对应原书 p. 69 的文献脉络。继续查阅时应回到原书该节和书末 Bibliography，区分最初提出的方法、后续实现与本文使用的 BookSim2 版本。本文末尾源码链接是实现对照，不作为原书历史论述的替代依据。

## 3.7 Exercises

*原书印刷页 69。*

自拟练习（不复制原书习题）：分别手算 2×2、4×4、8×8 Mesh 的节点数、直径和平均距离，再比较模型分配的 channel 对象数与数学上有效有向边数 `2*n*(k−1)*k^(n−1)`。解释两者不相等为何不必立即判定仿真器接错线。

## BookSim2 源码对照与适用边界

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

## 来源与继续阅读

- 原书第 3 章，pp. 45–74；各节页码已逐项列出。案例与原书公式均以本地参考书为依据。
- [BookSim2 固定版本源码](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)，节选保留[上游许可](/notes/booksim-notes/source-license.txt)。
- [全书章节/源码路线与图片来源](appendix-reading-map.md)。新增图均附 `.drawio` 源文件，插图是结构说明，不是测量波形。

[上一篇](02_a_simple_interconnection_network.md) · [下一篇](04_butterfly_networks.md) · [专栏目录](/booksim-series.html)
