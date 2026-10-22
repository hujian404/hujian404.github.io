# Chapter 23｜Performance Analysis

> 原书：William J. Dally、Brian Towles，*Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004），第 23 章，印刷页 449–472。本地参考 PDF 的页序为印刷页 +27。以下为中文学习整理，保留原书全部目录小节的编号与标题，不是逐句翻译。BookSim2 对照版本固定为 [`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

[专栏导读](00_Introduction.md) · [原书目录与页码对照](appendix-reading-map.md)

## 23.1 Measures of Interconnection Network Performance

*原书印刷页 449。*

测量前固定起止事件、消息/位单位、负载定义和稳定条件。throughput、latency 与 fault tolerance 需要各自的实验方法。

### 23.1.1 Throughput

*原书印刷页 452。*

offered 是希望送入的流量，injected 是实际进入边界的流量，accepted 是成功交付。丢弃网络或源端积压时三者可不同，必须分别观察。

### 23.1.2 Latency

*原书印刷页 455。*

说明是 head-to-head、head-to-tail 还是逐 flit latency，以及是否包含源端队列、接口和目的消费。不同边界的数据不能直接画在同一曲线上。

![BookSim 延迟边界](pic/23-metrics/latency-boundaries.svg)

*图 23-A：依据固定版本 `_RetireFlit` 统计整理的原创算例。head 生成 0、注入 3、tail 到达 10，则 packet latency=10、network latency=7；逐 flit latency 需要各自时间戳。*

### 23.1.3 Fault Tolerance

*原书印刷页 456。*

容错指标应同时报告故障模型、成功率和性能退化。理想无误码网络的正常运行结果并不提供 BER 或恢复能力证据。

### 23.1.4 Common Measurement Pitfalls

*原书印刷页 456。*

常见错误包括隐藏 source queue、单位混用、未热身、只统计完成的快消息，以及系统不稳定时仍报告平均延迟。报告必须包含吞吐和积压趋势。

## 23.2 Analysis

*原书印刷页 460。*

分析模型用于提出可检验的容量与延迟预测，而不是替代全部实现。应把假设、近似和适用范围写在公式旁。

### 23.2.1 Queuing Theory

*原书印刷页 461。*

稳定排队系统中 Little 定律为 `L=λW`，三者必须使用同一系统边界与长期平均。它不是在持续积压的网络中计算稳态延迟的工具。

### 23.2.2 Probabilistic Analysis

*原书印刷页 465。*

概率分析从 traffic 和独立性假设计算争用、利用率或丢失。第 2 章的三级递推就是例子；真实相关流可能偏离其独立模型。

## 23.3 Validation

*原书印刷页 467。*

validation 应用手算、小规模穷举、已知极限和独立模型交叉核验。仿真器没有 assert 只说明未触发已有检查，不证明模型实现了预期系统。

## 23.4 Case Study: Efficiency and Loss in the BBN Monarch Network

*原书印刷页 468。*

BBN Monarch 案例用效率与损失展示指标如何揭示网络机制。阅读时分清有效交付、内部工作量和丢失开销，再把同样的问题用于自己的仿真数据。

Monarch 是设计过但未完成的机器，不能把原书分析写成已交付系统的实测。其网络交替使用 switch 与 concentrator，采用 dropping flow control、地址散列及同步帧内的同地址 access combining。集中度提高资源利用，也增加碰撞损失；效率与丢失的联合分析比只看原始 channel 带宽更能反映设计取舍。

## 23.5 Bibliographic Notes

*原书印刷页 470。*

本节对应原书 p. 470 的文献脉络。继续查阅时应回到原书该节和书末 Bibliography，区分最初提出的方法、后续实现与本文使用的 BookSim2 版本。本文末尾源码链接是实现对照，不作为原书历史论述的替代依据。

## 23.6 Exercises

*原书印刷页 471。*

自拟练习（不复制原书习题）：对第25章的三个点同时记录 packet latency、network latency、flit latency、injected和accepted flit rate。需要完整饱和曲线时再加密负载、扩展窗口和多seed；不要用这三个低负载 smoke 点直接拟合饱和吞吐上限。

## BookSim2 源码对照与适用边界

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/trafficmanager.cpp 第 731–738 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.cpp#L731-L738)。

```cpp
            _plat_stats[f->cl]->AddSample( f->atime - head->ctime);
            _nlat_stats[f->cl]->AddSample( f->atime - head->itime);
            _frag_stats[f->cl]->AddSample( (f->atime - head->atime) - (f->id - head->id) );

            if(_pair_stats){
                _pair_plat[f->cl][f->src*_nodes+dest]->AddSample( f->atime - head->ctime );
                _pair_nlat[f->cl][f->src*_nodes+dest]->AddSample( f->atime - head->itime );
            }
```

tail 到达后，_plat_stats 用 head ctime，_nlat_stats 用 head itime；_flat_stats 则在每个 flit 退休时统计自己的 itime→atime。注入率若启用 flit 单位，构造时会除以平均 packet size 转成 packet 生成概率。它与 Constellation 评估器的 received/sent 比例不同，不能照搬列名解释。

## 来源与继续阅读

- 原书第 23 章，pp. 449–472；各节页码已逐项列出。案例与原书公式均以本地参考书为依据。
- [BookSim2 固定版本源码](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)，节选保留[上游许可](/notes/booksim-notes/source-license.txt)。
- [全书章节/源码路线与图片来源](appendix-reading-map.md)。新增图均附 `.drawio` 源文件，插图是结构说明，不是测量波形。

[上一篇](22_buses.md) · [下一篇](24_simulation.md) · [专栏目录](/booksim-series.html)
