# Chapter 14｜Deadlock and Livelock｜等待环与前进性

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. 不前进有多种原因

Deadlock 是资源互等形成无法解除的循环；livelock 是持续移动却不能到达目的；starvation 是有机会却长期未获服务。过载导致源端队列持续增长又是另一种现象。看到仿真 timeout，第一步应是定位 packet、VC 和等待资源，而不是立即把它命名为死锁。

## 2. 资源依赖图的顶点是 channel / VC

当一个 packet 保持资源 A 时可以请求 B，就建立 A→B。VC 级依赖图与 router 物理拓扑不同：物理环可以通过单调 VC 类别或转向限制打断，增加物理路径也可能新增资源依赖。

对规则 Mesh，维序路由在每维单调前进且按固定维度次序转换，可用这种顺序说明依赖不会回到更早阶段。Torus 则有回绕，要额外处理同维环。这个论证依赖所允许的转移，不能仅凭几何距离下降判断。

## 3. 协议依赖需要额外检查

请求可能等待响应释放事务，而响应又需要被请求占住的资源，形成协议层循环。BookSim 的 read/write 消息类别和 VC 区间为建模提供入口，但它不自动等价于完整 TileLink 或 AXI4 adapter 的一致性与顺序实现。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/booksim_config.cpp 第 197–206 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/booksim_config.cpp#L197-L206)。

```cpp
  // Control assignment of packets to VCs
  _int_map["read_request_begin_vc"] = 0;
  _int_map["read_request_end_vc"] = 5;
  _int_map["write_request_begin_vc"] = 2;
  _int_map["write_request_end_vc"] = 7;
  _int_map["read_reply_begin_vc"] = 8;
  _int_map["read_reply_end_vc"] = 13;
  _int_map["write_reply_begin_vc"] = 10;
  _int_map["write_reply_end_vc"] = 15;

```

默认配置为 read request、write request、read reply 等定义 begin/end VC 区间。部分默认区间相互重叠，并且针对默认 VC 数；改变 num_vcs 或 use_read_write 后必须重新核对，不能把默认值当作任意配置的无死锁保证。该版本也没有像 Constellation 那样在生成前统一验证任意 routing relation 的流程。

## 5. 学习练习与实验边界

为一个单向环画具体 VC 的等待图，再用两类 VC 和转移限制尝试切断循环。运行时保存 head 所占资源和等待请求的快照；若只因 latency_thres 中止，应先区分性能门槛与真正循环。随机仿真通过不替代对允许转移的论证。

## 源码与阅读导航

- [src/booksim_config.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/booksim_config.cpp)
- [src/routefunc.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routefunc.cpp)
- [src/trafficmanager.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.cpp)
- [src/flit.hpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/flit.hpp)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](13_buffered_flow_control.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 15 — Quality of Service｜优先级、隔离与保证](15_quality_of_service.md)
