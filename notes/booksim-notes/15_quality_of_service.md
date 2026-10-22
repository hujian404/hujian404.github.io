# Chapter 15｜Quality of Service｜优先级、隔离与保证

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. QoS 不等于给报文加一个 priority

QoS 可能关注最低服务率、最大等待时间、尾延迟、流量隔离或公平性。这些目标不同，需要不同的 admission、调度或资源保留机制。平均 latency 下降不说明每一类业务都改善，更不能据此声称具备最坏时延保证。

严格优先级会让高优先业务先获得资源，但持续高负载可能饿死低优先业务；年龄策略有助于避免长期等待，却仍取决于实现的优先级更新、下游可用性和服务模型。

## 2. 分清类别、VC 和物理子网

class 表示统计与策略类别；VC 是逻辑资源；subnet 是独立网络模型。它们可以映射，但不要求编号相等。共享 VC / 链路时仍会相互影响，完全独立子网也会花费额外硬件预算。

要讨论保证，需说明输入负载上界、burst 限制、buffer 保留和每级服务约束。没有这些条件，仿真中的优先级只能说明特定负载下的策略效果。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/trafficmanager.cpp 第 78–93 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.cpp#L78-L93)。

```cpp
    if ( priority == "class" ) {
        _pri_type = class_based;
    } else if ( priority == "age" ) {
        _pri_type = age_based;
    } else if ( priority == "network_age" ) {
        _pri_type = network_age_based;
    } else if ( priority == "local_age" ) {
        _pri_type = local_age_based;
    } else if ( priority == "queue_length" ) {
        _pri_type = queue_length_based;
    } else if ( priority == "hop_count" ) {
        _pri_type = hop_count_based;
    } else if ( priority == "sequence" ) {
        _pri_type = sequence_based;
    } else if ( priority == "none" ) {
        _pri_type = none;
```

TrafficManager 将配置字符串映射为 class、age、network_age、local_age 等模式，生成 flit 时写入 pri。后续优先级还要进入 router / allocator 的请求规则；没有进入真正竞争点的标签不会带来调度效果。统计应按 class 和最差流分别读，不能只合并所有样本。

## 5. 学习练习与实验边界

构造两个业务类，先在相同负载下比较无优先级与 class priority，再持续提高高优先级流量。记录低优先级接收率与最长等待，检查是否存在 starvation。将结果称为经验性隔离或调度效果，而不是未经证明的确定性 QoS 保证。

## 源码与阅读导航

- [src/trafficmanager.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.cpp)
- [src/flit.hpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/flit.hpp)
- [src/routers/iq_router.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routers/iq_router.cpp)
- [src/booksim_config.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/booksim_config.cpp)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](14_deadlock_and_livelock.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 16 — Router Architecture｜流水线中的状态与事件](16_router_architecture.md)
