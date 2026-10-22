# Chapter 10｜Adaptive Routing

> 原书：William J. Dally、Brian Towles，*Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004），第 10 章，印刷页 189–202。本地参考 PDF 的页序为印刷页 +27。以下为中文学习整理，保留原书全部目录小节的编号与标题，不是逐句翻译。BookSim2 对照版本固定为 [`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

[专栏导读](00_Introduction.md) · [原书目录与页码对照](appendix-reading-map.md)

## 10.1 Adaptive Routing Basics

*原书印刷页 189。*

自适应路由由合法候选路径、拥塞指标和选择规则组成。credit、可用 VC 和队列长度是不同信号；反馈滞后可能让多个源同时选择看似空闲的方向。

## 10.2 Minimal Adaptive Routing

*原书印刷页 192。*

minimal adaptive 在使剩余距离缩短的候选中选择，可降低额外 hop；然而热点可能覆盖所有最短路径。算法还必须满足第 14 章的无死锁条件。

## 10.3 Fully Adaptive Routing

*原书印刷页 193。*

fully adaptive 允许更广的路径集合，可能通过非最短路径绕开拥塞。更大自由度同时增加依赖、绕路与活锁控制的复杂度。

## 10.4 Load-Balanced Adaptive Routing

*原书印刷页 195。*

load-balanced adaptive 在短路径和绕路间权衡，需要考虑剩余距离、通路容量及拥塞。局部空队列不能证明该路径的全程代价低。

## 10.5 Search-Based Routing

*原书印刷页 196。*

search-based routing 通过探测或搜索寻找路径，建立过程本身消耗时间和控制资源。应把搜路成本与实际数据传输区分开，不能只统计成功数据的 latency。

## 10.6 Case Study: Adaptive Routing in the Thinking Machines CM-5

*原书印刷页 196。*

Thinking Machines CM-5 案例展示自适应路径选择与具体网络结构的关系。比较它和 BookSim 算法前，先核对拓扑、决策点、状态可见范围和流控假设。

CM-5 数据网络先向 folded Clos 的公共祖先上行，再沿目的标签确定性下行。上行在空闲链路中随机选择；全部忙时等待。因此只有上行阶段是这里的自适应选择，下行不是任意选路。header 中的 height 字段指示需要上行到哪一级，这把路由策略与消息编码直接联系起来。

## 10.7 Bibliographic Notes

*原书印刷页 201。*

本节对应原书 p. 201 的文献脉络。继续查阅时应回到原书该节和书末 Bibliography，区分最初提出的方法、后续实现与本文使用的 BookSim2 版本。本文末尾源码链接是实现对照，不作为原书历史论述的替代依据。

## 10.8 Exercises

*原书印刷页 201。*

自拟练习（不复制原书习题）：先构造一个流量热点，画出某个 router 到目标的多个 productive 方向；分别记录 relation 的候选和最终获分配的输出。增加终端阻塞后检查是否存在长期不前进的 packet，并用状态定位，而不是把任何 timeout 都解释成死锁。

## BookSim2 源码对照与适用边界

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/routefunc.cpp 第 932–941 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routefunc.cpp#L932-L941)。

```cpp
void min_adapt_mesh( const Router *r, const Flit *f, int in_channel, OutputSet *outputs, bool inject )
{
  int vcBegin = 0, vcEnd = gNumVCs-1;
  if ( f->type == Flit::READ_REQUEST ) {
    vcBegin = gReadReqBeginVC;
    vcEnd = gReadReqEndVC;
  } else if ( f->type == Flit::WRITE_REQUEST ) {
    vcBegin = gWriteReqBeginVC;
    vcEnd = gWriteReqEndVC;
  } else if ( f->type ==  Flit::READ_REPLY ) {
```

`min_adapt_mesh` 是具体实现入口，需要向下读 productive 输出、escape 路径和 VC 约束，再到 IQRouter 中看请求过滤。不要把另一个拓扑的 adaptive 函数直接套给 Mesh；函数注册、VC 区间和 escape 前提必须成组核对。

## 来源与继续阅读

- 原书第 10 章，pp. 189–202；各节页码已逐项列出。案例与原书公式均以本地参考书为依据。
- [BookSim2 固定版本源码](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)，节选保留[上游许可](/notes/booksim-notes/source-license.txt)。
- [全书章节/源码路线与图片来源](appendix-reading-map.md)。新增图均附 `.drawio` 源文件，插图是结构说明，不是测量波形。

[上一篇](09_oblivious_routing.md) · [下一篇](11_routing_mechanics.md) · [专栏目录](/booksim-series.html)
