# Chapter 5｜Torus Networks

> 原书：William J. Dally、Brian Towles，*Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004），第 5 章，印刷页 89–110。本地参考 PDF 的页序为印刷页 +27。以下为中文学习整理，保留原书全部目录小节的编号与标题，不是逐句翻译。BookSim2 对照版本固定为 [`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

[专栏导读](00_Introduction.md) · [原书目录与页码对照](appendix-reading-map.md)

## 5.1 The Structure of Torus Networks

*原书印刷页 90。*

k-ary n-cube 在每个维度组织长度 k 的环；去掉 wrap-around 连接得到有限 Mesh。每个节点的网络方向端口通常为 2n，另有 terminal 端口。维度和每维规模同时影响 radix、距离及布线。

| 数量（每 router 一个 terminal） | Mesh | Torus（通常 k≥3） |
|---|---|---|
| 端点 | k^n | k^n |
| 直径（最短路） | n(k−1) | n⌊k/2⌋ |
| 有效有向内部 channel | 2n(k−1)k^(n−1) | 2nk^n |

这些是图模型的计数；BookSim KNCube 分配的对象数需按源码解释，不能用对象数反证表中有限 Mesh 的边数。k=2 等退化规模还要声明平行端口的计数。

## 5.2 Performance

*原书印刷页 92。*

Torus 的 wrap 缩短许多节点对的距离，却引入长线、路由选择和环形资源依赖。比较 Mesh 与 Torus 时，要注明是否保持节点数、链路位宽、时钟或布线预算相同。

### 5.2.1 Throughput

*原书印刷页 92。*

吞吐看最忙 channel，而不是只看总带宽。维度顺序、正负方向选择与 traffic permutation 都会改变负载；均匀流量下的结论不应直接推广到热点流量。

### 5.2.2 Latency

*原书印刷页 95。*

对单维环，最短距离取 `min(|x−y|, k−|x−y|)`，再逐维相加。较少 hop 可能被较长 wrap 线的传输时间抵消。

### 5.2.3 Path Diversity

*原书印刷页 96。*

多维路径可改变维度顺序，环上还可能有等长正反路径。路径选择空间越大，越需要说明选择概率和死锁约束。

## 5.3 Building Mesh and Torus Networks

*原书印刷页 98。*

逻辑环可折叠布线，以减少最长导线；但折叠可能改变线交叉、封装和 channel 延迟。分析拓扑图后还要画物理映射，才能判断理论延迟是否能落地。

## 5.4 Express Cubes

*原书印刷页 100。*

Express cubes 通过额外快速连接跳过中间节点，降低远距离通信开销。它改变端口、带宽及布线预算，不能只把原链路延迟减小来冒充结构变化。

## 5.5 Case Study: The MIT J-Machine

*原书印刷页 102。*

MIT J-Machine 案例把低维网络和细粒度消息处理联系起来。重点看网络与节点实现如何配合，而不是把一个拓扑标签当作完整的消息驱动系统。

J-Machine 将消息驱动处理器与网络紧密集成，节点可用一条指令从寄存器发送短消息。原书机柜例子按 8×8×16 Mesh 安排处理节点，并把 I/O 节点放在阵列边缘，使存储与 I/O 都能通过消息访问。它说明物理三维封装和短消息接口是同一系统设计的部分；“出现在 Torus 一章”不等于所有实际配置都用了 wrap-around。

## 5.6 Bibliographic Notes

*原书印刷页 106。*

本节对应原书 p. 106 的文献脉络。继续查阅时应回到原书该节和书末 Bibliography，区分最初提出的方法、后续实现与本文使用的 BookSim2 版本。本文末尾源码链接是实现对照，不作为原书历史论述的替代依据。

## 5.7 Exercises

*原书印刷页 107。*

自拟练习（不复制原书习题）：先用 n=1、k=8 手画0→7和0→4，分别记录 Mesh、Torus 的跳数和平局选择。随后阅读 `dor_next_torus` 的边界与 partition 更新；比较时分别报告链路周期假设和 hop 数，不能只给总体平均延迟。

## BookSim2 源码对照与适用边界

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/networks/kncube.cpp 第 118–121 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/kncube.cpp#L118-L121)。

```cpp
      // torus channel is longer due to wrap around
      int latency = _mesh ? 1 : 2 ;

      //get the input channel number
```

`_mesh` 控制默认 latency；`SetLatency` 同时作用于数据和 credit channel。该实现分配的邻接对象带有 wrap 组织，Mesh 靠路由约束避免使用边界回绕，不能只数指针就判断某条路径会被选中。Torus 的 `dim_order_torus` 还会对 VC 区间进行分割。

## 来源与继续阅读

- 原书第 5 章，pp. 89–110；各节页码已逐项列出。案例与原书公式均以本地参考书为依据。
- [BookSim2 固定版本源码](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)，节选保留[上游许可](/notes/booksim-notes/source-license.txt)。
- [全书章节/源码路线与图片来源](appendix-reading-map.md)。新增图均附 `.drawio` 源文件，插图是结构说明，不是测量波形。

[上一篇](04_butterfly_networks.md) · [下一篇](06_non_blocking_networks.md) · [专栏目录](/booksim-series.html)
