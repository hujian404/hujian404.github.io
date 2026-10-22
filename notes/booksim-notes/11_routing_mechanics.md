# Chapter 11｜Routing Mechanics

> 原书：William J. Dally、Brian Towles，*Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004），第 11 章，印刷页 203–220。本地参考 PDF 的页序为印刷页 +27。以下为中文学习整理，保留原书全部目录小节的编号与标题，不是逐句翻译。BookSim2 对照版本固定为 [`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

[专栏导读](00_Introduction.md) · [原书目录与页码对照](appendix-reading-map.md)

## 11.1 Table-Based Routing

*原书印刷页 203。*

routing mechanics 讨论路径选择如何编码和执行。表项宽度、查表次数、header 开销与更新方式会影响面积和延迟；算法上等价的路由不一定有相同实现成本。

### 11.1.1 Source Routing

*原书印刷页 204。*

source routing 把路径信息放在源端构造的 header 中，沿途消费。它减轻逐跳路径计算，却增加 header 长度，并要求拓扑变化时更新源端信息。

### 11.1.2 Node-Table Routing

*原书印刷页 208。*

node-table routing 在每个节点按目的或标签查下一跳。表项可以随系统映射调整，但需要考虑分布式更新一致性与表的容量。

## 11.2 Algorithmic Routing

*原书印刷页 211。*

algorithmic routing 由地址与当前节点状态计算方向，适合规则拓扑。BookSim 的 C++ routing function 是性能模型中的软件实现，其执行耗时不自动等于硬件 RC 延迟。

## 11.3 Case Study: Oblivious Source Routing in the IBM Vulcan Network

*原书印刷页 212。*

IBM Vulcan 案例是 oblivious source routing。对照路径在何处计算、如何放入消息、沿途如何消费，才能理解它与逐跳 table routing 的差别。

SP1/SP2 的 8×8 switch chip 受 source route 控制；原书介绍的端口除数据外还有 tag 与反向 token，前者标识有效 flit，后者返回流控 credit。八个芯片组成 32-port switch module，再按机器规模互连。路径编码解决“去哪”，token 解决“能否发”，这两个职责应在模型中分开。

## 11.4 Bibliographic Notes

*原书印刷页 217。*

本节对应原书 p. 217 的文献脉络。继续查阅时应回到原书该节和书末 Bibliography，区分最初提出的方法、后续实现与本文使用的 BookSim2 版本。本文末尾源码链接是实现对照，不作为原书历史论述的替代依据。

## 11.5 Exercises

*原书印刷页 217。*

自拟练习（不复制原书习题）：固定网络、VC 和负载，只比较 routing_delay=1 与0，核对路径不变时零负载时延发生什么变化。若实验涉及物理意义，再说明省略 RC 拍需要何种提前计算假设，不能只报告 simulator 更快的数值。

## BookSim2 源码对照与适用边界

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/routers/iq_router.cpp 第 76–82 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routers/iq_router.cpp#L76-L82)。

```cpp
  string const rf = config.GetStr("routing_function") + "_" + config.GetStr("topology");
  map<string, tRoutingFunction>::const_iterator rf_iter = gRoutingFunctionMap.find(rf);
  if(rf_iter == gRoutingFunctionMap.end()) {
    Error("Invalid routing function: " + rf);
  }
  _rf = rf_iter->second;

```

构造函数把算法名和拓扑拼成唯一键，从全局 map 获取函数指针；找不到会直接报错。后续 `_RouteEvaluate` / `_RouteUpdate` 分开实现时序，lookahead 信息保存在 Flit 的 `la_route_set`。读软件循环时要同时看计划完成时间，而非把函数先后顺序当作流水拍数。

本章原书讨论的完整系统/电路机制超出该片段的模型范围。源码片段用于识别相近资源与接口；未实现的电路细节、服务保证或协议行为，不能由命名相似推定存在。

## 来源与继续阅读

- 原书第 11 章，pp. 203–220；各节页码已逐项列出。案例与原书公式均以本地参考书为依据。
- [BookSim2 固定版本源码](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)，节选保留[上游许可](/notes/booksim-notes/source-license.txt)。
- [全书章节/源码路线与图片来源](appendix-reading-map.md)。新增图均附 `.drawio` 源文件，插图是结构说明，不是测量波形。

[上一篇](10_adaptive_routing.md) · [下一篇](12_flow_control_basics.md) · [专栏目录](/booksim-series.html)
