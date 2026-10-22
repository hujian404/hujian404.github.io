# Chapter 1｜Introduction to Interconnection Networks

> 原书：William J. Dally、Brian Towles，*Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004），第 1 章，印刷页 1–24。本地参考 PDF 的页序为印刷页 +27。以下为中文学习整理，保留原书全部目录小节的编号与标题，不是逐句翻译。BookSim2 对照版本固定为 [`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

[专栏导读](00_Introduction.md) · [原书目录与页码对照](appendix-reading-map.md)

## 1.1 Three Questions About Interconnection Networks

*原书印刷页 2。*

原书先问三个问题：互连网络是什么，在哪里使用，以及为什么重要。它的任务是让一组终端交换信息；网络既包括连接关系，也包括共享资源的使用规则。对于 NoC，终端可以是 core、cache、memory controller 或加速器，不能只把 router 的连线图当成完整网络。共享连接资源能替代大量专用连线，但也使带宽、争用和延迟成为系统设计的关键问题。

![互连网络的终端视图](pic/1/image-20260807161813826.png)

*来源：Dally 与 Towles，原书 Figure 1.1，p. 2；沿用本专栏已有局部插图，权利归原出版者/作者。*

图中终端共享同一网络资源，不意味着所有通信在同一拍竞争同一条物理线。拓扑决定可并行路径，路由与流控决定这些路径怎样被使用。

## 1.2 Uses of Interconnection Networks

*原书印刷页 4。*

原书以处理器—存储器、I/O 和分组交换结构说明需求如何决定设计。学习时先写出消息格式、可靠性、顺序及吞吐约束，再选择网络。相同拓扑用在不同协议中，流控和接口设计可能完全不同。

### 1.2.1 Processor-Memory Interconnect

*原书印刷页 5。*

读请求通常携带地址和命令，响应可能携带整条 cache line；请求与响应的长度和依赖不对称。必须计入协议诱发的流量，尤其要区分网络资源死锁和一致性协议的等待环。

### 1.2.2 I/O Interconnect

*原书印刷页 8。*

I/O 互连连接设备和内存系统，带宽之外还涉及 DMA、缓冲、顺序与软件可见完成。终端的生产和消费能力会改变网络观察到的负载。

### 1.2.3 Packet Switching Fabric

*原书印刷页 11。*

交换结构位于外部输入、输出线路之间。线卡排队、fabric 传输和输出调度共同影响系统吞吐；内部 speedup 不能自动消除输出端的拥塞。

## 1.3 Network Basics

*原书印刷页 13。*

按拓扑、路由、流控、router 和性能五个层次组织设计，每层都要向下一层交付可检查的约束。例如“最短路径”只限定路由长度，不保证无死锁，也不保证所有最短路径负载均匀。

### 1.3.1 Topology

*原书印刷页 13。*

拓扑定义终端、交换节点和 channel。比较 radix 时要声明是否包括本地端口，比较带宽时要说明按单向 channel 还是双向物理连接计数。

### 1.3.2 Routing

*原书印刷页 16。*

路由给出从源到目的地的合法路径或下一跳集合；其选择会改变 channel load，因此拓扑的理论容量不等于某种路由实际能达到的吞吐。

### 1.3.3 Flow Control

*原书印刷页 17。*

流控以 packet、flit 等单位管理带宽和存储资源。丢弃、等待和偏转会产生不同的可靠性、延迟及前进性问题。

### 1.3.4 Router Architecture

*原书印刷页 19。*

router 把算法变成数据通路、状态机和调度逻辑。逻辑功能相同，流水级划分及反馈延迟不同，也会得到不同性能。

![Router 的输入缓冲、交换与分配](pic/1/image-20260807163123141.png)

*来源：Dally 与 Towles，原书 Figure 1.11，p. 19；沿用本专栏已有局部插图，权利归原出版者/作者。*

数据从输入缓冲经过 crossbar 到输出，控制分配同时约束下游空间和本拍带宽。输入 i 与输出 j 各只能参与至多一次单位容量传输；这一约束在第 19 章转化为二部图匹配。下游有空位但未赢得 crossbar，或者赢得候选仲裁却没有下游容量，都不能完成发送。

### 1.3.5 Performance of Interconnection Networks

*原书印刷页 19。*

延迟—负载曲线应同时标出零负载延迟、饱和区和测量单位。只报平均 latency 而不报 accepted traffic，可能把丢包或者源端积压掩盖起来。

![延迟与 offered traffic 的关系](pic/1/image-20260807163305190.png)

*来源：Dally 与 Towles，原书 Figure 1.12，p. 20；沿用本专栏已有局部插图，权利归原出版者/作者。*

曲线起点是给定实现的零负载延迟 T0；理想最短距离和实际平均路径给出不同基线。负载上升后队列等待增加，在饱和附近急剧放大。图中区分拓扑和路由容量限制，说明更多物理带宽若没有被路由有效使用，也不能自动转化为 accepted throughput。

## 1.4 History

*原书印刷页 21。*

原书的历史脉络说明互连从专用机器结构发展为可复用设计方法。阅读经典案例的价值在于理解引脚、布线和实现技术如何塑造选择，而不是把当年的参数当成现代工艺默认值。

## 1.5 Organization of this Book

*原书印刷页 23。*

第 1、2 章建立问题和完整小案例；3–7 章研究拓扑，8–11 章研究路由，12–15 章研究流控，16–22 章研究 router 与接口，23–25 章研究性能与仿真。本专栏保留这 25 章以及原书小节编号，源码和追加实验放在各章末或附录。

## BookSim2 源码对照与适用边界

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/networks/network.cpp 第 80–91 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/networks/network.cpp#L80-L91)。

```cpp
Network * Network::New(const Configuration & config, const string & name)
{
  const string topo = config.GetStr( "topology" );
  Network * n = NULL;
  if ( topo == "torus" ) {
    KNCube::RegisterRoutingFunctions() ;
    n = new KNCube( config, name, false );
  } else if ( topo == "mesh" ) {
    KNCube::RegisterRoutingFunctions() ;
    n = new KNCube( config, name, true );
  } else if ( topo == "cmesh" ) {
    CMesh::RegisterRoutingFunctions() ;
```

`Network::New` 选择拓扑对象；之后还要读 router 工厂、routing function 注册、TrafficManager 注入与统计。拓扑工厂不决定整个网络行为。

## 来源与继续阅读

- 原书第 1 章，pp. 1–24；各节页码已逐项列出。案例与原书公式均以本地参考书为依据。
- [BookSim2 固定版本源码](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)，节选保留[上游许可](/notes/booksim-notes/source-license.txt)。
- [全书章节/源码路线与图片来源](appendix-reading-map.md)。新增图均附 `.drawio` 源文件，插图是结构说明，不是测量波形。

[上一篇](00_Introduction.md) · [下一篇](02_a_simple_interconnection_network.md) · [专栏目录](/booksim-series.html)
