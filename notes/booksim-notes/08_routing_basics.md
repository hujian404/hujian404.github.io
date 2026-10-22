# Chapter 8｜Routing Basics

> 原书：William J. Dally、Brian Towles，*Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004），第 8 章，印刷页 159–172。本地参考 PDF 的页序为印刷页 +27。以下为中文学习整理，保留原书全部目录小节的编号与标题，不是逐句翻译。BookSim2 对照版本固定为 [`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

[专栏导读](00_Introduction.md) · [原书目录与页码对照](appendix-reading-map.md)

## 8.1 A Routing Example

*原书印刷页 160。*

同一拓扑中的不同路径会产生不同负载和前进性。先在小图上列出源宿与路径，再讨论 routing algorithm；只列算法名称很难检查转弯与端口编号错误。

## 8.2 Taxonomy of Routing Algorithms

*原书印刷页 162。*

deterministic 每个源宿固定路径；oblivious 的选择不依赖运行时拥塞；adaptive 根据网络状态调整。minimal/non-minimal 是另一个维度，随机选择并不自动等于自适应。

## 8.3 The Routing Relation

*原书印刷页 163。*

routing relation 给出状态与目的地允许选择的下一 channel 集合。实现还要说明状态包含什么，以及 VC class 如何限制合法转移；返回候选集合不等于最终赢得资源。

## 8.4 Deterministic Routing

*原书印刷页 164。*

确定性路由有利于分析路径、顺序与 channel load，但可能把某种 permutation 压到少数链路。实现简单不意味着性能总是最优。

### 8.4.1 Destination-Tag Routing in Butterfly Networks

*原书印刷页 165。*

butterfly 按逐级目的标签选择输出；每级消费的地址字段必须与连线排列一致。对所有源宿做小规模可达性穷举，通常比只测一个例子更有效。

### 8.4.2 Dimension-Order Routing in Cube Networks

*原书印刷页 166。*

cube 网络按固定维度顺序消除坐标差。Mesh 的 XY 路由是二维特例；Torus 还要确定环的正负方向和处理依赖环的方法。

手算示例：二维 Mesh，坐标 (0,0)→(2,1)，先 X 后 Y 的输出为 `+X,+X,+Y`。允许 XY/YX 二选一会改变 routing relation；它是否可安全使用，还需按第 14 章检查 channel/VC 依赖。

## 8.5 Case Study: Dimension-Order Routing in the Cray T3D

*原书印刷页 168。*

Cray T3D 案例展示维度顺序路由与具体网络实现的配合。阅读时同时检查地址解释、方向选择和资源分类，避免把“DOR”理解成无需任何流控约束。

T3D 的 3-D Torus router 分别用 x、y、z 三个相同芯片完成各维度处理。packet 先在 x 方向推进，到达正确 x 坐标后交给 y，再交给 z。这个拆分之所以可行，正是因为路由的维度顺序固定；若加入任意回到前一维的选择，原先的数据通路连接和控制证明都需要重审。

## 8.6 Bibliographic Notes

*原书印刷页 170。*

本节对应原书 p. 170 的文献脉络。继续查阅时应回到原书该节和书末 Bibliography，区分最初提出的方法、后续实现与本文使用的 BookSim2 版本。本文末尾源码链接是实现对照，不作为原书历史论述的替代依据。

## 8.7 Exercises

*原书印刷页 171。*

自拟练习（不复制原书习题）：在 routefunc.cpp 中找到 `dim_order_mesh` 与 `dor_next_mesh`，手算0→15和15→0的每一步，再核对注入时 `inject=true` 的特殊 output=-1。尝试记录候选 VC 范围，分清“允许使用”与“当前可分配”。

## BookSim2 源码对照与适用边界

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

## 来源与继续阅读

- 原书第 8 章，pp. 159–172；各节页码已逐项列出。案例与原书公式均以本地参考书为依据。
- [BookSim2 固定版本源码](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)，节选保留[上游许可](/notes/booksim-notes/source-license.txt)。
- [全书章节/源码路线与图片来源](appendix-reading-map.md)。新增图均附 `.drawio` 源文件，插图是结构说明，不是测量波形。

[上一篇](07_slicing_and_dicing.md) · [下一篇](09_oblivious_routing.md) · [专栏目录](/booksim-series.html)
