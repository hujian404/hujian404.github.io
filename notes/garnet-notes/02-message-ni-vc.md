# 从 Message 到 flit：NI、vnet 与 VC

[专栏导读](00-reading-map.md) · 源码基线 `ec031fa4e9` · 更新：2026-10-23

## 先分清四个对象

| 对象 | 职责 | 常见误解 |
|---|---|---|
| Message / packet | 协议消息及其网络传输表示 | 一条消息总是一个 flit |
| flit | 链路传输与缓冲流控的单位 | flit 是 cache line |
| vnet | 协议消息类别及其网络资源分组 | vnet 就是一条独立物理线 |
| VC | 某输入端口上的逻辑队列与包占用状态 | 增加 VC 等于增加链路带宽 |

默认每 vnet 4 个 VC。若有 3 个 vnet，每输入端口有 12 个 VC，而非整个 router 仅 12 个。控制类 VC 默认深度 1 flit，数据类默认 4 flit；深度单位与 VC 数量不同。一个包可以长于 VC buffer，依靠 credit 边前进边腾出槽位。

## NI 是协议和 flit 网络的边界

阅读 `NetworkInterface::wakeup()` → `flitisizeMessage()` → `calculateVC()`。NI 从协议 MessageBuffer 取消息，为目标分配输出 VC，将消息拆成 flit，写入 NI 队列，再由调度器送入网络。多播目的集合会在 NI 被处理成多个单播传输，不能假定路由器硬件复制多播。

固定源码中 `flitisizeMessage()` 按消息字节数和输出端口位宽计算 flit 数，并设置 `src_delay`。在默认 128 bit = 16 byte flit 下，8 byte 控制消息占 1 flit，72 byte 数据消息占 `ceil(72/16)=5` flit。单 flit 包是 HEAD_TAIL；长包依次为 HEAD、BODY、TAIL。

standalone 协议将 LD、IFETCH、ST 分到 vnet 0、1、2。前两种为控制消息，第三种为数据消息。因此改变 `--inj-vnet` 会改变包长和流量构成，不能只看相同 packets/node/cycle 就认定链路负载相等。

## 目的端也会造成等待

接收 NI 不仅收 flit，还要将完整消息放入协议接收 buffer。buffer 满时，尾 flit 的交付会推迟；NI 通过 callback 在下游可接收时继续处理。网络平均 queueing delay 既可能包含源端等待，也可能包含目的端等待，不能将所有 queueing delay 都解释为 router 内部拥塞。

练习：把链路位宽改为 64 bit，72 byte 消息需要 9 个 flit。预测长包序列化时间为何上升，再检查实际配置中 NI 和链路位宽是否一致。该改动未包含在本系列七组实测中。

## 对照源码

- [NI 拆包与接收](https://github.com/hujian404/gem5/blob/ec031fa4e97945c426244566fd6196c7cb2b8e7c/src/mem/ruby/network/garnet/NetworkInterface.cc)
- [VC 与 buffer 参数](https://github.com/hujian404/gem5/blob/ec031fa4e97945c426244566fd6196c7cb2b8e7c/src/mem/ruby/network/garnet/GarnetNetwork.py)
- [standalone 消息类别](https://github.com/hujian404/gem5/blob/ec031fa4e97945c426244566fd6196c7cb2b8e7c/src/mem/ruby/protocol/Garnet_standalone-cache.sm)

[下一篇：路由器源码：从输入缓冲到交换分配](03-router-pipeline.md)
