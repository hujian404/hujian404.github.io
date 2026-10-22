# Chapter 8｜Routing Basics｜从目标节点到合法资源集合

> 以《Principles and Practices of Interconnection Networks》的章节主题为学习顺序；本文为概念整理与固定版本源码解读，不是原书逐句翻译。BookSim2 基线：[`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

## 1. 路由输出的是允许的下一步

路由决定 packet 可以使用哪些路径；分配器决定这些候选资源何时授予请求。二者相关但职责不同。最短路由仅使用降低到目的距离的步骤，非最短路由可能为负载均衡绕行；确定性路由对同一源宿固定，oblivious 路由可随机但不依据当前拥塞，自适应路由使用网络状态。

这些分类不是同一维度：随机路由可以是最短的，自适应路由也可以受到最短路径约束。

## 2. 用坐标追踪 XY / DOR

4×4 Mesh 中节点按 `id=y*4+x` 编号，0=(0,0)，15=(3,3)。维序路由先完成一个坐标差，再完成下一个；例如先X后Y时路径为0→1→2→3→7→11→15。交换维度顺序可能选择另一条同样6跳的路径，但链路热点不同。

## 3. 不只选择 output port，还要选择 VC 范围

路径合法性可能依赖消息类型、当前 VC 或阶段。BookSim 的 routing function 向 OutputSet 填入 output_port、VC 区间和优先级，再由 VA 结合资源状态申请输出 VC。这比“返回一个方向整数”表达能力更强。

## 4. BookSim 源码拆解

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/outputset.cpp 第 51–60 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/outputset.cpp#L51-L60)。

```cpp
void OutputSet::AddRange( int output_port, int vc_start, int vc_end, int pri )
{

  sSetElement s;

  s.vc_start = vc_start;
  s.vc_end   = vc_end;
  s.pri      = pri;
  s.output_port = output_port;
  _outputs.insert( s );
```

一个元素保存连续 VC 区间、候选输出和优先级；OutputSet 可以含多个元素，不保证函数返回时已经做了唯一仲裁。IQRouter 用 `routing_function + "_" + topology` 查注册表，例如 `dor` 与 `mesh` 组合得到 `dor_mesh`。仅看函数名、不核对注册键，是常见配置错误。

## 5. 学习练习与实验边界

在 routefunc.cpp 中找到 `dim_order_mesh` 与 `dor_next_mesh`，手算0→15和15→0的每一步，再核对注入时 `inject=true` 的特殊 output=-1。尝试记录候选 VC 范围，分清“允许使用”与“当前可分配”。

## 源码与阅读导航

- [src/outputset.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/outputset.cpp)
- [src/routefunc.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routefunc.cpp)
- [src/routers/iq_router.cpp](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/routers/iq_router.cpp)

源码节选版权归 Trustees of The Leland Stanford Junior University，保留[上游许可与免责声明](/notes/booksim-notes/source-license.txt)。新增架构图与算例为教学整理；未执行的方案不标作测量结果。

[上一篇](07_slicing_and_dicing.md) · [专栏导读](00_Introduction.md)

---

[下一篇：Chapter 9 — Oblivious Routing｜随机化不等于自适应](09_oblivious_routing.md)
