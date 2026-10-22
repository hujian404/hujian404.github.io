# BookSim Notes｜按原书章节阅读互连网络

本专栏以 William J. Dally、Brian Towles 的 *Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004）为主线，严格保留全书 25 章及目录列出的所有小节编号、英文标题和顺序。中文内容是学习笔记，不是原书译本；每个小节标注印刷页码，方便回书核查。

阅读一章时，先理解原书的问题与假设，再看章末固定版本 BookSim2 的源码。模拟器未实现的电路、协议、故障恢复和服务保证会明确说明，不能把几个同名配置项当成原书系统的完整复现。

## 原书组织与阅读路径

| 范围 | 原书内容 | 阅读产出 |
|---|---|---|
| 第 1–2 章 | 导论与完整小网络案例 | 从规格、封装到路由、流控和性能闭环 |
| 第 3–7 章 | Topology | 图指标、路径多样性、非阻塞条件与实现成本 |
| 第 8–11 章 | Routing | 路由关系、负载分布、路径选择与实现机制 |
| 第 12–15 章 | Flow Control | 无缓冲/电路/有缓冲、前进性与服务契约 |
| 第 16–22 章 | Router Architecture | 数据通路、仲裁、分配、接口、错误控制与总线 |
| 第 23–25 章 | Performance | 分析假设、统计方法与原书仿真案例 |

第 2 章是 **64×64、radix-4、三级 butterfly、dropping flow control**。第 12 章讲无缓冲和电路交换，credit 与 VC 在第 13 章展开。第 25 章按原书分别讨论 routing、flow control performance 和 fault tolerance；新增 2×2 Mesh 校验放在补充实验，避免改写原书案例。

## 章节目录

- [1. Introduction to Interconnection Networks](01_introduction_to_interconnection_networks.md)（p. 1）
- [2. A Simple Interconnection Network](02_a_simple_interconnection_network.md)（p. 25）
- [3. Topology Basics](03_topology_basics.md)（p. 45）
- [4. Butterfly Networks](04_butterfly_networks.md)（p. 75）
- [5. Torus Networks](05_torus_networks.md)（p. 89）
- [6. Non-Blocking Networks](06_non_blocking_networks.md)（p. 111）
- [7. Slicing and Dicing](07_slicing_and_dicing.md)（p. 145）
- [8. Routing Basics](08_routing_basics.md)（p. 159）
- [9. Oblivious Routing](09_oblivious_routing.md)（p. 173）
- [10. Adaptive Routing](10_adaptive_routing.md)（p. 189）
- [11. Routing Mechanics](11_routing_mechanics.md)（p. 203）
- [12. Flow Control Basics](12_flow_control_basics.md)（p. 221）
- [13. Buffered Flow Control](13_buffered_flow_control.md)（p. 233）
- [14. Deadlock and Livelock](14_deadlock_and_livelock.md)（p. 257）
- [15. Quality of Service](15_quality_of_service.md)（p. 285）
- [16. Router Architecture](16_router_architecture.md)（p. 305）
- [17. Router Datapath Components](17_router_datapath_components.md)（p. 325）
- [18. Arbitration](18_arbitration.md)（p. 349）
- [19. Allocation](19_allocation.md)（p. 363）
- [20. Network Interfaces](20_network_interfaces.md)（p. 389）
- [21. Error Control](21_error_control.md)（p. 411）
- [22. Buses](22_buses.md)（p. 427）
- [23. Performance Analysis](23_performance_analysis.md)（p. 449）
- [24. Simulation](24_simulation.md)（p. 473）
- [25. Simulation Examples](25_simulation_examples.md)（p. 495）

## 源码、实验和引用规则

BookSim2 基线为 [`28f43299f1706a3160ffac721ca461d74eb6e618`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。源码片段可按 permalink 回到对应行，版权与免责声明见[上游许可](/notes/booksim-notes/source-license.txt)。BookSim 是性能模拟器；阅读其中 C++ 容器和事件调度时，不应把它们直接当作可综合硬件。

- [完整原书目录、小节页码、源码路线与图片清单](appendix-reading-map.md)：含原书附录 A/B/C 的位置，区别于本专栏追加附录。
- [补充实验：2×2 Mesh 配置、工具链与实际结果](appendix-simulation-results.md)：只验证构建、参数和统计路径，未声称复现原书全部图表。
- 图按章节分类保存在 `pic/`，每张新增图同时保留 SVG 和 draw.io；图注说明原书依据、抽象范围与是否测量结果。
- 第 18 章引用 SiliconCrafters 的固定优先级与轮转仲裁博客，借鉴讲解角度并注明原链接；技术判断仍结合原书和固定源码核验。

原书 PDF 仅作本地阅读参考，不随网站发布。正文摘述原理并标明出处，不分发整本教材。所有实验环境只公开工具链与配置，不公开服务器地址、账户或认证信息。

[返回专栏目录](/booksim-series.html)
