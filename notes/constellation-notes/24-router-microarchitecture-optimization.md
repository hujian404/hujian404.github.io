# 24｜Router Microarchitecture 优化

> 更新：2026-10-22。源码基线：[`c1b42cd`](https://github.com/ucb-bar/constellation/tree/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510)。本文按原定章节顺序展开；源码节选、教学示例与实验计划分别标明。运行版本、工具链及本次四项代表性验证见[实验复现附录](appendix-reproduction.md)；教学示意与未执行的扩展实验另行标明。

## 1. 优化必须从瓶颈证据开始

首先判断瓶颈是 RC 译码、VA 冲突、SA 竞争、credit 不足、crossbar 时序还是终端 backpressure。Router.scala 提供 VA / SA stall 调试连接与利用率采样逻辑，但计数的精确事件仍需追到 InputUnit 和 sample 的实现，不能仅凭信号名字下结论。

## 2. 可扩展点是一个生成器函数

以下为固定版本的源码节选，省略外围上下文：[查看 src/main/scala/router/Router.scala 第 23–23 行](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/router/Router.scala#L23-L23)。

```scala
  vcAllocator: VCAllocatorParams => Parameters => VCAllocator = (vP) => (p) => new RotatingSingleVCAllocator(vP)(p)
```

`vcAllocator` 的类型为 `VCAllocatorParams => Parameters => VCAllocator`：先传结构参数，再传 CDE 参数上下文，返回待实例化的模块。Router 内再调用 `Module(...)`。这种高阶函数把实现选择留在生成阶段，不是在硬件中同时放置所有 allocator 后再选择。

可从 vcalloc/ 的 SingleVCAllocator、MultiVCAllocator、ISLIP、PIM、Prioritizing 等实现对照学习。名称不同不代表在所有网络下某一个总更优，需要看支持的并行分配、状态更新、组合路径和公平性条件。

## 3. 为每项优化列出成本

| 优化候选 | 可能收益 | 成本与风险 |
| --- | --- | --- |
| 合并 pipeline | 降低 cycles | 关键路径与选择对齐 |
| 提高分配并行度 | 减少 VA 阻塞 | 仲裁复杂度、冲突处理 |
| 更改 buffer 组织 | 存储映射或读写改善 | 端口数、旁路、credit 契约 |
| 减小路由译码 | 缩短 RC 路径 | 不可删除真实合法 flow |

Chisel 中 `DontCare` 只表达不关心的信号值，不能用于掩盖有有效事务时的未驱动控制。one-hot mux 的选择应有对应断言；计数器应有界；锁定状态必须只由约定的完成事件推进。

## 4. 优化验收的四级证据

第一，结构检查通过；第二，新增边界用例与已有功能回归通过；第三，在多个负载和包长下找到一致且可解释的变化；第四，用匹配约束的综合 / 时序结果报告面积与频率。没有第四级结果时可以报告 cycle-level 改善，但不应声称提升了最终物理吞吐或降低能耗。

练习：只改变 combineSAST 或 allocator 一项，写出预期减少哪个 stall、增加哪条组合路径、哪个用例最可能暴露错误。将未达到收益的实验同样记录，形成可复查的优化笔记。

## 源码与延伸阅读

以下链接均固定到本章使用的源码版本：

- [src/main/scala/router/Router.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/router/Router.scala)
- [src/main/scala/router/vcalloc/VCAllocator.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/router/vcalloc/VCAllocator.scala)
- [src/main/scala/router/vcalloc/SingleVCAllocator.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/router/vcalloc/SingleVCAllocator.scala)
- [src/main/scala/router/SwitchAllocator.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/router/SwitchAllocator.scala)

源码节选版权归 The Regents of the University of California，遵循 [BSD-3-Clause 许可及免责声明](/notes/constellation-notes/source-license.txt)。文字解读与教学图为专栏整理内容。

---

[上一篇](23-vc-buffer-flow-control-experiments.md) · [专栏导读](00-series-guide.md)

[下一篇：25｜从 Constellation 到自己的 NoC 研究](25-from-constellation-to-noc-research.md)
