# Chapter 12｜Flow Control Basics｜存储槽与发送许可

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. 路由决定去哪里，流控决定能否发送

即使 packet 已经知道下一跳，也必须确认下游具有可用存储资源。否则 flit 会丢失或覆盖未消费数据。常见流控分别在 packet、flit 或更大资源块上分配许可，其缓存需求与阻塞传播不同。

Store-and-forward 等完整 packet 到齐再转发；cut-through 尝试在 packet 未完全到齐前前进；wormhole 允许很小的逐跳缓冲，但一个 packet 会同时占用多跳资源。它减少完整报文缓冲需求，却扩大阻塞传播范围。

## 2. Credit 是对下游容量的认识

发送方维护下游占用或剩余容量，发送时消耗许可，接收方释放槽位时返回 credit。若深度 D、许可往返 R 拍、每拍最多发送一个 flit，在无争用的简化模型中，可持续速率受 `min(1,D/R)` 的量级约束。这里 R 包括相关流水和返回过程，不是只看一条线的延迟。

## 3. VC 所有权与剩余槽位不同

一个输出 VC 可能仍属于前一个 packet，但已经空出几个槽。新 head 是否能占用它，不能仅根据 buffer 没满判断。tail 的发送和 tail credit 的到达也可能对应不同的资源释放时点。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/buffer_state.cpp 第 620–632 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/buffer_state.cpp#L620-L632)。

```cpp
void BufferState::SendingFlit( Flit const * const f )
{
  int const vc = f->vc;

  assert( f && ( vc >= 0 ) && ( vc < _vcs ) );

  ++_occupancy;
  if(_occupancy > _size) {
    Error("Buffer overflow.");
  }

  ++_vc_occupancy[vc];

```

BufferState 在发送时更新占用，并把 buffer policy 的容量逻辑与报文所有权关联起来。继续读 ProcessCredit、TakeBuffer 和 `wait_for_tail_credit` 分支：BookSim 的该选项决定是否等待 tail 的存储返回后才允许重用 VC，不应直接照搬其他 NoC 的释放语义。

## 5. 学习练习与实验边界

用深度2的单 VC 手写发送、在途、下游排队与返回事件，检查每个槽位许可只消耗 / 返还一次。随后增加 credit_delay，观察连续发送是否出现气泡。不要把某个负载下降归因于路由，先检查许可往返是否被 buffer 深度覆盖。

## 源码与阅读导航

- [src/buffer_state.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/buffer_state.cpp)
- [src/credit.hpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/credit.hpp)
- [src/routers/iq_router.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routers/iq_router.cpp)
- [src/booksim_config.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/booksim_config.cpp)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](11_routing_mechanics.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 13 — Buffered Flow Control｜VC 划分与 HOL 阻塞](13_buffered_flow_control.md)
