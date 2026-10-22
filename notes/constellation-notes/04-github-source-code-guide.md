# 04｜GitHub 工程结构与源码阅读方法

> 更新：2026-10-22。源码基线：[`c1b42cd`](https://github.com/ucb-bar/constellation/tree/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510)。本文按原定章节顺序展开；源码节选、教学示例与实验计划分别标明。运行版本、工具链及本次四项代表性验证见[实验复现附录](appendix-reproduction.md)；教学示意与未执行的扩展实验另行标明。

## 1. 固定版本，再建立阅读顺序

本系列采用规划文件中的 commit `c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510`。源码链接都固定到这一提交；`master`、在线 latest 文档和个人 fork 可能继续变化。复现实验还应记录 Chipyard、Rocket Chip、JDK、sbt、Chisel 和模拟器版本，不能只记录 Constellation SHA。

建议在独立参考目录检出该提交，不要在有未提交修改的工作目录直接切换版本：

```bash
git clone https://github.com/ucb-bar/constellation.git constellation-study
cd constellation-study
git checkout --detach c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510
git rev-parse HEAD
```

以上为复现准备命令，本轮另在实验 fork 的 Chipyard 集成环境执行了增量编译和代表性测试；上面的独立 checkout 用于源码阅读，不等于完整构建环境。

## 2. 按问题定位目录

| 目录 / 文件 | 第一遍要寻找什么 |
| --- | --- |
| `test/Configs.scala` | `TestConfig00`：最小实际入口 |
| `noc/Parameters.scala` | 参数展开、合法性检查 |
| `topology/Topologies.scala` | 物理有向边判定 |
| `channel/Parameters.scala`、`Channel.scala` | 资源参数与接口方向 |
| `routing/RoutingRelations.scala` | 合法 VC 转移 |
| `router/Router.scala` | 子模块实例和连接 |
| `router/InputUnit.scala`、`OutputUnit.scala` | 缓存、报文状态、credit |
| `protocol/`、`soc/` | 协议打包与 Chipyard 集成 |
| `test/TrafficEvalHarness.scala`、`resources/csrc/` | 流量产生与统计 |

表中 Scala 路径均相对 `src/main/scala/`。测试套件另在 `src/test/scala/constellation/NocTests.scala`。

## 3. 从测试名字反向追配置

以下为固定版本的源码节选，省略外围上下文：[查看 src/test/scala/constellation/NocTests.scala 第 57–60 行](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/test/scala/constellation/NocTests.scala#L57-L60)。

```scala
abstract class NoCTest(configs: Seq[Config]) extends BaseNoCTest(p => new NoCChiselTester()(p), configs)
abstract class TLNoCTest(configs: Seq[Config]) extends BaseNoCTest(p => new TLNoCChiselTester()(p), configs)
abstract class AXI4NoCTest(configs: Seq[Config]) extends BaseNoCTest(p => new AXI4NoCChiselTester()(p), configs)
abstract class EvalNoCTest(configs: Seq[Config]) extends BaseNoCTest(p => new EvalNoCChiselTester()(p), configs, Seq("../../../src/main/resources/csrc/netrace/netrace.o"))
```

`NoCTest00` 是 ScalaTest suite，`TestConfig00` 是生成器配置，`NoCChiselTester` 是包住硬件 harness 的 Chisel Module。它们名字相似但角色不同。先找到 suite 如何传递配置，再看 harness 如何读取 `NoCTesterKey`，最后才看 NoC 实例化。

可以在源码根目录使用以下检索，而不是全仓库按文件逐个阅读：

```bash
rg -n 'class TestConfig00|class NoCTest00' src
rg -n 'InternalNoCParams|new NoC|new Router' src/main/scala
rg -n 'router_req|vcalloc_req|credit_return|vc_free' src/main/scala/router
```

## 4. 每一段代码留下四条笔记

记录输入、输出、状态和不变量。例如 OutputUnit 的输入包含分配和 credit 返回，输出包含资源可用信息；状态包括 `occupied`、`c` 和 `flow`；不变量是 credit 不超界、同一输出 VC 不被两个报文同时占用。这样读完一个类后能解释它的硬件职责，而不仅是知道成员变量名称。

Chisel 用法优先按此固定版本理解：该树的 `build.sbt` 含历史 standalone 依赖与 Chisel 3.5.6 plugin 配置，Chipyard 集成还由父工程决定依赖。不要直接套用最新版 Chisel 的构建模板。练习：写出 `NoCTest00 → TestConfig00 → TestHarness → NoC → Router` 的路径表，并为每条边找到实际引用。

## 源码与延伸阅读

以下链接均固定到本章使用的源码版本：

- [src/test/scala/constellation/NocTests.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/test/scala/constellation/NocTests.scala)
- [src/main/scala/test/TestHarness.scala](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/src/main/scala/test/TestHarness.scala)
- [build.sbt](https://github.com/ucb-bar/constellation/blob/c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510/build.sbt)

源码节选版权归 The Regents of the University of California，遵循 [BSD-3-Clause 许可及免责声明](/notes/constellation-notes/source-license.txt)。文字解读与教学图为专栏整理内容。

---

[上一篇](03-constellation-architecture.md) · [专栏导读](00-series-guide.md)

[下一篇：05｜NoC Specification 与 NoCParams](05-noc-specification.md)
