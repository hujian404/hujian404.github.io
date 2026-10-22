# Chapter 21｜Error Control

> 原书：William J. Dally、Brian Towles，*Principles and Practices of Interconnection Networks*（Morgan Kaufmann，2004），第 21 章，印刷页 411–426。本地参考 PDF 的页序为印刷页 +27。以下为中文学习整理，保留原书全部目录小节的编号与标题，不是逐句翻译。BookSim2 对照版本固定为 [`28f4329`](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)。

[专栏导读](00_Introduction.md) · [原书目录与页码对照](appendix-reading-map.md)

## 21.1 Know Thy Enemy: Failure Modes and Fault Models

*原书印刷页 411。*

先定义 transient/permanent 故障、错误发生位置、独立性和覆盖范围，再选控制方案。没有 fault model 的“容错率”不可比较。

## 21.2 The Error Control Process: Detection, Containment, and Recovery

*原书印刷页 414。*

detection 发现错误，containment 阻止扩散，recovery 恢复正确服务。检测码不是恢复协议，重传也必须处理重复、顺序和丢失确认。

## 21.3 Link Level Error Control

*原书印刷页 415。*

link-level 把错误控制局限在相邻节点之间，可缩短恢复路径，但需要缓存、序号、确认和状态恢复。

### 21.3.1 Link Monitoring

*原书印刷页 415。*

监测误码和链路健康有助于判断偶发错误还是永久退化。阈值、采样窗口和故障定位会影响误判。

### 21.3.2 Link-Level Retransmission

*原书印刷页 416。*

重传需要保存未确认数据，防止坏 flit 被消费，并定义 ACK/NACK 丢失后的处理。credit 与可靠性确认并不是同一个信号。

### 21.3.3 Channel Reconfiguration, Degradation, and Shutdown

*原书印刷页 419。*

重配置、降级或关闭 channel 会改变可达性、容量和路由依赖；故障后仍需检查连通与无死锁，而不只是把 bandwidth 减小。

## 21.4 Router Error Control

*原书印刷页 421。*

router 内部的控制、存储和交换也可能出错。只给物理链路加 CRC 不能覆盖错误转发或状态损坏。

## 21.5 Network-Level Error Control

*原书印刷页 422。*

network-level 可以换路径或隔离故障节点，需要全局或分布式故障信息以及一致的更新方法。

## 21.6 End-to-end Error Control

*原书印刷页 423。*

end-to-end 检查覆盖中间层未能捕获的损坏，并承担最终正确交付责任。不同层的保护互补，不能简单以某一层可靠为由删除所有其他检查。

## 21.7 Bibliographic Notes

*原书印刷页 423。*

本节对应原书 p. 423 的文献脉络。继续查阅时应回到原书该节和书末 Bibliography，区分最初提出的方法、后续实现与本文使用的 BookSim2 版本。本文末尾源码链接是实现对照，不作为原书历史论述的替代依据。

## 21.8 Exercises

*原书印刷页 424。*

自拟练习（不复制原书习题）：先写清错误注入点、概率单位、是否独立、检测延迟、重传规则和可靠性交付指标。最小验证应覆盖无错等价、单次可恢复错误、重复 ack、超时、重放资源耗尽，并检查重传流量是否计入 offered / accepted。不要虚构 `crc_enable` 等不存在的配置项。

## BookSim2 源码对照与适用边界

固定版本节选（仅去除行末空白），省略外围上下文：[查看 src/channel.hpp 第 91–94 行](https://github.com/booksim/booksim2/blob/28f43299f1706a3160ffac721ca461d74eb6e618/src/channel.hpp#L91-L94)。

```cpp
void Channel<T>::Send(T * data) {
  _input = data;
}

```

Send 只是接受一个待交付指针，后续交付由 channel 调度完成。这里没有按比特采样错误的操作。若扩展可靠性研究，应在独立的错误 / 恢复层增加事件和统计，保留 baseline，并检查恢复消息是否需要新的 VC 隔离规则。

本章原书讨论的完整系统/电路机制超出该片段的模型范围。源码片段用于识别相近资源与接口；未实现的电路细节、服务保证或协议行为，不能由命名相似推定存在。

## 来源与继续阅读

- 原书第 21 章，pp. 411–426；各节页码已逐项列出。案例与原书公式均以本地参考书为依据。
- [BookSim2 固定版本源码](https://github.com/booksim/booksim2/tree/28f43299f1706a3160ffac721ca461d74eb6e618)，节选保留[上游许可](/notes/booksim-notes/source-license.txt)。
- [全书章节/源码路线与图片来源](appendix-reading-map.md)。新增图均附 `.drawio` 源文件，插图是结构说明，不是测量波形。

[上一篇](20_network_interfaces.md) · [下一篇](22_buses.md) · [专栏目录](/booksim-series.html)
