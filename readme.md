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


## Bad Transfer Protocol

### 协议头
| 4 Bytes         | 32 Bytes | 1 Bytes | X Bytes            | 1 Bytes | 1 Bytes | Y Bytes        | 2 Bytes | Z bytes |
|-----------------|----------|---------|--------------------|---------|---------|----------------|---------|---------|
| utc time +/- 30 | digest   | 混淆字段长度  | 混淆字段 (0 <= X < 48) | 指令      | host长度  | host (Y < 254) | 端口号     | 数据载荷    |

| 1 Bytes | X Bytes            | 16 Bytes |
|---------|--------------------|----------|
| 混淆字段长度  | 混淆字段 (32 <= X < 64 | 载荷数据     |

### 简介
BTP是简单有状态应用层协议，连接时需要握手
第一次握手由client发起，接到request后server会：
1. 验证utc time误差是否在180s以防止长延迟重放攻击；
2. 校验包固定部分的长度
3. 验证由uuid生成的digest，以验证密码并防篡改
第二次握手即server生成32字节的随机token发回，不做校验
第三次握手client将随机数加到首包前，server接收后验证通过则传输开始
以上握手中的任何错误都会抛出BTPException，即认为遭到主动探测，
当前线程会catch这个异常并尝试解析HTTP请求，如果解析成功，
则~~fallback，立刻开始反向代理到白名单页面~~返回一个固定的页面(还是这个简单，反向代理太坑了)

### 安全性
BTP的连接时间取决于其中包裹的应用层协议的连接时间
握手也许会成为特征，但是由于是私有协议，也许不会被探测？
握手可以提供宝贵的防重放保护，所以先握着吧
