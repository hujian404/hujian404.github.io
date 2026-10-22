# Chapter 17｜Router Datapath Components

> 原书：William J. Dally、Brian Towles，*Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004），第 17 章，印刷页 325–348。本地参考 PDF 的页序为印刷页 +27。以下为中文学习整理，保留原书全部目录小节的编号与标题，不是逐句翻译。BookSim2 对照版本固定为 [`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

[专栏导读](00_Introduction.md) · [原书目录与页码对照](appendix-reading-map.md)

## 17.1 Input Buffer Organization

*原书印刷页 325。*

输入缓冲组织决定存储效率、并发访问与队头阻塞。相同总 buffer 数，按端口、VC 或共享池组织，也会产生不同的容量可达性。

### 17.1.1 Buffer Partitioning

*原书印刷页 326。*

静态分区简单但可能一部分满而另一部分闲；共享池提高统计复用，却需要空闲表、配额和防止某流独占的机制。

### 17.1.2 Input Buffer Data Structures

*原书印刷页 328。*

FIFO、链表和共享存储索引的数据结构影响读写端口、元数据和回收路径。性能仿真中的容器不应直接当成 SRAM 实现。

### 17.1.3 Input Buffer Allocation

*原书印刷页 333。*

buffer allocation 决定新 flit 或新 packet 能取得哪些槽位，需要与 VC 所有权和 backpressure 协同，而不是只比较一个全局剩余数。

## 17.2 Switches

*原书印刷页 334。*

switch 提供内部数据搬运。bus、crossbar 和小网络具有不同的并发度、面积、线长和控制代价。

### 17.2.1 Bus Switches

*原书印刷页 335。*

bus switch 共享传输媒介，结构简单但并发受到限制。增加位宽提高每次传输量，并不增加独立输入输出配对数。

### 17.2.2 Crossbar Switches

*原书印刷页 338。*

crossbar 支持多个不冲突配对同时传输；交叉点、输入扇出和输出多路选择随规模增大。

### 17.2.3 Network Switches

*原书印刷页 342。*

network switch 用内部多级连接替代全连接，降低单点 radix 或布线压力，同时引入内部冲突与额外调度。

## 17.3 Output Organization

*原书印刷页 343。*

输出可选择寄存、排队或直接接到链路。输出缓冲能吸收内部突发，但必须说明入队端口数、服务率及与下游 credit 的关系。

## 17.4 Case Study: The Datapath of the IBM Colony Router

*原书印刷页 344。*

IBM Colony router 数据通路是本章案例。读图时对照输入组织、内部交换和输出组织；软件 IQRouter 的 queue 不能作为原芯片存储结构的等价证明。

Colony 的关键是混合数据通路：先尝试输入排队的 bypass crossbar，以在低负载保持低延迟；请求失败且输入积累一个 chunk（8 flit）后，再申请共享 central memory。中央存储需要承受多个输入同时被阻塞的写入需求。这将“常见情况快路径”和“拥塞存储能力”分开，也揭示为何纯 IQRouter 不足以复刻该 router。

## 17.5 Bibliographic Notes

*原书印刷页 347。*

本节对应原书 p. 347 的文献脉络。继续查阅时应回到原书该节和书末 Bibliography，区分最初提出的方法、后续实现与本文使用的 BookSim2 版本。本文末尾源码链接是实现对照，不作为原书历史论述的替代依据。

## 17.6 Exercises

*原书印刷页 348。*

自拟练习（不复制原书习题）：手算 latency=1与3的交付时间，再沿 TrafficManager::_Step 核对 ReadInputs、Evaluate、WriteOutputs 的调度关系。修改 datapath 后重点检查“一个 flit 只移动一次”和“反向 credit 不重复”，并区分数据 channel 与 credit channel 的延迟。

## BookSim2 源码对照与适用边界

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

本章原书讨论的完整系统/电路机制超出该片段的模型范围。源码片段用于识别相近资源与接口；未实现的电路细节、服务保证或协议行为，不能由命名相似推定存在。

## 来源与继续阅读

- 原书第 17 章，pp. 325–348；各节页码已逐项列出。案例与原书公式均以本地参考书为依据。
- [BookSim2 固定版本源码](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)，节选保留[上游许可](/notes/booksim-notes/source-license.txt)。
- [全书章节/源码路线与图片来源](appendix-reading-map.md)。新增图均附 `.drawio` 源文件，插图是结构说明，不是测量波形。

[上一篇](16_router_architecture.md) · [下一篇](18_arbitration.md) · [专栏目录](/booksim-series.html)
