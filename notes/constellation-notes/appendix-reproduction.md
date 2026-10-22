# 实验附录｜在个人 fork 中复现 Constellation

> 核对日期：2026-10-22。本文记录已实际检查的工具链、fork 差异和本次 smoke test。命令使用通用工作目录，不依赖特定机器身份。学习正文保留上游固定提交，运行入口采用兼容适配后的个人 fork。

## 1. 区分阅读基线与运行基线

| 层次 | 仓库 / 提交 | 用途 |
| --- | --- | --- |
| 上游源码阅读 | `ucb-bar/constellation@c1b42cd0c7c7d6e4fc1ed9bf1f86fbd3b31ac510` | 正文中的固定接口、实现与行号 |
| 实验 fork | [`hujian404/constellation@e01ef4ab5ce3cab80431c420ce5d5fa3f67c3dd3`](https://github.com/hujian404/constellation/tree/e01ef4ab5ce3cab80431c420ce5d5fa3f67c3dd3) | 已适配构建与评估门槛的运行版本 |
| 父工程 | [`hujian404/chipyard@e27c6561c0066c1f60bf4eb4885a38391c850ac0`](https://github.com/hujian404/chipyard/tree/e27c6561c0066c1f60bf4eb4885a38391c850ac0) | 本次实际使用的 Chipyard 集成工程 |

不能只记录一个 Constellation SHA 就声称环境完全固定。本次父工程还存在本地 sbt 适配、Netrace 路径兼容链接和其他已有工作区状态；Espresso 子模块也显示为非干净状态。因此以下记录是“实际环境中的 smoke 验证”，不是一次全新、干净 checkout 的端到端复现证明。验证过程中没有覆盖或清理这些已有修改。

## 2. 本次核实的工具链

| 工具 / 组件 | 实际版本或提交 | 证据 |
| --- | --- | --- |
| OS / 架构 | Ubuntu 22.04.5 LTS，Linux 6.8.0-136-generic，x86_64 | 系统版本查询 |
| Java | Eclipse Temurin OpenJDK 23.0.2+7 | `java -version` |
| sbt | 1.11.4 | 父工程 `project/build.properties` |
| Scala | 2.13.16 | `show scalaVersion` |
| Chisel | 6.7.0 | `show libraryDependencies` |
| chiseltest | 6.0.0 | `show libraryDependencies` |
| Verilator | 5.046，开发修订 `v5.046-55-g1264184fb` | `verilator --version` |
| GNU C++ | 11.4.0 | `g++ --version` |
| GNU Make | 4.3 | 系统 make 版本查询 |
| CMake | 3.22.1 | `cmake --version` |
| Espresso | `2cc477880bd99a40f257155a676fc61fd53e0d9e`，存在本地差异 | 子模块 HEAD / status |
| Netrace | `bf30293e05da0ff7057be209deb7dc0317f08b09` | 子模块 HEAD |
| Rocket Chip | `55bcad0f59436de98ea510334121de8546b9e9d7` | 子模块 HEAD |
| Diplomacy | `fe5e131d4fc8adec14a3ce4a4935bb5c0a269871` | 子模块 HEAD |

fork 的 ScalaTest 声明仍是动态版本 `3.2.+`，不能据此填写一个未经解析核对的精确小版本。需要严格重建时应额外归档 resolved dependency report、工具安装来源以及 Espresso 本地补丁。这里展示的是已有可工作组合，不建议为了阅读正文盲目升级全部工具。

## 3. fork 改了什么，没证明什么

对比上游阅读基线与实验 fork，主要差异位于 `build.sbt`、`test/Configs.scala` 和 `mydocs/`：

1. Scala 调整为 2.13.16；Chipyard 集成分支补充 chiseltest 6.0.0 与 ScalaTest 测试依赖。
2. 历史 `chisel3-plugin` 只在 standalone 分支添加，集成模式使用父工程提供的 Chisel plugin，避免重复或不兼容的插件组合。
3. `EvalTestConfig03.requiredMaxLatency` 从 210 调为 250。
4. 增加环境、构建与测试记录。

第三项是**验收门槛变化**，不是 router、路由或流控优化。本次观测的最大时延是 225 cycles，超过原门槛 210，却满足 fork 的 250；不能将“现在通过”写成“硬件时延降低”。源码中的 generic throughput 报告也需按第 19 章解释其分母。

父工程本地把 sbt 从 1.8.2 调整到 1.11.4，属于构建环境适配，不在 Constellation fork 的提交边界内。历史文档还记录了 JVM 网络配置、Espresso 安装和 Verilator PCH 兼容 wrapper；这些应与设计参数分开归档。

## 4. 已有集成工程中的最短验证路径

本段假设已准备好上述兼容 Chipyard 工程及其所需子模块，并已将 `generators/constellation` 切到实验 fork 提交。它是运行验证步骤，不是一键安装脚本。先在父工程根目录执行：

```bash
export CHIPYARD_ROOT="$(pwd)"
test -f "$CHIPYARD_ROOT/build.sbt"
test -f "$CHIPYARD_ROOT/generators/constellation/build.sbt"

# 集成模式由父工程提供 Chisel / Rocket Chip
unset CONSTELLATION_STANDALONE
export PATH="$HOME/.local/bin:$PATH"
export JAVA_OPTS="-Xmx8G -Dfile.encoding=UTF-8 -Djava.net.preferIPv4Stack=true"
export SBT_OPTS="-Xmx8G -Djava.net.preferIPv4Stack=true"

git rev-parse HEAD
git -C generators/constellation rev-parse HEAD
git status --short
git -C generators/constellation status --short
sbt -batch -no-colors 'project constellation' \
  'show scalaVersion' 'show libraryDependencies' compile
```

JVM IPv4 选项来自已有环境适配，不是 NoC 正确性要求。`PATH` 中的用户态工具应明确记录来源；执行全量测试前，还应按可用资源限制 forked test 并发，不能将源码中 72 的并发上限直接等同于当前机器适合的设置。

### Netrace 链接前提

评估 suite 会链接预构建的 `netrace.o`。确保子模块存在，并用位置无关代码编译；在集成模式下核对测试代码的相对链接路径：

```bash
cd "$CHIPYARD_ROOT"
make -C generators/constellation/src/main/resources/csrc/netrace \
  netrace.o CC=gcc CFLAGS="-Wall -O3 -c -g -fPIC"

# 仅当目标不存在时创建兼容链接；若已有不同文件，先检查，不覆盖
mkdir -p src/main/resources/csrc
if [ ! -e src/main/resources/csrc/netrace ] && \
   [ ! -L src/main/resources/csrc/netrace ]; then
  ln -s ../../../../generators/constellation/src/main/resources/csrc/netrace \
    src/main/resources/csrc/netrace
fi
test -f src/main/resources/csrc/netrace/netrace.o
```

这里的四级 `..` 是从 `src/main/resources/csrc` 返回父工程根目录。少写层级会产生能被创建却无法解析的链接。该步骤是集成测试链接兼容，不应被解释为 NoC 生成器的一部分。

### 本次实际执行的代表性测试

```bash
cd "$CHIPYARD_ROOT"
sbt -batch -no-colors 'project constellation' \
  'testOnly constellation.NoCTest00 constellation.NoCTestTL00 constellation.NoCTestAXI400 constellation.NoCTestEval03'
```

| Suite | 配置 / 机制 | 2026-10-22 本次结果 |
| --- | --- | --- |
| `NoCTest00` | 两节点 core NoC | PASS |
| `NoCTestTL00` | TileLink 传输 harness | PASS |
| `NoCTestAXI400` | AXI4 传输 harness | PASS |
| `NoCTestEval03` | 带评估门槛的十节点单向环 | PASS（fork 门槛） |

汇总为 4 suites、4 tests succeeded、0 failed、0 aborted，进程退出码 0。增量 compile 的 sbt 时间为 2 s，测试任务报告 18 s；这些时间使用已有依赖和构建产物，**不是全新编译耗时**。本次测试不是新的 Netrace 应用回放实验，不能仅因链接了 Netrace 就把 Eval03 结果称为 trace workload 性能。

已知旧日志中另有 2026-08-10 的全量记录：93 tests succeeded、0 failed、0 aborted，sbt Total time 930 s。它是本次查阅的历史证据，原始日志没有完整绑定本次全部环境状态，不能冒充 2026-10-22 新跑的全量回归。

## 5. Eval03 的结果应如何读

本次日志报告：

```text
Min throughput: 2, 6, 0.97619
Median latency: 28
Max latency: 225
```

按 `TrafficEval.cpp`，latency 是逐 flit 的 `current_cycle - creation_cycle`，包含 C++ 入口队列等待。`0.97619` 是流 2→6 的窗口接收数 / 产生数比例，不是该输出每拍传输了 0.97619 个 flit。窗口边界不同还可能导致某些流的此比例大于 1，并不表示物理链路突破了容量。

| 检查项 | 配置门槛 | 本次报告 | 判定 |
| --- | --- | --- | --- |
| 最差流比例 | ≥ 0.9 | 0.97619 | 满足 |
| 中位 flit 时延 | ≤ 30 cycles | 28 cycles | 满足 |
| 最大 flit 时延（上游） | ≤ 210 cycles | 225 cycles | 不满足原门槛 |
| 最大 flit 时延（fork） | ≤ 250 cycles | 225 cycles | 满足调整门槛 |

这些是单一配置、固定随机源和既定窗口的观测，尚未构成饱和吞吐曲线、多 seed 置信区间、面积或频率结果。原始日志保留于本地验证缓存；公开版只整理必要的无身份摘要：[本次验证记录](/notes/constellation-notes/experiments/2026-10-22-smoke-summary.txt)。

## 6. 继续学习的顺序

先结合第 5–10 章手算 `TestConfig00` 的规格，再跑 `NoCTest00`。随后读第 11–14 章，在数据、选择、credit 和 VC 所有权之间建立逐拍关系。最后读第 18–20 章，自行增加注入率扫描，并保留完整统计口径和配置。

fork 的详细工程说明可参考固定版本的 [构建说明](https://github.com/hujian404/constellation/blob/e01ef4ab5ce3cab80431c420ce5d5fa3f67c3dd3/mydocs/BUILD_AND_RUN_CONSTELLATION.md)与[历史测试记录](https://github.com/hujian404/constellation/blob/e01ef4ab5ce3cab80431c420ce5d5fa3f67c3dd3/mydocs/TEST_RESULTS.md)。本附录以本次实际检查和执行结果为准，避免把历史说明中的推断直接当作新的测量结论。

[返回专栏导读](00-series-guide.md)
