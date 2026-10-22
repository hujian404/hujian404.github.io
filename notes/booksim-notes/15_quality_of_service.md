# Chapter 15｜Quality of Service

> 原书：William J. Dally、Brian Towles，*Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004），第 15 章，印刷页 285–304。本地参考 PDF 的页序为印刷页 +27。以下为中文学习整理，保留原书全部目录小节的编号与标题，不是逐句翻译。BookSim2 对照版本固定为 [`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

[专栏导读](00_Introduction.md) · [原书目录与页码对照](appendix-reading-map.md)

## 15.1 Service Classes and Service Contracts

*原书印刷页 285。*

QoS 首先是服务契约：承诺什么带宽、延迟或丢失界，以及流量需要遵守什么约束。优先级只是实现工具，不能单独构成端到端保证。

## 15.2 Burstiness and Network Delays

*原书印刷页 287。*

平均注入率相同的两条流可能有不同突发性，导致完全不同的排队峰值。应给出流量包络和服务条件，才能讨论最坏延迟。

### 15.2.1 (σ, ρ) Regulated Flows

*原书印刷页 287。*

(σ,ρ) 约束在时间窗 t 内限制到达量不超过 σ+ρt；σ 表示突发预算，ρ 是长期速率。单位必须与 buffer 和服务速率一致。

### 15.2.2 Calculating Delays

*原书印刷页 288。*

延迟上界来自到达包络与服务曲线的水平距离，还需要系统稳定和服务假设。仅给出 σ、ρ 不能凭空算出保证。

## 15.3 Implementation of Guaranteed Services

*原书印刷页 290。*

guaranteed service 要把契约转成可验证的容量与调度条件。分配足够资源之外，还要检查每跳排队与跨跳组合。

### 15.3.1 Aggregate Resource Allocation

*原书印刷页 291。*

aggregate allocation 为一组流预留总资源，降低状态量；组内争用仍可能影响单流，不能把组保证直接解释为每流保证。

### 15.3.2 Resource Reservation

*原书印刷页 292。*

reservation 显式承诺资源，需要准入控制、配置一致性和释放规则；否则总预约可能超过物理容量。

## 15.4 Implementation of Best-Effort Services

*原书印刷页 294。*

best-effort 可以改善公平性和平均性能，但没有承诺就不应发布硬延迟界。latency fairness 与 throughput fairness 也不是同一目标。

### 15.4.1 Latency Fairness

*原书印刷页 294。*

优先照顾等待较久消息可改善延迟公平，但可能改变带宽份额和队列稳定性。要说明年龄从生成、注入还是进入 router 开始。

### 15.4.2 Throughput Fairness

*原书印刷页 296。*

公平吞吐需定义按 flow、terminal 还是字节计份额。长包与短包按 packet 轮转可能获得不同字节带宽。

## 15.5 Separation of Resources

*原书印刷页 297。*

资源隔离限制相互影响，代价是空闲资源可能无法共享。virtual network、VC 和物理 subnet 的隔离范围不同。

### 15.5.1 Tree Saturation

*原书印刷页 297。*

tree saturation 描述热点阻塞向上游扩散，使无关流也被阻塞。仅增加某个 router 的缓存可能扩大积压，并未消除结构性干扰。

### 15.5.2 Non-interfering Networks

*原书印刷页 299。*

non-interfering 的保证需要恰当资源和调度隔离，不能由“non-blocking topology”这个名字推出。

## 15.6 Case Study: ATM Service Classes

*原书印刷页 299。*

ATM service classes 案例用于理解业务契约和流量约束。将其映射到 NoC 前，先重写带宽、延迟、丢失以及准入控制的具体含义。

ATM 用固定 53-byte cell 承载业务，并区分 CBR、VBR-rt、VBR、ABR 与 UBR。实时可变速率业务除了平均速率，还关心突发、delay 和 jitter；UBR 则属于 best effort。该案例说明 service class 只是契约入口，还需持续/峰值速率、突发容忍等参数及相应资源机制。

## 15.7 Case Study: Virtual Networks in the Avici TSR

*原书印刷页 300。*

Avici TSR 的 virtual networks 案例与资源分隔相关。独立队列帮助限制阻塞传播，但端到端保证仍依赖共享链路和调度。

原书的隔离目标是避免通往拥塞目的地 B 的积压，占满目的地 A 也需要的缓冲。TSR 按目的地相关类别分离 VC 和注入缓冲，切断这种长期持有造成的干扰；物理 channel 带宽仍被共享。能逐拍重新分配的带宽，与可能被无限期占住的缓冲，必须采用不同的隔离分析。

## 15.8 Bibliographic Notes

*原书印刷页 302。*

本节对应原书 p. 302 的文献脉络。继续查阅时应回到原书该节和书末 Bibliography，区分最初提出的方法、后续实现与本文使用的 BookSim2 版本。本文末尾源码链接是实现对照，不作为原书历史论述的替代依据。

## 15.9 Exercises

*原书印刷页 303。*

自拟练习（不复制原书习题）：构造两个业务类，先在相同负载下比较无优先级与 class priority，再持续提高高优先级流量。记录低优先级接收率与最长等待，检查是否存在 starvation。将结果称为经验性隔离或调度效果，而不是未经证明的确定性 QoS 保证。

## BookSim2 源码对照与适用边界

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/trafficmanager.cpp 第 78–93 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.cpp#L78-L93)。

```cpp
    if ( priority == "class" ) {
        _pri_type = class_based;
    } else if ( priority == "age" ) {
        _pri_type = age_based;
    } else if ( priority == "network_age" ) {
        _pri_type = network_age_based;
    } else if ( priority == "local_age" ) {
        _pri_type = local_age_based;
    } else if ( priority == "queue_length" ) {
        _pri_type = queue_length_based;
    } else if ( priority == "hop_count" ) {
        _pri_type = hop_count_based;
    } else if ( priority == "sequence" ) {
        _pri_type = sequence_based;
    } else if ( priority == "none" ) {
        _pri_type = none;
```

TrafficManager 将配置字符串映射为 class、age、network_age、local_age 等模式，生成 flit 时写入 pri。后续优先级还要进入 router / allocator 的请求规则；没有进入真正竞争点的标签不会带来调度效果。统计应按 class 和最差流分别读，不能只合并所有样本。

本章原书讨论的完整系统/电路机制超出该片段的模型范围。源码片段用于识别相近资源与接口；未实现的电路细节、服务保证或协议行为，不能由命名相似推定存在。

## 来源与继续阅读

- 原书第 15 章，pp. 285–304；各节页码已逐项列出。案例与原书公式均以本地参考书为依据。
- [BookSim2 固定版本源码](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)，节选保留[上游许可](/notes/booksim-notes/source-license.txt)。
- [全书章节/源码路线与图片来源](appendix-reading-map.md)。新增图均附 `.drawio` 源文件，插图是结构说明，不是测量波形。

[上一篇](14_deadlock_and_livelock.md) · [下一篇](16_router_architecture.md) · [专栏目录](/booksim-series.html)
