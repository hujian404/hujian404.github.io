# Chapter 10｜Adaptive Routing｜候选路径与拥塞反馈

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. 自适应的依据和范围

拥塞信息可以是本地 buffer occupancy、credit、队列长度或远端反馈；其时效与采样范围都影响决策。自适应路由不能只说“选更空的路径”，必须明确比较哪些资源、按哪个周期观察，以及如何处理平局。

最短自适应只在 productive 方向之间选择；非最短自适应还可能绕行。多给候选路径会扩大资源依赖，也可能使仲裁更难，因此需同步考虑 escape、VC 分区和前进性。

## 2. 合法候选与最终选择可能分属不同模块

在 BookSim 中，routefunc 可以枚举多个输出 / VC 候选，IQRouter 的分配阶段再结合资源占用和优先级选择。不能看到 AddRange 多次就断言 routing function 本身已经选出“队列最短的端口”。

## 3. 自适应不能省去无死锁论证

常见方法保留一个按确定性规则前进的 escape 子网络，并规定进入后的转移限制。应核对当前 VC、escape VC 范围与自适应资源之间的转换；仅保证几何上每一步接近目的，仍不能保证资源依赖无环。

## 4. BookSim 源码拆解

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

## 5. 学习练习与实验边界

先构造一个流量热点，画出某个 router 到目标的多个 productive 方向；分别记录 relation 的候选和最终获分配的输出。增加终端阻塞后检查是否存在长期不前进的 packet，并用状态定位，而不是把任何 timeout 都解释成死锁。

## 源码与阅读导航

- [src/routefunc.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routefunc.cpp)
- [src/routers/iq_router.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routers/iq_router.cpp)
- [src/buffer_state.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/buffer_state.cpp)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](09_oblivious_routing.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 11 — Routing Mechanics｜路由表、计算与 lookahead](11_routing_mechanics.md)
