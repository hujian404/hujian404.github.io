# Chapter 23｜Performance Analysis｜先定义事件，再解释曲线

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. Offered、injected 和 accepted 是三个量

Offered load 是产生器希望提供的需求，injected rate 是网络入口实际发送的速率，accepted rate 是出口实际收到的速率。拥塞时源队列可能不断积压，实际接纳低于期望。只看成功送达的报文延迟，还会遗漏未完成报文的等待。

## 2. 用时间线解释三个 latency

![BookSim latency 的时间边界](pic/23-metrics/latency-boundaries.svg)

在图示 ctime=0、head itime=3、tail atime=10 的例子中，packet latency=10，network latency=7。flit latency 则对每个 flit 计算自己的 atime−itime，不能用 tail 与 head 的时间差替代。图是教学算例，并非某次测量数据。

Little 定律 `L=λW` 可用于稳定系统、匹配边界与单位下的守恒检查；λ 若按 packet/cycle，L就应按 packet，W按相应 packet 驻留时间。把 flit rate 和 packet latency 随手相乘没有同样含义。

## 3. 零负载与饱和点都要说明条件

零负载时延包括路径、router / link delay 与序列化；靠近饱和时等待上升。有限采样窗口内 throughput 似乎稳定，不证明无限时间下队列稳定；过载中止阈值也不是拓扑理论容量。对每条曲线同时报告流量、包长、VC、seed、warmup和单位。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/trafficmanager.cpp 第 731–738 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.cpp#L731-L738)。

```cpp
            _plat_stats[f->cl]->AddSample( f->atime - head->ctime);
            _nlat_stats[f->cl]->AddSample( f->atime - head->itime);
            _frag_stats[f->cl]->AddSample( (f->atime - head->atime) - (f->id - head->id) );

            if(_pair_stats){
                _pair_plat[f->cl][f->src*_nodes+dest]->AddSample( f->atime - head->ctime );
                _pair_nlat[f->cl][f->src*_nodes+dest]->AddSample( f->atime - head->itime );
            }
```

tail 到达后，_plat_stats 用 head ctime，_nlat_stats 用 head itime；_flat_stats 则在每个 flit 退休时统计自己的 itime→atime。注入率若启用 flit 单位，构造时会除以平均 packet size 转成 packet 生成概率。它与 Constellation 评估器的 received/sent 比例不同，不能照搬列名解释。

## 5. 学习练习与实验边界

对第25章的三个点同时记录 packet latency、network latency、flit latency、injected和accepted flit rate。需要完整饱和曲线时再加密负载、扩展窗口和多seed；不要用这三个低负载 smoke 点直接拟合饱和吞吐上限。

## 源码与阅读导航

- [src/trafficmanager.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.cpp)
- [src/trafficmanager.hpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/trafficmanager.hpp)
- [src/booksim_config.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/booksim_config.cpp)
- [src/stats.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/stats.cpp)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](22_buses.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 24 — Simulation｜构建、配置与可重复的周期模型](24_simulation.md)
