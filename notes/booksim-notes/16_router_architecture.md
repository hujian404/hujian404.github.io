# Chapter 16｜Router Architecture｜流水线中的状态与事件

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. 从输入缓冲到输出 channel

经典输入缓冲 VC router 包含输入队列、路由计算、VC allocation、switch allocation 和 switch traversal。Head 建立下一跳资源绑定，body / tail 继承上下文，但每个 flit 仍需获得发送机会和 credit。

路由器的性能不只取决于 stage 数：端口数、VC 数、仲裁实现、buffer 访问和长线共同约束周期时间。周期级模型省掉一拍，并不能直接证明实际硬件的纳秒时延更低。

## 2. Evaluate / Update 组织模拟时序

![BookSim 周期对象关系](pic/02-model/simulation-model.svg)

IQRouter 将多个 stage 的 Evaluate 与 Update 分开，并用队列记录计划完成时间。这样在同一模拟周期内，多个模块能够基于受控的状态观察计算结果，而不被宿主机函数调用先后无意改变。

## 3. 三种 speedup 的不同作用

input_speedup 增加输入向交换结构提供的逻辑机会，output_speedup 改变输出并行资源，internal_speedup 影响内部推进与外部周期之间的关系。它们可能要求额外 output buffering；不能将其中任一值直接解释为端口 payload 位宽。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/routers/iq_router.cpp 第 226–244 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routers/iq_router.cpp#L226-L244)。

```cpp
void IQRouter::_InternalStep( )
{
  if(!_active) {
    return;
  }

  _InputQueuing( );
  bool activity = !_proc_credits.empty();

  if(!_route_vcs.empty())
    _RouteEvaluate( );
  if(_vc_allocator) {
    _vc_allocator->Clear();
    if(!_vc_alloc_vcs.empty())
      _VCAllocEvaluate( );
  }
  if(_hold_switch_for_packet) {
    if(!_sw_hold_vcs.empty())
      _SWHoldEvaluate( );
```

先进行 InputQueuing，再按待处理队列启动 RC、VA、SA 和 traversal 的 Evaluate，后半段对应 Update。某队列为空时跳过工作是模拟优化，不代表硬件不存在。读一个 stall 时要找到请求何时被排入、何时被判定可完成、何时真正更新绑定。

## 5. 学习练习与实验边界

固定单 flow 和4-flit packet，从 head 的路由队列开始列出每级完成时间。再增加另一个输入竞争同一输出，说明新增等待属于 VA、SA 还是 credit。对 speedup 或 speculation 的比较应同时说明额外存储和模型时序假设。

## 源码与阅读导航

- [src/routers/iq_router.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routers/iq_router.cpp)
- [src/routers/iq_router.hpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routers/iq_router.hpp)
- [src/vc.hpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/vc.hpp)
- [src/booksim_config.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/booksim_config.cpp)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](15_quality_of_service.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 17 — Router Datapath Components｜队列、crossbar 与链路](17_router_datapath_components.md)
