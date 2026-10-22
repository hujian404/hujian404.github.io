# 18｜Netrace 与 Traffic Evaluation

> 更新：2026-10-22。源码基线：[`c1b42cd`](https://github.com/ucb-bar/constellation/tree/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510)。本文按原定章节顺序展开；源码节选、教学示例与实验计划分别标明。运行版本、工具链及本次四项代表性验证见[实验复现附录](appendix-reproduction.md)；教学示意与未执行的扩展实验另行标明。

## 1. 合成流量与 trace 回放回答不同问题

合成流量通过每个 flow 的注入率隔离观察网络行为，适合做负载扫描；Netrace 回放带有应用通信与依赖关系，适合比较特定 workload。后者仍不是完整 CPU / cache / memory 时序模拟，不应把网络回放加速比直接写成应用加速比。

## 2. 评估参数在 Scala 与 C++ 之间传递

以下为固定版本的源码节选，省略外围上下文：[查看 src/main/scala/test/TrafficEvalHarness.scala 第 72–85 行](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/test/TrafficEvalHarness.scala#L72-L85)。

```scala
case class NoCEvalParams(
  nocParams: NoCParams = NoCParams(),
  warmupCycles: Int = 5000,
  measurementCycles: Int = 20000,
  drainTimeoutCycles: Int = 100000,
  flitsPerPacket: Int = 4,
  flows: (Int, Int) => Double = (a: Int, b: Int) => 0.0,
  requiredThroughput: Double = 0.0,
  requiredMedianLatency: Int = 99999,
  requiredMaxLatency: Int = 99999,
  netraceEnable: Boolean = false,
  netraceRegion: Int = 2, // this is the PARSEC region-of-interest
  netraceTrace: String = "blackscholes_64c_simsmall.tra.bz2",
  netraceIgnoreDependencies: Boolean = false
```

NoCEvalParams 通过 `toConfigStr` 生成 noceval.cfg。EvalHarness 提供 cycle 计数并连接 TrafficEvalIngress / Egress；后续由 C++ 模型产生与回收 flit。这里 case class 的默认值是生成配置的默认，不应与 C++ 在没有配置文件时的默认值混为一谈。

固定版本官方路径在兼容的 Chipyard / VCS 环境中为：

```bash
cd chipyard/sims/vcs
make SUB_PROJECT=constellation BINARY=none CONFIG=EvalTestConfig00 MODEL=EvalHarness run-binary-debug
# 复制 generated-src 中实际生成的 noceval.cfg 为独立实验配置，修改后再运行
make SUB_PROJECT=constellation BINARY=none CONFIG=EvalTestConfig00 MODEL=EvalHarness run-binary-debug EXTRA_SIM_FLAGS="+eval_params=/absolute/path/noceval.cfg"
```

命令中的配置路径需替换为真实文件；本次没有执行该仿真。

## 3. Trace 设置必须和端点映射匹配

应逐项检查 `netrace_enable`、`netrace_trace`、`netrace_region`、`netrace_ignore_dependencies`，以及 trace 节点如何映射到 ingress / egress。默认 region 2 的注释指向 PARSEC ROI，但实际 trace 是否具有该 region 必须检查其元数据。

保留 dependencies 时，后续包是否能注入会受前序包完成影响；忽略 dependencies 改变了工作负载语义。这两个结果应标成不同实验，不能把忽略依赖当成单纯提速仿真。

## 4. 注入率的单位来自实现

C++ 随机模型用 `sample*flits_per_packet < flow.rate` 判断生成 packet，因此在适用范围内，rate 表达期望 flit/cycle，而不是 packet/cycle。每个 ingress 的多个 flow 还会把包放入共同的入口软件队列；总 offered load 超过入口能力时，等待会积累在网络之前。

练习：先对一个 flow 设置 rate=0.1、packet 长度 4，手算期望 packet 生成概率为 0.025/拍；然后检查实际注入与产生是否分离。Trace 实验再记录文件校验值、region、依赖开关、映射表和结束条件，否则同名 workload 也可能并非同一实验。

## 源码与延伸阅读

以下链接均固定到本章使用的源码版本：

- [src/main/scala/test/TrafficEvalHarness.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/test/TrafficEvalHarness.scala)
- [src/main/resources/csrc/TrafficEval.cpp](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/resources/csrc/TrafficEval.cpp)
- [docs/source/Evaluation/index.rst](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/docs/source/Evaluation/index.rst)

源码节选版权归 The Regents of the University of California，遵循 [BSD-3-Clause 许可及免责声明](/notes/constellation-notes/source-license.txt)。文字解读与教学图为专栏整理内容。

---

[上一篇](17-test-framework.md) · [专栏导读](00-series-guide.md)

[下一篇：19｜NoC 性能评价方法](19-noc-performance-evaluation.md)
