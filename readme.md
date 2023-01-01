### Bad Proxy
自用垃圾代理，使用Bad Transfer Protocol传输数据，BTP还在构思中，也没测试过墙能力。

只支持单用户，使用Python所以性能比较bad。


Bad Transfer Protocol究竟是什么？

今天小编就来帮助大家了解一下Bad Transfer Protocol。

关于什么是Bad Transfer Protocol，小编也不知道呢。

好了，以上就是什么是Bad Transfer Protocol。

希望小编精心整理的这篇内容能够解决你的困惑。

虽然很Bad，但是并不是小编的错哦。

因为通往自由之路是如此宝贵。


### Bad Transfer Protocol
| 32 Bytes | 1 Bytes | X Bytes            | 1 Bytes | 1 Bytes | Y Bytes        | 2 Bytes | Z bytes |
|----------|---------|--------------------|---------|---------|----------------|---------|---------|
| digest   | 混淆字段长度  | 混淆字段 (0 <= X < 48) | 指令      | host长度  | host (Y < 254) | 端口号     | 数据载荷    |

| 1 Bytes | X Bytes            | 16 Bytes |
|---------|--------------------|----------|
| 混淆字段长度  | 混淆字段 (32 <= X < 64 | 载荷数据     |

