# Chapter 18｜Arbitration｜一个资源选一个请求

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. 仲裁器的任务比 allocator 小

仲裁器在多个请求中为一个资源选出获胜者。固定优先级便于实现但可能饥饿，round-robin 用轮转起点改善同优先级请求的服务机会，matrix arbiter 则用相对次序表达优先级状态。

公平性需要附加条件：请求持续存在、资源最终可服务、优先级没有无限压制。若下游一直不能接收，不能用轮询指针存在来保证该请求有限时间完成。

## 2. 指针何时更新决定服务语义

生成一个 grant 和真正完成服务是不同事件。硬件或模拟器应规定在申请、grant、accept 还是成功传输后更新状态。更新过早可能跳过未完成请求，更新过晚则可能反复偏向同一请求。

## 3. 相同仲裁器放在不同竞争点，效果不同

输入端选择 VC、输出端选择输入、VC allocator 内部仲裁都可能使用相似算法，但请求集合和持有时间不同。packet 级锁定还会让长包占用更久。不能只凭 arb_type 名称推导整网公平性。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/arbiters/roundrobin_arb.cpp 第 50–54 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/arbiters/roundrobin_arb.cpp#L50-L54)。

```cpp
void RoundRobinArbiter::UpdateState() {
  // update priority matrix using last grant
  if ( _selected > -1 )
    _pointer = ( _selected + 1 ) % _size ;
}
```

当 selected 有效时，pointer 更新到获胜输入的下一位置。仲裁器将选择和 UpdateState 分开提供，调用者应决定何时提交状态更新；需要继续到 separable allocator 中追调用，而不是假定 Arbitrate 本身已经推进指针。带显式 pri 时还要检查不同优先级如何覆盖轮转顺序。

## 5. 学习练习与实验边界

用三个同优先级持续请求画出6次服务序列；再插入一次“grant未被接受”，比较更新和不更新指针的差别。最后加入一个更高 priority 的请求，解释轮询为何不一定保证低优先级带宽。

## 源码与阅读导航

- [src/arbiters/roundrobin_arb.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/arbiters/roundrobin_arb.cpp)
- [src/arbiters/arbiter.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/arbiters/arbiter.cpp)
- [src/allocators/separable_input_first.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/allocators/separable_input_first.cpp)
- [src/allocators/separable_output_first.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/allocators/separable_output_first.cpp)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](17_router_datapath_components.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 19 — Allocation｜从局部仲裁到二分图匹配](19_allocation.md)
