# Chapter 17｜Router Datapath Components｜队列、crossbar 与链路

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. 数据通路和资源控制要一起读

数据通路包括输入 buffer、交换选择、输出队列和 channel；控制通路包括 VC 状态、分配请求、grant、credit 和 packet 绑定。只看到 flit 从一个容器移动到另一个容器，还不足以确认为什么允许这次发送。

多个输入可以同时请求同一个输出，但一个普通输出 lane 每拍只能选择一个输入。增加 crossbar speedup 后，逻辑匹配约束会变化，不能仍用单 lane 的吞吐上限解释所有配置。

## 2. 模型对象不等于真实 SRAM / 线网

BookSim 的 Buffer 和 VC 使用软件容器保存 flit。它们可准确组织预定周期事件，却不会自动推导 SRAM 读写端口、寄存器实现、布线拥塞和时钟。使用功耗模块时也要核对工艺、活动率和参数来源。

## 3. Channel 如何表达延迟

Channel<T> 可以传递 Flit 或 Credit，队列保存预定交付时间。发送调用、ReadInputs 和 WriteOutputs 分属模型流程；单纯在 Send 调用之后立刻调用 Receive，不等于一个完整网络周期。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/channel.hpp 第 101–107 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/channel.hpp#L101-L107)。

```cpp
void Channel<T>::ReadInputs() {
  if(_input) {
    _wait_queue.push(make_pair(GetSimTime() + _delay - 1, _input));
    _input = 0;
  }
}

```

非空输入被放入带交付时间的 wait_queue，WriteOutputs 只有在对应 GetSimTime 时才暴露它。`delay−1` 要结合外层调度读，不能只看这一项就断言配置1拍链路其实为零延迟。SetLatency 还要求正数，链路不能通过该接口随意设为0。

## 5. 学习练习与实验边界

手算 latency=1与3的交付时间，再沿 TrafficManager::_Step 核对 ReadInputs、Evaluate、WriteOutputs 的调度关系。修改 datapath 后重点检查“一个 flit 只移动一次”和“反向 credit 不重复”，并区分数据 channel 与 credit channel 的延迟。

## 源码与阅读导航

- [src/channel.hpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/channel.hpp)
- [src/buffer.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/buffer.cpp)
- [src/vc.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/vc.cpp)
- [src/flitchannel.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/flitchannel.cpp)
- [src/routers/iq_router.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routers/iq_router.cpp)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](16_router_architecture.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 18 — Arbitration｜一个资源选一个请求](18_arbitration.md)
