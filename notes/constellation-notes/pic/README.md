# Constellation 图示归档

按章节与主题整理。每幅新图同时提供可编辑的 `.drawio` 和网页引用的 `.svg`，二者使用相同节点与坐标；在 draw.io 中修改后请同步更新 SVG，避免图源与展示稿不一致。

| 目录 | 内容 | 引用章节 |
| --- | --- | --- |
| 00-series-guide | 原有整体 SoC 图 | 00 |
| 03-architecture | 生成器与硬件分层 | 03 |
| 06-topology | 有向链路与双向链 | 06 |
| 08-flow | flow、vNet 与 VC | 08 |
| 10-elaboration | Scala 到 RTL 的边界 | 10 |
| 11-router | router 数据与控制通路 | 11 |
| 12-flow-control | credit 与 VC 所有权 | 12 |
| 20-experiments | 可复现实验流程 | 20 |

新图是教学结构示意，不是自动生成拓扑、周期精确波形、性能数据或物理布局。06 图中的虚线仅用来区别反向物理链路；11 图中的虚线表示控制；12 / 20 图中的虚线表示返回路径，请结合各图说明阅读。

## 工程规格与时序图（2026-10-22）

新增五幅采用统一的白底、衬线字体、细线和低饱和色，由 draw.io 原生导出 SVG，保留同名可编辑图源：

| 文件 | 说明 | 引用章节 |
| --- | --- | --- |
| 06-topology/mesh-engineering-spec | flow 裁剪前的 2×2 Mesh 规格、资源与 terminal 映射 | 06 |
| 07-interfaces/ready-valid-timing | 终端握手、数据保持与接收事件 | 07 |
| 11-router/router-engineering-spec | flit 数据、资源分配与反向状态 | 11 |
| 12-flow-control/credit-accounting-timing | credit pre / post 状态及同拍返回和消耗 | 12 |
| 14-pipeline/packet-pipeline-schedule | head / body / tail 的理想事件顺序 | 14 |

这些时序是依据接口与计数语义绘制的教学示意，不是本次测试抓取的波形。正文逐一列出假设和适用边界。图中若线条交叉而没有连接点，不表示信号连接。
