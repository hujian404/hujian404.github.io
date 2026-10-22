# Chapter 11｜Routing Mechanics｜路由表、计算与 lookahead

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. 算法相同，实现时序仍可能不同

同一 DOR 算法可以通过组合计算、表查询或提前计算实现。关键差别是输入信息、逻辑开销、计算位置和流水线边界。硬件中一个查表拍与软件模型中一次函数调用不是同一时间单位。

在 BookSim 中，routing_delay 是建模的周期参数；函数调用在宿主机消耗多少 CPU 时间，不等于被模拟的 router 花了多少周期。

## 2. Lookahead 把下一跳信息提前准备

前一跳可以在发送 head 时准备下一 router 的路由信息，使接收方省去独立 RC 阶段。它需要知道下一跳输入位置和目标信息，还要保持候选信息与报文一致。routing_delay=0 因而不能简单解释为“路由逻辑在物理上零延迟”。

## 3. 追一条完整控制链

阅读顺序是 routing 注册键 → flit / VC 路由状态 → OutputSet → VA 请求。若使用 lookahead，还要追 `la_route_set` 的生成和消费。修改地址编码或端口编号时，应同时检查这些边界。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/routers/iq_router.cpp 第 76–82 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routers/iq_router.cpp#L76-L82)。

```cpp
  string const rf = config.GetStr("routing_function") + "_" + config.GetStr("topology");
  map<string, tRoutingFunction>::const_iterator rf_iter = gRoutingFunctionMap.find(rf);
  if(rf_iter == gRoutingFunctionMap.end()) {
    Error("Invalid routing function: " + rf);
  }
  _rf = rf_iter->second;

```

构造函数把算法名和拓扑拼成唯一键，从全局 map 获取函数指针；找不到会直接报错。后续 `_RouteEvaluate` / `_RouteUpdate` 分开实现时序，lookahead 信息保存在 Flit 的 `la_route_set`。读软件循环时要同时看计划完成时间，而非把函数先后顺序当作流水拍数。

## 5. 学习练习与实验边界

固定网络、VC 和负载，只比较 routing_delay=1 与0，核对路径不变时零负载时延发生什么变化。若实验涉及物理意义，再说明省略 RC 拍需要何种提前计算假设，不能只报告 simulator 更快的数值。

## 源码与阅读导航

- [src/routers/iq_router.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routers/iq_router.cpp)
- [src/flit.hpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/flit.hpp)
- [src/routefunc.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routefunc.cpp)
- [src/vc.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/vc.cpp)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](10_adaptive_routing.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 12 — Flow Control Basics｜存储槽与发送许可](12_flow_control_basics.md)
