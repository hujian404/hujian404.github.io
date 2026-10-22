# Chapter 6｜Non-Blocking Networks

> 原书：William J. Dally、Brian Towles，*Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004），第 6 章，印刷页 111–144。本地参考 PDF 的页序为印刷页 +27。以下为中文学习整理，保留原书全部目录小节的编号与标题，不是逐句翻译。BookSim2 对照版本固定为 [`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

[专栏导读](00_Introduction.md) · [原书目录与页码对照](appendix-reading-map.md)

## 6.1 Non-Blocking vs. Non-Interfering Networks

*原书印刷页 112。*

non-blocking 讨论是否能在给定连接状态下建立新连接；non-interfering 讨论既有流能否互不影响地获得服务。连接可达和按速率交付是不同命题，必须说明单播/多播、允许重排与否、带宽及时间模型。

## 6.2 Crossbar Networks

*原书印刷页 112。*

N×N crossbar 让不同输入到不同输出的连接可以并行，但同一输出的多请求仍需仲裁。交叉点数量随 N² 增长，控制和布线也会成为成本。

## 6.3 Clos Networks

*原书印刷页 116。*

Clos 用多个较小交换机构建较大连接结构。以下条件适用于经典对称三级单播电路连接模型，不能直接当成有缓冲 packet 网络的吞吐公式。

### 6.3.1 Structure and Properties of Clos Networks

*原书印刷页 116。*

C(n,m,r) 有 r 个 n×m 输入交换机、m 个 r×r 中间交换机及 r 个 m×n 输出交换机，端点为 rn。中间级规模 m 决定路径选择空间及成本。

### 6.3.2 Unicast Routing on Strictly Non-Blocking Clos Networks

*原书印刷页 118。*

严格无阻塞的经典充分条件是 m≥2n−1：为新输入输出对选择中间级时，两端既有连接最多共同排除 2(n−1) 个中间交换机，无需移动已建立连接。

例如 C(4,m,r)：严格无阻塞取 m≥7，而允许全局重排时 m≥4。节省的是中间级数量，付出的可能是重排既有连接的控制成本。两种条件不能混报。

### 6.3.3 Unicast Routing on Rearrangeable Clos Networks

*原书印刷页 122。*

允许重排既有路径时，经典单播条件降为 m≥n。重排会带来控制和业务迁移成本，因此不能把 rearrangeable 的条件声称为严格无阻塞。

### 6.3.4 Routing Clos Networks Using Matrix Decomposition

*原书印刷页 126。*

用矩阵记录输入组到输出组的连接数量，再分解成满足中间交换级约束的部分。这个全局连接分配问题不同于 router 在一拍中选择几个 flit。

### 6.3.5 Multicast Routing on Clos Networks

*原书印刷页 128。*

多播允许一次输入连接复制到多个输出，所需分支和中间级资源不再服从简单单播配对。单播无阻塞条件不能原样套用。

### 6.3.6 Clos Networks with More Than Three Stages

*原书印刷页 133。*

递归展开较大的中间交换机构成更多级 Clos，可降低单个交换器 radix，但增加级数和控制路径。需要重新核算端到端延迟及级间连接。

## 6.4 Beneˇs Networks

*原书印刷页 134。*

Benes 网络提供可重排的置换连接；其路由依赖全局路径安排。它增加 butterfly 的路径选择能力，但仍应区分连接建立过程和数据传输过程。

## 6.5 Sorting Networks

*原书印刷页 135。*

排序网络把目的标签按比较交换规则组织，借助排序实现特定连接需求。排序所需级数、重复目的和集中流量的处理条件必须明确。

## 6.6 Case Study: The Velio VC2002 (Zeus) Grooming Switch

*原书印刷页 137。*

Velio VC2002（Zeus）grooming switch 是本章案例。阅读时把业务整理、可重排连接和多级结构联系起来；不要将其误称为 IQRouter 的一种参数配置。

VC2002 是 TDM circuit switch：不仅把某输入送到某输出，还把输入流中的时隙重新映射到输出时隙。原书例子处理 72 路 STS-48 流，每路由多个 STS-1 时隙组成。要分析该系统，必须同时考虑空间连接与时间映射；只配置 packet 网络的 72 个端口，会漏掉问题的关键部分。

## 6.7 Bibliographic Notes

*原书印刷页 142。*

本节对应原书 p. 142 的文献脉络。继续查阅时应回到原书该节和书末 Bibliography，区分最初提出的方法、后续实现与本文使用的 BookSim2 版本。本文末尾源码链接是实现对照，不作为原书历史论述的替代依据。

## 6.8 Exercises

*原书印刷页 142。*

自拟练习（不复制原书习题）：画一个小型三阶段网络，给两组端点不冲突的连接找内部路径，分别尝试“不移动既有路径”和“允许重新分配”。在仿真层面则检查实际流量置换和每链路负载，避免把随机 uniform 的好结果解释为所有置换的无阻塞保证。

## BookSim2 源码对照与适用边界

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/networks/fattree.cpp 第 79–83 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/fattree.cpp#L79-L83)。

```cpp
  //levels * routers_per_level
  _size = _n * powi( _k , _n - 1 );

  //(channels per level = k*routers_per_level* up/down) * (levels-1)
  _channels = (2*_k * powi( _k , _n-1 ))*(_n-1);
```

源码根据 k、n 计算级数和 switch 数，随后在 `_BuildNet` 中按 level 建立端口。顶层和其他层的 radix 不同。选择 FatTree 路由时要读实际 upward / downward 选择策略，以及内部链路是否为目标流量提供足够容量。

本章原书讨论的完整系统/电路机制超出该片段的模型范围。源码片段用于识别相近资源与接口；未实现的电路细节、服务保证或协议行为，不能由命名相似推定存在。

## 来源与继续阅读

- 原书第 6 章，pp. 111–144；各节页码已逐项列出。案例与原书公式均以本地参考书为依据。
- [BookSim2 固定版本源码](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)，节选保留[上游许可](/notes/booksim-notes/source-license.txt)。
- [全书章节/源码路线与图片来源](appendix-reading-map.md)。新增图均附 `.drawio` 源文件，插图是结构说明，不是测量波形。

[上一篇](05_torus_networks.md) · [下一篇](07_slicing_and_dicing.md) · [专栏目录](/booksim-series.html)
