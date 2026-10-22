# 16｜Chipyard / RocketChip 集成

> 更新：2026-10-22。源码基线：[`c1b42cd`](https://github.com/ucb-bar/constellation/tree/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510)。本文按原定章节顺序展开；源码节选、教学示例与实验计划分别标明。运行版本、工具链及本次四项代表性验证见[实验复现附录](appendix-reproduction.md)；教学示意与未执行的扩展实验另行标明。

## 1. 独立 NoC 与完整 SoC 的边界

Chipyard-Standalone 用 harness 驱动 NoC，便于观察路由、流控和负载；Chipyard-SoC 将网络接入实际总线与协议端点，才会暴露地址空间、外设、缓存、coherence 和时钟域约束。独立网络测试通过之后，还应在集成环境验证真实事务。

固定版本的 `soc/` 包含 Buses.scala、Configs.scala 和 GlobalNoC.scala。各自负责总线 wrapper、配置片段和共享全局网络。上游文档提到 Chipyard 的 MultiNoCConfig / SharedNoCConfig，具体用法需要匹配相同 Chipyard 版本。

## 2. 配置片段改的是总线实例化

以下为固定版本的源码节选，省略外围上下文：[查看 src/main/scala/soc/Configs.scala 第 17–27 行](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/soc/Configs.scala#L17-L27)。

```scala
class WithSbusNoC(tlnocParams: TLNoCParams, inlineNoC: Boolean = false) extends Config((site, here, up) => {
  case TLNetworkTopologyLocated(InSubsystem) => {
    up(TLNetworkTopologyLocated(InSubsystem), site).map(topo => {
      topo match {
        case j: TLBusWrapperTopology => {
          new TLBusWrapperTopology(j.instantiations.map(inst => inst match {
            case (SBUS, sbus_params: SystemBusParams) =>
              (SBUS, ConstellationSystemBusParams(sbus_params, tlnocParams, inlineNoC))
            case a => a
          }), j.connections)
        }
```

该片段读取上层 `TLNetworkTopologyLocated(InSubsystem)`，保留拓扑连接信息，但把 SystemBus 对应实例替换为 Constellation wrapper。`Config((site,here,up)=>...)` 是 CDE 参数覆盖机制，不是 Chisel 中的寄存器配置端口。

`LazyModule` 负责先建立协议 / 参数连接图，再通过 `LazyModuleImp` 实现硬件。总线宽度、端点能力与连接关系需要在生成前协商；因此直接把一个裸 `new Router` 接到总线不能完成替换。

## 3. 集成必须提供的映射

| 信息 | 为什么需要 |
| --- | --- |
| master / manager 到物理节点 | 决定 terminal 位置与通信距离 |
| ingress / egress 顺序 | 协议生成的 ID 必须与映射一致 |
| 地址与事务能力 | 保留可达地址、source ID 和协议协商结果 |
| vNet 与资源划分 | 多消息类别的前进性 |
| 数据宽度与转换 | 影响 flit 数、buffer 和 credit |
| clock / reset / crossing | 跨域接口与初始化一致性 |

GlobalNoC 将多个逻辑互连放到共享物理网络时，节省物理资源的同时引入新的竞争。它不能直接复用“每条逻辑总线独立时”的所有性能和隔离结论。

## 4. 建议的集成验收

先保留最小 CPU / memory / peripheral 系统，运行可观察的读写事务，再扩展到多个发起端和一致性流量。对每一步保存生成参数、端点顺序、地址映射、仿真输出和失败波形。若出现超时，应先确认协议终端和地址路由是否正确，而不是立即增加 VC。

练习：选定一条 SystemBus，画出替换前的 master→crossbar→manager 与替换后的 master→adapter→NoC→adapter→manager，并为每个边界标明协议、位宽和时钟。本文没有改动 Chipyard 工程，也没有声明完成 SoC 启动测试。

## 源码与延伸阅读

以下链接均固定到本章使用的源码版本：

- [src/main/scala/soc/Configs.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/soc/Configs.scala)
- [src/main/scala/soc/Buses.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/soc/Buses.scala)
- [src/main/scala/soc/GlobalNoC.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/soc/GlobalNoC.scala)
- [docs/source/SoCIntegration/index.rst](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/docs/source/SoCIntegration/index.rst)

源码节选版权归 The Regents of the University of California，遵循 [BSD-3-Clause 许可及免责声明](/notes/constellation-notes/source-license.txt)。文字解读与教学图为专栏整理内容。

---

[上一篇](15-tilelink-axi4-protocol.md) · [专栏导读](00-series-guide.md)

[下一篇：17｜Constellation Test Framework](17-test-framework.md)
