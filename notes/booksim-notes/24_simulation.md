# Chapter 24｜Simulation｜构建、配置与可重复的周期模型

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. 固定源码与构建入口

本系列源码固定为 BookSim2 `28f43299f1706a3160ffac721ca461d74eb6e618`。构建入口是 src/Makefile，依赖 C / C++ compiler、GNU Make、Flex 和 Bison。固定提交仍不足以完全重建数值，还需保存工具版本、有效配置、seed 和运行输出。

```bash
git clone https://github.com/booksim/booksim2.git booksim-study
cd booksim-study
git checkout --detach 28f43299f1706a3160ffac721ca461d74eb6e618
make -C src -j4
```

本次已在独立临时目录完成构建并运行三个 smoke 配置。该提交的 main 将正常 Run 的 true 转成 -1（Unix 255），而非通常的0；返回码必须和最终统计、错误及 unstable 标记共同判断，具体见[验证附录](appendix-simulation-results.md)。

## 2. 周期精确的范围来自模型假设

BookSim 按离散周期组织 router、channel、credit 和 traffic；这不意味着它自动模拟门级传播、CDC、协议所有状态或物理拥塞。研究结论应限定在模型表达的层次，并说明哪些参数由硬件实现或外部模型提供。

源码里的计算开销影响仿真运行速度，配置里的 delay 影响被模拟网络；宿主机用了多少秒和 packet 花了多少cycle是两个坐标。

## 3. Warmup、采样、排空与停止

warmup_periods、sample_period、max_samples 与收敛阈值影响样本集合。过小的窗口会让曲线波动，过大的排队可能触发 latency_thres；不稳定标记、超时和提前终止必须保留，不能只取最后打印的一行平均值。

比较设计时一次只改变目标因素，其他配置明确写出。默认值也属于实验配置，版本变化可能改变默认，因此不能只保存覆盖的两三个参数。

这个版本在达到 max_samples 时也可能从 running 进入 drain 并返回成功，不能把正常结束直接解释为满足连续三次稳定采样。正式实验应保存收敛历史，必要时扩大窗口与采样上限。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/trafficmanager.cpp 第 954–961 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.cpp#L954-L961)。

```cpp
void TrafficManager::_Step( )
{
    bool flits_in_flight = false;
    for(int c = 0; c < _classes; ++c) {
        flits_in_flight |= !_total_in_flight_flits[c].empty();
    }
    if(flits_in_flight && (_deadlock_timer++ >= _deadlock_warn_timeout)){
        _deadlock_timer = 0;
```

_Step 推进一个网络周期，先组织接收 / credit，再处理生成和注入，以及网络对象的周期操作。读取时沿实际函数完整跟踪，不要把主循环里的一个 C++ statement 当成硬件的一个 stage。Run 管理仿真重复与结束，BatchTrafficManager 又具有不同的测量目标。

## 5. 学习练习与实验边界

先执行第25章的最小配置并保存 stdout 和退出码，再重复相同 seed 检查可重复性。多seed统计时显式改 seed，不把确定性重跑当成独立样本。保存异常结果和收敛状态，避免在图表中悄悄丢弃过载点。

## 源码与阅读导航

- [src/trafficmanager.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.cpp)
- [src/Makefile](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/Makefile)
- [src/booksim_config.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/booksim_config.cpp)
- [src/batchtrafficmanager.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/batchtrafficmanager.cpp)
- [src/main.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/main.cpp)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](23_performance_analysis.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 25 — Simulation Examples｜从 smoke 到实验闭环](25_simulation_examples.md)
