# Chapter 7｜Slicing and Dicing

> 原书：William J. Dally、Brian Towles，*Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004），第 7 章，印刷页 145–158。本地参考 PDF 的页序为印刷页 +27。以下为中文学习整理，保留原书全部目录小节的编号与标题，不是逐句翻译。BookSim2 对照版本固定为 [`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

[专栏导读](00_Introduction.md) · [原书目录与页码对照](appendix-reading-map.md)

## 7.1 Concentrators and Distributors

*原书印刷页 146。*

集中器减少连接到后续网络的入口数，分配器把流分散到后续资源。入口数减少会提高共享程度，任何面积节省都必须与带宽和阻塞一起评估。

### 7.1.1 Concentrators

*原书印刷页 146。*

多个 terminal 汇入较少网络入口时，要计算各终端同时活跃的负载。只减少 router 数、不报告 concentration factor，会造成吞吐比较失真。

### 7.1.2 Distributors

*原书印刷页 148。*

distributor 的作用是把通信分布到可用入口或网络资源；它与只决定目的地的路由译码不同，其策略会影响后续 channel load。

## 7.2 Slicing and Dicing

*原书印刷页 149。*

slicing 改变数据位、维度或 channel 在物理资源上的分配。应分别写出一次消息如何跨切片、各切片怎样同步，以及是否增加序列化时间。

### 7.2.1 Bit Slicing

*原书印刷页 149。*

bit slicing 把同一个逻辑字的不同位分到不同切片；需要对齐、deskew 和一致的控制。它不等价于多个彼此独立发送完整 packet 的网络。

### 7.2.2 Dimension Slicing

*原书印刷页 151。*

dimension slicing 按维度划分实现资源，把高 radix 节点的连接压力分摊开；维度之间的交接可能增加内部转发和物理延迟。

### 7.2.3 Channel Slicing

*原书印刷页 152。*

channel slicing 将逻辑连接按 channel 划分实现，区别于把一条 channel 的数据位拆开。比较时需要保持逻辑带宽和调度假设一致。

## 7.3 Slicing Multistage Networks

*原书印刷页 153。*

在多级网络中，切片要沿级间对应关系保持正确连接。封装节省不能只数一个 switch，还需把跨级控制、同步和重组成本算进去。

## 7.4 Case Study: Bit Slicing in the Tiny Tera

*原书印刷页 155。*

Tiny Tera 的 bit slicing 案例用来说明宽交换数据通路如何跨器件组织。BookSim 的 subnets 或 speedup 只有在传输语义匹配时才可作近似，不能仅凭名称视为原设计的位切片复现。

Tiny Tera 以 32×32、8-bit-wide crossbar 为核心，port card 负责输入/输出缓冲，中央 scheduler 决定 crossbar 配置。原书特别区分 advertised aggregate bandwidth 与单方向有效 throughput：把输入和输出带宽相加得到的 1 Tbit/s，不能当成 1 Tbit/s 单向交付率。位切片还要求各切片执行同一调度，才能在输出重组。

## 7.5 Bibliographic Notes

*原书印刷页 157。*

本节对应原书 p. 157 的文献脉络。继续查阅时应回到原书该节和书末 Bibliography，区分最初提出的方法、后续实现与本文使用的 BookSim2 版本。本文末尾源码链接是实现对照，不作为原书历史论述的替代依据。

## 7.6 Exercises

*原书印刷页 157。*

自拟练习（不复制原书习题）：设计两组同消息 bit 数、同总 buffer bits 的实验，显式换算 packet_size 和 slot 数。另做一个改变 concentration 的比较，记录每 router 的端点数、有效链路容量和注入竞争。先写换算表，再开始扫描，避免把单位变化当成收益。

## BookSim2 源码对照与适用边界

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/booksim_config.cpp 第 47–49 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/booksim_config.cpp#L47-L49)。

```cpp
  // Physical sub-networks
  _int_map["subnets"] = 1;

```

这里默认只创建一套子网。TrafficManager 根据消息类型、配置映射和 subnet 数决定使用哪一套网络；CMesh 的端点与 router 数也不再一一对应。实际硬件面积、功耗和时钟需要独立模型或实现结果支持，不能从 speedup 选项直接推出。

本章原书讨论的完整系统/电路机制超出该片段的模型范围。源码片段用于识别相近资源与接口；未实现的电路细节、服务保证或协议行为，不能由命名相似推定存在。

## 来源与继续阅读

- 原书第 7 章，pp. 145–158；各节页码已逐项列出。案例与原书公式均以本地参考书为依据。
- [BookSim2 固定版本源码](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)，节选保留[上游许可](/notes/booksim-notes/source-license.txt)。
- [全书章节/源码路线与图片来源](appendix-reading-map.md)。新增图均附 `.drawio` 源文件，插图是结构说明，不是测量波形。

[上一篇](06_non_blocking_networks.md) · [下一篇](08_routing_basics.md) · [专栏目录](/booksim-series.html)
