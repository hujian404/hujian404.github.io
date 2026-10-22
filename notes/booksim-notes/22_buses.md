# Chapter 22｜Buses

> 原书：William J. Dally、Brian Towles，*Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004），第 22 章，印刷页 427–448。本地参考 PDF 的页序为印刷页 +27。以下为中文学习整理，保留原书全部目录小节的编号与标题，不是逐句翻译。BookSim2 对照版本固定为 [`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

[专栏导读](00_Introduction.md) · [原书目录与页码对照](appendix-reading-map.md)

## 22.1 Bus Basics

*原书印刷页 428。*

bus 让多个参与者共享传输媒介，连接和寻址简单，但争用、负载电容及广播范围限制扩展。对比网络时应固定终端数、消息大小和有效数据率。

## 22.2 Bus Arbitration

*原书印刷页 432。*

bus arbitration 决定谁获得共享媒介，需要定义集中/分布式实现、授予时序和保持长度。按 burst 占用的公平性不同于逐 beat 公平。

## 22.3 High Performance Bus Protocol

*原书印刷页 436。*

高性能协议通过重叠、解耦和突发减少控制开销，但同时增加事务标识、排队及完成排序的复杂度。

### 22.3.1 Bus Pipelining

*原书印刷页 436。*

pipelining 重叠多个事务的不同阶段，提高吞吐；单个事务延迟未必同比降低，且必须处理流水中的等待和取消。

### 22.3.2 Split-Transaction Buses

*原书印刷页 438。*

split transaction 将请求与较晚响应分开，使等待目标服务时不必一直占住总线；需要关联 ID 和未完成事务状态。

### 22.3.3 Burst Messages

*原书印刷页 439。*

burst 让一次控制开销覆盖多次数据传输，提高长消息效率，但可能延长其他请求者等待时间。

## 22.4 From Buses to Networks

*原书印刷页 441。*

从 bus 到网络意味着从一个共享仲裁点变为分布式路径和资源管理。协议的广播、顺序与事务依赖必须重新映射，不能只替换物理线。

## 22.5 Case Study: The PCI Bus

*原书印刷页 443。*

PCI bus 案例把前述基本机制落实为实际总线协议。本章原书案例是 PCI，不能直接当作 PCI Express 分组网络的描述。

原书 PCI 是同步、复用 address/data 线且支持流水仲裁的共享总线；burst 把地址/控制开销摊到多个数据阶段。学习时应把一次交易的地址阶段、数据阶段、等待与所有权切换画在同一时序上，再与 split-transaction 思想对照。这里的历史参数只用于原书案例，不代表当前 PCIe 的链路或事务规则。

## 22.6 Bibliographic Notes

*原书印刷页 446。*

本节对应原书 p. 446 的文献脉络。继续查阅时应回到原书该节和书末 Bibliography，区分最初提出的方法、后续实现与本文使用的 BookSim2 版本。本文末尾源码链接是实现对照，不作为原书历史论述的替代依据。

## 22.7 Exercises

*原书印刷页 446。*

自拟练习（不复制原书习题）：以4个节点、每报文4 flit为例，分别按 flit 级仲裁和 packet 级锁定手算服务次序。与单级 crossbar 对比时给相同的总带宽 / 成本预算；如需仿真 bus，先新增独立模型并做容量守恒测试。

## BookSim2 源码对照与适用边界

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/networks/network.cpp 第 93–100 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/network.cpp#L93-L100)。

```cpp
  } else if ( topo == "fly" ) {
    KNFly::RegisterRoutingFunctions() ;
    n = new KNFly( config, name );
  } else if ( topo == "qtree" ) {
    QTree::RegisterRoutingFunctions() ;
    n = new QTree( config, name );
  } else if ( topo == "tree4" ) {
    Tree4::RegisterRoutingFunctions() ;
```

factory 是核对网络模型支持范围的入口。若实现 bus，应把每个时隙 / 事务可获得的全局服务许可、占用时间与端点队列显式建模，而不是只把不同端点接到同一 router。还要定义广播复制是否消耗额外服务机会。

本章原书讨论的完整系统/电路机制超出该片段的模型范围。源码片段用于识别相近资源与接口；未实现的电路细节、服务保证或协议行为，不能由命名相似推定存在。

## 来源与继续阅读

- 原书第 22 章，pp. 427–448；各节页码已逐项列出。案例与原书公式均以本地参考书为依据。
- [BookSim2 固定版本源码](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)，节选保留[上游许可](/notes/booksim-notes/source-license.txt)。
- [全书章节/源码路线与图片来源](appendix-reading-map.md)。新增图均附 `.drawio` 源文件，插图是结构说明，不是测量波形。

[上一篇](21_error_control.md) · [下一篇](23_performance_analysis.md) · [专栏目录](/booksim-series.html)
