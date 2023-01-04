## Bad Proxy
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

| 32 Bytes | 1 Bytes | X Bytes            | 4 Bytes            | 1 Bytes | 1 Bytes | Y Bytes        | 2 Bytes | Z bytes |
|----------|---------|--------------------|--------------------|---------|---------|----------------|---------|---------|
| digest   | 混淆字段长度  | 混淆字段 (0 <= X < 64) | utc timestamp +-30 | 指令      | host长度  | host (Y < 254) | 端口号     | 数据载荷    |

| 1 Bytes | X Bytes            | 16 Bytes |
|---------|--------------------|----------|
| 混淆字段长度  | 混淆字段 (32 <= X < 64 | 载荷数据     |

BTP是简单无状态应用层协议, 主要参考vless实现, 主要区别如下
1. 相比保留了vmess的时间验证和哈希认证: vmess是将时间和消息, 密钥一起摘要,
服务器根据算出合法时间段内所有的哈希值进行比对, 有一个成功则合法,
而我嫌麻烦则直接发送了utc时间戳; 哈希值用于认证和防止篡改,
而时间戳校验可以防止长延迟的重放攻击, 据说gfw会把抓到的包保存好几天进行重放

2. 协议首包直接发送数据, 这是跟Trojan学的, 可以避免包长度被探测,
在此之上还加入了随机长度的混淆字段, 避免协议包头尤其是时间戳, 出现某些可能的特征

### 安全性
1. 加密
和vless一样, BTP不提供加密, 采用tls进行传输, 未来会提供websocket传输
2. 重放攻击
长延迟重放由时间戳校验防御, 超时最多4分钟/240秒则包失效(210s超时, +-30秒随机)
短延迟重放由lru防御, 每个合法连接的协议头摘要会被存到一个默认大小为240000的中lru,
这样可以在1000qps的服务器上防御4分钟内的重放攻击(据说gfw会在一秒钟之内就开始重放)
3. 主动探测
本来要实现个fallback的但是发现反向代理真是大坑, 所以只做了个假页面, 探测到http请求时返回

### 小功能
使用了 [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community)
维护的geolocation-cn系列文件做白名单, 其中的域名不进行代理直接freedom出站,
用户须把该项目中的data文件夹内的全部文件拷贝到domains中, 即可进行读取

## 未来计划
- [ ] 支持websocket
- [ ] 支持反向代理
