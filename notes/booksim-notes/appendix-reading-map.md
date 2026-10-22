# 原书目录、页码与 BookSim2 阅读地图

依据参考 PDF 的 Contents（目录页 vii–xvi）核对。印刷页 +27 为本地 PDF 页序；例如印刷 p. 1 对应 PDF 第 28 页。本文保留目录里的全部二级和三级小节，正文末尾的源码对照与引用属于学习补充，不占用原书编号。

## [1. Introduction to Interconnection Networks](01_introduction_to_interconnection_networks.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 1.1 | Three Questions About Interconnection Networks | 2 |
| 1.2 | Uses of Interconnection Networks | 4 |
| 1.2.1 | Processor-Memory Interconnect | 5 |
| 1.2.2 | I/O Interconnect | 8 |
| 1.2.3 | Packet Switching Fabric | 11 |
| 1.3 | Network Basics | 13 |
| 1.3.1 | Topology | 13 |
| 1.3.2 | Routing | 16 |
| 1.3.3 | Flow Control | 17 |
| 1.3.4 | Router Architecture | 19 |
| 1.3.5 | Performance of Interconnection Networks | 19 |
| 1.4 | History | 21 |
| 1.5 | Organization of this Book | 23 |

源码入口：[src/networks/network.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/network.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [2. A Simple Interconnection Network](02_a_simple_interconnection_network.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 2.1 | Network Specifications and Constraints | 25 |
| 2.2 | Topology | 27 |
| 2.3 | Routing | 31 |
| 2.4 | Flow Control | 32 |
| 2.5 | Router Design | 33 |
| 2.6 | Performance Analysis | 36 |
| 2.7 | Exercises | 42 |

源码入口：[src/networks/fly.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/fly.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [3. Topology Basics](03_topology_basics.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 3.1 | Nomenclature | 46 |
| 3.1.1 | Channels and Nodes | 46 |
| 3.1.2 | Direct and Indirect Networks | 47 |
| 3.1.3 | Cuts and Bisections | 48 |
| 3.1.4 | Paths | 48 |
| 3.1.5 | Symmetry | 49 |
| 3.2 | Traffic Patterns | 50 |
| 3.3 | Performance | 51 |
| 3.3.1 | Throughput and Maximum Channel Load | 51 |
| 3.3.2 | Latency | 55 |
| 3.3.3 | Path Diversity | 57 |
| 3.4 | Packaging Cost | 60 |
| 3.5 | Case Study: The SGI Origin 2000 | 64 |
| 3.6 | Bibliographic Notes | 69 |
| 3.7 | Exercises | 69 |

源码入口：[src/networks/kncube.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/kncube.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [4. Butterfly Networks](04_butterfly_networks.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 4.1 | The Structure of Butterfly Networks | 75 |
| 4.2 | Isomorphic Butterflies | 77 |
| 4.3 | Performance and Packaging Cost | 78 |
| 4.4 | Path Diversity and Extra Stages | 81 |
| 4.5 | Case Study: The BBN Butterfly | 84 |
| 4.6 | Bibliographic Notes | 86 |
| 4.7 | Exercises | 86 |

源码入口：[src/networks/fly.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/fly.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [5. Torus Networks](05_torus_networks.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 5.1 | The Structure of Torus Networks | 90 |
| 5.2 | Performance | 92 |
| 5.2.1 | Throughput | 92 |
| 5.2.2 | Latency | 95 |
| 5.2.3 | Path Diversity | 96 |
| 5.3 | Building Mesh and Torus Networks | 98 |
| 5.4 | Express Cubes | 100 |
| 5.5 | Case Study: The MIT J-Machine | 102 |
| 5.6 | Bibliographic Notes | 106 |
| 5.7 | Exercises | 107 |

源码入口：[src/networks/kncube.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/kncube.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [6. Non-Blocking Networks](06_non_blocking_networks.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 6.1 | Non-Blocking vs. Non-Interfering Networks | 112 |
| 6.2 | Crossbar Networks | 112 |
| 6.3 | Clos Networks | 116 |
| 6.3.1 | Structure and Properties of Clos Networks | 116 |
| 6.3.2 | Unicast Routing on Strictly Non-Blocking Clos Networks | 118 |
| 6.3.3 | Unicast Routing on Rearrangeable Clos Networks | 122 |
| 6.3.4 | Routing Clos Networks Using Matrix Decomposition | 126 |
| 6.3.5 | Multicast Routing on Clos Networks | 128 |
| 6.3.6 | Clos Networks with More Than Three Stages | 133 |
| 6.4 | Beneˇs Networks | 134 |
| 6.5 | Sorting Networks | 135 |
| 6.6 | Case Study: The Velio VC2002 (Zeus) Grooming Switch | 137 |
| 6.7 | Bibliographic Notes | 142 |
| 6.8 | Exercises | 142 |

源码入口：[src/networks/fattree.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/fattree.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [7. Slicing and Dicing](07_slicing_and_dicing.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 7.1 | Concentrators and Distributors | 146 |
| 7.1.1 | Concentrators | 146 |
| 7.1.2 | Distributors | 148 |
| 7.2 | Slicing and Dicing | 149 |
| 7.2.1 | Bit Slicing | 149 |
| 7.2.2 | Dimension Slicing | 151 |
| 7.2.3 | Channel Slicing | 152 |
| 7.3 | Slicing Multistage Networks | 153 |
| 7.4 | Case Study: Bit Slicing in the Tiny Tera | 155 |
| 7.5 | Bibliographic Notes | 157 |
| 7.6 | Exercises | 157 |

源码入口：[src/booksim_config.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/booksim_config.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [8. Routing Basics](08_routing_basics.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 8.1 | A Routing Example | 160 |
| 8.2 | Taxonomy of Routing Algorithms | 162 |
| 8.3 | The Routing Relation | 163 |
| 8.4 | Deterministic Routing | 164 |
| 8.4.1 | Destination-Tag Routing in Butterfly Networks | 165 |
| 8.4.2 | Dimension-Order Routing in Cube Networks | 166 |
| 8.5 | Case Study: Dimension-Order Routing in the Cray T3D | 168 |
| 8.6 | Bibliographic Notes | 170 |
| 8.7 | Exercises | 171 |

源码入口：[src/outputset.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/outputset.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [9. Oblivious Routing](09_oblivious_routing.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 9.1 | Valiant’s Randomized Routing Algorithm | 174 |
| 9.1.1 | Valiant’s Algorithm on Torus Topologies | 174 |
| 9.1.2 | Valiant’s Algorithm on Indirect Networks | 175 |
| 9.2 | Minimal Oblivious Routing | 176 |
| 9.2.1 | Minimal Oblivious Routing on a Folded Clos (Fat Tree) | 176 |
| 9.2.2 | Minimal Oblivious Routing on a Torus | 178 |
| 9.3 | Load-Balanced Oblivious Routing | 180 |
| 9.4 | Analysis of Oblivious Routing | 180 |
| 9.5 | Case Study: Oblivious Routing in the Avici Terabit Switch Router(TSR) | 183 |
| 9.6 | Bibliographic Notes | 186 |
| 9.7 | Exercises | 187 |

源码入口：[src/routefunc.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routefunc.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [10. Adaptive Routing](10_adaptive_routing.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 10.1 | Adaptive Routing Basics | 189 |
| 10.2 | Minimal Adaptive Routing | 192 |
| 10.3 | Fully Adaptive Routing | 193 |
| 10.4 | Load-Balanced Adaptive Routing | 195 |
| 10.5 | Search-Based Routing | 196 |
| 10.6 | Case Study: Adaptive Routing in the Thinking Machines CM-5 | 196 |
| 10.7 | Bibliographic Notes | 201 |
| 10.8 | Exercises | 201 |

源码入口：[src/routefunc.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routefunc.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [11. Routing Mechanics](11_routing_mechanics.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 11.1 | Table-Based Routing | 203 |
| 11.1.1 | Source Routing | 204 |
| 11.1.2 | Node-Table Routing | 208 |
| 11.2 | Algorithmic Routing | 211 |
| 11.3 | Case Study: Oblivious Source Routing in the IBM Vulcan Network | 212 |
| 11.4 | Bibliographic Notes | 217 |
| 11.5 | Exercises | 217 |

源码入口：[src/routers/iq_router.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routers/iq_router.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [12. Flow Control Basics](12_flow_control_basics.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 12.1 | Resources and Allocation Units | 222 |
| 12.2 | Bufferless Flow Control | 225 |
| 12.3 | Circuit Switching | 228 |
| 12.4 | Bibliographic Notes | 230 |
| 12.5 | Exercises | 230 |

源码入口：[src/channel.hpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/channel.hpp)。具体覆盖范围和未实现机制见本章末尾。

## [13. Buffered Flow Control](13_buffered_flow_control.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 13.1 | Packet-Buffer Flow Control | 234 |
| 13.2 | Flit-Buffer Flow Control | 237 |
| 13.2.1 | Wormhole Flow Control | 237 |
| 13.2.2 | Virtual-Channel Flow Control | 239 |
| 13.3 | Buffer Management and Backpressure | 245 |
| 13.3.1 | Credit-Based Flow Control | 245 |
| 13.3.2 | On/Off Flow Control | 247 |
| 13.3.3 | Ack/Nack Flow Control | 249 |
| 13.4 | Flit-Reservation Flow Control | 251 |
| 13.4.1 | A Flit-Reservation Router | 252 |
| 13.4.2 | Output Scheduling | 253 |
| 13.4.3 | Input Scheduling | 255 |
| 13.5 | Bibliographic Notes | 256 |
| 13.6 | Exercises | 256 |

源码入口：[src/buffer_state.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/buffer_state.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [14. Deadlock and Livelock](14_deadlock_and_livelock.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 14.1 | Deadlock | 258 |
| 14.1.1 | Agents and Resources | 258 |
| 14.1.2 | Wait-For and Holds Relations | 259 |
| 14.1.3 | Resource Dependences | 260 |
| 14.1.4 | Some Examples | 260 |
| 14.1.5 | High-Level (Protocol) Deadlock | 262 |
| 14.2 | Deadlock Avoidance | 263 |
| 14.2.1 | Resource Classes | 263 |
| 14.2.2 | Restricted Physical Routes | 267 |
| 14.2.3 | Hybrid Deadlock Avoidance | 270 |
| 14.3 | Adaptive Routing | 272 |
| 14.3.1 | Routing Subfunctions and Extended Dependences | 272 |
| 14.3.2 | Duato’s Protocol for Deadlock-Free Adaptive Algorithms | 276 |
| 14.4 | Deadlock Recovery | 277 |
| 14.4.1 | Regressive Recovery | 278 |
| 14.4.2 | Progressive Recovery | 278 |
| 14.5 | Livelock | 279 |
| 14.6 | Case Study: Deadlock Avoidance in the Cray T3E | 279 |
| 14.7 | Bibliographic Notes | 281 |
| 14.8 | Exercises | 282 |

源码入口：[src/booksim_config.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/booksim_config.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [15. Quality of Service](15_quality_of_service.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 15.1 | Service Classes and Service Contracts | 285 |
| 15.2 | Burstiness and Network Delays | 287 |
| 15.2.1 | (σ, ρ) Regulated Flows | 287 |
| 15.2.2 | Calculating Delays | 288 |
| 15.3 | Implementation of Guaranteed Services | 290 |
| 15.3.1 | Aggregate Resource Allocation | 291 |
| 15.3.2 | Resource Reservation | 292 |
| 15.4 | Implementation of Best-Effort Services | 294 |
| 15.4.1 | Latency Fairness | 294 |
| 15.4.2 | Throughput Fairness | 296 |
| 15.5 | Separation of Resources | 297 |
| 15.5.1 | Tree Saturation | 297 |
| 15.5.2 | Non-interfering Networks | 299 |
| 15.6 | Case Study: ATM Service Classes | 299 |
| 15.7 | Case Study: Virtual Networks in the Avici TSR | 300 |
| 15.8 | Bibliographic Notes | 302 |
| 15.9 | Exercises | 303 |

源码入口：[src/trafficmanager.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [16. Router Architecture](16_router_architecture.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 16.1 | Basic Router Architecture | 305 |
| 16.1.1 | Block Diagram | 305 |
| 16.1.2 | The Router Pipeline | 308 |
| 16.2 | Stalls | 310 |
| 16.3 | Closing the Loop with Credits | 312 |
| 16.4 | Reallocating a Channel | 313 |
| 16.5 | Speculation and Lookahead | 316 |
| 16.6 | Flit and Credit Encoding | 319 |
| 16.7 | Case Study: The Alpha 21364 Router | 321 |
| 16.8 | Bibliographic Notes | 324 |
| 16.9 | Exercises | 324 |

源码入口：[src/routers/iq_router.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routers/iq_router.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [17. Router Datapath Components](17_router_datapath_components.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 17.1 | Input Buffer Organization | 325 |
| 17.1.1 | Buffer Partitioning | 326 |
| 17.1.2 | Input Buffer Data Structures | 328 |
| 17.1.3 | Input Buffer Allocation | 333 |
| 17.2 | Switches | 334 |
| 17.2.1 | Bus Switches | 335 |
| 17.2.2 | Crossbar Switches | 338 |
| 17.2.3 | Network Switches | 342 |
| 17.3 | Output Organization | 343 |
| 17.4 | Case Study: The Datapath of the IBM Colony Router | 344 |
| 17.5 | Bibliographic Notes | 347 |
| 17.6 | Exercises | 348 |

源码入口：[src/channel.hpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/channel.hpp)。具体覆盖范围和未实现机制见本章末尾。

## [18. Arbitration](18_arbitration.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 18.1 | Arbitration Timing | 349 |
| 18.2 | Fairness | 351 |
| 18.3 | Fixed Priority Arbiter | 352 |
| 18.4 | Variable Priority Iterative Arbiters | 354 |
| 18.4.1 | Oblivious Arbiters | 354 |
| 18.4.2 | Round-Robin Arbiter | 355 |
| 18.4.3 | Grant-Hold Circuit | 355 |
| 18.4.4 | Weighted Round-Robin Arbiter | 357 |
| 18.5 | Matrix Arbiter | 358 |
| 18.6 | Queuing Arbiter | 360 |
| 18.7 | Exercises | 362 |

源码入口：[src/arbiters/roundrobin_arb.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/arbiters/roundrobin_arb.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [19. Allocation](19_allocation.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 19.1 | Representations | 363 |
| 19.2 | Exact Algorithms | 366 |
| 19.3 | Separable Allocators | 367 |
| 19.3.1 | Parallel Iterative Matching | 371 |
| 19.3.2 | iSLIP | 371 |
| 19.3.3 | Lonely Output Allocator | 372 |
| 19.4 | Wavefront Allocator | 373 |
| 19.5 | Incremental vs. Batch Allocation | 376 |
| 19.6 | Multistage Allocation | 378 |
| 19.7 | Performance of Allocators | 380 |
| 19.8 | Case Study: The Tiny Tera Allocator | 383 |
| 19.9 | Bibliographic Notes | 385 |
| 19.10 | Exercises | 386 |

源码入口：[src/allocators/islip.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/allocators/islip.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [20. Network Interfaces](20_network_interfaces.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 20.1 | Processor-Network Interface | 390 |
| 20.1.1 | Two-Register Interface | 391 |
| 20.1.2 | Register-Mapped Interface | 392 |
| 20.1.3 | Descriptor-Based Interface | 393 |
| 20.1.4 | Message Reception | 393 |
| 20.2 | Shared-Memory Interface | 394 |
| 20.2.1 | Processor-Network Interface | 395 |
| 20.2.2 | Cache Coherence | 397 |
| 20.2.3 | Memory-Network Interface | 398 |
| 20.3 | Line-Fabric Interface | 400 |
| 20.4 | Case Study: The MIT M-Machine Network Interface | 403 |
| 20.5 | Bibliographic Notes | 407 |
| 20.6 | Exercises | 408 |

源码入口：[src/flit.hpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/flit.hpp)。具体覆盖范围和未实现机制见本章末尾。

## [21. Error Control](21_error_control.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 21.1 | Know Thy Enemy: Failure Modes and Fault Models | 411 |
| 21.2 | The Error Control Process: Detection, Containment, and Recovery | 414 |
| 21.3 | Link Level Error Control | 415 |
| 21.3.1 | Link Monitoring | 415 |
| 21.3.2 | Link-Level Retransmission | 416 |
| 21.3.3 | Channel Reconfiguration, Degradation, and Shutdown | 419 |
| 21.4 | Router Error Control | 421 |
| 21.5 | Network-Level Error Control | 422 |
| 21.6 | End-to-end Error Control | 423 |
| 21.7 | Bibliographic Notes | 423 |
| 21.8 | Exercises | 424 |

源码入口：[src/channel.hpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/channel.hpp)。具体覆盖范围和未实现机制见本章末尾。

## [22. Buses](22_buses.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 22.1 | Bus Basics | 428 |
| 22.2 | Bus Arbitration | 432 |
| 22.3 | High Performance Bus Protocol | 436 |
| 22.3.1 | Bus Pipelining | 436 |
| 22.3.2 | Split-Transaction Buses | 438 |
| 22.3.3 | Burst Messages | 439 |
| 22.4 | From Buses to Networks | 441 |
| 22.5 | Case Study: The PCI Bus | 443 |
| 22.6 | Bibliographic Notes | 446 |
| 22.7 | Exercises | 446 |

源码入口：[src/networks/network.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/network.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [23. Performance Analysis](23_performance_analysis.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 23.1 | Measures of Interconnection Network Performance | 449 |
| 23.1.1 | Throughput | 452 |
| 23.1.2 | Latency | 455 |
| 23.1.3 | Fault Tolerance | 456 |
| 23.1.4 | Common Measurement Pitfalls | 456 |
| 23.2 | Analysis | 460 |
| 23.2.1 | Queuing Theory | 461 |
| 23.2.2 | Probabilistic Analysis | 465 |
| 23.3 | Validation | 467 |
| 23.4 | Case Study: Efficiency and Loss in the BBN Monarch Network | 468 |
| 23.5 | Bibliographic Notes | 470 |
| 23.6 | Exercises | 471 |

源码入口：[src/trafficmanager.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [24. Simulation](24_simulation.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 24.1 | Levels of Detail | 473 |
| 24.2 | Network Workloads | 475 |
| 24.2.1 | Application-Driven Workloads | 475 |
| 24.2.2 | Synthetic Workloads | 476 |
| 24.3 | Simulation Measurements | 478 |
| 24.3.1 | Simulator Warm-Up | 479 |
| 24.3.2 | Steady-State Sampling | 481 |
| 24.3.3 | Confidence Intervals | 482 |
| 24.4 | Simulator Design | 484 |
| 24.4.1 | Simulation Approaches | 485 |
| 24.4.2 | Modeling Source Queues | 488 |
| 24.4.3 | Random Number Generation | 490 |
| 24.4.4 | Troubleshooting | 491 |
| 24.5 | Bibliographic Notes | 491 |
| 24.6 | Exercises | 492 |

源码入口：[src/trafficmanager.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.cpp)。具体覆盖范围和未实现机制见本章末尾。

## [25. Simulation Examples](25_simulation_examples.md)

| 原书节号 | 原书标题 | 印刷页 |
|---|---|---|
| 25.1 | Routing | 495 |
| 25.1.1 | Latency | 496 |
| 25.1.2 | Throughput Distributions | 499 |
| 25.2 | Flow Control Performance | 500 |
| 25.2.1 | Virtual Channels | 500 |
| 25.2.2 | Network Size | 502 |
| 25.2.3 | Injection Processes | 503 |
| 25.2.4 | Prioritization | 505 |
| 25.2.5 | Stability | 507 |
| 25.3 | Fault Tolerance | 508 |

源码入口：[src/trafficmanager.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.cpp)。具体覆盖范围和未实现机制见本章末尾。

## 原书附录与本专栏补充的区别

| 原书内容 | 印刷页 | 用途 |
|---|---|---|
| Appendix A — Nomenclature | 511 | 统一符号 |
| Appendix B — Glossary | 515 | 核对术语 |
| Appendix C — Network Simulator | 521 | 原书模拟器背景；不等同于当前 BookSim2 固定版本 |
| Bibliography | 523 | 原始文献 |
| Index | 539 | 按术语检索 |

本站的 `appendix-simulation-results.md` 是新增实验，不是原书 Appendix C。各章 Exercises 下是自拟学习任务，不是教材习题答案。

## 图片与再利用说明

新增图统一采用白底、深蓝结构线、低饱和青色强调和衬线字体。标签采用英文，中文解释放在图注，方便学术文档复用。图中的比例、流水拍数和物理线长仅在显式给出时才有定量含义。

| 图 | 原理依据 | 可编辑文件 | 网页图 |
|---|---|---|---|

| 2-A | 原书 §2.1–2.2；分级与封装预算 | [draw.io](/notes/booksim-notes/pic/02-butterfly/butterfly-budget.drawio) | [SVG](/notes/booksim-notes/pic/02-butterfly/butterfly-budget.svg) |
| 12-A | 原书 §12.3；建立/确认/数据/释放 | [draw.io](/notes/booksim-notes/pic/12-flow/circuit-sequence.drawio) | [SVG](/notes/booksim-notes/pic/12-flow/circuit-sequence.svg) |
| 13-A | 原书 §13.3.1；许可守恒 | [draw.io](/notes/booksim-notes/pic/13-buffered/credit-conservation.drawio) | [SVG](/notes/booksim-notes/pic/13-buffered/credit-conservation.svg) |
| 14-A | 原创资源依赖教学例；原书 §14.2.1 | [draw.io](/notes/booksim-notes/pic/14-deadlock/resource-dependency.drawio) | [SVG](/notes/booksim-notes/pic/14-deadlock/resource-dependency.svg) |
| 16-A | 原书 §16.1–16.4 与 IQRouter；抽象架构 | [draw.io](/notes/booksim-notes/pic/16-router/iq-router.drawio) | [SVG](/notes/booksim-notes/pic/16-router/iq-router.svg) |
| 18-A | 原创服务轨迹；原书 §18.4.2 | [draw.io](/notes/booksim-notes/pic/18-arbitration/round-robin-service.drawio) | [SVG](/notes/booksim-notes/pic/18-arbitration/round-robin-service.svg) |
| 19-A | 原创二部图算例；原书 §19.1–19.2 | [draw.io](/notes/booksim-notes/pic/19-allocation/bipartite-matching.drawio) | [SVG](/notes/booksim-notes/pic/19-allocation/bipartite-matching.svg) |
| 23-A | 固定版本 TrafficManager::_RetireFlit；原创时间戳算例 | [draw.io](/notes/booksim-notes/pic/23-metrics/latency-boundaries.drawio) | [SVG](/notes/booksim-notes/pic/23-metrics/latency-boundaries.svg) |
| 补充 | BookSim2 软件对象关系；非 RTL | [draw.io](/notes/booksim-notes/pic/02-model/simulation-model.drawio) | [SVG](/notes/booksim-notes/pic/02-model/simulation-model.svg) |

保留的教材局部插图：第 1 章 Figure 1.1（p. 2）、Figure 1.11（p. 19）、Figure 1.12（p. 20），沿用现有 `pic/1/` 图片；其权利归教材作者/出版者，不能随本站原创图的说明推定获得再许可。

## 参考资料与借鉴范围

- William J. Dally and Brian Towles. *Principles and Practices of Interconnection Networks*. Morgan Kaufmann, 2004。章节、案例和公式的首要来源；各章列印刷页码。原书图未整页复制，新图为注明依据的重新组织/原创教学图。
- [BookSim2](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)：固定版本源码，一切实现结论均限定于此版本。
- [SiliconCrafters, Fixed Priority Arbiter](https://www.siliconcrafters.com/post/fixed-priority-arbiter)，2024-03-30（2024-05-16 更新）：第 18 章 prefix-mask 的补充讲解来源，未复制 RTL。
- [SiliconCrafters, Round Robin Arbiter](https://www.siliconcrafters.com/post/round-robin-arbiter)，2024-03-31（2024-05-16 更新）：第 18 章轮转优先级和结构比较的补充来源，未复制代码与图片。

[专栏导读](00_Introduction.md) · [补充实验](appendix-simulation-results.md) · [专栏目录](/booksim-series.html)
