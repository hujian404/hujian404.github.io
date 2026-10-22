# 17｜Constellation Test Framework

> 更新：2026-10-22。源码基线：[`c1b42cd`](https://github.com/ucb-bar/constellation/tree/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510)。本文按原定章节顺序展开；源码节选、教学示例与实验计划分别标明。运行版本、工具链及本次四项代表性验证见[实验复现附录](appendix-reproduction.md)；教学示意与未执行的扩展实验另行标明。

## 1. 先确认正在运行哪个层次的测试

| 配置 | 测试族 | 覆盖重点 |
| --- | --- | --- |
| TestConfigXX | NoCTestXX | 核心 NoC 报文传输 |
| TLTestConfigXX | NoCTestTLXX | TileLink adapter 与传输 |
| AXI4TestConfigXX | NoCTestAXI4XX | AXI4 adapter 与传输 |
| EvalTestConfigXX | 评估 harness / 对应测试 | 流量、时延、吞吐门槛 |

固定版本中的准确 suite 名称以 `NocTests.scala` 为准；例如 core 的测试叫 `NoCTest00`，并不是 `TestConfig00`。不要用零匹配的测试过滤器产生“无测试失败”的假成功。

## 2. 测试框架如何连接硬件

以下为固定版本的源码节选，省略外围上下文：[查看 src/test/scala/constellation/NocTests.scala 第 10–13 行](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/test/scala/constellation/NocTests.scala#L10-L13)。

```scala
class NoCChiselTester(implicit val p: Parameters) extends Module {
  val th = Module(new TestHarness)
  when (th.io.success) { stop() }
}
```

tester 创建 TestHarness，并在 success 时调用 Chisel `stop()`；BaseNoCTest 使用 chiseltest 和 Verilator backend，最终 `runUntilStop(timeout=1000*1000)`。超时上限只是兜底，不是无死锁的证明。

在已经准备好固定版本 standalone 依赖的 Linux 环境中，可用以下方式选择 core suite：

```bash
export CONSTELLATION_STANDALONE=1
sbt 'testOnly constellation.NoCTest00'
```

这是依据 `build.sbt` 和 suite 名称给出的命令，不是本次验证通过记录。历史 standalone 依赖是否能解析取决于仓库与环境；Chipyard 内运行时应改用父工程实际项目入口。评估 suite 还依赖 Netrace 对象文件，不能把 core 命令当成全量测试部署脚本。

## 3. 让失败能定位到具体机制

建议先跑单 flow，再跑多输入竞争、目的端阻塞、单 flit packet、长 packet 和 reset 后首包。检查守恒：成功注入的唯一 flit 数应与成功接收数一致；每个 ID 恰好出现一次；payload、目的端与 head/tail 关系正确。若有 fifo 约束，再检查该流的顺序。

对 credit 修改，要额外覆盖 free 与 alloc 同拍；对仲裁修改，要在长短包混合和持续竞争下观察前进性。随机测试 seed、参数和超时值都应随日志保存，才能复现失败。

## 4. 生成检查、功能测试与性能测试分工

构建检查捕捉非法 topology / flow / routing；功能测试捕捉数据与资源错误；性能测试在正确前提下分析拥塞。三者应分开记录，功能跑通并不说明设计达到目标带宽。

练习：为两节点基线设计一个“接收端停 20 拍再恢复”的测试，预期没有丢包、credit 不超界、恢复后能排空。先写预期事件，再观察波形；不要只依赖最后 success 一位来解释设计行为。

## 5. 实验 fork 的本次验证入口

本轮使用 Chipyard 父工程中的 `project constellation`，没有启用 `CONSTELLATION_STANDALONE`。已经执行增量 compile，并通过 `NoCTest00`、`NoCTestTL00`、`NoCTestAXI400`、`NoCTestEval03` 四项 suite，0 failed、0 aborted。其余 suite 的 93/93 通过记录来自查阅到的历史日志，不冒充本次全量执行。

工具链、fork 相对上游的差异、Netrace 链接前提和完整命令见[实验复现附录](appendix-reproduction.md)。尤其应保留 Eval03 的最大时延阈值变化信息，否则“通过测试”会被错误解释为硬件改善。

## 源码与延伸阅读

以下链接均固定到本章使用的源码版本：

- [src/test/scala/constellation/NocTests.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/test/scala/constellation/NocTests.scala)
- [src/main/scala/test/TestHarness.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/test/TestHarness.scala)
- [build.sbt](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/build.sbt)

源码节选版权归 The Regents of the University of California，遵循 [BSD-3-Clause 许可及免责声明](/notes/constellation-notes/source-license.txt)。文字解读与教学图为专栏整理内容。

---

[上一篇](16-chipyard-integration.md) · [专栏导读](00-series-guide.md)

[下一篇：18｜Netrace 与 Traffic Evaluation](18-netrace-traffic-evaluation.md)
