# Chapter 21｜Error Control｜可靠性机制与模型边界

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. 先定义错误，再讨论恢复

错误控制需要区分位翻转、丢失、重复、错误目的与永久链路失效。CRC 检测和 ECC 纠正针对编码错误，重传协议还需要序号、超时、ack / nack、重放 buffer 和去重。检测到错误并不等于能够恢复，也不等于模型自动包含其带宽成本。

## 2. 可靠性开销会反过来改变网络

编码冗余占用传输位数，重放缓存占用空间，重传消耗带宽，ack / nack 可能带来额外依赖。若只添加一个“错误概率”却不建模恢复流量和状态，无法评估完整恢复机制。

即使 flit 在模型中能被创建、接收和释放，也不能据此宣称已经模拟了真实 payload 的 BER、CRC 或 ECC。

## 3. 固定版本没有可直接开启的通用 BER / CRC 模型

基础 Channel<T> 按时间队列交付对象，没有默认逐位编码、位翻转、校验与重放流程。配置中的 legacy link_failures / fail_seed 也不能替代瞬态传输错误模型；部分 fault-aware routing 支持应按具体拓扑和路由单独核查。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/channel.hpp 第 91–94 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/channel.hpp#L91-L94)。

```cpp
void Channel<T>::Send(T * data) {
  _input = data;
}

```

Send 只是接受一个待交付指针，后续交付由 channel 调度完成。这里没有按比特采样错误的操作。若扩展可靠性研究，应在独立的错误 / 恢复层增加事件和统计，保留 baseline，并检查恢复消息是否需要新的 VC 隔离规则。

## 5. 学习练习与实验边界

先写清错误注入点、概率单位、是否独立、检测延迟、重传规则和可靠性交付指标。最小验证应覆盖无错等价、单次可恢复错误、重复 ack、超时、重放资源耗尽，并检查重传流量是否计入 offered / accepted。不要虚构 `crc_enable` 等不存在的配置项。

## 源码与阅读导航

- [src/channel.hpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/channel.hpp)
- [src/booksim_config.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/booksim_config.cpp)
- [src/networks/network.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/network.cpp)
- [src/flit.hpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/flit.hpp)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](20_network_interfaces.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 22 — Buses｜共享介质与交换网络的比较边界](22_buses.md)
