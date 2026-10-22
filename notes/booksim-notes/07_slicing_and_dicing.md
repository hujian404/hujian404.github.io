# Chapter 7｜Slicing and Dicing｜带宽、radix 与物理代价

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. 切分的是哪一种资源

网络可按终端集中度、链路宽度、物理子网或时间复用方式切分。把一个宽网络拆成两套窄网络，会改变链路序列化、路由器数量、消息隔离和负载分布；把更多 terminal 集中到同一 router，则减少 router 数但提高本地 radix 与竞争。

必须先声明保持不变的预算：总 pin 带宽、线资源、逻辑 buffer bits，还是目标面积。不同预算下，没有一个切分方案总是更好。

## 2. 定宽消息与 flit 数的关系

若消息需要传 M bit、每 flit 有 W bit 可用载荷，理想 flit 数为 `ceil(M/W)`，再考虑头部和协议元数据。链路变窄后如果仍保持 packet_size 不变，就相当于偷偷缩小消息，无法公平比较序列化时延。

类似地，V 个 VC、每 VC D flit 的总存储槽数是 V×D；跨不同 flit 宽度比较时应换成 bits，并说明控制位和存储映射未被简单公式覆盖。

## 3. BookSim 参数不是自动物理设计工具

`subnets` 表示复制的物理网络模型，`input_speedup`、`output_speedup` 和 `internal_speedup` 控制交换资源或内部推进能力，它们都不等同于“把每根数据线扩大若干倍”。集中式网络另有 c、xr、yr 等参数，需要结合 CMesh 构建代码理解。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/booksim_config.cpp 第 47–49 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/booksim_config.cpp#L47-L49)。

```cpp
  // Physical sub-networks
  _int_map["subnets"] = 1;

```

这里默认只创建一套子网。TrafficManager 根据消息类型、配置映射和 subnet 数决定使用哪一套网络；CMesh 的端点与 router 数也不再一一对应。实际硬件面积、功耗和时钟需要独立模型或实现结果支持，不能从 speedup 选项直接推出。

## 5. 学习练习与实验边界

设计两组同消息 bit 数、同总 buffer bits 的实验，显式换算 packet_size 和 slot 数。另做一个改变 concentration 的比较，记录每 router 的端点数、有效链路容量和注入竞争。先写换算表，再开始扫描，避免把单位变化当成收益。

## 源码与阅读导航

- [src/booksim_config.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/booksim_config.cpp)
- [src/networks/cmesh.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/cmesh.cpp)
- [src/trafficmanager.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.cpp)
- [src/power/power_module.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/power/power_module.cpp)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](06_non_blocking_networks.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 8 — Routing Basics｜从目标节点到合法资源集合](08_routing_basics.md)
