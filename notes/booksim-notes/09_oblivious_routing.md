# Chapter 9｜Oblivious Routing｜随机化不等于自适应

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. 决策不依赖实时拥塞

Oblivious routing 按源宿、报文信息及预设随机选择决定路径，不读取当前队列或 credit 来判断哪条路更空。确定性 DOR 是其中一个特例。随机化可以分散规则流量的热点，却不保证更短路径或更低时延。

## 2. Valiant 的中间节点与两阶段路径

典型思路是先随机选中间节点，再从中间节点前往目标。这样可削弱输入流量与固定路径之间的关联，但往往增加平均 hop 数。对于低负载，绕行开销可能占主导；对于某些不均匀流量，均衡才可能补偿额外开销。

阶段转换不是只有一个软件标签：为避免两阶段路径重新形成资源环，实现还需处理 VC 类别。某个 VC 数量不足时，不能只把断言关闭再继续实验。

## 3. 控制随机性才可解释结果

应分别记录 traffic 的随机选择、routing 随机中间节点和 permutation seed。相同 seed 的重复运行可检验确定性，但不能被当作多个独立样本。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/routefunc.cpp 第 1276–1284 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routefunc.cpp#L1276-L1284)。

```cpp
void valiant_mesh( const Router *r, const Flit *f, int in_channel, OutputSet *outputs, bool inject )
{
  int vcBegin = 0, vcEnd = gNumVCs-1;
  if ( f->type == Flit::READ_REQUEST ) {
    vcBegin = gReadReqBeginVC;
    vcEnd = gReadReqEndVC;
  } else if ( f->type == Flit::WRITE_REQUEST ) {
    vcBegin = gWriteReqBeginVC;
    vcEnd = gWriteReqEndVC;
```

继续沿函数中的 `f->intm` 与 `f->ph` 读中间目的和阶段变化，并核对 VC 区间如何按阶段划分。Flit 中这两个字段标为 mutable，说明路由函数可以更新路径上下文；这不是当前拥塞反馈，因此仍属于 oblivious 机制。

## 5. 学习练习与实验边界

对相同 topology、包长和 offered load 比较 DOR 与 Valiant，分别使用 uniform 和一种规则置换，记录 hop、packet latency 与 accepted rate。不能只选一个对 DOR 不利的点；也要展示低负载绕行代价。这里是对照方案，不预填性能提升数字。

## 源码与阅读导航

- [src/routefunc.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routefunc.cpp)
- [src/flit.hpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/flit.hpp)
- [src/booksim_config.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/booksim_config.cpp)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](08_routing_basics.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 10 — Adaptive Routing｜候选路径与拥塞反馈](10_adaptive_routing.md)
