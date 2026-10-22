# Chapter 13｜Buffered Flow Control｜VC 划分与 HOL 阻塞

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. 为什么多个 VC 可能帮助前进

单一输入队列的 head 若被阻塞，后面即使要去空闲输出，也可能无法越过它，这就是 head-of-line 阻塞。多个 VC 提供独立报文上下文与队列，使某些未阻塞报文有机会继续申请资源。但它们仍共享输入、crossbar 或物理输出带宽。

## 2. 同容量比较才有解释力

比较2 VC×8 flit和4 VC×4 flit，总槽位都是16。后一种有更多独立上下文，但每 VC 更浅，可能更难覆盖 credit 往返；仲裁复杂度也不同。4 VC×8则同时加倍总容量，不能将其收益全部归因于 VC 数。

BookSim 区分 router 内 Buffer / VC 的实际队列，与上游 BufferState 对下游资源的跟踪。两者不能只按变量名 occupancy 混成同一份存储。

## 3. Private 与共享策略的边界

`buffer_policy=private` 为每 VC 设定容量，其他策略通过保留额度与共享池管理槽位。共享总容量不能替代必要的独立前进资源；协议依赖、escape 和不同类别的保证仍需保留。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/buffer_state.cpp 第 599–602 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/buffer_state.cpp#L599-L602)。

```cpp
    if(_wait_for_tail_credit && !_vc_occupancy[vc] && _tail_sent[vc]) {
      assert(_in_use_by[vc] >= 0);
      _in_use_by[vc] = -1;
    }
```

这一分支在发送过 tail 且占用降到零时释放 VC 所有者，体现了等待 tail credit 的策略。阅读时还要看 SendingFlit 中不等待的分支，否则会错误地认为所有配置都采用同一个释放时点。VC availability 与 capacity 在 VA / SA 中分别参与过滤。

## 5. 学习练习与实验边界

固定总槽位，对比2×8和4×4，并使用一个目的端阻塞、另一个目的端可前进的流量。记录每流时延、实际接收速率和阻塞来源；uniform 平均值不足以确认 HOL 传播改善。另一组再单独增加总容量，区分切分与容量效应。

## 源码与阅读导航

- [src/buffer_state.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/buffer_state.cpp)
- [src/buffer.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/buffer.cpp)
- [src/vc.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/vc.cpp)
- [src/buffer_state.hpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/buffer_state.hpp)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](12_flow_control_basics.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 14 — Deadlock and Livelock｜等待环与前进性](14_deadlock_and_livelock.md)
