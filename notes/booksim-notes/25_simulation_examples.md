# Chapter 25｜Simulation Examples｜从 smoke 到实验闭环

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. 三份可以直接保存的最小配置

本专栏附带 `experiments/mesh2x2-flit002.cfg`、`mesh2x2-flit010.cfg` 和 `mesh2x2-flit020.cfg`。除注入率为0.02、0.10、0.20外，其他设置一致：2×2 Mesh、DOR、4 VC×4 flit、4-flit packet、uniform、seed=1，注入率单位显式设为 flit/node/cycle。

将 experiments 目录放到固定版本源码仓库根目录后运行：

```bash
make -C src -j4
./src/booksim experiments/mesh2x2-flit002.cfg > smoke-002.log
./src/booksim experiments/mesh2x2-flit010.cfg > smoke-010.log
./src/booksim experiments/mesh2x2-flit020.cfg > smoke-020.log
```

配置下载：[0.02](/notes/booksim-notes/experiments/mesh2x2-flit002.cfg)、[0.10](/notes/booksim-notes/experiments/mesh2x2-flit010.cfg)、[0.20](/notes/booksim-notes/experiments/mesh2x2-flit020.cfg)。该固定提交在正常完成时返回 Unix 退出码255，不能直接用通常的 exit 0 约定判断。请同时核对最终统计、排空与异常信息，包装脚本示例见[验证摘要](appendix-simulation-results.md)。

## 2. 注入单位的源码证据

默认 injection_rate 按 packet/cycle 解释；本例启用 `injection_rate_uses_flits=1`。4-flit packet、负载0.10时，产生器使用的平均 packet 生成概率为0.025/node/cycle，而不是每拍0.10个packet。端点实际可注入速率还会受到队列与credit限制。

## 3. 三个点的用途与边界

这些配置用于核实构建、配置解析、路由组合和统计输出。它们没有扫描饱和区，也没有排除所有自发送；不能从小Mesh的低负载结果推断大规模网络、多种traffic或RTL实现的表现。

本次实际执行结果另列于[验证摘要](appendix-simulation-results.md)。那里区分运行环境、观测值和没有执行的扩展实验。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/trafficmanager.cpp 第 209–212 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.cpp#L209-L212)。

```cpp
    if(config.GetInt("injection_rate_uses_flits")) {
        for(int c = 0; c < _classes; ++c)
            _load[c] /= _GetAveragePacketSize(c);
    }
```

_load 除以平均 packet size 后交给注入过程。保持 flit 负载不变、改 packet_size，会同时改变 packet 生成频率和序列化；保持 packet/cycle 不变则改变总 flit 需求。两类对照实验回答不同问题，不能混在一张横轴不明的图里。

## 5. 学习练习与实验边界

下一步先扩大 sample_period 和seed范围，再选择一种目标流量逐步扫描负载。若研究VC，保持总slots；若研究topology，核对channel延迟和端口容量；若研究allocator，说明delay是否固定。每个结果都应回到具体配置、原始计数与失败状态，才能成为可复查的研究记录。

## 源码与阅读导航

- [src/trafficmanager.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.cpp)
- [src/examples/mesh88_lat](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/examples/mesh88_lat)
- [src/booksim_config.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/booksim_config.cpp)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](24_simulation.md) · [专栏导读](00_Introduction.md)

---

[返回专栏目录](/booksim-series.html)
