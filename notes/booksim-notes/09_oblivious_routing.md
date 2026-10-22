# Chapter 9｜Oblivious Routing

> 原书：William J. Dally、Brian Towles，*Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004），第 9 章，印刷页 173–188。本地参考 PDF 的页序为印刷页 +27。以下为中文学习整理，保留原书全部目录小节的编号与标题，不是逐句翻译。BookSim2 对照版本固定为 [`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

[专栏导读](00_Introduction.md) · [原书目录与页码对照](appendix-reading-map.md)

## 9.1 Valiant’s Randomized Routing Algorithm

*原书印刷页 174。*

Valiant 路由先到随机中间节点，再到最终目的节点，用额外路径长度换取更均匀的负载。中间节点选择分布和两阶段所用路由必须明确；它不观察瞬时拥塞，因此属于 oblivious。

### 9.1.1 Valiant’s Algorithm on Torus Topologies

*原书印刷页 174。*

在 Torus 上，两段路由可能分别跨多个维度与 wrap 连接。除增加 hop 外，还要解决阶段转换及每段环形资源依赖。

### 9.1.2 Valiant’s Algorithm on Indirect Networks

*原书印刷页 175。*

间接网络上通过随机中间选择打散输入模式。必须按具体级间结构安排两段路径，不能把直接网络的坐标算法原样搬到交换级。

## 9.2 Minimal Oblivious Routing

*原书印刷页 176。*

minimal oblivious 只在最短路径集合中按固定概率选择。它避免 Valiant 的额外距离，却无法像非最短路径那样绕开所有集中模式。

### 9.2.1 Minimal Oblivious Routing on a Folded Clos (Fat Tree)

*原书印刷页 176。*

folded Clos/fat tree 利用上行路径选择分散流量，下行方向则受目的位置约束。集中度、上行容量和源宿映射共同决定是否真正负载均衡。

### 9.2.2 Minimal Oblivious Routing on a Torus

*原书印刷页 178。*

Torus 的维度顺序与等长方向提供随机化空间；概率选择必须保持算法规定的最短性，且与 VC 依赖限制相容。

## 9.3 Load-Balanced Oblivious Routing

*原书印刷页 180。*

load-balanced oblivious 按已知 traffic 或鲁棒目标离线确定路径概率。它与每一拍读取队列深度的 adaptive 不同，traffic 改变后需要重新检验分配。

## 9.4 Analysis of Oblivious Routing

*原书印刷页 180。*

把每条候选路径的概率乘以源宿需求，再累加到经过的 channel，即可求期望负载。比较算法时要同时报告最大 channel load、路径长度和适用 traffic 假设。

可按以下顺序独立核对：先归一化 traffic matrix，再枚举合法路径及概率，随后逐 channel 累加需求，最后求最大负载和平均长度。对比 BookSim 结果前，先确认模拟器的算法与这里的路径分布相同。

## 9.5 Case Study: Oblivious Routing in the Avici Terabit Switch Router(TSR)

*原书印刷页 183。*

Avici TSR 是本章 oblivious routing 案例。关注路径分散如何配合拓扑和服务隔离，避免把它简化成“随机路由一定比确定性好”。

Avici TSR 使用 3-D Torus fabric 连接 line card，并通过 source routing 支持部分填充和故障后不规则的连接。源端把精确方向串编码进消息，沿途按它转发。它说明 oblivious 是“选择不依赖瞬时拥塞”，并不表示硬编码一条永不更新的规则坐标路径；拓扑和故障信息仍可影响源端选择。

## 9.6 Bibliographic Notes

*原书印刷页 186。*

本节对应原书 p. 186 的文献脉络。继续查阅时应回到原书该节和书末 Bibliography，区分最初提出的方法、后续实现与本文使用的 BookSim2 版本。本文末尾源码链接是实现对照，不作为原书历史论述的替代依据。

## 9.7 Exercises

*原书印刷页 187。*

自拟练习（不复制原书习题）：对相同 topology、包长和 offered load 比较 DOR 与 Valiant，分别使用 uniform 和一种规则置换，记录 hop、packet latency 与 accepted rate。不能只选一个对 DOR 不利的点；也要展示低负载绕行代价。这里是对照方案，不预填性能提升数字。

## BookSim2 源码对照与适用边界

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/routefunc.cpp 第 1276–1284 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routefunc.cpp#L1276-L1284)。

```cpp
void valiant_mesh( const Router *r, const Flit *f, int in_channel, OutputSet *outputs, bool inject )
{
  int vcBegin = 0, vcEnd = gNumVCs-1;
  if ( f->type == Flit::READ_REQUEST ) {
    vcBegin = gReadReqBeginVC;
    vcEnd = gReadReqEndVC;
  } else if ( f->type == Flit::WRITE_REQUEST ) {
    vcBegin = gWriteReqBeginVC;
    vcEnd = gWriteReqEndVC;
```

继续沿函数中的 `f->intm` 与 `f->ph` 读中间目的和阶段变化，并核对 VC 区间如何按阶段划分。Flit 中这两个字段标为 mutable，说明路由函数可以更新路径上下文；这不是当前拥塞反馈，因此仍属于 oblivious 机制。

## 来源与继续阅读

- 原书第 9 章，pp. 173–188；各节页码已逐项列出。案例与原书公式均以本地参考书为依据。
- [BookSim2 固定版本源码](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)，节选保留[上游许可](/notes/booksim-notes/source-license.txt)。
- [全书章节/源码路线与图片来源](appendix-reading-map.md)。新增图均附 `.drawio` 源文件，插图是结构说明，不是测量波形。

[上一篇](08_routing_basics.md) · [下一篇](10_adaptive_routing.md) · [专栏目录](/booksim-series.html)
