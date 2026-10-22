# Chapter 19｜Allocation

> 原书：William J. Dally、Brian Towles，*Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004），第 19 章，印刷页 363–388。本地参考 PDF 的页序为印刷页 +27。以下为中文学习整理，保留原书全部目录小节的编号与标题，不是逐句翻译。BookSim2 对照版本固定为 [`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

[专栏导读](00_Introduction.md) · [原书目录与页码对照](appendix-reading-map.md)

## 19.1 Representations

*原书印刷页 363。*

allocation 同时匹配多个申请者和资源。用二部图表示输入—输出请求，每个单位容量端点至多被选一次；arbiter 只解决其中一个局部冲突。

## 19.2 Exact Algorithms

*原书印刷页 366。*

maximum matching 追求最大匹配数，maximal matching 只保证不能再直接加入边。前者一般需要更复杂搜索，不能因为结果无冲突就称为最大。

![局部极大与最大匹配的区别](pic/19-allocation/bipartite-matching.svg)

*图 19-A：原创二部图算例。请求为 I0→O0、I0→O1、I1→O0；只取 I0→O0 得到大小 1 的极大匹配，改为 I0→O1 与 I1→O0 则为大小 2 的最大匹配。*

## 19.3 Separable Allocators

*原书印刷页 367。*

separable allocator 将二维匹配拆为两组局部仲裁。先输入后输出与反向顺序会限制不同候选，局部公平不自动得到全局满吞吐。

### 19.3.1 Parallel Iterative Matching

*原书印刷页 371。*

PIM 通过请求、grant、accept 的迭代增加匹配。迭代数影响质量和控制时间，比较时应保持每拍可执行的工作量一致。

### 19.3.2 iSLIP

*原书印刷页 371。*

iSLIP 使用轮转指针和规定的指针更新时机来减少长期冲突。阅读实现时核对 accept 后哪些指针更新，而不是把所有 grant 都算成服务。

### 19.3.3 Lonely Output Allocator

*原书印刷页 372。*

lonely output allocator 优先利用竞争少的输出，尝试减少局部选择浪费。评价仍需覆盖不同请求矩阵和长期流量。

## 19.4 Wavefront Allocator

*原书印刷页 373。*

wavefront 以有序传播的方式确定不冲突分配。传播方向、起点变化与实现深度一起影响时序和公平。

## 19.5 Incremental vs. Batch Allocation

*原书印刷页 376。*

incremental 每次基于已有分配补充资源，batch 则对一批请求整体安排。两者对释放时机、重算成本和等待时间的影响不同。

## 19.6 Multistage Allocation

*原书印刷页 378。*

多级分配要使各级选择相容。第一级成功不代表完整端到端分配成功，可能需要保留、撤销或重试状态。

## 19.7 Performance of Allocators

*原书印刷页 380。*

除单次匹配数外，还应测长期吞吐、公平、延迟、迭代次数及逻辑复杂度。某个小图的最大匹配不能证明特定 allocator 对任意 traffic 都最优。

## 19.8 Case Study: The Tiny Tera Allocator

*原书印刷页 383。*

Tiny Tera allocator 案例将调度算法与高速交换控制结合。对照原书的请求模型及实现预算，再判断 BookSim allocator 能覆盖其中哪些行为。

Tiny Tera 为 32-port crossbar 采用 output-first 的三轮 iSLIP，需在每次约 51 ns 的配置周期内完成。原书优化利用第一阶段输出仲裁的结果提前生成输入匹配 mask，使多轮工作能够流水交叠。性能模型中多做几轮循环只是算法效果，若不相应建模控制时序，就没有体现这项实现代价。

## 19.9 Bibliographic Notes

*原书印刷页 385。*

本节对应原书 p. 385 的文献脉络。继续查阅时应回到原书该节和书末 Bibliography，区分最初提出的方法、后续实现与本文使用的 BookSim2 版本。本文末尾源码链接是实现对照，不作为原书历史论述的替代依据。

## 19.10 Exercises

*原书印刷页 386。*

自拟练习（不复制原书习题）：在图示请求矩阵上手动跑一轮和多轮 grant / accept，记录匹配边和指针。对比不同 allocator 时同时保存输入图、priority 和最终 matching，避免仅凭全网 throughput 猜测某次仲裁为什么失败。

## BookSim2 源码对照与适用边界

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/allocators/islip.cpp 第 56–64 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/allocators/islip.cpp#L56-L64)。

```cpp
  for ( int iter = 0; iter < _iSLIP_iter; ++iter ) {
    // Grant phase

    vector<int> grants(_outputs, -1);

    for ( output = 0; output < _outputs; ++output ) {

      // Skip loop if there are no requests
      // or the output is already matched
```

每轮会跳过已经匹配的输出，再进行 grant 和 accept。VA 的资源通常是输出 VC，SA 的资源通常是交换端口或展开后的 lane；两张请求图的维度和许可约束不同。对照 `Allocator::NewAllocator` 可核对 islip、pim、separable_input_first 等准确配置名。

## 来源与继续阅读

- 原书第 19 章，pp. 363–388；各节页码已逐项列出。案例与原书公式均以本地参考书为依据。
- [BookSim2 固定版本源码](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)，节选保留[上游许可](/notes/booksim-notes/source-license.txt)。
- [全书章节/源码路线与图片来源](appendix-reading-map.md)。新增图均附 `.drawio` 源文件，插图是结构说明，不是测量波形。

[上一篇](18_arbitration.md) · [下一篇](20_network_interfaces.md) · [专栏目录](/booksim-series.html)
