# Chapter 20｜Network Interfaces

> 原书：William J. Dally、Brian Towles，*Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004），第 20 章，印刷页 389–410。本地参考 PDF 的页序为印刷页 +27。以下为中文学习整理，保留原书全部目录小节的编号与标题，不是逐句翻译。BookSim2 对照版本固定为 [`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

[专栏导读](00_Introduction.md) · [原书目录与页码对照](appendix-reading-map.md)

## 20.1 Processor-Network Interface

*原书印刷页 390。*

processor-network interface 把程序或事务转换为网络消息。寄存器访问次数、排队、拷贝、阻塞和通知机制会进入端到端开销。

### 20.1.1 Two-Register Interface

*原书印刷页 391。*

two-register interface 用极小接口交付数据和状态，硬件简单，但处理器可能需要较多显式操作。

### 20.1.2 Register-Mapped Interface

*原书印刷页 392。*

register-mapped interface 提供更丰富的控制和数据寄存器，要定义并发访问、所有权与内存可见顺序。

### 20.1.3 Descriptor-Based Interface

*原书印刷页 393。*

descriptor-based interface 由描述符交付消息范围和控制信息，可减少逐字软件操作，代价是描述符管理及取数延迟。

### 20.1.4 Message Reception

*原书印刷页 393。*

接收端要安排落地缓冲、通知和消费进度。网络已经到达不等于软件已经可以安全读取完整消息。

## 20.2 Shared-Memory Interface

*原书印刷页 394。*

共享存储接口将 load/store、一致性消息和内存请求映射到网络。协议依赖会改变消息方向、大小和资源类别。

### 20.2.1 Processor-Network Interface

*原书印刷页 395。*

处理器侧接口需保留未完成事务与返回关联，并在网络 backpressure 下保持正确顺序。

### 20.2.2 Cache Coherence

*原书印刷页 397。*

cache coherence 将一个访问扩展成请求、探测、数据和确认等事务。独立合成流量不能自动再现这些因果关系。

### 20.2.3 Memory-Network Interface

*原书印刷页 398。*

内存侧接口还受控制器队列和存储服务率限制；热点 memory controller 可能成为瓶颈，即使网络内部链路未饱和。

## 20.3 Line-Fabric Interface

*原书印刷页 400。*

line-fabric interface 把外部线路数据组织成内部 fabric 单位，涉及分段、重组、整形和队列；fabric 的 flit 到达不能替代整包外部交付完成。

## 20.4 Case Study: The MIT M-Machine Network Interface

*原书印刷页 403。*

MIT M-Machine network interface 是本章案例。它与第 5 章 J-Machine 不同；阅读时追踪软件操作、消息进入网络和接收通知的完整边界。

M-Machine 的 MAP 节点把多线程处理器、cache、memory controller、network interface 和 2-D Torus router 集成起来。线程先在连续寄存器中组成消息，再执行 SEND；指令携带长度、目标与 handler 等信息。网络接口因此不是一个无代价的 TrafficManager 注入函数，而是软件指令、地址解释和接收处理之间的契约。

## 20.5 Bibliographic Notes

*原书印刷页 407。*

本节对应原书 p. 407 的文献脉络。继续查阅时应回到原书该节和书末 Bibliography，区分最初提出的方法、后续实现与本文使用的 BookSim2 版本。本文末尾源码链接是实现对照，不作为原书历史论述的替代依据。

## 20.6 Exercises

*原书印刷页 408。*

自拟练习（不复制原书习题）：在教学时间线 ctime=0、head itime=3、tail atime=10 上，算出 packet latency=10、network latency=7、源端等待=3。再追一个 request-reply 事务的目的和返回生成时机，说明其中没有被模型表达的真实系统功能。

## BookSim2 源码对照与适用边界

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/flit.hpp 第 56–63 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/flit.hpp#L56-L63)。

```cpp
  int  ctime;
  int  itime;
  int  atime;

  int  id;
  int  pid;

  bool record;
```

Flit 同时保存 id、pid、src / dest、head / tail、cl 等字段；TrafficManager::_GeneratePacket 设置创建信息，_Step 在真实发送时设置 itime，接收时写 atime。不同统计对象的起止事件见第23章，不能只把所有输出都叫 network latency。

本章原书讨论的完整系统/电路机制超出该片段的模型范围。源码片段用于识别相近资源与接口；未实现的电路细节、服务保证或协议行为，不能由命名相似推定存在。

## 来源与继续阅读

- 原书第 20 章，pp. 389–410；各节页码已逐项列出。案例与原书公式均以本地参考书为依据。
- [BookSim2 固定版本源码](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)，节选保留[上游许可](/notes/booksim-notes/source-license.txt)。
- [全书章节/源码路线与图片来源](appendix-reading-map.md)。新增图均附 `.drawio` 源文件，插图是结构说明，不是测量波形。

[上一篇](19_allocation.md) · [下一篇](21_error_control.md) · [专栏目录](/booksim-series.html)
