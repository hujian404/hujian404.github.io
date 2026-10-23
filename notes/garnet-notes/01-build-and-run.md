# 环境与第一次实验：确认版本、时钟和输出

[专栏导读](00-reading-map.md) · 源码基线 `ec031fa4e9` · 更新：2026-10-23

## 构建与版本

以下命令在 Linux 上执行。准备 C++20 编译器、Python 3.10+ 与开发头文件、SCons、zlib、m4；本机缺少系统开发包时，参照 fork 的 `mydocs/BUILD_AND_RUN_GEM5.md` 用户态安装说明。不要用宿主 Python 直接运行包含 `m5` 的配置。

```bash
git clone https://github.com/hujian404/gem5.git
cd gem5
git checkout ec031fa4e97945c426244566fd6196c7cb2b8e7c
scons build/Garnet_standalone/gem5.opt -j8
build/Garnet_standalone/gem5.opt --build-info
```

专用 preset 设置 `PROTOCOL="Garnet_standalone"`，本系列验证的是该专用路径下的二进制。此处使用 legacy Ruby 配置链；不要仅凭 `ALL` 或目录名称推断兼容性，应核对实际 build-info、控制器命名空间并独立验证。运行结果目录放在源码树外，每组使用独立目录。

```bash
build/Garnet_standalone/gem5.opt -d ../results/first-xy \
  configs/example/garnet_synth_traffic.py \
  --num-cpus=16 --num-dirs=16 --network=garnet \
  --topology=Mesh_XY --mesh-rows=4 --routing-algorithm=1 \
  --synthetic=uniform_random --injectionrate=0.1 \
  --sim-cycles=50000000
```

`--num-cpus` 在这里创建 tester，不是运行程序的处理器。16 个 tester、16 个 directory controller 通过各自 NI 连接到 16 个 router，不能用终端数直接代替 router 数。

## 三种时间单位

配置脚本设置全局频率 `1ps`。源码 `GarnetSyntheticTraffic::tick()` 的停止条件是：

```cpp
if (curTick() >= simCycles)
    exitSimulationLoopClassic("Network Tester completed simCycles");
```

因此参数名虽叫 sim-cycles，此提交实际传入的是 **tick 阈值**，并在 tester 唤醒时检查，非对齐阈值可能到下一次检查才结束。实测 `system.clk_domain.clock=1000`、`system.ruby.clk_domain.clock=500`，单位均为 tick：

| 量 | 本实验 |
|---|---|
| 50,000,000 tick | 50 微秒 |
| tester 1 GHz | 50,000 tester 周期 |
| Ruby 2 GHz | 100,000 Ruby 周期 |
| 延迟 6,000 tick | 12 Ruby 周期，或 6 tester 周期 |

最终以 `stats.txt` 的 `simTicks/simFreq` 与 `config.ini` 时钟为准。注入率是每节点每 **tester 周期** 的生成概率，不能与每 Ruby 周期注入量混用。随机数离散精度、背压和包长还会使实际 flit 注入量偏离简单估算。

## 成功的证据

检查进程正常退出、日志包含 `Network Tester completed simCycles`，并确认接收 flit 大于零、延迟有限。`config.ini` 证明参数实际落到了哪个 SimObject，`stats.txt` 给出测量结果，`stdout.log` 记录构建版本和结束原因。全部保留后再比较实验。

常见错误：参数 `--network=garnet2.0` 不适用于本提交；拓扑使用 `Mesh_XY`；拓扑名称本身不选择坐标 XY 代码，必须显式 `--routing-algorithm=1`。无 HDF5/libpng 的构建警告不妨碍本系列 standalone 实验。

## 对照源码

- [专用构建 preset](https://github.com/hujian404/gem5/blob/ec031fa4e97945c426244566fd6196c7cb2b8e7c/build_opts/Garnet_standalone)
- [配置和全局频率](https://github.com/hujian404/gem5/blob/ec031fa4e97945c426244566fd6196c7cb2b8e7c/configs/example/garnet_synth_traffic.py)
- [tick 与注入逻辑](https://github.com/hujian404/gem5/blob/ec031fa4e97945c426244566fd6196c7cb2b8e7c/src/cpu/testers/garnet_synthetic_traffic/GarnetSyntheticTraffic.cc)
- [用户态环境说明](https://github.com/hujian404/gem5/blob/ec031fa4e97945c426244566fd6196c7cb2b8e7c/mydocs/BUILD_AND_RUN_GEM5.md)

[下一篇：从 Message 到 flit：NI、vnet 与 VC](02-message-ni-vc.md)

