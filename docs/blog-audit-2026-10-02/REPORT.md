# Blog 全文核查与修改意见

核查日期：2026-10-02。原文目录：`C:/Project/blog`。

已逐篇核阅目录内的 **175 个 Markdown 文件**（包括个人简介、草稿与未完成笔记），共约 **108 万字符、44,423 行**，字符数包含代码和 front matter。共整理 **320 条修改意见，涉及 138 个文件**。原文未修改；下文提供原文定位、问题说明、修改建议及相应依据。

| 类型 | 条数 | 含义 |
| --- | ---: | --- |
| 事实／技术错误 | 183 | 明确的概念、数字、代码、命令或配置错误；也包含与正文矛盾的实现 |
| 条件／版本澄清 | 65 | 补充适用前提、历史版本或现行标准；不全部等于原文事实错误 |
| 字词／链接 | 72 | 明显错字、名称拼写、误译和链接目标错误 |

条数按“修改意见组”统计：一条可合并同篇重复错字或相同成因的问题；跨篇重复问题分别定位。混合问题按主要技术含义归类。因此，320 不是独立错误单词的总数。

## 如何阅读与核查边界

P1 为建议优先修改的事项，可能造成错误实验结论、消息丢失、更新失败、递归告警或错误安全判断；P2 为其他技术修正与条件说明；P3 为字词和链接修正。这是修订顺序建议。

逐篇清单列出全部文件，包含没有发现问题的文章，便于检查遗漏：[175 个文件的核查清单](<C:/Project/MyProject/blogger/docs/blog-audit-2026-10-02/article-checklist.md>)。

依据优先采用协议规范、项目官方文档、官方源码、作者原始资料和工具手册。历史教程按其使用版本判断；仅因今天有新版本，不直接判旧笔记错误。译文中的错误若原作者也有，会在具体条目中说明，并建议加译者注。字词、算术和同篇代码／配置矛盾可直接由原文核对。

**覆盖范围：**Markdown 正文、front matter、文本形式的命令和代码均已核阅。代码以静态检查为主，争议行为另做针对性验证；未在所有硬件、Linux 发行版、Java 和服务部署环境完整复现，配图和截图也未逐张 OCR。因此，“未发现可确认的明显错误”不表示所有运行结果、图片数据或私人经历均已独立验证。个人感受、设计偏好及缺少外部证据的经历不作事实性否定。

**来源读取边界：**部分历史网页抓取受限，核查时使用对应官方手册、版本源码或搜索可取得的材料补证。报告引用链接供复查；来源访问记录保留成功与失败，不把无法抓取等同于链接已失效。

## 建议优先修改的例子

| 条目 | 需要修改的核心问题 |
| --- | --- |
| [R046](#r046) | MySQL 备份脚本不能保证恢复到指定新库，且转储失败仍可能淘汰旧备份。 |
| [R061](#r061) | Redis pipeline 性能测试没有排入 GET 命令，原耗时与性能结论需要撤回并重测。 |
| [R025](#r025) | 直接截断序列化后的 JSON，可能产生无法解析的日志，且未控制 UTF-8 字节数。 |
| [R216](#r216) | 告警发送失败后再用同一个告警 logger 记录异常，会递归提交告警。 |
| [R241](#r241) | RabbitMQ 的 Future 完成不代表处理成功；失败也 ACK 会丢失可重试消息。 |
| [R249](#r249) | 同源策略不能作为 CSRF 防御；跨源请求并不都被阻止。 |
| [R262](#r262) | 更新器没有核实下载完整性；截断的文件也可能进入替换流程。 |
| [R263](#r263) | 更新器先删除旧 EXE，后续移动失败时可能失去可运行版本。 |
| [R270](#r270) | X-Forwarded-For 可能是代理链，不能直接当作一个可信 IP 查询。 |
| [R282](#r282) | 密码哈希、TLS 加密和日志脱敏需要区分；日志应省略密码。 |

## 逐篇修改意见

### A001

**about**

原文：[about/index.md](<C:/Project/blog/about/index.md>)。

记录日期：2025-01-01T20:00:00+08:00；状态：个人简介已阅；未发现可确认的明显字词错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A002

**Ubuntu下的环境配置和点灯**

原文：[hardware/Arduino/Ubuntu下的环境配置和点灯/index.md](<C:/Project/blog/hardware/Arduino/Ubuntu下的环境配置和点灯/index.md>)。

记录日期：2025-03-22T09:37:00+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A003

**Ubuntu下的环境配置和点灯**

原文：[hardware/ESP32/Ubuntu下的环境配置和点灯/index.md](<C:/Project/blog/hardware/ESP32/Ubuntu下的环境配置和点灯/index.md>)。

记录日期：2025-03-22T12:46:00+08:00；状态：正文已核阅；有修改意见。

#### R001

**字词/链接 · 字词 · P3**

定位：[原文第 32 行](<C:/Project/blog/hardware/ESP32/Ubuntu下的环境配置和点灯/index.md:32>)；待改表述／主题：` ESP32 IDF 框架 / ESP IDF `。

原文定位行（节选）：` ESP32 可以使用 Arduino IDE 进行开发，安装好相应的库即可，本文介绍的是官方推荐的 ESP32 IDF 框架。 `

问题：官方框架名为 ESP-IDF。

建议修改：统一写为“ESP-IDF（Espressif IoT Development Framework）”。

依据：[docs.espressif.com](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/index.html)。

### A004

**NodeMCU+MQTT与后台交互信息**

原文：[hardware/NodeMCU+MQTT与后台交互信息/index.md](<C:/Project/blog/hardware/NodeMCU+MQTT与后台交互信息/index.md>)。

记录日期：2023-01-17T13:30:52+08:00；状态：正文已核阅；有修改意见。

#### R002

**字词/链接 · 字词 · P3**

定位：[原文第 6 行](<C:/Project/blog/hardware/NodeMCU+MQTT与后台交互信息/index.md:6>)；待改表述／主题：` 后端接受 DHT11 数据 / 其在，通过 / 可订阅的的 / 匿名链接 `。

原文定位行（节选）：` summary: "后端接受 DHT11 数据的同时，可以控制 LED 的亮灭" `

问题：数据到达应为“接收”；存在重复字及误字。

建议修改：第6、70、72、396行等“接受”按语义改为“接收”；第18行改“其在通过…”；第52行删一个“的”；第80行改“匿名连接”。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R003

**条件/版本澄清 · 版本信息补充 · P2**

定位：[原文第 52 行](<C:/Project/blog/hardware/NodeMCU+MQTT与后台交互信息/index.md:52>)；待改表述／主题：` 实现了…MQTT v3.1 `。

原文定位行（节选）：` 它是一款实现了消息推送协议 MQTT v3.1 的开源消息代理软件，提供轻量级的，支持可发布/可订阅的的消息推送模式，使设备对设备之间的短消息通信变得简单。 `

问题：支持MQTT 3.1的陈述本身没有错，但本文介绍Mosquitto协议支持范围时漏掉3.1.1及5.0；应与使用版本一致。

建议修改：改为“支持 MQTT 5.0、3.1.1 和 3.1 的开源消息代理”。

依据：[mosquitto.org](https://mosquitto.org/)。

#### R004

**事实/技术错误 · 代码 · P2**

定位：[原文第 659 行](<C:/Project/blog/hardware/NodeMCU+MQTT与后台交互信息/index.md:659>)；待改表述／主题：` messageHandler.setDefaultTopic("#"); `。

原文定位行（节选）：` messageHandler.setDefaultTopic("#"); `

问题：# 是订阅过滤器通配符，不能作为发布主题。当前 Gateway 显式传 topic 会覆盖它，但默认值仍无效。

建议修改：删除该默认值或换成有效发布主题，例如 /device/led。

依据：[docs.oasis-open.org · mqtt-v3.1.1-os](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)。

### A005

**NodeMCU发送数据给树莓派**

原文：[hardware/NodeMCU发送数据给树莓派/index.md](<C:/Project/blog/hardware/NodeMCU发送数据给树莓派/index.md>)。

记录日期：2021-06-18T11:20:10+08:00；状态：正文已核阅；有修改意见。

#### R005

**事实/技术错误 · 事实 · P2**

定位：[原文第 17 行](<C:/Project/blog/hardware/NodeMCU发送数据给树莓派/index.md:17>)；待改表述／主题：` 用 C 实现了 Lua、Python 的编程环境 `。

原文定位行（节选）：`` NodeMCU 是一个开源的物联网平台。该平台基于 `eLua` 开源项目，底层使用 ESP8266 SDK 0.9.5 版本。NodeMCU 包含了可以运行在 ESP8266 Wi-Fi SoC 芯片之上的固件，以及基于 ESP-12 模组的硬件。用 C 实现了 Lua、Python 的编程环境，可以很方便地实现一些物联网应用。 ``

问题：NodeMCU 的 Lua 固件与本文烧录的 MicroPython 是不同固件，不能把 Python 环境归于 NodeMCU 固件。SDK 0.9.5 也只是早期历史。

建议修改：改为“本文使用基于 ESP8266 的 NodeMCU 开发板，烧录 MicroPython 固件；NodeMCU 原生固件主要提供 Lua 环境”。

依据：[仓库源码：nodemcu/nodemcu-firmware · nodemcu-firmware](https://github.com/nodemcu/nodemcu-firmware)；[docs.micropython.org · quickref](https://docs.micropython.org/en/latest/esp8266/quickref.html)。

#### R006

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 83 行](<C:/Project/blog/hardware/NodeMCU发送数据给树莓派/index.md:83>)；待改表述／主题：` 把 LED 正极连接上 D3，负极接地 `。

原文定位行（节选）：` 把 LED 正极连接上 D3，负极接地，然后通过命令行点亮 LED，根据上面的表格可以知道，D3 对应 GPIO0 `

问题：直接接裸 LED 缺少限流；GPIO0 还是启动配置引脚，外接负载需要保证复位时电平。

建议修改：示例明确串联按电压和 LED 额定电流计算的限流电阻，并优先选非启动配置 GPIO；注明 on/off 对外接正向 LED 的条件。

依据：[www.espressif.com · 0a-esp8266ex_datasheet_en.pdf](https://www.espressif.com/sites/default/files/documentation/0a-esp8266ex_datasheet_en.pdf)。

#### R007

**事实/技术错误 · 代码 · P1**

定位：[原文第 102 行](<C:/Project/blog/hardware/NodeMCU发送数据给树莓派/index.md:102>)；待改表述／主题：` wlan.connect(...) `。

问题：本节只 import network，未创建 wlan，独立执行会产生 NameError。

建议修改：在 connect 前补 wlan = network.WLAN(network.STA_IF) 和 wlan.active(True)。

依据：[docs.micropython.org · quickref](https://docs.micropython.org/en/latest/esp8266/quickref.html)。

### A006

**Ubuntu下的环境配置和点灯**

原文：[hardware/STC89C52/Ubuntu下的环境配置和点灯/index.md](<C:/Project/blog/hardware/STC89C52/Ubuntu下的环境配置和点灯/index.md>)。

记录日期：2025-03-22T10:28:00+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A007

**Ubuntu下的环境配置和点灯**

原文：[hardware/STM32F103C8T6/Ubuntu下的环境配置和点灯/index.md](<C:/Project/blog/hardware/STM32F103C8T6/Ubuntu下的环境配置和点灯/index.md>)。

记录日期：2025-03-22T13:04:00+08:00；状态：正文已核阅；有修改意见。

#### R008

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 119 行](<C:/Project/blog/hardware/STM32F103C8T6/Ubuntu下的环境配置和点灯/index.md:119>)；待改表述／主题：` 那就是因为芯片是 CS32F103C8T6 `。

原文定位行（节选）：` 那就是因为芯片是 CS32F103C8T6，一个中国仿制版本的芯片，原因参考博客： `

问题：仅凭调试端口 ID 不匹配不能唯一识别芯片厂家/型号。

建议修改：改为“可能是兼容芯片或目标配置与实际调试端口 ID 不匹配；先核对芯片丝印、探针和配置，再按实际 ID 设置 CPUTAPID”。

依据：[仓库源码：openocd-org/openocd · stm32f1x.cfg](https://github.com/openocd-org/openocd/blob/master/tcl/target/stm32f1x.cfg)。

#### R009

**字词/链接 · 字词 · P3**

定位：[原文第 124 行](<C:/Project/blog/hardware/STM32F103C8T6/Ubuntu下的环境配置和点灯/index.md:124>)；待改表述／主题：` 改称 0x2ba01477 `。

原文定位行（节选）：`` 可以把 `/usr/share/openocd/scripts/target/stm32f1x.cfg` 这个文件复制到当前的工程目录下，然后把文件中的 0x1ba01477 改称 0x2ba01477 就可以了 ``

问题：误字。

建议修改：改为“改成 0x2ba01477”。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A008

**两种方式的点灯**

原文：[hardware/STM32F103C8T6/两种方式的点灯/index.md](<C:/Project/blog/hardware/STM32F103C8T6/两种方式的点灯/index.md>)。

记录日期：2025-03-29T09:16:00+08:00；状态：正文已核阅；有修改意见。

#### R010

**字词/链接 · 字词 · P3**

定位：[原文第 21 行](<C:/Project/blog/hardware/STM32F103C8T6/两种方式的点灯/index.md:21>)；待改表述／主题：` 我实现学习 / Andrej Karpath / 线程的 HTTP 框架 / Keli `。

原文定位行（节选）：` > 你的工作不是写代码，而是配置、管道、编排、工作流、最佳实践。-- [Andrej Karpath](https://x.com/karpathy/status/1905051558783418370) `

问题：明显误字或拼写错误。

建议修改：依次改“我是先学习”“Andrej Karpathy”“现成的 HTTP 框架”“Keil”；第23行“组装搬和运”改“组装和搬运”，第76行删“代码，。”中的逗号。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A009

**无法再次烧录的问题**

原文：[hardware/STM32F103C8T6/无法再次烧录的问题/index.md](<C:/Project/blog/hardware/STM32F103C8T6/无法再次烧录的问题/index.md>)。

记录日期：2025-04-04T10:43:00+08:00；状态：正文已核阅；有修改意见。

#### R011

**事实/技术错误 · 事实 · P2**

定位：[原文第 17 行](<C:/Project/blog/hardware/STM32F103C8T6/无法再次烧录的问题/index.md:17>)；待改表述／主题：` PB13（板载 LED） `。

原文定位行（节选）：` 我使用 STM32CubeIDE 的 MX 工具配置点灯时，用的都是默认配置，只初始化了 PB13（板载 LED）的 GPIO。 `

问题：本文所用 Blue Pill 的板载 LED 在 PC13；也与上一篇 PC13 的描述矛盾。

建议修改：改为“PC13（此 Blue Pill 板子的板载 LED）”；其他板型以原理图为准。

依据：[仓库源码：ubogdan/STM32F103C8T6 · STM32F103C8T6](https://github.com/ubogdan/STM32F103C8T6)。

### A010

**使用OLED做一个简易手表**

原文：[hardware/使用OLED做一个简易手表/index.md](<C:/Project/blog/hardware/使用OLED做一个简易手表/index.md>)。

记录日期：2023-01-07T16:16:35+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A011

**使用OLED展示DHT11的温湿度数据**

原文：[hardware/使用OLED展示DHT11的温湿度数据/index.md](<C:/Project/blog/hardware/使用OLED展示DHT11的温湿度数据/index.md>)。

记录日期：2023-01-05T19:13:59+08:00；状态：正文已核阅；有修改意见。

#### R012

**字词/链接 · 字词 · P3**

定位：[原文第 66 行](<C:/Project/blog/hardware/使用OLED展示DHT11的温湿度数据/index.md:66>)；待改表述／主题：` ·![](images/DHT11接线图2.jpg) / N/C：not connect `。

原文定位行（节选）：` ·![](images/DHT11接线图2.jpg) `

问题：图片行多了中点；英文通常是 not connected。

建议修改：删去图片前“·”，将 N/C 写为“not connected（未连接）”。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R013

**事实/技术错误 · 代码 · P1**

定位：[原文第 211 行](<C:/Project/blog/hardware/使用OLED展示DHT11的温湿度数据/index.md:211>)；待改表述／主题：` delay(100); `。

原文定位行（节选）：` delay(100); `

问题：完整示例约每100ms读取一次 DHT11，超过其允许/推荐更新频率；读到缓存值或失败仍直接显示。

建议修改：DHT11 采集间隔至少1秒（以所用传感器版本数据手册为准），检查 chk 后再更新显示；屏幕刷新与采集分开。

依据：[docs.micropython.org · dht](https://docs.micropython.org/en/latest/esp8266/tutorial/dht.html)。

### A012

**使用树莓派和内网穿透远程点灯**

原文：[hardware/使用树莓派和内网穿透远程点灯/index.md](<C:/Project/blog/hardware/使用树莓派和内网穿透远程点灯/index.md>)。

记录日期：2021-06-15T17:44:58+08:00；状态：正文已核阅；有修改意见。

#### R014

**事实/技术错误 · 时效 · P2**

定位：[原文第 34 行](<C:/Project/blog/hardware/使用树莓派和内网穿透远程点灯/index.md:34>)；待改表述／主题：` 安装最新的 JDK 版本，目前是 OpenJDK 11 JDK `。

原文定位行（节选）：` 运行以下命令安装最新的 JDK 版本，目前是 OpenJDK 11 JDK： `

问题：default-jdk 安装发行版默认 JDK，不保证是上游最新版；2021年 Java 11 也已不是上游最新版本。

建议修改：改为“本示例使用 Java 11；default-jdk 安装当前发行版默认 JDK，先用 java -version 核实”。

依据：[packages.debian.org · default-jdk](https://packages.debian.org/bullseye/default-jdk)。

#### R015

**字词/链接 · 字词 · P3**

定位：[原文第 51 行](<C:/Project/blog/hardware/使用树莓派和内网穿透远程点灯/index.md:51>)；待改表述／主题：` Raspbin `。

原文定位行（节选）：` WiringPi 预装（Pre-installed）在标准的树莓派操作系统 Raspbin 中。可以使用下面的命令进行安装： `

问题：操作系统名称拼错。

建议修改：改为“Raspbian（现称 Raspberry Pi OS）”，并为 WiringPi 安装注明当年的发行版。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R016

**事实/技术错误 · 事实 · P2**

定位：[原文第 116 行](<C:/Project/blog/hardware/使用树莓派和内网穿透远程点灯/index.md:116>)；待改表述／主题：` custom_domains 必须和服务端的一致 `。

原文定位行（节选）：`` `custom_domains` 必须和服务端的一致。 ``

问题：frps 无需配置同名 [web] 和 custom_domains；HTTP 代理及域名在 frpc 配置，服务端配置 vhost 端口即可。

建议修改：删去 frps 示例的 [web] 段以及该句，说明域名需解析到 frps 公网地址，frpc custom_domains 决定路由。注明示例使用历史 INI 格式。

依据：[gofrp.org · vhost-http](https://gofrp.org/en/docs/examples/vhost-http/)。

#### R017

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 175 行](<C:/Project/blog/hardware/使用树莓派和内网穿透远程点灯/index.md:175>)；待改表述／主题：` 最好接个电阻 / GPIO_01 `。

原文定位行（节选）：`` 将 led 灯珠（最好接个电阻，防止电流过大烧掉）正极接到 `GPIO_01` 上，负极接地。 ``

问题：裸 LED 的限流电阻不应作为可选项；Pi4J v1 的 RaspiPin.GPIO_01 是 WiringPi 编号，易与 BCM1/物理1脚混淆。

建议修改：改为“串联限流电阻；本例 GPIO_01 对应 BCM18、40针排针的物理12脚”。

依据：[Raspberry Pi 官方文档 · raspberry-pi · gpio](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio)；[Pi4J v1 源码 · RaspiPin](https://www.pi4j.com/1.2/apidocs/src-html/com/pi4j/io/gpio/RaspiPin.html)。

### A013

**动手制作一个3×3×3的LED光立方**

原文：[hardware/动手制作一个3×3×3的LED光立方/index.md](<C:/Project/blog/hardware/动手制作一个3×3×3的LED光立方/index.md>)。

记录日期：2023-01-03T09:34:20+08:00；状态：正文已核阅；有修改意见。

#### R018

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 23 行](<C:/Project/blog/hardware/动手制作一个3×3×3的LED光立方/index.md:23>)；待改表述／主题：` 不太需要担心…LED 电流和功率 `。

原文定位行（节选）：` 2. LED 数量少，不太需要担心供电电压， LED 电流和功率的问题。 `

问题：即使只有27颗 LED，GPIO 的单脚、端口总电流以及限流方式仍须核算。每层共用一个200Ω电阻不适用于任意多灯同时点亮。

建议修改：改为“规模较小，但仍需核算电流；本文逐灯点亮示例使用共用层电阻，若扩展为同层多灯点亮，应每列限流并核算公共层驱动电流，必要时加三极管”。

依据：[ww1.microchip.com · Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf)。

### A014

**木制的小台钻**

原文：[hardware/木制的小台钻/index.md](<C:/Project/blog/hardware/木制的小台钻/index.md>)。

记录日期：2023-01-11T14:29:54+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A015

**步进电机和A4988的控制实践**

原文：[hardware/步进电机和A4988的控制实践/index.md](<C:/Project/blog/hardware/步进电机和A4988的控制实践/index.md>)。

记录日期：2023-01-10T09:36:59+08:00；状态：正文已核阅；有修改意见。

#### R019

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 93 行](<C:/Project/blog/hardware/步进电机和A4988的控制实践/index.md:93>)；待改表述／主题：` Continuous current per phase 1A / Maximum…2A `。

原文定位行（节选）：` | Continuous current per phase | 1A | `

问题：这是载板散热条件下的参考能力，不能当作所有A4988模块无条件连续额定值。

建议修改：表格注明载板型号、散热条件；补充上电前按采样电阻设置电流限值 Imax=Vref/(8Rs)，不直接用供电电流代替相电流。

依据：[www.pololu.com · 1182](https://www.pololu.com/product/1182)。

#### R020

**字词/链接 · 字词 · P3**

定位：[原文第 121 行](<C:/Project/blog/hardware/步进电机和A4988的控制实践/index.md:121>)；待改表述／主题：` 转自 / 驱动进程 / 输出引脚…链接 / 链接包含中文句子 `。

原文定位行（节选）：` A4988 驱动进程具有三个细分选择输入：MS1、MS2 和 MS3。通过为这些引脚设置适当的逻辑电平，我们可以将电机设置为五种不同的步进模式： `

问题：“转自”应为“转子”，driver误译为“驱动进程”；第20行把中文说明拼进URL导致链接错误。

建议修改：第61行改“转子”；第121、147、151行“驱动进程”改“驱动器”；第157行改“连接”；第20行将链接目标仅保留 https://lastminuteengineers.com/。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R021

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 139 行](<C:/Project/blog/hardware/步进电机和A4988的控制实践/index.md:139>)；待改表述／主题：` 高电平…顺时针…低电平…逆时针 `。

原文定位行（节选）：` DIR 引脚控制电机的旋转方向。高电平使电机顺时针旋转，低电平使其逆时针旋转。 `

问题：绝对方向依赖相线连接及观察轴端方向，不由 DIR 电平单独确定。

建议修改：改为“改变 DIR 电平会反转方向；本接线和观察方向下，高为顺时针、低为逆时针”。

依据：[www.pololu.com · 1182](https://www.pololu.com/product/1182)。

#### R022

**事实/技术错误 · 代码 · P2**

定位：[原文第 238 行](<C:/Project/blog/hardware/步进电机和A4988的控制实践/index.md:238>)；待改表述／主题：` STEPS_PER_REVOLUTION 是…200 `。

原文定位行（节选）：`` 这里的 `STEPS_PER_REVOLUTION` 是一个常量 200，因为 1.8° 的步距角，需要走两百步，才完成一圈的旋转。 ``

问题：200只适用于1.8°电机全步。文章提供细分切换函数后，rotateNLoop仍固定200，细分模式的圈数会不正确。

建议修改：每圈脉冲数按 360/步距角 × 细分倍率计算，并在切换细分时更新，或限定该函数只用于全步。

依据：[www.pololu.com · 1182](https://www.pololu.com/product/1182)。

### A016

**Exception and Traceback Logging in Python**

原文：[other/Exception and Traceback Logging in Python/index.md](<C:/Project/blog/other/Exception and Traceback Logging in Python/index.md>)。

记录日期：2026-09-07T10:39:33；状态：正文已核阅；有修改意见。

#### R023

**事实/技术错误 · 事实 · P2**

定位：[原文第 17 行](<C:/Project/blog/other/Exception and Traceback Logging in Python/index.md:17>)；待改表述／主题：` 任何复制或序列化…都会丢弃这个三元组 `。

原文定位行（节选）：` 三个机制几乎可以解释 Python 中所有异常日志记录的错误：记录携带的是一个实时的（类型-type、值-value、回溯-traceback）三元组，而不是一个字符串；第一个访问该记录的格式化程序会将渲染结果（formatter render）缓存起来供其他程序使用；任何复制或序列化该记录的操作都会丢弃这个三元组。搞清楚这三点，其余的问题——链式异常、异步逃逸路径、帧限制、数据脱敏——也就迎刃而解了。具体的操作步骤包括记录异常和回溯信息、捕获未处理的异常和警告，以及在日志记… `

问题：浅复制不会自动丢失 exc_info；标准 pickle 不能直接序列化 traceback，直接深复制可能失败而非自动剥离。原英文也有相同泛化。

建议修改：改为“默认 QueueHandler.prepare 会清除 exc_info；进程间传输需先转换 traceback；普通浅复制可保留 exc_info”。

依据：[Python 官方文档 · logging.handlers · logging.handlers.QueueHandler.prepare](https://docs.python.org/3.12/library/logging.handlers.html#logging.handlers.QueueHandler.prepare)。

#### R024

**事实/技术错误 · 翻译 · P2**

定位：[原文第 31 行](<C:/Project/blog/other/Exception and Traceback Logging in Python/index.md:31>)；待改表述／主题：` 当从 exc 中调用 raise NewError / 当从 None 中调用 __suppress_context__ `。

原文定位行（节选）：`` 第三个事实是链式异常。自 Python 3 起，在处理另一个异常时引发的每个异常都会带有指向它的链接：当异常隐式发生时，使用 `__context__`；当从 `exc` 中调用 `raise NewError` 时，使用 `__cause__`；当从 `None` 中调用 `__suppress_context__` 时，使用 `__suppress_context__`。默认的回溯渲染器会遍历这些链接并打印所有链接，链接之间用两个含义截然不同的句子之一连接。 ``

问题：把 Python 的 from 子句误译成“从…中调用”。

建议修改：改为“raise NewError from exc 设置显式原因 __cause__；raise NewError from None 设置 __suppress_context__=True，抑制隐式上下文的显示”。

依据：[Python 官方文档 · simple_stmts · the-raise-statement](https://docs.python.org/3/reference/simple_stmts.html#the-raise-statement)。

#### R025

**事实/技术错误 · 代码 · P1**

定位：[原文第 127 行](<C:/Project/blog/other/Exception and Traceback Logging in Python/index.md:127>)；待改表述／主题：` return json.dumps(payload, default=str)[:limit] `。

原文定位行（节选）：` return json.dumps(payload, default=str)[:limit] `

问题：硬切 JSON 字符串会破坏 JSON；len(str) 限制字符数，不能保证UTF-8字节上限。原来源也存在此问题。

建议修改：截断字段或删除帧后重新 json.dumps，并检查 len(body.encode('utf-8'))；过大时返回带 truncated=true 的合法最小 JSON。

依据：[Python 官方文档 · json](https://docs.python.org/3/library/json.html)。

#### R026

**事实/技术错误 · 翻译 · P2**

定位：[原文第 132 行](<C:/Project/blog/other/Exception and Traceback Logging in Python/index.md:132>)；待改表述／主题：` 数据编辑 / 编辑敏感数据 `。

原文定位行（节选）：` 步骤 6 — 在生成异常的线程上进行数据编辑。异常消息会携带失败调用中的所有内容：例如带有密码的 DSN、URL 中的令牌、一行客户数据。将数据编辑过滤器附加到日志记录器而不是处理程序，以便它在记录被排队、复制或发送之前运行。有关模式集及其失败模式，请参阅“在日志记录中编辑敏感数据”。 `

问题：redaction 在日志安全语境指脱敏，不是一般编辑。

建议修改：统一改为“数据脱敏”“对日志中的敏感数据进行脱敏”。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A017

**How Complex Systems Fail**

原文：[other/How Complex Systems Fail/index.md](<C:/Project/blog/other/How Complex Systems Fail/index.md>)。

记录日期：2026-09-15T17:21:54；状态：正文已核阅；有修改意见。

#### R027

**字词/链接 · 字词 · P3**

定位：[原文第 20 行](<C:/Project/blog/other/How Complex Systems Fail/index.md:20>)；待改表述／主题：` Cognitive Technologies Labratory `。

原文定位行（节选）：` Cognitive Technologies Labratory `

问题：实验室英文拼写错误（源网页本身也保留了该误字）。

建议修改：改为“Cognitive Technologies Laboratory”，或在忠实转录时加译注说明原文误拼。

依据：[原作者文章](https://how.complexsystems.fail/)。

### A018

**logging sucks**

原文：[other/logging sucks/index.md](<C:/Project/blog/other/logging sucks/index.md>)。

记录日期：2026-08-12T11:51:36；状态：正文已核阅；有修改意见。

#### R028

**事实/技术错误 · 事实 · P2**

定位：[原文第 113 行](<C:/Project/blog/other/logging sucks/index.md:113>)；待改表述／主题：` 17行 ×10,000…130,000行 `。

原文定位行（节选）：` 一次成功的请求会产生 17 行日志。现在乘以 10,000 个并发用户，每秒就会产生 130,000 行日志。其中大部分日志毫无用处。 `

问题：按给定数字应为170,000；并发人数也不能直接等同于每秒请求数。原来源也存在数字不一致。

建议修改：改为“若每秒10,000个请求、每个17行，则每秒170,000行”；或将前文每请求行数统一为13后再给130,000。

依据：[原作者文章](https://loggingsucks.com/)。

### A019

**Python Logging and Structured Data Architecture Guide for SREs**

原文：[other/Python Logging and Structured Data Architecture Guide for SREs/index.md](<C:/Project/blog/other/Python Logging and Structured Data Architecture Guide for SREs/index.md>)。

记录日期：2026-08-31T10:01:51；状态：正文已核阅；有修改意见。

#### R029

**事实/技术错误 · 事实 · P2**

定位：[原文第 121 行](<C:/Project/blog/other/Python Logging and Structured Data Architecture Guide for SREs/index.md:121>)；待改表述／主题：` json.dumps几乎完全是纯Python实现 `。

原文定位行（节选）：`` 序列化成本是标准库暴露其不足之处的唯一地方。除了最简单的类型之外，`json.dumps` 几乎完全是纯 Python 实现，而每秒处理数万条记录时，其成本就会变得非常可观。两种缓解措施可以很好地结合起来：一是将序列化器完全从请求路径中移除（如下所述的队列模式），二是使用速度更快的编码器，但保持相同的格式化接口。如果您的团队更倾向于采用预编译好的库，那么可以参考 [structlog、Loguru 和标准库日志记录的对比](https://python-observabili… ``

问题：CPython标准json模块通常使用 _json C加速器，该断言错误。

建议修改：改为“JSON序列化仍有成本；CPython有C加速实现，实际耗时需按字段和吞吐量测量”。

依据：[仓库源码：python/cpython · encoder.py](https://github.com/python/cpython/blob/main/Lib/json/encoder.py)。

#### R030

**事实/技术错误 · 事实 · P2**

定位：[原文第 129 行](<C:/Project/blog/other/Python Logging and Structured Data Architecture Guide for SREs/index.md:129>)；待改表述／主题：` 禁用…之前创建的所有日志记录器 `。

原文定位行（节选）：`` disable_existing_loggers 字段是最常让团队感到意外的字段：如果保留默认值 `True`，它会禁用 `dictConfig` 运行之前创建的所有日志记录器，这会导致之前导入的任何模块级日志记录器都被静默禁用。生产服务几乎总是希望将其设置为 `False`。`ext://` 前缀允许字典引用诸如 `ext://sys.stdout` 之类的活动对象而无需导入它们，从而保持配置的声明性和可序列化性。 ``

问题：disable_existing_loggers=True 存在例外：配置中显式列出的记录器及其后代不会按该规则禁用，root也不是这里的全部集合。

建议修改：改为“默认禁用已有的非root记录器，但配置中显式指定的记录器及其后代除外”。

依据：[Python 官方文档 · logging.config · configuration-dictionary-schema](https://docs.python.org/3/library/logging.config.html#configuration-dictionary-schema)。

#### R031

**事实/技术错误 · 事实 · P2**

定位：[原文第 133 行](<C:/Project/blog/other/Python Logging and Structured Data Architecture Guide for SREs/index.md:133>)；待改表述／主题：` 把…Filter挂载到Logger…每个输出目标…一致 `。

原文定位行（节选）：` 一套经得起生产环境实际考验的启动（bootstrap）流程并不复杂，而且值得严格按照顺序执行。第一步，先确定 LogRecord 的数据结构——包括 envelope（信封层）、correlation（关联信息层）和 payload（业务载荷层），因为后续的每一个决策都会依赖这些字段名。第二步，用一个 dictConfig 字典表达完整的日志处理图，并将 disable_existing_loggers 设置为 False；然后在应用入口处、任何请求开始处理之前，准确地调用一… `

问题：祖先 Logger 的 Filter 不作用于传播来的子 Logger 记录。第95、117、340行同类表述可能漏掉子模块日志。

建议修改：若需全应用统一脱敏/补字段，把Filter挂在共同的QueueHandler（入队前）或每个产生记录的Logger上；说明祖先Logger过滤器不覆盖后代。

依据：[Python 官方文档 · logging · filter-objects](https://docs.python.org/3/library/logging.html#filter-objects)。

#### R032

**事实/技术错误 · 事实 · P2**

定位：[原文第 168 行](<C:/Project/blog/other/Python Logging and Structured Data Architecture Guide for SREs/index.md:168>)；待改表述／主题：` 模块级锁会序列化处理程序的发出 `。

原文定位行（节选）：`` 标准日志调用是线程安全的：模块级锁会序列化处理程序的发出。然而，它们并不感知异步，并且自身不携带请求范围的上下文。正确的模式是将每个请求的元数据存储在 `contextvars.ContextVar` 对象中，并在发出日志时通过过滤器读取它们。上下文变量可以在任务内的 `await` 边界之间正确传播，并在创建新任务时被复制，这使得它们成为 asyncio 服务的理想原语。安全上下文传播的完整处理体现在上下文变量和线程安全中，而请求范围模式则具体应用于使用 `contextv… ``

问题：logging 的模块级锁保护共享配置；输出通常由各个 Handler 自己的锁串行化，不是所有 Handler 共用一个全局I/O锁。第505行重复同误。

建议修改：两处改为“同一Handler的输出受其锁保护，多个线程竞争同一慢Handler时可能阻塞”。

依据：[Python 官方文档 · logging · thread-safety](https://docs.python.org/3/library/logging.html#thread-safety)。

#### R033

**事实/技术错误 · 事实 · P2**

定位：[原文第 170 行](<C:/Project/blog/other/Python Logging and Structured Data Architecture Guide for SREs/index.md:170>)；待改表述／主题：` QueueHandler只负责…避免…格式化 `。

原文定位行（节选）：`` 处理程序执行的序列化和 I/O 操作绝不能运行在事件循环或请求工作线程上。使用 `QueueHandler` 包装具体的处理程序，`QueueHandler` 只负责将记录入队，并通过专用的 `QueueListener` 消费者线程来清空队列。这样可以避免调用路径上的格式化和写入延迟。本教程专门介绍如何使用 QueueHandler 实现[非阻塞日志记录](https://python-observability.com/python-logging-fundamental… ``

问题：默认prepare()会在生产线程调用format()、合并消息与异常文本并清除args/exc_info；只把最终I/O移到监听线程。第493、505行也重复此误。

建议修改：明确默认仍在调用线程准备记录；若要把JSON格式化也移到监听端，不给QueueHandler配置JSON Formatter，必要时按进程内/跨进程需求覆盖prepare。

依据：[Python 官方文档 · logging.handlers · logging.handlers.QueueHandler.prepare](https://docs.python.org/3.12/library/logging.handlers.html#logging.handlers.QueueHandler.prepare)。

#### R034

**字词/链接 · 字词 · P3**

定位：[原文第 262 行](<C:/Project/blog/other/Python Logging and Structured Data Architecture Guide for SREs/index.md:262>)；待改表述／主题：` secerity_number / 上下文传播和行李 / 重写检测代码 `。

原文定位行（节选）：` | Python level | levelno | OTel secerity_number | syslog severity | Typical production routing | `

问题：severity_number拼错；baggage、instrumentation翻译不合技术语境。

建议修改：改为“severity_number”“上下文传播与 Baggage（跨服务传播的键值上下文）”“重写插桩代码”。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A020

**Myers差分算法**

原文：[software/algorithm/Myers差分算法/index.md](<C:/Project/blog/software/algorithm/Myers差分算法/index.md>)。

记录日期：2025-06-01T10:44:00+08:00；状态：正文已核阅；有修改意见。

#### R035

**事实/技术错误 · 事实 · P2**

定位：[原文第 83 行](<C:/Project/blog/software/algorithm/Myers差分算法/index.md:83>)；待改表述／主题：` A(7)=空 `。

原文定位行（节选）：` A(7)=空，B(7)=i，执行插入操作，插入字符 i，此时，A 变成 complaint。 `

问题：删除 i 后 A=complant，第7个字符是 n，并非空。

建议修改：改为“A(7)=n，B(7)=i，在 n 前插入 i”，随后 n 和 t 匹配。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A021

**从定时器到时间轮：速率可控任务调度算法的演进**

原文：[software/algorithm/从定时器到时间轮：速率可控任务调度算法的演进/index.md](<C:/Project/blog/software/algorithm/从定时器到时间轮：速率可控任务调度算法的演进/index.md>)。

记录日期：2026-01-18T10:44:43；状态：草稿；正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A022

**随机密码的生成**

原文：[software/algorithm/随机密码的生成/index.md](<C:/Project/blog/software/algorithm/随机密码的生成/index.md>)。

记录日期：2025-11-14T11:11:08；状态：正文已核阅；有修改意见。

#### R036

**事实/技术错误 · 代码 · P2**

定位：[原文第 26 行](<C:/Project/blog/software/algorithm/随机密码的生成/index.md:26>)；待改表述／主题：` import string, random `。

原文定位行（节选）：` import string, random `

问题：random 的伪随机生成器不适合生成实际账号密码；shuffle 也没有密码学安全保证。

建议修改：用 secrets.choice；满足组成要求时可对 secrets 生成的候选密码做拒绝采样，避免再用 random.shuffle。默认长度建议至少16字符，按真实服务限制调整；不能笼统认定8–12位就是高强度。

依据：[Python 官方文档 · secrets](https://docs.python.org/3.10/library/secrets.html)。

### A023

**Python的Thread基础**

原文：[software/concurrency/Python的Thread基础/index.md](<C:/Project/blog/software/concurrency/Python的Thread基础/index.md>)。

记录日期：2026-01-01T09:35:51；状态：草稿；正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A024

**JPA+MySQL的主键选择**

原文：[software/database/jpa/JPA+MySQL的主键选择/index.md](<C:/Project/blog/software/database/jpa/JPA+MySQL的主键选择/index.md>)。

记录日期：2023-06-13T17:19:42+08:00；状态：正文已核阅；有修改意见。

#### R037

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 34 行](<C:/Project/blog/software/database/jpa/JPA+MySQL的主键选择/index.md:34>)；待改表述／主题：` 主键必须是逻辑性的而非业务性的 `。

原文定位行（节选）：` 有时候，一些具有唯一性的业务字段（比如，身份证，订单号）会被用作主键，但这并不是一个最佳的选择，主键必须是逻辑性的而非业务性的，它唯一的作用就是标志某行数据，主键不能具有任何业务性的含义。 `

问题：代理主键是设计选择，不是关系型数据库强制规则；数据库也能更新主键，JPA实体身份则有自己的限制。

建议修改：改为“多数易变业务场景建议代理主键；稳定自然键可作主键。JPA应用中不应更改已持久化实体的标识”。

依据：[Jakarta 规范 · 3.1](https://jakarta.ee/specifications/persistence/3.1/)。

#### R038

**字词/链接 · 字词 · P3**

定位：[原文第 54 行](<C:/Project/blog/software/database/jpa/JPA+MySQL的主键选择/index.md:54>)；待改表述／主题：` 引擎时 / 一颗B+Tree / 增加了方法磁盘IO `。

原文定位行（节选）：` 但采用 UUID 的话，由于每次插入主键的值近似于随机，因此每次新记录都要被插到现有索引页的中间某个位置，MySQL 不得不为了将新记录插到合适位置而移动数据，这样就造成了一定的开销。MySQL 为维护索引可能需要频繁的刷新缓冲，增加了方法磁盘 IO 的次数，而且时常需要对索引结构进行重组织。 `

问题：明显误字。

建议修改：改“引擎是”“一棵B+Tree”“增加了访问磁盘的IO次数”。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R039

**条件/版本澄清 · 版本条件 · P2**

定位：[原文第 71 行](<C:/Project/blog/software/database/jpa/JPA+MySQL的主键选择/index.md:71>)；待改表述／主题：` JPA提供四种…javax.persistence `。

原文定位行（节选）：`` 这四种生成策略定义在了 `javax.persistence.GenerationType` 中： ``

问题：四种GenerationType符合旧版javax.persistence/JPA；Jakarta Persistence 3.1新增UUID。应注明本文实际API版本，不能将新旧版本混为一谈。

建议修改：改为“JPA2.x 的javax.persistence有四种；Jakarta Persistence3.1 的jakarta.persistence另外包含UUID”。

依据：[Jakarta 规范 · 3.1](https://jakarta.ee/ja/specifications/persistence/3.1/)。

#### R040

**事实/技术错误 · 事实 · P2**

定位：[原文第 134 行](<C:/Project/blog/software/database/jpa/JPA+MySQL的主键选择/index.md:134>)；待改表述／主题：` Oracle不支持ID自增长列 `。

原文定位行（节选）：` Oracle 不支持 ID 自增长列而是使用序列的机制生成主键 ID。对此，可以选用序列（Sequence）作为主键生成策略。 `

问题：Oracle12c起支持identity列。

建议修改：表格注明Oracle版本和JPA提供者；对Oracle12c+补IDENTITY，旧版本使用sequence。

依据：[Oracle／Java 官方文档 · columns-pane](https://docs.oracle.com/en/database/oracle/sql-developer-web/21.1/sdweb/columns-pane.html)。

### A025

**JPA中的枚举类型字段存储**

原文：[software/database/jpa/JPA中的枚举类型字段存储/index.md](<C:/Project/blog/software/database/jpa/JPA中的枚举类型字段存储/index.md>)。

记录日期：2023-08-20T14:49:30+08:00；状态：正文已核阅；有修改意见。

#### R041

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 114 行](<C:/Project/blog/software/database/jpa/JPA中的枚举类型字段存储/index.md:114>)；待改表述／主题：` 添加新的类型…ordinal值的含义都将发生改变 `。

原文定位行（节选）：`` 可以看到数据库存储的是 `int` 类型的 0，也就是 `Status.OPEN.ordinal()` 的值，这种方式有个很大的缺点：如果在枚举类的类型中添加新的类型，那么存储到数据库中的 ordinal 值的含义都将发生改变，这意味着我们需要更新整个数据库的 `status` 字段的值。 ``

问题：仅当在已有值之前插入、重排或删除导致序号变化时才影响已有映射；追加到末尾不改变原序号。

建议修改：改为“调整已有枚举值的顺序或在中间插入/删除会改变部分ordinal映射；末尾追加不改变已有序号”。

依据：[Oracle／Java 官方文档 · Enum · ordinal()](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Enum.html#ordinal())。

### A026

**MySQL存储树状结构的数据**

原文：[software/database/mysql/MySQL存储树状结构的数据/index.md](<C:/Project/blog/software/database/mysql/MySQL存储树状结构的数据/index.md>)。

记录日期：2023-04-04T19:51:05+08:00；状态：草稿；正文已核阅；有修改意见。

#### R042

**条件/版本澄清 · 模型条件澄清 · P2**

定位：[原文第 38 行](<C:/Project/blog/software/database/mysql/MySQL存储树状结构的数据/index.md:38>)；待改表述／主题：` 行政区划依照省-市-区划分，是一棵完整…树 `。

原文定位行（节选）：` 在本文中，选择中国的行政区划作为案例，因为行政区划依照省-市-区划分，是一棵完整的分层的树状结构。 `

问题：三级树可作为教学简化模型，但不是中国全部行政区划的统一结构；直辖市、省直辖县级单位等有例外。

建议修改：说明用的是简化教学树，实际导入按数据源父子关系处理，不硬编码三级；GB/T2260-2007不能作为最新行政区快照。

依据：[全国人大：宪法 · t20190521_281393](https://www.npc.gov.cn/c2/c30834/201905/t20190521_281393.html)。

#### R043

**字词/链接 · 字词 · P3**

定位：[原文第 109 行](<C:/Project/blog/software/database/mysql/MySQL存储树状结构的数据/index.md:109>)；待改表述／主题：` 字节点 / 因外 / leve `。

原文定位行（节选）：` 首先我们需要明晰一些术语，父节点，字节点，叶子节点，祖先节点和后代节点： `

问题：误字。

建议修改：改“子节点”“因为”“level”；第308行“一颗树”改“一棵树”。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R044

**事实/技术错误 · 代码 · P1**

定位：[原文第 263 行](<C:/Project/blog/software/database/mysql/MySQL存储树状结构的数据/index.md:263>)；待改表述／主题：` 根节点id=0 / 表中中国id=1 `。

原文定位行（节选）：` Predicate<AreaVO> isRoot = areaVO -> Objects.equals(areaVO.getId(), "0"); `

问题：完整代码根节点为0，而样例中国为1，findFirst().get()会失败；方法接收id却未使用。

建议修改：统一根节点约定或用传入id查找，并处理根节点不存在。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A027

**MySQL数据的备份**

原文：[software/database/mysql/MySQL数据的备份/index.md](<C:/Project/blog/software/database/mysql/MySQL数据的备份/index.md>)。

记录日期：2023-09-15T14:30:04+08:00；状态：正文已核阅；有修改意见。

#### R045

**字词/链接 · 字词 · P3**

定位：[原文第 88 行](<C:/Project/blog/software/database/mysql/MySQL数据的备份/index.md:88>)；待改表述／主题：` 本片 / 然后又四张表 / my_db_bak.sql `。

原文定位行（节选）：`` 然后将刚刚备份的 `my_db_bak.sql` 的表结构和数据恢复到这个新建的库中： ``

问题：误字及文件名不一致。

建议修改：改“本篇”“有四张表”；第88行文件名与示例统一为my_db_back.sql。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R046

**事实/技术错误 · 代码 · P1**

定位：[原文第 136 行](<C:/Project/blog/software/database/mysql/MySQL数据的备份/index.md:136>)；待改表述／主题：` --databases ${db_name} `。

问题：此选项生成CREATE DATABASE/USE原库，不能直接保证恢复到另一个指定库；脚本也未判断转储失败就淘汰旧备份。

建议修改：明确备份文件是否带库名；恢复到新库时使用不带--databases的转储或审核重写USE。转储到临时文件，确认退出码及可恢复性后再改名和删除旧备份。

依据：[MySQL 官方文档 · mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html)。

### A028

**MySQL的事务**

原文：[software/database/mysql/MySQL的事务/index.md](<C:/Project/blog/software/database/mysql/MySQL的事务/index.md>)。

记录日期：2024-03-30T13:34:56+08:00；状态：正文已核阅；有修改意见。

#### R047

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 70 行](<C:/Project/blog/software/database/mysql/MySQL的事务/index.md:70>)；待改表述／主题：` 即使断电，也不会丢失 `。

原文定位行（节选）：` 持久性，指的是在事务完成后，所有的更新修改都会被持久化到数据库中，即使断电，也不会丢失事务所做出的修改。 `

问题：持久性保证受存储引擎、刷盘设置和硬件影响，不能脱离配置绝对保证。

建议修改：注明InnoDB在可靠存储及相应刷盘配置下保证已提交事务持久化，并解释innodb_flush_log_at_trx_commit=1；不是任意配置都断电无损。

依据：[MySQL 官方文档 · innodb-parameters · sysvar_innodb_flush_log_at_trx_commit](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_flush_log_at_trx_commit)。

#### R048

**字词/链接 · 字词 · P3**

定位：[原文第 129 行](<C:/Project/blog/software/database/mysql/MySQL的事务/index.md:129>)；待改表述／主题：` 隔离界别 / 确爆出 / 它确保在 `。

原文定位行（节选）：` 该隔离界别会导致不可重复读的问题，这意味着我们在一个事务中执行两个一模一样的 select 语句可能会得到不一样的结果。 `

问题：多处“界别”误写；第135行论述未完成。

建议修改：统一“隔离级别”；第299行改“却报出”；补完第135行可重复读的定义。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R049

**事实/技术错误 · 事实 · P2**

定位：[原文第 299 行](<C:/Project/blog/software/database/mysql/MySQL的事务/index.md:299>)；待改表述／主题：` 主键重复…所以…称为幻读 `。

原文定位行（节选）：` 客户端-2 没有查询到 id 为 3 的用户，但是确爆出了主键重复的异常信息，就好像是幻觉一样，所以该问题被称为“幻读”。 `

问题：主键唯一检查使用当前数据，快照SELECT与唯一检查视图不同；该现象不能作为经典幻读的定义。InnoDB RR快照读保持快照，锁定读用next-key锁抑制范围幻影。

建议修改：改写此例为“快照读与唯一性检查的差异”；幻读定义为同一查询谓词下可见行集合因其他事务改变而变化，另分清标准RR与InnoDB实现。

依据：[MySQL 官方文档 · innodb-consistent-read](https://dev.mysql.com/doc/refman/8.0/en/innodb-consistent-read.html)；[MySQL 官方文档 · innodb-next-key-locking](https://dev.mysql.com/doc/refman/8.0/en/innodb-next-key-locking.html)。

### A029

**MySQL的索引**

原文：[software/database/mysql/MySQL的索引/index.md](<C:/Project/blog/software/database/mysql/MySQL的索引/index.md>)。

记录日期：2024-02-03T14:44:42+08:00；状态：正文已核阅；有修改意见。

#### R050

**事实/技术错误 · 事实 · P2**

定位：[原文第 28 行](<C:/Project/blog/software/database/mysql/MySQL的索引/index.md:28>)；待改表述／主题：` 每个节点…拥有左、右两个子节点 `。

原文定位行（节选）：` 二叉树的每个节点，分别拥有左、右两个子节点，二叉树是最简单的一种树。 `

问题：二叉树每个节点最多两个子节点，叶子没有子节点。

建议修改：改为“最多有左、右两个子节点”。第77–78行B树性质需注明m为最大孩子数，叶子无孩子，根为叶子时可没有孩子。

依据：[NIST 算法与数据结构词典 · binarytree](https://xlinux.nist.gov/dads/HTML/binarytree.html)；[NIST 算法与数据结构词典 · btree](https://xlinux.nist.gov/dads/HTML/btree.html)。

#### R051

**字词/链接 · 字词 · P3**

定位：[原文第 76 行](<C:/Project/blog/software/database/mysql/MySQL的索引/index.md:76>)；待改表述／主题：` 有叶子节点 / 就先上面 / 再对树 `。

原文定位行（节选）：` 1. 有叶子节点必须出现在同一层。 `

问题：误字。

建议修改：改“所有叶子节点”“就像上面”“在对树”；B树性质先统一m阶定义再写键数与孩子数。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A030

**ORM是什么**

原文：[software/database/ORM是什么/index.md](<C:/Project/blog/software/database/ORM是什么/index.md>)。

记录日期：2025-12-12T10:54:27；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A031

**PG的字符类型**

原文：[software/database/postgresql/PG的字符类型/index.md](<C:/Project/blog/software/database/postgresql/PG的字符类型/index.md>)。

记录日期：2026-05-17T11:47:16；状态：正文已核阅；有修改意见。

#### R052

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 26 行](<C:/Project/blog/software/database/postgresql/PG的字符类型/index.md:26>)；待改表述／主题：` 超过n…都会报错 / 小于10485760 `。

原文定位行（节选）：` n 的范围：必须大于 0 小于 10485760，如果 char 没有传入 n，等价于 char(1)，如果 varchar 没有传入 n，则等价于无限长度和 text 一样（并非无限，存储字符串长度不超过大约 1GB）。 `

问题：超长部分都是空格可被截去；显式cast到char(n)/varchar(n)会截断而不报错；上限包括10485760。

建议修改：补上述两种例外，范围改“1≤n≤10485760”。

依据：[PostgreSQL 官方文档 · datatype-character](https://www.postgresql.org/docs/17/datatype-character.html)。

### A032

**创建数据库、模式和表**

原文：[software/database/postgresql/创建数据库、模式和表/index.md](<C:/Project/blog/software/database/postgresql/创建数据库、模式和表/index.md>)。

记录日期：2026-05-02T20:49:38；状态：草稿；正文已核阅；有修改意见。

#### R053

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 127 行](<C:/Project/blog/software/database/postgresql/创建数据库、模式和表/index.md:127>)；待改表述／主题：` 同一个模式…对象需要不同名字 `。

原文定位行（节选）：` 在同一个模式下，对象需要具有不同的名字，比如 index 和 table 不能重名，但是在不同模式下，一个名字可以重复使用，比如多租户系统下，schema-1 包含了 user 表，schema-2 也可以包含一个同样名字的 user 表。 `

问题：不同对象类别不都共享名字空间；同名函数可重载，函数名也可和表名相同。

建议修改：改为“表、索引、视图等关系对象共享名字空间；函数等按各自命名/重载规则”。

依据：[PostgreSQL 官方文档 · ddl-schemas](https://www.postgresql.org/docs/17/ddl-schemas.html)。

#### R054

**字词/链接 · 字词 · P3**

定位：[原文第 134 行](<C:/Project/blog/software/database/postgresql/创建数据库、模式和表/index.md:134>)；待改表述／主题：` 不制定schema / PG14以前 `。

原文定位行（节选）：` 每一个数据库新建后，PG 都会自动创建一个名为 public 的 schema，如果创建表或者其他对象时，不制定 schema，那么这些对象默认归属于 public 模式。 `

问题：应为“指定”；public默认CREATE权限分界应含PG14。

建议修改：改“指定”；改“PG14及以前默认CREATE和USAGE，PG15起默认仅USAGE（升级/模板继承的权限可能不同）”。

依据：[PostgreSQL 官方文档 · ddl-schemas](https://www.postgresql.org/docs/17/ddl-schemas.html)。

#### R055

**事实/技术错误 · 事实 · P2**

定位：[原文第 134 行](<C:/Project/blog/software/database/postgresql/创建数据库、模式和表/index.md:134>)；待改表述／主题：` 不指定schema…默认归属于public `。

原文定位行（节选）：` 每一个数据库新建后，PG 都会自动创建一个名为 public 的 schema，如果创建表或者其他对象时，不制定 schema，那么这些对象默认归属于 public 模式。 `

问题：新对象创建在search_path中第一个存在可用的模式；用户同名模式存在时会优先使用，与后文current_schema描述矛盾。

建议修改：改为“默认search_path为$user, public；创建到current_schema()返回的模式，通常在不存在同名用户模式时才是public”。

依据：[PostgreSQL 官方文档 · ddl-schemas](https://www.postgresql.org/docs/17/ddl-schemas.html)。

### A033

**表连接**

原文：[software/database/postgresql/表连接/index.md](<C:/Project/blog/software/database/postgresql/表连接/index.md>)。

记录日期：2026-06-06T10:09:03；状态：正文已核阅；有修改意见。

#### R056

**条件/版本澄清 · 业务模型条件 · P2**

定位：[原文第 71 行](<C:/Project/blog/software/database/postgresql/表连接/index.md:71>)；待改表述／主题：` 商品价格发生变动…修改订单表 `。

原文定位行（节选）：` 2. 如果实体类更改了信息，比如用户 alice 修改了手机号，商品价格发生变动，我们需要扫描整张订单表去修改相关的数据，因为所有的实体类信息都被冗余存储了，alice 下了 1000 次订单，那么她的个人信息就在这张表里出现了 1000 次，她修改了手机号就需要把 1000 条订单记录都修改一遍。 `

问题：当前用户/商品资料与历史交易快照是不同的数据语义。只有希望订单引用当前属性时才应随主数据更新，不能笼统要求更新历史订单成交价。

建议修改：注明本文只是演示关联当前实体信息；历史订单通常保存成交价、下单联系方式等快照，应按业务语义决定，不应自动批量改写。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A034

**角色、用户和权限**

原文：[software/database/postgresql/角色、用户和权限/index.md](<C:/Project/blog/software/database/postgresql/角色、用户和权限/index.md>)。

记录日期：2026-01-19T15:01:21；状态：草稿；正文已核阅；有修改意见。

#### R057

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 43 行](<C:/Project/blog/software/database/postgresql/角色、用户和权限/index.md:43>)；待改表述／主题：` 设置一个对应的nologin用户 `。

原文定位行（节选）：` PG 的超级用户 postgres 同时会在 Linux 下设置一个对应的 nologin 用户，名字也叫 postgres。 `

问题：这是安装方式相关的OS账号配置；本文sudo -iu postgres通常要求可执行的登录shell，与笼统nologin表述矛盾。

建议修改：注明Debian包创建的OS账号和数据库角色分别管理，实际shell/peer规则以本机配置为准，删除统一为nologin的断言。

依据：[PostgreSQL 官方文档 · auth-peer](https://www.postgresql.org/docs/17/auth-peer.html)。

#### R058

**字词/链接 · 字词 · P3**

定位：[原文第 133 行](<C:/Project/blog/software/database/postgresql/角色、用户和权限/index.md:133>)；待改表述／主题：` Memeber / 显示的 / 整个默认用户 / 一下一些 `。

原文定位行（节选）：`` 可以通过 `GRANT` 和 `REVOKE` 来把成员（Memeber，可以是角色，也可以是用户）添加到组或者从组中删除。 ``

问题：拼写及误字。

建议修改：改“Member”“显式地”“这个默认用户”“以下一些”。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R059

**事实/技术错误 · 事实 · P2**

定位：[原文第 142 行](<C:/Project/blog/software/database/postgresql/角色、用户和权限/index.md:142>)；待改表述／主题：` PUBLIC是默认角色 / 默认根角色 `。

原文定位行（节选）：` PUBLIC 又是所有角色所属的默认根角色，所以你无法把 PUBLIC 添加到任何组内。 `

问题：PUBLIC是代表所有角色的特殊权限集合，不是pg_roles里可管理、可登录的普通根角色。

建议修改：改为“PUBLIC是表示所有角色的特殊伪角色；向PUBLIC授权意味着对所有角色授权”。

依据：[PostgreSQL 官方文档 · sql-grant](https://www.postgresql.org/docs/17/sql-grant.html)。

### A035

**redis-py中连接池的使用**

原文：[software/database/redis/redis-py中连接池的使用/index.md](<C:/Project/blog/software/database/redis/redis-py中连接池的使用/index.md>)。

记录日期：2025-06-21T11:13:00+08:00；状态：正文已核阅；有修改意见。

#### R060

**字词/链接 · 字词 · P3**

定位：[原文第 29 行](<C:/Project/blog/software/database/redis/redis-py中连接池的使用/index.md:29>)；待改表述／主题：` ConnectPool / connect_pool / 接受指令 / 还可以还种 / max_connect `。

原文定位行（节选）：`` redis-py 创建客户端的方式是实例化一个 Redis 对象（Redis 类存在于 `client.py` 中），构造器中的一个参数——`connection_pool`，就是用来指定连接池对象的，通过源码可以看到，如果不传递 `connect_pool` 对象，那么在构造函数中，会自动创建一个连接池对象。 ``

问题：类名和参数名混写。

建议修改：统一ConnectionPool、connection_pool、max_connections；“接受结果”改“接收结果”；第197行改“还可以换种写法”。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R061

**事实/技术错误 · 代码 · P1**

定位：[原文第 220 行](<C:/Project/blog/software/database/redis/redis-py中连接池的使用/index.md:220>)；待改表述／主题：` 循环内只有pipe.execute() `。

原文定位行（节选）：` def get_some_data_4(num): `

问题：没有调用pipe.get()排队命令；执行的是空pipeline，108ms不能与10000次GET比较。

建议修改：循环内调用pipe.get('hello')，循环外只调用一次execute；若只批量GET可用pipeline(transaction=False)。重跑并撤回原性能和抓包结论。

依据：[redis-py 官方文档 · advanced_features](https://redis.readthedocs.io/en/v6.2.0/advanced_features.html)。

#### R062

**事实/技术错误 · 代码 · P1**

定位：[原文第 304 行](<C:/Project/blog/software/database/redis/redis-py中连接池的使用/index.md:304>)；待改表述／主题：` ThreadPoolExecutor(max_worker=10) `。

原文定位行（节选）：` with ThreadPoolExecutor(max_worker=10) as executor: `

问题：参数名错误，运行会TypeError。

建议修改：改max_workers=10。

依据：[Python 官方文档 · concurrent.futures · concurrent.futures.ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor)。

#### R063

**事实/技术错误 · 事实 · P2**

定位：[原文第 313 行](<C:/Project/blog/software/database/redis/redis-py中连接池的使用/index.md:313>)；待改表述／主题：` Redis客户端…线程安全…暂不下定论 `。

原文定位行（节选）：` 问题在于 Redis 客户端实例是否也是线程安全的，这一点暂时没有测试出来，不同的资料和 AI 给的结论也不相同，只能看源码了，这里先不下定论。 `

问题：redis-py文档明确普通连接池模式的Redis客户端可以跨线程共享；Pipeline和PubSub不可共享。

建议修改：引用所用6.2文档给出结论，并注明single_connection_client、事务pipeline和PubSub例外。

依据：[redis-py 官方文档 · advanced_features](https://redis.readthedocs.io/en/v6.2.0/advanced_features.html)。

#### R064

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 323 行](<C:/Project/blog/software/database/redis/redis-py中连接池的使用/index.md:323>)；待改表述／主题：` n=1,m=10性能比n=10,m=1更好 `。

原文定位行（节选）：`` n = 1，`max_connect` = 10 的性能会比 n = 10，`max_connect` = 1 的性能更好，更不容易出现以下的异常： ``

问题：总连接上限一样不代表吞吐更高；依赖worker类型、并发、CPU和请求工作量，串行worker也不一定用得上10条连接。

建议修改：将此句及第329行建议改为需压测的配置假设，注明(2×CPU)+1只是Gunicorn起始经验值；普通ConnectionPool满时通常报错，需等待可用BlockingConnectionPool。

依据：[仓库源码：benoitc/gunicorn · design.rst](https://github.com/benoitc/gunicorn/blob/23.0.0/docs/source/design.rst)。

### A036

**redis的string类型**

原文：[software/database/redis/redis的string类型/index.md](<C:/Project/blog/software/database/redis/redis的string类型/index.md>)。

记录日期：2025-06-21T11:13:00+08:00；状态：草稿；正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A037

**redis的配置文件**

原文：[software/database/redis/redis的配置文件/index.md](<C:/Project/blog/software/database/redis/redis的配置文件/index.md>)。

记录日期：2025-06-21T11:13:00+08:00；状态：草稿；正文已核阅；有修改意见。

#### R065

**事实/技术错误 · 事实 · P2**

定位：[原文第 41 行](<C:/Project/blog/software/database/redis/redis的配置文件/index.md:41>)；待改表述／主题：` bind0.0.0.0表示…接受所有远程连接 `。

原文定位行（节选）：` 以上修改，表示 Redis 接受所有远程连接，并且端口修改成了 16379 `

问题：bind只设置监听地址；protected-mode、ACL和防火墙仍能拒绝远程连接。

建议修改：改为“监听所有IPv4接口，远程访问还受保护模式、ACL及防火墙控制”；第47行把IPv6明确为回环::1。

依据：[仓库源码：redis/redis · redis.conf](https://raw.githubusercontent.com/redis/redis/7.0/redis.conf)。

### A038

**SQLAlchemy入门**

原文：[software/database/SQLAlchemy入门/index.md](<C:/Project/blog/software/database/SQLAlchemy入门/index.md>)。

记录日期：2026-02-06T10:21:53；状态：草稿；正文已核阅；有修改意见。

#### R066

**字词/链接 · 字词 · P3**

定位：[原文第 20 行](<C:/Project/blog/software/database/SQLAlchemy入门/index.md:20>)；待改表述／主题：` 建立在Corn之上 `。

原文定位行（节选）：` ORM 则是用 Python 的面向对象和数据库进行映射的框架。这是一种针对领域对象建模的方式，通常用于后台系统建模。用户能以对象为核心进行增删改查，ORM 是建立在 Corn 之上的更高层面的抽象和封装。 `

问题：组件名误拼。

建议修改：改“建立在Core之上”。

依据：[docs.sqlalchemy.org · intro](https://docs.sqlalchemy.org/en/20/intro.html)。

### A039

**sqlite创建表**

原文：[software/database/sqlite/sqlite创建表/index.md](<C:/Project/blog/software/database/sqlite/sqlite创建表/index.md>)。

记录日期：2025-06-20T17:25:00+08:00；状态：正文已核阅；有修改意见。

#### R067

**事实/技术错误 · 事实 · P2**

定位：[原文第 67 行](<C:/Project/blog/software/database/sqlite/sqlite创建表/index.md:67>)；待改表述／主题：` PRIMARY KEY唯一且非空 `。

原文定位行（节选）：` - PRIMARY KEY：主键约束，唯一且非空 `

问题：普通rowid表的非INTEGER主键允许NULL是SQLite历史兼容行为；INTEGER PRIMARY KEY、STRICT、WITHOUT ROWID或显式NOT NULL除外。

建议修改：补充SQLite例外，不沿用其他数据库的笼统结论。

依据：[SQLite 官方文档 · lang_createtable](https://www.sqlite.org/lang_createtable.html)。

#### R068

**事实/技术错误 · 代码 · P2**

定位：[原文第 76 行](<C:/Project/blog/software/database/sqlite/sqlite创建表/index.md:76>)；待改表述／主题：` 薪水默认为0，年龄比0大 `。

原文定位行（节选）：`` 创建一个新表 `t_user`，主键是 id，用户姓名非空，年龄的值要比 0 大，email 值唯一，薪水默认为 0，创建时间默认为当前日期时间，用户地址为字符串。 ``

问题：实际DDL是DEFAULT1000.5、CHECK(age>=0)。

建议修改：文字与代码统一：薪水1000.5、年龄大于等于0；需要强制年龄存在还要NOT NULL。第116行DEFAUTL改DEFAULT。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R069

**事实/技术错误 · 事实 · P2**

定位：[原文第 112 行](<C:/Project/blog/software/database/sqlite/sqlite创建表/index.md:112>)；待改表述／主题：` 每新增…表…sqlite_sequence就多一条 `。

原文定位行（节选）：`` 每新增一个带有 AUTOINCREMENT 的表，`sqlite_sequence` 就会多一条记录，删除了带有 AUTOINCREMENT 的表，`sqlite_sequence` 对应的那一条记录也会自动被删除。 ``

问题：sqlite_sequence记录通常在首次插入数据时创建，不是CREATE TABLE就必有对应行。

建议修改：改为“首次插入该AUTOINCREMENT表的数据时创建该表的序列记录，后续按需要更新”。

依据：[SQLite 官方文档 · autoinc](https://sqlite.org/autoinc.html)。

### A040

**sqlite命令行下的命令解释**

原文：[software/database/sqlite/sqlite命令行下的命令解释/index.md](<C:/Project/blog/software/database/sqlite/sqlite命令行下的命令解释/index.md>)。

记录日期：2025-06-01T10:44:00+08:00；状态：草稿；正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A041

**sqlite的数据类型**

原文：[software/database/sqlite/sqlite的数据类型/index.md](<C:/Project/blog/software/database/sqlite/sqlite的数据类型/index.md>)。

记录日期：2025-06-02T11:05:00+08:00；状态：正文已核阅；有修改意见。

#### R070

**事实/技术错误 · 事实 · P2**

定位：[原文第 33 行](<C:/Project/blog/software/database/sqlite/sqlite的数据类型/index.md:33>)；待改表述／主题：` SQLite…长度没有任何限制 `。

原文定位行（节选）：` SQLite 对字符串、BLOB 或数值的长度没有施加任何限制，所以 varchar(50) 的 50 在 SQLite 中会被忽略。 `

问题：不执行varchar(n)长度不等于无长度上限；SQLITE_MAX_LENGTH默认10亿字节，还有运行时限制。

建议修改：改为“varchar(n)的n不强制，但字符串/BLOB仍受SQLITE_MAX_LENGTH等限制”；第31、61行补STRICT及类型亲和性转换的条件。

依据：[SQLite 官方文档 · limits](https://sqlite.org/limits.html)；[SQLite 官方文档 · datatype3](https://sqlite.org/datatype3.html)。

#### R071

**事实/技术错误 · 事实 · P2**

定位：[原文第 61 行](<C:/Project/blog/software/database/sqlite/sqlite的数据类型/index.md:61>)；待改表述／主题：` TEXT列…存储integer、real… `。

原文定位行（节选）：` 举个简单的例子：SQLite 的一列数据是可以存储不同类型的值的，这很灵活，一个定义为 TEXT 的列，存储 integer，real，blob 都可以。 `

问题：普通TEXT亲和性列会把数值转为文本，不能以该例说明原样保留各种存储类；BLOB通常不转。

建议修改：用无类型列或BLOB亲和性列演示不同存储类；用typeof()显示TEXT列数值转换结果。第26行intergere改integer。

依据：[SQLite 官方文档 · datatype3](https://sqlite.org/datatype3.html)。

### A042

**SQL中的各种连接**

原文：[software/database/SQL中的各种连接/index.md](<C:/Project/blog/software/database/SQL中的各种连接/index.md>)。

记录日期：2023-07-22T08:14:02+08:00；状态：正文已核阅；有修改意见。

#### R072

**条件/版本澄清 · 概念/适用条件 · P2**

定位：[原文第 213 行](<C:/Project/blog/software/database/SQL中的各种连接/index.md:213>)；待改表述／主题：` inner join类似集合交集 / union实现FULL `。

原文定位行（节选）：` 所以，inner join 就类似于数学集合中的交集，用文字简单的表述就是： `

问题：集合图可以作有限教学类比，但不能表达SQL连接的行配对和重复语义；用UNION去重也不能通用模拟FULL JOIN。

建议修改：补一对多反例；通用模拟用LEFT JOIN UNION ALL 加只保留未匹配左行的RIGHT JOIN。第30行公示改公式，第67行r1,m2改r1,m1。

依据：[PostgreSQL 官方文档 · queries-table-expressions](https://www.postgresql.org/docs/17/queries-table-expressions.html)。

#### R073

**事实/技术错误 · 事实 · P2**

定位：[原文第 320 行](<C:/Project/blog/software/database/SQL中的各种连接/index.md:320>)；待改表述／主题：` 结果集记录数量就是右表记录数量 `。

原文定位行（节选）：` 也就是说，结果集的记录数量就是右表的记录数量。 `

问题：左表有多个匹配行时，一条右表记录会展开为多行；只有每条右行最多匹配一个左行才相等。

建议修改：改为“保留所有右表行；若左表连接键唯一，本例结果行数等于右表行数”。

依据：[PostgreSQL 官方文档 · queries-table-expressions](https://www.postgresql.org/docs/17/queries-table-expressions.html)。

#### R074

**事实/技术错误 · 事实 · P2**

定位：[原文第 374 行](<C:/Project/blog/software/database/SQL中的各种连接/index.md:374>)；待改表述／主题：` outer join是full outer join简写 `。

原文定位行（节选）：` outer join 是 full outer join 的简写，它的全称是全外连接，是外连接中的一种。 `

问题：OUTER可省略，但FULL不能省略；outer join是外连接总称，单独OUTER JOIN不是通用FULL JOIN语法。

建议修改：节标题改FULL OUTER JOIN，写“可简写为FULL JOIN；LEFT/RIGHT JOIN也是外连接”。

依据：[PostgreSQL 官方文档 · queries-table-expressions](https://www.postgresql.org/docs/17/queries-table-expressions.html)。

### A043

**Docker挂代理**

原文：[software/docker/Docker挂代理/index.md](<C:/Project/blog/software/docker/Docker挂代理/index.md>)。

记录日期：2025-02-06T21:03:00+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A044

**Docker部署Nginx**

原文：[software/docker/Docker部署Nginx/index.md](<C:/Project/blog/software/docker/Docker部署Nginx/index.md>)。

记录日期：2023-04-30T20:01:32+08:00；状态：正文已核阅；有修改意见。

#### R075

**事实/技术错误 · 事实 · P1**

定位：[原文第 24 行](<C:/Project/blog/software/docker/Docker部署Nginx/index.md:24>)；待改表述／主题：` DOS攻击…基本没有任何作用 `。

原文定位行（节选）：` * 在稳定性方面，Nginx 采取了分阶段资源分配技术，使得 CPU 与内存的占用率非常低。Nginx 官方表示，Nginx 保持 1 万个没有活动的连接，而这些连接只占用 2.5MB 内存，因此，类似 DOS 这样的攻击对 Nginx 来说基本上是没有任何作用的。 `

问题：连接管理性能好不能推出免疫DoS；应用、连接、CPU、内存或带宽仍可耗尽。

建议修改：删去该结论；第23行删除固定5万最大并发，改为依赖资源/配置；“内核Poll模型”改“事件驱动，按平台采用epoll/kqueue等机制”。

依据：[NGINX 官方文档 · events](https://nginx.org/en/docs/events.html)；[NGINX 官方文档 · ngx_http_limit_req_module](https://nginx.org/en/docs/http/ngx_http_limit_req_module.html)。

#### R076

**事实/技术错误 · 代码 · P1**

定位：[原文第 328 行](<C:/Project/blog/software/docker/Docker部署Nginx/index.md:328>)；待改表述／主题：` proxy_pass http://192.168.10.103:8080/hello `。

原文定位行（节选）：` proxy_pass http://192.168.10.103:8080/hello `

问题：缺少指令结尾分号，Nginx配置测试失败。

建议修改：补分号；第125、167行容器静态目录统一为/usr/share/nginx/html；第353、355行192.169误写改192.168。

依据：[NGINX 官方文档 · beginners_guide](https://nginx.org/en/docs/beginners_guide.html)。

#### R077

**事实/技术错误 · 事实 · P2**

定位：[原文第 378 行](<C:/Project/blog/software/docker/Docker部署Nginx/index.md:378>)；待改表述／主题：` backend-api不能写back_api…URL不能下划线 `。

原文定位行（节选）：`` upstream 设置了一组服务器群，用于反向代理，注意，backend-api 不能写成 `back_api`，因为 URL 不能有下划线。 ``

问题：Nginx upstream组名可以带下划线；它不是要求解析的公网DNS主机名。

建议修改：删除该限制，说明upstream名称与proxy_pass引用必须一致；DNS主机名规范与upstream符号名分开解释。

依据：[NGINX 官方文档 · ngx_http_upstream_module](https://nginx.org/en/docs/http/ngx_http_upstream_module.html)。

#### R078

**事实/技术错误 · 时效 · P2**

定位：[原文第 417 行](<C:/Project/blog/software/docker/Docker部署Nginx/index.md:417>)；待改表述／主题：` url_hash / fair `。

原文定位行（节选）：`` | `url_hash` | 依据 URL 分配方式，按照访问的 URL 的 hash 结果来分配请求，使每个 URL 定向到同一个后端服务器 | ``

问题：url_hash不是当前原生指令；fair通常属于第三方模块，不能列成开箱即用默认策略。

建议修改：URL哈希写为hash $request_uri [consistent]；fair注明依赖第三方模块和构建支持；ip_hash只提供亲和性，不能独自保证session一致性。

依据：[NGINX 官方文档 · ngx_http_upstream_module](https://nginx.org/en/docs/http/ngx_http_upstream_module.html)。

### A045

**Docker部署SpringBoot应用**

原文：[software/docker/Docker部署SpringBoot应用/index.md](<C:/Project/blog/software/docker/Docker部署SpringBoot应用/index.md>)。

记录日期：2023-04-30T16:29:10+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A046

**Docker部署一个Gunicorn+Flask应用**

原文：[software/docker/Docker部署一个Gunicorn+Flask应用/index.md](<C:/Project/blog/software/docker/Docker部署一个Gunicorn+Flask应用/index.md>)。

记录日期：2023-05-02T10:26:48+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A047

**Elasticsearch的基本概念**

原文：[software/elk/Elasticsearch的基本概念/index.md](<C:/Project/blog/software/elk/Elasticsearch的基本概念/index.md>)。

记录日期：2026-03-04T09:48:44；状态：草稿；正文已核阅；有修改意见。

#### R079

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 69 行](<C:/Project/blog/software/elk/Elasticsearch的基本概念/index.md:69>)；待改表述／主题：` LIKE %数据库%意味着全表扫描 / 关系型数据库…做不到分词评分 `。

原文定位行（节选）：`` 比如博客站点的搜索，用户输入“数据库”，目的是为了查看哪些博客提到了“数据库”，如果是传统的关系型数据库，用 `LIKE %数据库%` 这种模糊匹配来实现，就意味着全表扫描，检索时间随着博客数量增大而增大。 ``

问题：普通BTree通常无法有效支持前导通配符，但PG pg_trgm GIN/GiST可支持；PG全文搜索、MySQL FULLTEXT均有分词/评分能力。

建议修改：限定为“只用普通BTree及LIKE的方案”，补数据库原生全文搜索和专用索引，避免把RDBMS功能描述为不可能。

依据：[PostgreSQL 官方文档 · pgtrgm](https://www.postgresql.org/docs/17/pgtrgm.html)；[PostgreSQL 官方文档 · textsearch](https://www.postgresql.org/docs/17/textsearch.html)。

#### R080

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 187 行](<C:/Project/blog/software/elk/Elasticsearch的基本概念/index.md:187>)；待改表述／主题：` text类型不支持精确查询 `。

原文定位行（节选）：` text 类型的数据会经过分词器（analyzer）分词，然后建立倒排索引。它不支持精确查询，常用于索引非结构化文本字段，例如电子邮件的正文或产品描述。 `

问题：term查询可对text的索引词项作精确匹配，只是通常不是原字符串精确匹配；原串应使用keyword多字段。

建议修改：改为“不适合对原始整段字符串作等值匹配；term针对分析后的词项”。第63行“再插入”改“在插入”。

依据：[Elastic 官方文档 · query-dsl-term-query](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/query-dsl-term-query.html)。

### A048

**elk的搭建**

原文：[software/elk/elk的搭建/index.md](<C:/Project/blog/software/elk/elk的搭建/index.md>)。

记录日期：2026-03-03T11:53:40；状态：正文已核阅；有修改意见。

#### R081

**事实/技术错误 · 代码 · P2**

定位：[原文第 114 行](<C:/Project/blog/software/elk/elk的搭建/index.md:114>)；待改表述／主题：` 关闭安全配置，后文仍用HTTPS及密码 `。

原文定位行（节选）：` 如果仅仅是测试，可以改成简化为单机模式，并且关闭安全配置： `

问题：单机无安全配置与后续带TLS/认证的Kibana和curl步骤属于两条不同流程，不能直接顺序执行。

建议修改：拆为保留安全和本地无安全两个互斥方案，各自给完整elasticsearch.yml、kibana.yml和验证URL；-k仅跳过证书验证，不是服务端不用证书。

依据：[Elastic 官方文档 · configuring-stack-security](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/configuring-stack-security.html)。

### A049

**filebeat收集python日志**

原文：[software/elk/filebeat收集python日志/index.md](<C:/Project/blog/software/elk/filebeat收集python日志/index.md>)。

记录日期：2026-03-27T11:58:59；状态：正文已核阅；有修改意见。

#### R082

**事实/技术错误 · 时效 · P2**

定位：[原文第 37 行](<C:/Project/blog/software/elk/filebeat收集python日志/index.md:37>)；待改表述／主题：` 旧版本7.x之前…log类型 `。

原文定位行（节选）：` 但文本聚焦于磁盘日志文件的读取，因此这里仅介绍 filestream 类型的 input（旧版本 7.x 之前，用的是 log 类型，filestream 是对旧版 log 类型的重构，性能更好，且解决了旧版中一些顽固的 inode 重用等问题）。 `

问题：log输入在7.16弃用，9.0默认禁用；不能把迁移界线写为7.x之前。

建议修改：改为“filestream为推荐输入；log自7.16弃用、9.0默认禁用”。第15行底下改低下、介绍如果改介绍如何，第37行文本改本文，第88行之需要改只需要。

依据：[Elastic 官方文档 · filebeat-input-log](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-log)。

### A050

**filebeat的使用**

原文：[software/elk/filebeat的使用/index.md](<C:/Project/blog/software/elk/filebeat的使用/index.md>)。

记录日期：2026-03-08T14:16:52；状态：草稿；正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A051

**QueryDSL基础**

原文：[software/elk/QueryDSL基础/index.md](<C:/Project/blog/software/elk/QueryDSL基础/index.md>)。

记录日期：2026-04-04T19:37:08；状态：草稿；正文已核阅；有修改意见。

#### R083

**事实/技术错误 · 事实 · P2**

定位：[原文第 141 行](<C:/Project/blog/software/elk/QueryDSL基础/index.md:141>)；待改表述／主题：` Filter就是精确匹配 `。

原文定位行（节选）：` Filter 就是精确匹配，找出匹配查询子句的文档，当我们仅仅需要精确的匹配文档，而不需要影响文档相关性的时候，就使用 Filter Context，往往在高度结构化的文档集合中使用的更多： `

问题：filter context决定是否计算_score，不限定只能等值匹配，range/geo/match也可放filter。

建议修改：改为“filter只判断是否匹配，不计算相关性分数”；第251行exists是找有索引值的文档，无值应must_not exists；第260行LIKE %search改LIKE 'search%'。

依据：[Elastic 官方文档 · query-filter-context](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/query-filter-context.html)；[Elastic 官方文档 · query-dsl-exists-query](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/query-dsl-exists-query.html)。

### A052

**IEEE 754标准以及0.1加0.2不等于0.3的问题**

原文：[software/fundamentals/IEEE 754标准以及0.1加0.2不等于0.3的问题/index.md](<C:/Project/blog/software/fundamentals/IEEE 754标准以及0.1加0.2不等于0.3的问题/index.md>)。

记录日期：2024-06-17T13:56:39+08:00；状态：草稿；正文已核阅；有修改意见。

#### R084

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 141 行](<C:/Project/blog/software/fundamentals/IEEE 754标准以及0.1加0.2不等于0.3的问题/index.md:141>)；待改表述／主题：` M 和 E 分别是实际存储的 exp 和 frac `。

原文定位行（节选）：` 这里的 M、E 和 exp、frac 不可混淆，M 和 E 会通过某种规则，转换成一串 0 和 1 分别存入 exp 和 frac 的字段中。 `

问题：尾数和指数的对应关系写反。

建议修改：改为：E 对应 exp 字段，M 的有效数字部分对应 frac 字段（并说明正规数的隐含首位）。

依据：[Oracle／Java 官方文档 · ncg_math](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_math.html)。

### A053

**数据存储度量单位差异**

原文：[software/fundamentals/数据存储度量单位差异/index.md](<C:/Project/blog/software/fundamentals/数据存储度量单位差异/index.md>)。

记录日期：2024-06-13T20:11:39+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A054

**时间与计算机**

原文：[software/fundamentals/时间与计算机/index.md](<C:/Project/blog/software/fundamentals/时间与计算机/index.md>)。

记录日期：2021-11-27T10:58:15+08:00；状态：正文已核阅；有修改意见。

#### R085

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 60 行](<C:/Project/blog/software/fundamentals/时间与计算机/index.md:60>)；待改表述／主题：` 手动调整原子钟，使得误差不至于超过一秒 `。

原文定位行（节选）：` 时间也是如此，为了兼顾基于天文测量的世界时，人类会持续观测世界时与这个新时钟的差距，也就是建立一条新的标准，不断纠正，原子时和世界时的误差。简单的说就是，如果地球转速变慢或者变快了，就让原子钟加一秒或者减一秒，这个一秒就是“闰秒”，当世界时和原子时差了 0.9 秒，人们就会手动调整原子钟的时间。 `

问题：闰秒调整的是 UTC 与 TAI 的整数秒差，不是让原子钟改变走速。约束的是 UT1 与 UTC。

建议修改：改为：通过在 UTC 中引入闰秒，使 |UT1−UTC| 小于 0.9 秒；TAI 连续计时。

依据：[www.iers.org · IERS_Leap_Seconds.pdf](https://www.iers.org/SharedDocs/Publikationen/EN/IERS/Documents/IERS_Leap_Seconds.pdf?__blob=publicationFile&v=1)。

#### R086

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 94 行](<C:/Project/blog/software/fundamentals/时间与计算机/index.md:94>)；待改表述／主题：` 2038 年问题 `。

原文定位行（节选）：` Unix 时间戳是从 1970 年 1 月 1 日（UTC/GMT 的午夜）开始所经过的秒数，不考虑闰秒。系统用的是 32 位有符号整型存储，所以最大是 2147483647 秒，也就是格林尼治时间 2038 年 1 月 19 日凌晨 03:14:07 就会溢出，变成了第 -2147483648 秒（代表格林尼治时间 1901 年 12 月 13 日 20:45:52）。 `

问题：该问题针对以有符号 32 位整数计秒的时间表示，不能泛化到所有计算机。

建议修改：明确 time_t/存储格式的位宽；64 位时间表示不受这个同一边界限制。

依据：[Linux／工具手册 · time_t.3type](https://man7.org/linux/man-pages/man3/time_t.3type.html)。

#### R087

**字词/链接 · 字词错误 · P3**

定位：[原文第 279 行](<C:/Project/blog/software/fundamentals/时间与计算机/index.md:279>)；待改表述／主题：` 预兆公历；ISO_lOCAL_DATE；地球自传 `。

原文定位行（节选）：`` 在 `DateTimeFormatter` 中，内置了一些常量，比如 `BASIC_ISO_DATE`，`ISO_lOCAL_DATE`，`ISO_LOCAL_DATE_TIME`，`ISO_TIME` 等等，不过我更倾向于 `ofPattern`，能够直接看到格式。 ``

问题：术语及字母大小写错误（另见 L56、L279）。

建议修改：分别改为“前推公历”“ISO_LOCAL_DATE”“地球自转”。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A055

**聊聊Unicode、UTF-8、UTF-16以及UTF-32的那些事儿**

原文：[software/fundamentals/聊聊Unicode、UTF-8、UTF-16以及UTF-32的那些事儿/index.md](<C:/Project/blog/software/fundamentals/聊聊Unicode、UTF-8、UTF-16以及UTF-32的那些事儿/index.md>)。

记录日期：2022-08-21T21:04:42+08:00；状态：正文已核阅；有修改意见。

#### R088

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 94 行](<C:/Project/blog/software/fundamentals/聊聊Unicode、UTF-8、UTF-16以及UTF-32的那些事儿/index.md:94>)；待改表述／主题：` Unicode 没有规定这些字节该如何存储 `。

原文定位行（节选）：` 通俗的来说，Unicode 是一种标准，规定了每个字符对应的数字，但是没有规定数字存储在具体的计算机系统中排列的顺序，占据多少个字节，所以 UTF（Unicode 转换格式，Unicode Transformation Format），也就是 Unicode 的**具体实现**应运而生了。 `

问题：Unicode 标准包含 UTF-8、UTF-16、UTF-32 的编码定义。

建议修改：改为：码点是抽象编号；具体字节表示由 UTF 编码形式和编码方案确定。

依据：[Unicode 标准 · chapter-3](https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-3/)。

#### R089

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 126 行](<C:/Project/blog/software/fundamentals/聊聊Unicode、UTF-8、UTF-16以及UTF-32的那些事儿/index.md:126>)；待改表述／主题：` 0x00000000 到 0x7FFFFFFF `。

原文定位行（节选）：`` 实际上 UTF-32 的最高位（符号位）不使用，为 0，所以每一个字符由 `0` 到十六进制的 `7FFFFFFF` 的 31 位数值表示。 ``

问题：把历史 UCS-4 的 31 位空间误当成现代 UTF-32 的有效值。

建议修改：UTF-32 编码 Unicode 标量值：U+0000～U+10FFFF，排除 U+D800～U+DFFF；同步修改 L132。

依据：[Unicode 标准 · chapter-3](https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-3/)。

#### R090

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 206 行](<C:/Project/blog/software/fundamentals/聊聊Unicode、UTF-8、UTF-16以及UTF-32的那些事儿/index.md:206>)；待改表述／主题：` BMP 中的字符 `。

原文定位行（节选）：`` 1. 用 2 个字节（即 16 比特长的单个码元）表示处于 `U+0000~U+FFFF` 范围的字符。 ``

问题：BMP 包含代理码点，不能全部当成可单独编码的字符。

建议修改：单个 UTF-16 码元对应 BMP 中除代理区以外的标量值；L280 的 UTF-8 BMP 说明也排除代理区。

依据：[Unicode 标准 · chapter-3](https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-3/)。

#### R091

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 290 行](<C:/Project/blog/software/fundamentals/聊聊Unicode、UTF-8、UTF-16以及UTF-32的那些事儿/index.md:290>)；待改表述／主题：` 110xxxxx；11110xxx `。

原文定位行（节选）：` | 000080 - 0007FF 共 1920 个代码 | 00000000 00000yyy yyzzzzzz | 110yyyyy（C0-DF） 10zzzzzz（80-BF） | 第一个字节由 110 开始，接着的字节由 10 开始 | `

问题：合法 UTF-8 首字节范围不是 C0～DF、F0～F7；必须排除过长编码、代理值、超过 U+10FFFF 的编码。

建议修改：290～292行表格应给出现代UTF-8合法首字节范围C2～DF、E0～EF、F0～F4，并补E0/ED/F0/F4后续字节限制；现表C0～DF、F0～F7会包含非法编码。

依据：[RFC 3629](https://www.rfc-editor.org/rfc/rfc3629.html)。

#### R092

**字词/链接 · 字词错误 · P3**

定位：[原文第 345 行](<C:/Project/blog/software/fundamentals/聊聊Unicode、UTF-8、UTF-16以及UTF-32的那些事儿/index.md:345>)；待改表述／主题：` UTF-16；不在；小段 `。

原文定位行（节选）：` *示例四，汉字“𪜾”使用 UTF-16 表示：* `

问题：对应小节讲 UTF-8；另有“不再”“小端”的错字（L373、L383）。

建议修改：标题改为 UTF-8；“不在”改“不再”；“小段”改“小端”。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A056

**逻辑帧和渲染帧**

原文：[software/game/逻辑帧和渲染帧/index.md](<C:/Project/blog/software/game/逻辑帧和渲染帧/index.md>)。

记录日期：2026-08-03T10:50:39；状态：正文已核阅；有修改意见。

#### R093

**事实/技术错误 · 概念混淆 · P2**

定位：[原文第 21 行](<C:/Project/blog/software/game/逻辑帧和渲染帧/index.md:21>)；待改表述／主题：` 渲染帧 `。

原文定位行（节选）：` 渲染帧则与 GPU 和显示器有关，显示器是按照一定的帧率，把渲染帧一帧帧绘制到电脑屏幕上，一般的帧率有 60HZ，120HZ，144HZ 等等，以 60HZ 为例，意味着 1 秒内刷新了 60 次画面，也就是约 16 毫秒刷新一帧画面。 `

问题：程序渲染帧率 FPS 与显示器刷新率 Hz 不等同。

建议修改：区分帧率与刷新率，并说明垂直同步、丢帧及重复显示的情况。

依据：[docs.unity3d.com · TimeFrameManagement](https://docs.unity3d.com/Manual/TimeFrameManagement.html)。

#### R094

**条件/版本澄清 · 算法适用条件 · P2**

定位：[原文第 61 行](<C:/Project/blog/software/game/逻辑帧和渲染帧/index.md:61>)；待改表述／主题：` State2 `。

原文定位行（节选）：` 一上面的时间线为例，Render2 可以插值，渲染出游戏单位运动到（1.5，1）的位置，这样看起来就不是跳过去，而是平滑的移动过去了。 `

问题：两个已知状态之间的插值需要已经计算出后一状态；当前时间领先于最新逻辑状态时不能直接获得未来状态。

建议修改：说明插值需要两个已知的逻辑状态，常见做法是渲染落后一个逻辑步；若按图在16ms时预测33ms未来位置，应称外推并说明预测前提。61行“一上面的”改“以上面的”。

依据：[docs.unity3d.com · TimeFrameManagement](https://docs.unity3d.com/Manual/TimeFrameManagement.html)。

### A057

**GTK4在Linux和Windows下的HelloWorld**

原文：[software/gtk/GTK4在Linux和Windows下的HelloWorld/index.md](<C:/Project/blog/software/gtk/GTK4在Linux和Windows下的HelloWorld/index.md>)。

记录日期：2025-04-13T09:01:00+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A058

**Beszel的搭建和告警配置**

原文：[software/linux/Beszel的搭建和告警配置/index.md](<C:/Project/blog/software/linux/Beszel的搭建和告警配置/index.md>)。

记录日期：2026-02-27T14:02:51；状态：正文已核阅；有修改意见。

#### R095

**字词/链接 · 字词错误 · P3**

定位：[原文第 52 行](<C:/Project/blog/software/linux/Beszel的搭建和告警配置/index.md:52>)；待改表述／主题：` setttings `。

原文定位行（节选）：` 把自己开通的 SMTP 服务器的地址，端口，用户名和密钥填写在 Mail setttings 中： `

问题：单词多写了一个 t。

建议修改：改为 settings。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A059

**CentOS+Hugo建站不完全指北**

原文：[software/linux/CentOS+Hugo建站不完全指北/index.md](<C:/Project/blog/software/linux/CentOS+Hugo建站不完全指北/index.md>)。

记录日期：2021-05-08T16:33:58+08:00；状态：草稿；正文已核阅；有修改意见。

#### R096

**事实/技术错误 · 版本时效 · P2**

定位：[原文第 4 行](<C:/Project/blog/software/linux/CentOS+Hugo建站不完全指北/index.md:4>)；待改表述／主题：` CentOS7 `。

原文定位行（节选）：` summary: "CentOS7+Hugo+Nginx 搭建网站" `

问题：该历史环境教程可以保留，但 CentOS7 已结束支持，当前下载源路径和新部署建议需注明。

建议修改：在本篇及 ID60、94 的 CentOS7 内容加历史版本说明；旧镜像按 CentOS Vault 归档获取。

依据：[www.centos.org · centos-linux-eol](https://www.centos.org/centos-linux-eol/)。

#### R097

**字词/链接 · 字词错误 · P3**

定位：[原文第 222 行](<C:/Project/blog/software/linux/CentOS+Hugo建站不完全指北/index.md:222>)；待改表述／主题：` GitHub Page `。

原文定位行（节选）：` 如果没有云服务器的同学，可以使用 GitHub Page + Hugo 的解决方案，就是把 public 文件夹托管到 GitHub 上。网上有很多教程，这里不再赘述。 `

问题：产品名称应为 GitHub Pages。

建议修改：改为 GitHub Pages。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A060

**CentOS防火墙的一些操作**

原文：[software/linux/CentOS防火墙的一些操作/index.md](<C:/Project/blog/software/linux/CentOS防火墙的一些操作/index.md>)。

记录日期：2021-05-07T16:23:29+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A061

**Cron在Linux中的用法**

原文：[software/linux/Cron在Linux中的用法/index.md](<C:/Project/blog/software/linux/Cron在Linux中的用法/index.md>)。

记录日期：2023-06-23T09:38:40+08:00；状态：正文已核阅；有修改意见。

#### R098

**事实/技术错误 · 命令错误 · P2**

定位：[原文第 86 行](<C:/Project/blog/software/linux/Cron在Linux中的用法/index.md:86>)；待改表述／主题：` 0 0 1 1 ?及其后的例子 `。

原文定位行（节选）：` | 0 0 1 1 ? | 1 月 1 日的 0 时 0 分 | `

问题：86～89行是五字段示例，但使用了Linux crontab不支持的?；99行另夹入六时间字段的Quartz示例。

建议修改：Linux例子改为0 0 1 1 *、59 6 15 5 *、30 15 * 9 0、30 19 * 12 6；99行的六时间字段示例移到Quartz小节。

依据：[Linux／工具手册 · crontab.5](https://www.man7.org/linux/man-pages/man5/crontab.5.html)。

#### R099

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 99 行](<C:/Project/blog/software/linux/Cron在Linux中的用法/index.md:99>)；待改表述／主题：` ?、L、W、#的语法表 `。

原文定位行（节选）：`` - `?` 表示不指定值。使用的场景为不需要关心当前设置这个字段的值。例如：要在每月的 8 号触发一个操作，但不关心是周几，我们可以这么设置 `0 0 0 8 * ?` ``

问题：把 Quartz Cron 与 Linux crontab 混在同一语法表中。

建议修改：将Linux五时间字段与Quartz六/七字段分开；Linux章节保留逗号、范围、星号和步长语法，Quartz专用符号另起小节。Linux星期通常支持0和7都表示周日；Quartz星期编号不同。

依据：[Linux／工具手册 · crontab.5](https://www.man7.org/linux/man-pages/man5/crontab.5.html)；[www.quartz-scheduler.org · crontrigger](https://www.quartz-scheduler.org/documentation/quartz-2.3.0/tutorials/crontrigger.html)。

#### R100

**事实/技术错误 · 命令错误 · P2**

定位：[原文第 111 行](<C:/Project/blog/software/linux/Cron在Linux中的用法/index.md:111>)；待改表述／主题：` crontab -u `。

原文定位行（节选）：` - crontab -u [用户名]：编辑任何其他用户的 crontab 文件 `

问题：-u 指定用户，不是编辑操作本身；-i 通常配合删除确认。

建议修改：编辑写 crontab -u 用户名 -e（需相应权限）；交互删除写 crontab -i -r。

依据：[Linux／工具手册 · crontab.1](https://man7.org/linux/man-pages/man1/crontab.1.html)。

### A062

**Debian12安装jdk21**

原文：[software/linux/Debian/Debian12安装jdk21/index.md](<C:/Project/blog/software/linux/Debian/Debian12安装jdk21/index.md>)。

记录日期：2024-10-20T10:09:00+08:00；状态：正文已核阅；有修改意见。

#### R101

**事实/技术错误 · 命令错误 · P2**

定位：[原文第 61 行](<C:/Project/blog/software/linux/Debian/Debian12安装jdk21/index.md:61>)；待改表述／主题：` PATH="$PATH:$JAVA_HOME/bin" `。

原文定位行（节选）：` export PATH="$PATH:$JAVA_HOME/bin" `

问题：追加到 PATH 后部会继续优先匹配旧 Java，不能保证切换至 JDK21。

建议修改：改为 PATH="$JAVA_HOME/bin:$PATH"，或使用 update-alternatives；用 command -v java、java -version 验证。

依据：[GNU 官方手册 · Command-Search-and-Execution](https://www.gnu.org/software/bash/manual/html_node/Command-Search-and-Execution.html)。

### A063

**Debian12安装MongoDB**

原文：[software/linux/Debian/Debian12安装MongoDB/index.md](<C:/Project/blog/software/linux/Debian/Debian12安装MongoDB/index.md>)。

记录日期：2025-02-15T08:58:00+08:00；状态：正文已核阅；有修改意见。

#### R102

**字词/链接 · 字词错误 · P3**

定位：[原文第 68 行](<C:/Project/blog/software/linux/Debian/Debian12安装MongoDB/index.md:68>)；待改表述／主题：` aux `。

原文定位行（节选）：` 1. 在 win 系统上的 VirtualBox 可能没有开启 aux 指令集，导致 mongodb 无法启动，需要关闭 hyper-v，然后把设置中，处理器的特性都勾上。 `

问题：MongoDB CPU 要求中的指令集拼错。

建议修改：改为 AVX；MongoDB 5.0 及以后 x86_64 的硬件要求按官方文档列明。

依据：[www.mongodb.com · production-notes](https://www.mongodb.com/docs/v7.0/administration/production-notes/)。

### A064

**Debian12安装PostgreSQL**

原文：[software/linux/Debian/Debian12安装PostgreSQL/index.md](<C:/Project/blog/software/linux/Debian/Debian12安装PostgreSQL/index.md>)。

记录日期：2024-11-10T09:04:00+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A065

**Debian12安装Prometheus和Grafana**

原文：[software/linux/Debian/Debian12安装Prometheus和Grafana/index.md](<C:/Project/blog/software/linux/Debian/Debian12安装Prometheus和Grafana/index.md>)。

记录日期：2024-10-13T09:02:55+08:00；状态：正文已核阅；有修改意见。

#### R103

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 34 行](<C:/Project/blog/software/linux/Debian/Debian12安装Prometheus和Grafana/index.md:34>)；待改表述／主题：` Loki `。

原文定位行（节选）：` ELK 主要是日志收集和分析，类似的是 Prometheus 生态下的 Loki。 `

问题：Loki 属于 Grafana 生态的日志系统，并非 Prometheus 项目的日志组件。

建议修改：改为：Prometheus 负责指标；Grafana Loki 负责日志，Grafana 可查询两者。

依据：[Grafana 官方文档 · overview](https://grafana.com/docs/loki/latest/get-started/overview/)。

#### R104

**事实/技术错误 · 配置错误 · P1**

定位：[原文第 174 行](<C:/Project/blog/software/linux/Debian/Debian12安装Prometheus和Grafana/index.md:174>)；待改表述／主题：` root_url包含Grafana内部端口 `。

原文定位行（节选）：` root_url = %(protocol)s://%(domain)s:%(http_port)s/你自己设置的nginx代理路径/ `

问题：示例公开地址是http://example.com/monitor/，但root_url使用内部http_port（通常3000），且未展示domain设置，可能生成错误链接和跳转。

建议修改：直接设置root_url=http://example.com/monitor/，或正确配置公开domain/协议/端口；HTTPS终止时按公开HTTPS URL设置。

依据：[Grafana 官方文档 · run-grafana-behind-a-proxy](https://grafana.com/tutorials/run-grafana-behind-a-proxy/)。

#### R105

**事实/技术错误 · 代码错误 · P1**

定位：[原文第 335 行](<C:/Project/blog/software/linux/Debian/Debian12安装Prometheus和Grafana/index.md:335>)；待改表述／主题：` f.write(b"\0" * target_disk) `。

原文定位行（节选）：` f.write(b"\0" * target_disk) `

问题：先在内存中分配相当于目标磁盘大小的字节串，可能在写盘之前就MemoryError；目标文件大小也没有扣除已用磁盘空间。

建议修改：分块写入固定大小缓冲区，按已用/可用空间计算需要增加的量，并用try/finally清理测试文件。

依据：[Python 官方文档 · stdtypes · bytes](https://docs.python.org/3/library/stdtypes.html#bytes)；[Python 官方文档 · shutil · shutil.disk_usage](https://docs.python.org/3/library/shutil.html#shutil.disk_usage)。

### A066

**Debian12安装Redis**

原文：[software/linux/Debian/Debian12安装Redis/index.md](<C:/Project/blog/software/linux/Debian/Debian12安装Redis/index.md>)。

记录日期：2024-11-17T16:25:48+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A067

**VirtualBox创建Debian12虚拟机**

原文：[software/linux/Debian/VirtualBox创建Debian12虚拟机/index.md](<C:/Project/blog/software/linux/Debian/VirtualBox创建Debian12虚拟机/index.md>)。

记录日期：2024-11-16T09:07:50+08:00；状态：正文已核阅；有修改意见。

#### R106

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 287 行](<C:/Project/blog/software/linux/Debian/VirtualBox创建Debian12虚拟机/index.md:287>)；待改表述／主题：` sudo `。

原文定位行（节选）：` Debian 12 默认是没有 sudo 命令，需要自己安装，所以在一开始的时候，如果用普通用户登陆，我们想要执行一些命令没法使用 sudo。 `

问题：Debian 安装时是否创建 root 密码影响 sudo 的默认安装和首个用户授权。

建议修改：明确：未设置 root 密码时通常安装 sudo 并授权首个用户；已设置 root 密码时，可能需要 su 后手动安装配置。

依据：[wiki.debian.org · sudo](https://wiki.debian.org/sudo)。

#### R107

**条件/版本澄清 · 版本条件 · P2**

定位：[原文第 342 行](<C:/Project/blog/software/linux/Debian/VirtualBox创建Debian12虚拟机/index.md:342>)；待改表述／主题：` netselect-apt -sn `。

原文定位行（节选）：`` 然后执行命令：`netselect-apt -sn` ``

问题：不指定发行版默认跟随 stable，会在 stable 变更后生成其他发行版的源；-n 表示包含 non-free。

建议修改：Debian12 教程显式指定 bookworm，例如 netselect-apt -s -n bookworm，并核对生成的 sources.list。

依据：[Debian 工具手册 · netselect-apt.1.en](https://manpages.debian.org/trixie/netselect-apt/netselect-apt.1.en.html)。

#### R108

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 422 行](<C:/Project/blog/software/linux/Debian/VirtualBox创建Debian12虚拟机/index.md:422>)；待改表述／主题：` ping `。

原文定位行（节选）：` 设置静态 IP 要注意，选择的这个 IP 没有被其他局域网设备使用过，可以通过 ping、IP neigh，nmap 等命令确认。 `

问题：ping 无响应不证明地址无人使用，设备可能离线或禁用 ICMP。

建议修改：静态地址应在 DHCP 池外并由网络管理者保留；可辅助做 ARP 冲突探测，但不把扫描结果当成永久无冲突保证。

依据：[RFC 5227](https://www.rfc-editor.org/rfc/rfc5227.html)。

### A068

**df和du详解**

原文：[software/linux/df和du详解/index.md](<C:/Project/blog/software/linux/df和du详解/index.md>)。

记录日期：2024-06-18T11:00:51+08:00；状态：正文已核阅；有修改意见。

#### R109

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 86 行](<C:/Project/blog/software/linux/df和du详解/index.md:86>)；待改表述／主题：` 默认 `。

原文定位行（节选）：`` -d 参数（`--max-depth`）很有用，可以指定最大的层级数目（-d N，表示列出小于等于 N 层的文件或目录），不指定该参数 du 默认是会展示所有层级的文件。 ``

问题：du 默认报告目录累计大小，不逐个列出普通文件。

建议修改：逐个显示文件需 du -a；只要目录汇总用默认选项，单个总计可用 du -s。

依据：[GNU 官方手册 · du-invocation](https://www.gnu.org/software/coreutils/manual/html_node/du-invocation.html)。

#### R110

**字词/链接 · 字词错误 · P3**

定位：[原文第 94 行](<C:/Project/blog/software/linux/df和du详解/index.md:94>)；待改表述／主题：` 文档系统 `。

原文定位行（节选）：` df 显示有关已挂载文档系统的信息，du 专注于这些文档系统中的单个文档和目录。 `

问题：名词写错。

建议修改：改为文件系统。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A069

**DroidCam下载和使用**

原文：[software/linux/DroidCam下载和使用/index.md](<C:/Project/blog/software/linux/DroidCam下载和使用/index.md>)。

记录日期：2026-01-28T23:13:25；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A070

**FHS文件系统规范**

原文：[software/linux/FHS文件系统规范/index.md](<C:/Project/blog/software/linux/FHS文件系统规范/index.md>)。

记录日期：2025-02-01T15:36:00+08:00；状态：草稿；空提纲／参考资料；无实质技术正文。

只有提纲、前言标题或参考链接，缺少可核实的技术正文。本轮不把这种空提纲计作内容正确的技术文章。

### A071

**frp服务的使用**

原文：[software/linux/frp服务的使用/index.md](<C:/Project/blog/software/linux/frp服务的使用/index.md>)。

记录日期：2025-07-19T14:03:00+08:00；状态：正文已核阅；有修改意见。

#### R111

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 15 行](<C:/Project/blog/software/linux/frp服务的使用/index.md:15>)；待改表述／主题：` 与互联网隔绝 `。

原文定位行（节选）：` 在内网环境下，主机都是与互联网隔绝的，如果我们想要在公网访问一个内网的设备，其中一个办法就是使用内网穿透技术，它解决了家庭宽带、企业局域网等环境下无法从外部直接访问内部服务的问题。 `

问题：内网地址不等于没有互联网连接；frpc 通常依赖能主动连接公网 frps。

建议修改：改为：位于 NAT/防火墙后，公网无法直接发起到该主机的连接，但主机可向公网建立出站连接。

依据：[gofrp.org · overview](https://gofrp.org/en/docs/overview/)。

### A072

**Linux中与查找相关的命令**

原文：[software/linux/Linux中与查找相关的命令/index.md](<C:/Project/blog/software/linux/Linux中与查找相关的命令/index.md>)。

记录日期：2024-06-19T09:00:51+08:00；状态：正文已核阅；有修改意见。

#### R112

**字词/链接 · 字词错误 · P3**

定位：[原文第 154 行](<C:/Project/blog/software/linux/Linux中与查找相关的命令/index.md:154>)；待改表述／主题：` /user/bin；-empy `。

原文定位行（节选）：` * -empy 表示空文件/目录，例如找到空文件：find /etc -type f -empty，找到空目录：find /etc -type d -empty `

问题：目录和 find 选项拼错（另见 L154）。

建议修改：改为 /usr/bin 和 -empty。

依据：[GNU 官方手册 · find](https://www.gnu.org/software/findutils/manual/html_mono/find.html)。

#### R113

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 211 行](<C:/Project/blog/software/linux/Linux中与查找相关的命令/index.md:211>)；待改表述／主题：` 一次 `。

原文定位行（节选）：` find 的 -exec 的终止符有两个，分号和加号，其中分号会使得每一个 find 到的文件去执行一次 -exec 后跟的命令。而加号则会让 find 到的文件一次性执行完 -exec 后跟的命令。 `

问题：find -exec … + 会在命令行长度限制内分批执行，不保证所有结果只调用一次。

建议修改：改为：尽量将多个结果合并为一批，必要时执行多批。

依据：[GNU 官方手册 · Multiple-Files](https://www.gnu.org/software/findutils/manual/html_node/find_html/Multiple-Files.html)。

### A073

**Linux之间使用scp命令传输文件**

原文：[software/linux/Linux之间使用scp命令传输文件/index.md](<C:/Project/blog/software/linux/Linux之间使用scp命令传输文件/index.md>)。

记录日期：2023-05-07T11:33:54+08:00；状态：正文已核阅；有修改意见。

#### R114

**字词/链接 · 字词错误 · P3**

定位：[原文第 105 行](<C:/Project/blog/software/linux/Linux之间使用scp命令传输文件/index.md:105>)；待改表述／主题：` 198.168 `。

原文定位行（节选）：` scp -P 22222 -r test/ ubuntu@198.168.10.107:/home/ubuntu `

问题：前后示例是 192.168 私网网段，此处地址误写。

建议修改：改为与示例一致的 192.168，并修正语法框中的缺失右括号。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A074

**Linux命令行设置代理**

原文：[software/linux/Linux命令行设置代理/index.md](<C:/Project/blog/software/linux/Linux命令行设置代理/index.md>)。

记录日期：2025-09-11T17:58:00+08:00；状态：正文已核阅；有修改意见。

#### R115

**字词/链接 · 链接错误 · P3**

定位：[原文第 9 行](<C:/Project/blog/software/linux/Linux命令行设置代理/index.md:9>)；待改表述／主题：` http://127 `。

原文定位行（节选）：` 假设你的代理是 [http://127.0.0.1:17890，可以在当前终端里执行](http://127.0.0.1:17890，可以在当前终端里执行)： `

问题：Markdown 链接目标包含了中文正文，无法按意图打开。

建议修改：将中文解释移到链接括号外；目标只保留代理 URL。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A075

**Linux的grep命令展示匹配项的前后n行信息**

原文：[software/linux/Linux的grep命令展示匹配项的前后n行信息/index.md](<C:/Project/blog/software/linux/Linux的grep命令展示匹配项的前后n行信息/index.md>)。

记录日期：2023-07-03T17:27:59+08:00；状态：正文已核阅；有修改意见。

#### R116

**字词/链接 · 字词错误 · P3**

定位：[原文第 36 行](<C:/Project/blog/software/linux/Linux的grep命令展示匹配项的前后n行信息/index.md:36>)；待改表述／主题：` 列 `。

原文定位行（节选）：`` -C 参数（`--context`），除了显示符合范本样式的那一列之外，并显示该列之前后的内容。 ``

问题：-A/-B/-C 展示的是上下文行，不是列。

建议修改：改为“行”，示例补足数量参数，例如 grep -A 3 pattern file。

依据：[GNU 官方手册 · grep](https://www.gnu.org/software/grep/manual/grep.html)。

### A076

**Linux的排序命令sort**

原文：[software/linux/Linux的排序命令sort/index.md](<C:/Project/blog/software/linux/Linux的排序命令sort/index.md>)。

记录日期：2024-06-19T14:00:51+08:00；状态：正文已核阅；有修改意见。

#### R117

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 25 行](<C:/Project/blog/software/linux/Linux的排序命令sort/index.md:25>)；待改表述／主题：` LC_COLLATE=en_US.UTF-8 `。

原文定位行（节选）：`` sort 的默认使用字母顺序来进行升序排列，如果 locale 命令看到 `LC_COLLATE="en_US.UTF-8"`，那就是按照 ASCII 来排序了。 ``

问题：en_US.UTF-8 的排序由语言环境规则决定，不等于 ASCII 字节顺序。

建议修改：需要可复现的字节顺序时使用 LC_ALL=C sort …；区分字符编码与排序规则。

依据：[GNU 官方手册 · sort-invocation](https://www.gnu.org/software/coreutils/manual/html_node/sort-invocation.html)。

#### R118

**事实/技术错误 · 代码错误 · P2**

定位：[原文第 127 行](<C:/Project/blog/software/linux/Linux的排序命令sort/index.md:127>)；待改表述／主题：` sorted(...).thenComparing `。

原文定位行（节选）：`` 就像其他编程语言一样，-k 参数就是为了按照某个或者某几个字段进行排序，类似于 SQL 里面的 order by 多个字段，并且每个字段都可以定义升降序（desc，asc），Python 中的 sort 函数的 key，Java 里的 `stream().sorted(...).thenComparing(...)` 都是实现了类似的多字段排序的效果。 ``

问题：Stream 没有 thenComparing 方法，该方法属于 Comparator。

建议修改：写成 stream.sorted(Comparator.comparing(...).thenComparing(...))。

依据：[Oracle／Java 官方文档 · Comparator](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Comparator.html)。

### A077

**Linux的权限系统**

原文：[software/linux/Linux的权限系统/index.md](<C:/Project/blog/software/linux/Linux的权限系统/index.md>)。

记录日期：2023-07-29T09:54:51+08:00；状态：正文已核阅；有修改意见。

#### R119

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 131 行](<C:/Project/blog/software/linux/Linux的权限系统/index.md:131>)；待改表述／主题：` 不然没法使用这个账号登录 `。

原文定位行（节选）：` 添加了新账号下一步就是设置密码，不然没法使用这个账号登录： `

问题：锁定密码不等于任何认证方式都无法登录；SSH 公钥登录还受 sshd、PAM、账号状态影响。

建议修改：改为：要使用密码认证需设置密码；公钥等其他认证另行配置。

依据：[Linux／工具手册 · useradd.8](https://man7.org/linux/man-pages/man8/useradd.8.html)。

#### R120

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 220 行](<C:/Project/blog/software/linux/Linux的权限系统/index.md:220>)；待改表述／主题：` 执行顺序 `。

原文定位行（节选）：`` 每次用户登录时，都会执行 `.bash_profile` 和 .bashrc，这里的执行顺序如下： ``

问题：登录 Bash 首先读取 /etc/profile，再读取首个存在的 ~/.bash_profile、~/.bash_login、~/.profile；bashrc 是否被读取依赖这些文件显式 source。

建议修改：重写顺序图；交互非登录 Bash 读取 ~/.bashrc，/etc/bashrc 是否参与取决于发行版配置。

依据：[GNU 官方手册 · Bash-Startup-Files](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html)。

#### R121

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 333 行](<C:/Project/blog/software/linux/Linux的权限系统/index.md:333>)；待改表述／主题：` u符号代表当前用户 `。

原文定位行（节选）：` u符号代表当前用户。 `

问题：chmod 的 u/g 指文件属主/文件属组，与执行 chmod 的当前用户/当前用户组不是同一概念。

建议修改：u=文件所有者；g=文件所属组；o=其余用户；sticky bit 删除限制还包括有特权的进程。

依据：[GNU 官方手册 · Setting-Permissions](https://www.gnu.org/software/coreutils/manual/html_node/Setting-Permissions.html)。

#### R122

**字词/链接 · 命令/字词错误 · P3**

定位：[原文第 485 行](<C:/Project/blog/software/linux/Linux的权限系统/index.md:485>)；待改表述／主题：` gpassed `。

原文定位行（节选）：` gpassed -a bob math `

问题：命令应为 gpasswd。另有“200 原”“第中间”“baserc”“pubic”等拼写（L47/L55/L234/L315/L369）。

建议修改：改为 gpasswd；分别改成“中间”“200 元”“bashrc”“public”；.bash_history 补前导点（L208）。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R123

**条件/版本澄清 · 字词/条件遗漏 · P2**

定位：[原文第 510 行](<C:/Project/blog/software/linux/Linux的权限系统/index.md:510>)；待改表述／主题：` /etc/groups；newgrp必须是既有组成员 `。

原文定位行（节选）：`` jack 的 gid 为 1008，我们通过 `/etc/groups` 可以看到 gid 为 1008 的就是 jack 的同名用户组： ``

问题：组数据库路径为/etc/group；某些实现允许非成员凭组密码切换，不能无条件说必须已是成员。

建议修改：路径统一改/etc/group；newgrp说明成员/组密码及权限条件；新建文件属组还可能受父目录setgid位影响。

依据：[Linux／工具手册 · newgrp.1](https://man7.org/linux/man-pages/man1/newgrp.1.html)；[Linux／工具手册 · group.5](https://man7.org/linux/man-pages/man5/group.5.html)。

### A078

**Linux的链接**

原文：[software/linux/Linux的链接/index.md](<C:/Project/blog/software/linux/Linux的链接/index.md>)。

记录日期：2024-06-07T17:00:51+08:00；状态：正文已核阅；有修改意见。

#### R124

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 23 行](<C:/Project/blog/software/linux/Linux的链接/index.md:23>)；待改表述／主题：` 镜像副本 `。

原文定位行（节选）：` 硬链接实际上创建了一个原始文件的镜像副本，创建后即使删除了原始文件，镜像副本也不会受到影响，硬链接直接指向真实文件。 `

问题：硬链接是同一 inode 的另一目录项，不复制数据。

建议修改：改为：两个名字引用同一文件，修改任一名字所指内容会反映到另一个名字。

依据：[Linux／工具手册 · link.2](https://man7.org/linux/man-pages/man2/link.2.html)。

#### R125

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 85 行](<C:/Project/blog/software/linux/Linux的链接/index.md:85>)；待改表述／主题：` 512 字节并不是全部存储数据 `。

原文定位行（节选）：` 扇区的 512 字节并不是全部存储数据，而是包含了几个部分： `

问题：向系统暴露的 512 字节逻辑扇区是数据负载；同步、头标、ECC 等物理编码开销在额外空间中。

建议修改：区分逻辑扇区的数据容量与介质上的物理格式开销。

依据：[www.seagate.com · tp613_4k_transition.pdf](https://www.seagate.com/files/staticfiles/docs/pdf/whitepaper/tp613_4k_transition.pdf)。

#### R126

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 112 行](<C:/Project/blog/software/linux/Linux的链接/index.md:112>)；待改表述／主题：` 8 位；6 位；1023 `。

原文定位行（节选）：` * 柱面数（10 位） = 1023 `

问题：传统 BIOS CHS 是柱面10位、磁头8位、扇区6位；柱面编号0～1023对应1024个柱面。

建议修改：交换110/114行位数：扇区6位，磁头8位；柱面编号0～1023对应1024个柱面。理论256磁头时容量512×63×1024×256=8,455,716,864字节；采用255头兼容几何时也必须用1024柱面，明确是哪一种限制。

依据：[tldp.org · Large-Disk-HOWTO](https://tldp.org/HOWTO/html_single/Large-Disk-HOWTO/)。

#### R127

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 143 行](<C:/Project/blog/software/linux/Linux的链接/index.md:143>)；待改表述／主题：` 一个文件，至少要占用一个数据块 `。

原文定位行（节选）：` 可以看到，磁盘块的大小是 4096 Bytes，也就是 4K，相当于 8 个扇区。一个文件，至少要占用一个数据块，一个数据块不能有两个或者以上的文件。 `

问题：空文件可不占数据块；稀疏文件和 inline data 等也使这条绝对说法不成立；stat 的 IO Block 不是已分配块大小的充分证据。

建议修改：改为：常见非空、非内联普通文件按文件系统分配单位分配空间；区分 st_blksize、st_blocks、文件系统块大小。

依据：[Linux／工具手册 · inode.7](https://man7.org/linux/man-pages/man7/inode.7.html)；[docs.kernel.org · ifork](https://docs.kernel.org/filesystems/ext4/ifork.html)。

#### R128

**字词/链接 · 字词错误 · P3**

定位：[原文第 205 行](<C:/Project/blog/software/linux/Linux的链接/index.md:205>)；待改表述／主题：` 真是文件；books.tx；book.txt `。

原文定位行（节选）：` 29665 lrwxrwxrwx 1 koril koril  11 Feb 24 16:29 soft_link_books.txt -> ./books.txt `

问题：“真实”误写，示例文件名不一致（另见 L46/L175/L183）。

建议修改：改为“真实文件”，文件名统一 books.txt。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R129

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 245 行](<C:/Project/blog/software/linux/Linux的链接/index.md:245>)；待改表述／主题：` 减少为 0…回收 `。

原文定位行（节选）：`` 这个数字表示有几个硬链接指向原始文件，这里有两个，一个是 `books.txt`，另一个是 `hard_link_books.txt`，而软链接并不会增加这个数值，如果这个值减少为 0，说明没有硬链接指向原始文件了，那么系统就会回收这个数据块。 ``

问题：最后一个硬链接被删后，仍被进程打开的文件不会立即释放。

建议修改：加上：链接计数为零且最后一个打开引用释放后，才回收资源。

依据：[Linux／工具手册 · unlink.2](https://man7.org/linux/man-pages/man2/unlink.2.html)。

### A079

**ntfy服务的使用**

原文：[software/linux/ntfy服务的使用/index.md](<C:/Project/blog/software/linux/ntfy服务的使用/index.md>)。

记录日期：2025-07-03T17:37:00+08:00；状态：正文已核阅；有修改意见。

#### R130

**事实/技术错误 · 配置错误 · P2**

定位：[原文第 58 行](<C:/Project/blog/software/linux/ntfy服务的使用/index.md:58>)；待改表述／主题：` base-url: "notify.test.com" `。

原文定位行（节选）：` base-url: "notify.test.com" `

问题：base-url 需要包含协议的外部访问 URL。

建议修改：当前 HTTP 代理例改为 http://notify.test.com；HTTPS 部署则使用相应 https URL。

依据：[docs.ntfy.sh · config](https://docs.ntfy.sh/config/)。

### A080

**Shell的快捷键**

原文：[software/linux/Shell的快捷键/index.md](<C:/Project/blog/software/linux/Shell的快捷键/index.md>)。

记录日期：2026-05-24T09:52:08；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A081

**ssh心跳保活**

原文：[software/linux/ssh心跳保活/index.md](<C:/Project/blog/software/linux/ssh心跳保活/index.md>)。

记录日期：2025-02-06T20:03:00+08:00；状态：正文已核阅；有修改意见。

#### R131

**事实/技术错误 · 路径错误 · P2**

定位：[原文第 39 行](<C:/Project/blog/software/linux/ssh心跳保活/index.md:39>)；待改表述／主题：` ~/.SSH/config `。

原文定位行（节选）：` 如果你只是想防止 SSH 连接超时，建议在 客户端 的 ~/.SSH/config 里加： `

问题：Linux 路径区分大小写；OpenSSH 默认读取 ~/.ssh/config。

建议修改：改为 ~/.ssh/config。

依据：[OpenBSD 官方手册 · ssh_config](https://man.openbsd.org/ssh_config)。

### A082

**SSH日志**

原文：[software/linux/SSH日志/index.md](<C:/Project/blog/software/linux/SSH日志/index.md>)。

记录日期：2025-06-29T10:00:00+08:00；状态：正文已核阅；有修改意见。

#### R132

**字词/链接 · 字词错误 · P3**

定位：[原文第 50 行](<C:/Project/blog/software/linux/SSH日志/index.md:50>)；待改表述／主题：` 时间辍 `。

原文定位行（节选）：` 包含时间辍，服务器名称（hostname），进程名字，进程 PID，冒号后面就是日志信息，对于 SSH 而言，主要是身份验证是否通过。 `

问题：错字。

建议修改：改为时间戳。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R133

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 61 行](<C:/Project/blog/software/linux/SSH日志/index.md:61>)；待改表述／主题：` 客户端尝试了太多认证方式 `。

原文定位行（节选）：` - 客户端尝试了太多认证方式，SSH 服务主动断开：Connection closed by authenticating user root 121.37.128.117 port 55686 [preauth] `

问题：Connection closed … [preauth] 只说明认证前连接关闭，不能据此确定超过认证次数。

建议修改：明确仅凭该行无法判断原因；超过次数通常有 Too many authentication failures 或 maximum authentication attempts exceeded 等记录。

依据：[仓库源码：openssh/openssh-portable · auth.c](https://github.com/openssh/openssh-portable/blob/master/auth.c)。

### A083

**Top命令的一些进阶用法**

原文：[software/linux/Top命令的一些进阶用法/index.md](<C:/Project/blog/software/linux/Top命令的一些进阶用法/index.md>)。

记录日期：2024-03-10T10:20:03+08:00；状态：正文已核阅；有修改意见。

#### R134

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 61 行](<C:/Project/blog/software/linux/Top命令的一些进阶用法/index.md:61>)；待改表述／主题：` 僵尸进程通常意味着…没有正常退出 `。

原文定位行（节选）：` zombie：僵尸进程，是指等待其父进程释放它的进程，如果父进程先退出，它可能会成为孤儿进程。僵尸进程通常意味着应用程序或服务没有正常退出。 长时间运行的系统上的一些僵尸进程通常不是什么大问题。 `

问题：僵尸进程已经终止，只是退出状态尚未被父进程 wait 回收；正常退出也可产生。

建议修改：改为：已退出但未被回收的进程；孤儿是父进程先退出的另一概念。

依据：[Linux／工具手册 · wait.2](https://man7.org/linux/man-pages/man2/wait.2.html)。

#### R135

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 72 行](<C:/Project/blog/software/linux/Top命令的一些进阶用法/index.md:72>)；待改表述／主题：` 如果高，CPU 可能会过度工作 `。

原文定位行（节选）：` id：idle time，是空闲时间的百分比（如果高，CPU 可能会过度工作）。 `

问题：id 是空闲时间比例，解释方向反了。

建议修改：改为：id 越高通常越空闲，越低说明 CPU 忙；ni 是运行被调整 nice 值的进程所消耗的用户态 CPU 时间，不是“好值”。

依据：[Linux／工具手册 · top.1](https://man7.org/linux/man-pages/man1/top.1.html)。

#### R136

**事实/技术错误 · 概念混淆 · P2**

定位：[原文第 92 行](<C:/Project/blog/software/linux/Top命令的一些进阶用法/index.md:92>)；待改表述／主题：` free：可用…Swap…虚拟内存 `。

原文定位行（节选）：` free：可用的内存大小 `

问题：free 是完全空闲物理内存，available 是可供新程序使用且不必交换的估计量；Swap 只是虚拟内存机制的一部分。

建议修改：区分 free/available、交换空间/整个虚拟内存；不能由 Swap 非零直接推断 RAM 不足。

依据：[Linux／工具手册 · top.1](https://man7.org/linux/man-pages/man1/top.1.html)。

### A084

**TextEditor中文输入重复显示的BUG**

原文：[software/linux/Ubuntu/TextEditor中文输入重复显示的BUG/index.md](<C:/Project/blog/software/linux/Ubuntu/TextEditor中文输入重复显示的BUG/index.md>)。

记录日期：2025-07-05T16:31:00+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A085

**Ubuntu24.04时间错误的问题**

原文：[software/linux/Ubuntu/Ubuntu24.04时间错误的问题/index.md](<C:/Project/blog/software/linux/Ubuntu/Ubuntu24.04时间错误的问题/index.md>)。

记录日期：2025-06-17T20:10:00+08:00；状态：正文已核阅；有修改意见。

#### R137

**字词/链接 · 字词错误 · P3**

定位：[原文第 29 行](<C:/Project/blog/software/linux/Ubuntu/Ubuntu24.04时间错误的问题/index.md:29>)；待改表述／主题：` Loca `。

原文定位行（节选）：` 可以看到时区是正确的，但是 RTC/UTC/Loca 时间都错了，Local time 应该是 2025-06-17 19:51:53，也就是说，Local time 比正确 UTC 时间超了 16 小时。 `

问题：应为 Local（时钟误差的推断另需与截图及参考时钟核对）。

建议修改：改为 Local。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A086

**Ubuntu24.04设置桌面软件自启动**

原文：[software/linux/Ubuntu/Ubuntu24.04设置桌面软件自启动/index.md](<C:/Project/blog/software/linux/Ubuntu/Ubuntu24.04设置桌面软件自启动/index.md>)。

记录日期：2025-01-30T15:42:00+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A087

**Virtualbox无法打开虚拟机的问题**

原文：[software/linux/Ubuntu/Virtualbox无法打开虚拟机的问题/index.md](<C:/Project/blog/software/linux/Ubuntu/Virtualbox无法打开虚拟机的问题/index.md>)。

记录日期：2025-08-17T09:33:00+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A088

**使用mitmproxy进行抓包**

原文：[software/linux/Ubuntu/使用mitmproxy进行抓包/index.md](<C:/Project/blog/software/linux/Ubuntu/使用mitmproxy进行抓包/index.md>)。

记录日期：2025-02-02T14:34:00+08:00；状态：正文已核阅；有修改意见。

#### R138

**字词/链接 · 字词/链接错误 · P3**

定位：[原文第 16 行](<C:/Project/blog/software/linux/Ubuntu/使用mitmproxy进行抓包/index.md:16>)；待改表述／主题：` mimproxy；自动成；链接 `。

原文定位行（节选）：` 所以把目光放到了开源的抓包工具：[mimproxy](https://mitmproxy.org/)，支持命令行、web 界面以及 Python API 调用。 `

问题：工具名改 mitmproxy；L54“自动成”改“自动生成”；L50“专用链接”改“专用连接”；L42 链接目标删中文。

建议修改：链接目标只保留 http://example.com/，解释放在括号外。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A089

**公网VPS下的Ubuntu系统保护措施**

原文：[software/linux/Ubuntu/公网VPS下的Ubuntu系统保护措施/index.md](<C:/Project/blog/software/linux/Ubuntu/公网VPS下的Ubuntu系统保护措施/index.md>)。

记录日期：2023-05-04T20:21:41+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A090

**卸载和弹出移动硬盘**

原文：[software/linux/Ubuntu/卸载和弹出移动硬盘/index.md](<C:/Project/blog/software/linux/Ubuntu/卸载和弹出移动硬盘/index.md>)。

记录日期：2025-05-01T16:41:00+08:00；状态：正文已核阅；有修改意见。

#### R139

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 59 行](<C:/Project/blog/software/linux/Ubuntu/卸载和弹出移动硬盘/index.md:59>)；待改表述／主题：` umount 是需要 sudo 权限的 `。

原文定位行（节选）：` 这个命令和 umount 类似，但是 umount 是需要 sudo 权限的。执行这个命令后，USB 设备保持物理连接，硬盘仍可重新挂载（通过 mount 或者 udisksctl mount 指令）。 `

问题：umount 在 fstab user/users 等授权条件下可由普通用户调用。

建议修改：改为：普通挂载通常需要特权；fstab 授权或 udisks/Polkit 可允许普通用户卸载；L71“关闭闭”改“关闭”。

依据：[Linux／工具手册 · umount.8](https://man7.org/linux/man-pages/man8/umount.8.html)。

### A091

**树莓派4B安装Ubuntu Server 22.04**

原文：[software/linux/Ubuntu/树莓派4B安装Ubuntu Server 22.04/index.md](<C:/Project/blog/software/linux/Ubuntu/树莓派4B安装Ubuntu Server 22.04/index.md>)。

记录日期：2023-04-30T11:53:00+08:00；状态：正文已核阅；有修改意见。

#### R140

**事实/技术错误 · 事实/拼写错误 · P2**

定位：[原文第 78 行](<C:/Project/blog/software/linux/Ubuntu/树莓派4B安装Ubuntu Server 22.04/index.md:78>)；待改表述／主题：` 用户名和密码都是：Ubuntu `。

原文定位行（节选）：` 上电后，会提示键入用户名和密码，默认的用户名和密码都是：Ubuntu，然后系统会提示修改默认的密码，修改成功后就进入系统了。 `

问题：该镜像默认凭据为小写 ubuntu，大小写会影响登录。

建议修改：改为 ubuntu/ubuntu；L44“准本”改“准备”；L156 写 Ubuntu22.04=jammy，而非所有22.x。

依据：[ubuntu.com · how-to-install-ubuntu-on-your-raspberry-pi](https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi)。

### A092

**usr目录的历史背景**

原文：[software/linux/usr目录的历史背景/index.md](<C:/Project/blog/software/linux/usr目录的历史背景/index.md>)。

记录日期：2025-02-01T15:19:00+08:00；状态：草稿；空提纲／参考资料；无实质技术正文。

只有提纲、前言标题或参考链接，缺少可核实的技术正文。本轮不把这种空提纲计作内容正确的技术文章。

### A093

**VirtualBox中虚拟机运行缓慢的解决方案**

原文：[software/linux/VirtualBox中虚拟机运行缓慢的解决方案/index.md](<C:/Project/blog/software/linux/VirtualBox中虚拟机运行缓慢的解决方案/index.md>)。

记录日期：2024-06-13T18:10:59+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A094

**VirtualBox创建CentOS7虚拟机**

原文：[software/linux/VirtualBox创建CentOS7虚拟机/index.md](<C:/Project/blog/software/linux/VirtualBox创建CentOS7虚拟机/index.md>)。

记录日期：2023-07-08T08:28:46+08:00；状态：正文已核阅；有修改意见。

#### R141

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 18 行](<C:/Project/blog/software/linux/VirtualBox创建CentOS7虚拟机/index.md:18>)；待改表述／主题：` 两者的不同…CentOS 完全开源 `。

原文定位行（节选）：` CentOS（Community Enterprise Operating System，中文意思是社区企业操作系统）是 Linux 发行版之一，它是来自于 Red Hat Enterprise Linux 依照开放源代码规定释出的源代码所编译而成。由于出自同样的源代码，因此有些要求高度稳定性的服务器以 CentOS 替代商业版的 Red Hat Enterprise Linux 使用。两者的不同，在于 CentOS 完全开源。 `

问题：RHEL 本身也由开源软件构成，不能把两者差异概括成一方开源、一方不开放。

建议修改：写清商业订阅、支持和发行方式的差别。

依据：[www.redhat.com · open-source](https://www.redhat.com/en/about/open-source)。

#### R142

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 245 行](<C:/Project/blog/software/linux/VirtualBox创建CentOS7虚拟机/index.md:245>)；待改表述／主题：` yum…需要联网 `。

原文定位行（节选）：` 2. 需要联网 `

问题：yum 可以使用本地目录或挂载介质仓库，并非必然需要互联网。

建议修改：改为：使用远程仓库时需要网络；离线环境可建立本地 yum 仓库并解析依赖。

依据：[docs.redhat.com · sec-configuring_yum_and_yum_repositories](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/system_administrators_guide/sec-configuring_yum_and_yum_repositories)。

#### R143

**条件/版本澄清 · 命令适用条件 · P2**

定位：[原文第 437 行](<C:/Project/blog/software/linux/VirtualBox创建CentOS7虚拟机/index.md:437>)；待改表述／主题：` rpm -e --nodeps mariadb-libs `。

原文定位行（节选）：` rpm -e --nodeps mariadb-libs-5.5.68-1.el7.x86_64 `

问题：跳过依赖检查会留下破损依赖；MySQL 官方提供兼容库以支持迁移。

建议修改：说明--nodeps只跳过依赖检查，不解决依赖。采用本地yum事务或按官方迁移流程安装MySQL兼容库，并检查最终依赖完整性。

依据：[MySQL 官方文档](https://dev.mysql.com/doc/mysql-yum-repo-quick-guide/en/)。

#### R144

**字词/链接 · 字词错误 · P3**

定位：[原文第 577 行](<C:/Project/blog/software/linux/VirtualBox创建CentOS7虚拟机/index.md:577>)；待改表述／主题：` /usr/loacl/redis/；Vitual Box；NetworkManger；变软 `。

原文定位行（节选）：`` 将安装包下的默认配置文件模板 `redis-5.0.0/redis.conf`，拷贝到 `/usr/loacl/redis/` 下。 ``

问题：路径和名称拼写错误；L815 把 Nginx 启动写成 redisd。

建议修改：改 /usr/local/redis/、VirtualBox、NetworkManager、“编译”；L750补“不用”；L815改 nginxd。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R145

**事实/技术错误 · 配置错误 · P1**

定位：[原文第 626 行](<C:/Project/blog/software/linux/VirtualBox创建CentOS7虚拟机/index.md:626>)；待改表述／主题：` ExecReload通过SIGHUP重载Redis `。

原文定位行（节选）：` ExecReload=/bin/kill -s HUP $MAINPID `

问题：本教程Redis5忽略SIGHUP，此ExecReload不会按预期重读redis.conf。

建议修改：去掉该无效重载定义，按CONFIG SET支持的参数动态修改并按需CONFIG REWRITE；需重启的设置明确重启。

依据：[仓库源码：redis/redis · server.c](https://raw.githubusercontent.com/redis/redis/5.0/src/server.c)；[Redis 官方文档 · config-set](https://redis.io/docs/latest/commands/config-set/)。

### A095

**使用systemd管理简单的服务**

原文：[software/linux/使用systemd管理简单的服务/index.md](<C:/Project/blog/software/linux/使用systemd管理简单的服务/index.md>)。

记录日期：2025-07-11T15:22:00+08:00；状态：正文已核阅；有修改意见。

#### R146

**字词/链接 · 字词错误 · P3**

定位：[原文第 75 行](<C:/Project/blog/software/linux/使用systemd管理简单的服务/index.md:75>)；待改表述／主题：` WangtedBy `。

原文定位行（节选）：` [Install] 的 WangtedBy 表示当启用（enable）该服务时，要将其加入到哪些 target 的 wants 目录中。 `

问题：配置项拼写错误。

建议修改：改为 WantedBy。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R147

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 137 行](<C:/Project/blog/software/linux/使用systemd管理简单的服务/index.md:137>)；待改表述／主题：` 主服务进程执行完成之后 `。

原文定位行（节选）：` - exec 与 simple 类似，不同之处在于， 只有在该服务的主服务进程执行完成之后，systemd 才会认为该服务启动完成。 其他后继单元必须一直阻塞到这个时间点之后才能继续启动。换句话说， simple 表示当 fork() 函数返回时，即算是启动完成，而 exec 则表示仅在 fork() 与 execve() 函数都执行成功时，才算是启动完成。 这就意味着对于 exec 类型的服务来说， 如果不能成功调用主服务进程（例如 User= 不存在、或者二进制可执行文件… `

问题：Type=exec 等待成功 execve 启动程序，不等程序退出；该句与后面的解释矛盾。

建议修改：改为“主服务进程的可执行程序成功启动之后”。

依据：[Linux／工具手册 · systemd.service.5](https://man7.org/linux/man-pages/man5/systemd.service.5.html)。

#### R148

**条件/版本澄清 · 版本条件 · P2**

定位：[原文第 141 行](<C:/Project/blog/software/linux/使用systemd管理简单的服务/index.md:141>)；待改表述／主题：` notify 尚不能与 PrivateNetwork=yes 一起使用 `。

原文定位行（节选）：`` - notify 与 exec 类似，不同之处在于， 该服务将会在启动完成之后通过 `sd_notify(3)` 之类的接口发送一个通知消息。systemd 将会在启动后继单元之前， 首先确保该进程已经成功的发送了这个消息。如果设为此类型，那么下文的 NotifyAccess= 将只能设为非 none 值。如果未设置 NotifyAccess= 选项、或者已经被明确设为 none ，那么将会被自动强制修改为 main 。注意，目前 Type=notify 尚不能与 Priva… ``

问题：这是旧版本限制，不宜沿用到本文2025年环境。

建议修改：按所用 systemd 版本说明；现代通知使用文件系统命名的 Unix socket，不再保留这条普遍禁用结论。

依据：[Linux／工具手册 · systemd.service.5](https://man7.org/linux/man-pages/man5/systemd.service.5.html)。

#### R149

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 240 行](<C:/Project/blog/software/linux/使用systemd管理简单的服务/index.md:240>)；待改表述／主题：` always: 无条件重启 `。

原文定位行（节选）：` - always: 无条件重启 `

问题：systemctl stop/restart 等由 systemd 主动结束进程时不会触发该自动重启条件；StartLimitBurst 统计启动次数不只是失败次数。

建议修改：改为：进程正常/异常退出都会自动重启，但有管理操作与启动限流等例外；60秒最多3次启动包括首次启动。

依据：[Linux／工具手册 · systemd.service.5](https://man7.org/linux/man-pages/man5/systemd.service.5.html)。

### A096

**命令行设计的艺术**

原文：[software/linux/命令行设计的艺术/index.md](<C:/Project/blog/software/linux/命令行设计的艺术/index.md>)。

记录日期：2025-11-17T17:01:23；状态：草稿；正文已核阅；有修改意见。

#### R150

**字词/链接 · 字词错误 · P3**

定位：[原文第 199 行](<C:/Project/blog/software/linux/命令行设计的艺术/index.md:199>)；待改表述／主题：` 用用 `。

原文定位行（节选）：`` 选项（Option）是另外一种 CLI 的传参手段，和位置参数不同，它一般是用用连字符和单字母名称 (比如：-l、-h、-v) 或双连字符和多字母名称 (比如：`--list`、`--help`、`--version`）。 ``

问题：重复字；L20“图像的的”及其他明显重复按原文核对。

建议修改：改为“用”。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A097

**如何在Linux中查看机器的参数和性能**

原文：[software/linux/如何在Linux中查看机器的参数和性能/index.md](<C:/Project/blog/software/linux/如何在Linux中查看机器的参数和性能/index.md>)。

记录日期：2023-05-02T13:59:32+08:00；状态：正文已核阅；有修改意见。

#### R151

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 54 行](<C:/Project/blog/software/linux/如何在Linux中查看机器的参数和性能/index.md:54>)；待改表述／主题：` Socket(s)…即物理核心数 `。

原文定位行（节选）：` * Socket(s)：CPU 插槽数，即物理核心数 `

问题：插槽/CPU 封装数不等于核心数。

建议修改：Socket(s) 是 CPU 插槽/封装数；每封装可含多个核心和多个逻辑线程。

依据：[Linux／工具手册 · lscpu.1](https://man7.org/linux/man-pages/man1/lscpu.1.html)。

#### R152

**字词/链接 · 字词错误 · P3**

定位：[原文第 153 行](<C:/Project/blog/software/linux/如何在Linux中查看机器的参数和性能/index.md:153>)；待改表述／主题：` 如果您想 df `。

原文定位行（节选）：`` 如果您想 df 以人类可读的格式运行，请使用 `--human-readable （-h 简称）` 选项： ``

问题：该段解释 du，应为 du；L20“如果”应为“如何”。

建议修改：同步修正这两个词。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R153

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 212 行](<C:/Project/blog/software/linux/如何在Linux中查看机器的参数和性能/index.md:212>)；待改表述／主题：` 生成 10000 个素数 `。

原文定位行（节选）：` 先使用一个 thread 执行一次 cpu 性能测试，该指令会生成 10000 个素数，根据消耗的时间来衡量 cpu 的性能 `

问题：cpu-max-prime=10000 是素数测试的整数上限，不是生成10000个素数。

建议修改：改为：每个 CPU 测试事件计算/检查直到该上限的素数；比较 events/s 时固定上限、线程数与时间。

依据：[仓库源码：akopytov/sysbench · sb_cpu.c](https://github.com/akopytov/sysbench/blob/master/src/tests/cpu/sb_cpu.c)。

### A098

**环境变量**

原文：[software/linux/环境变量/index.md](<C:/Project/blog/software/linux/环境变量/index.md>)。

记录日期：2025-11-14T15:13:37；状态：正文已核阅；有修改意见。

#### R154

**条件/版本澄清 · 适用/字词错误 · P2**

定位：[原文第 38 行](<C:/Project/blog/software/linux/环境变量/index.md:38>)；待改表述／主题：` 子进程也无法访问 shell 变量 `。

原文定位行（节选）：` shell 变量仅存在于当前终端，如果推出了终端或者打开了新的 shell，这个变量就没有了，shell 的子进程也无法访问 shell 变量。 `

问题：exec 启动程序不会自动继承未 export 的变量，但 fork 出的 subshell（如括号子 shell）会继承 shell 状态。另有“推出”“改变量”。

建议修改：限定为执行独立程序的环境继承；改“退出”“该变量”（L124/L137）。

依据：[GNU 官方手册 · Command-Execution-Environment](https://www.gnu.org/software/bash/manual/html_node/Command-Execution-Environment.html)。

#### R155

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 71 行](<C:/Project/blog/software/linux/环境变量/index.md:71>)；待改表述／主题：` 很动态…安全性相对较高 `。

原文定位行（节选）：` 环境变量是很动态的，它一般在某个程序进程运行前设置，并且不会持久化到磁盘中，因此安全性相对较高。 `

问题：环境是进程启动时继承的副本；修改父 shell 不会更新已运行的子进程。环境还可能被调试接口/日志等读取，不能天然保证密钥安全。

建议修改：改为：便于启动时注入配置，不自动支持运行时更新；密钥保护仍依赖权限、日志处理和部署方式。

依据：[Linux／工具手册 · environ.7](https://man7.org/linux/man-pages/man7/environ.7.html)。

### A099

**误删除glibc后的教训**

原文：[software/linux/误删除glibc后的教训/index.md](<C:/Project/blog/software/linux/误删除glibc后的教训/index.md>)。

记录日期：2023-07-20T16:04:55+08:00；状态：正文已核阅；有修改意见。

#### R156

**事实/技术错误 · 代码错误 · P2**

定位：[原文第 73 行](<C:/Project/blog/software/linux/误删除glibc后的教训/index.md:73>)；待改表述／主题：` OutputStream outputStream `。

原文定位行（节选）：` OutputStream outputStream = Files.newOutputStream(p2.resolve(String.valueOf(cnt))); `

问题：每轮新建输出流后未关闭。

建议修改：每次循环用 try-with-resources 包住 Files.newOutputStream；L47“有仅有”改“仅有”。

依据：[Oracle／Java 官方文档 · OutputStream](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/OutputStream.html)。

### A100

**DNS和域名的一些记录**

原文：[software/network/DNS和域名的一些记录/index.md](<C:/Project/blog/software/network/DNS和域名的一些记录/index.md>)。

记录日期：2023-11-25T10:07:16+08:00；状态：正文已核阅；有修改意见。

#### R157

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 18 行](<C:/Project/blog/software/network/DNS和域名的一些记录/index.md:18>)；待改表述／主题：` 每台主机…IPv4 `。

原文定位行（节选）：`` 互联网上的每台主机的逻辑地址使用的是 IPv4 地址，它由一串 32 位的二进制数表示，每 8 位划为一组，再转换成十进制，就是我们平时看到的点分十进制格式：`a.b.c.d`，例如：192.168.0.1，IP 地址对于人类而言，很难记忆，我们更擅长记住有意义的文字符号，而非数字。 ``

问题：互联网还使用 IPv6，主机不必都具有 IPv4 地址。

建议修改：限定本节讨论 IPv4，并介绍 IPv6 为128位；通过NAT访问互联网的终端不必各自拥有公网IPv4（L54）。

依据：[RFC 8200](https://www.rfc-editor.org/rfc/rfc8200.html)；[RFC 3022](https://www.rfc-editor.org/rfc/rfc3022.html)。

#### R158

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 26 行](<C:/Project/blog/software/network/DNS和域名的一些记录/index.md:26>)；待改表述／主题：` 应对苏联核打击…分布式指挥系统 `。

原文定位行（节选）：` 互联网的历史是从美苏冷战开始的，美国国防高级研究计划局开发了阿帕网，也就是后来互联网的鼻祖，阿帕网一开始就是为了应对苏联核打击而设计的分布式指挥系统，分散的节点之间通过网络连接通讯，所以就诞生了网络传输协议 TCP，UDP 等，网络节点之间通讯需要知道节点的地址，就衍生出了 IP 地址的概念，用来标志一个网络节点的逻辑地址，而人类很难记住每个节点的 IP 地址，所以自然而然的希望给每个节点起个英文名，这样访问别的节点的时候，只要输入英文的别名就行了，但是底层的计算机网络系统依… `

问题：把 RAND 的抗毁通信研究与 ARPANET 的建设目标混为一谈。

建议修改：改为：ARPANET 以计算机资源共享等研究需求为目标；抗核战争起源说是流传的误解。

依据：[www.internetsociety.org · ISOC-History-of-the-Internet_2012Oct.pdf](https://www.internetsociety.org/wp-content/uploads/2017/09/ISOC-History-of-the-Internet_2012Oct.pdf)。

#### R159

**字词/链接 · 字词/链接错误 · P3**

定位：[原文第 28 行](<C:/Project/blog/software/network/DNS和域名的一些记录/index.md:28>)；待改表述／主题：` 全程；APRANET；goog.com.；注册管理结构 `。

原文定位行（节选）：`` 起初，斯坦福大学维护了一个名为 `HOSTS.txt` 的文本文件，该文件将 APRANET 上的主机名映射到数字地址，地址一开始是手动分配的，后来，Feinler 在 NIC 中的服务器上设置了 WHOIS 目录，用于检索有关资源、联系人和实体的信息。她和她的团队提出了域的概念。Feinler 建议域应该基于计算机物理地址的位置。例如，教育机构的计算机具有 edu 域。她和她的团队从 1972 年到 1989 年管理着主机命名注册表。 ``

问题：术语拼写错误；L101 链接目标含中文。

建议修改：改为全称、ARPANET、google.com.、注册管理机构；根服务器链接目标仅留 https://root-servers.org/。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R160

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 80 行](<C:/Project/blog/software/network/DNS和域名的一些记录/index.md:80>)；待改表述／主题：` google.com…www.google.com. `。

原文定位行（节选）：`` 之前举例的 `google.com` 其实是一种域名简略的写法，它的**完全限定域名**（FQDN，Fully qualified domain name）是： ``

问题：www.google.com. 和 google.com. 是两个不同的 DNS 名称。

建议修改：google.com 的绝对名称写 google.com.；www.google.com 的绝对名称写 www.google.com.。

依据：[RFC 1034](https://www.rfc-editor.org/rfc/rfc1034.html)。

#### R161

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 94 行](<C:/Project/blog/software/network/DNS和域名的一些记录/index.md:94>)；待改表述／主题：` 13 个独立的 IP 地址…UDP `。

原文定位行（节选）：` 根域名服务器，在全球范围内共有 13 台（以英文字母 A 到 M 依序命名），但这个数字指的是逻辑上的（就是说有 13 个独立的 IP 地址），并不是说物理上只有 13 台服务器，DNS 使用 UDP 协议传输报文信息，会受到 MTU 的限制，详细信息，可以参考以下解答： `

问题：13 指 A～M 的根服务器标识；每个标识有 IPv4 和 IPv6，DNS 也支持 TCP。512字节历史限制不等同一般MTU。

建议修改：改为13个命名权威服务器标识及任播实例；区分传统UDP512字节、EDNS扩展和TCP。

依据：[www.iana.org · servers](https://www.iana.org/domains/root/servers)；[root-servers.org · faq](https://root-servers.org/faq/)；[RFC 7766](https://www.rfc-editor.org/rfc/rfc7766.html)。

#### R162

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 175 行](<C:/Project/blog/software/network/DNS和域名的一些记录/index.md:175>)；待改表述／主题：` 所有域名解析…先从根域…VeriSign…对应IP `。

原文定位行（节选）：`` 所有域名解析都要先从根域开始，根域的维护者是 ICANN，顶级域的维护者是各个域名注册管理机构，所以用大白话来说，我想通过 DNS 知道 `www.google.com` 的 IP 地址是什么，DNS 会先从根域开始找起，ICANN 的服务器并不知道 `www.google.com` 的 IP 地址，但它能告诉程序，.com 的顶级域去哪里找，然后程序就会跑去 .com 的维护者，也就是 VeriSign 公司的服务器去找，VeriSign 就会告诉程序 `google.co… ``

问题：缓存命中无需每次查询根；com 通常返回 google.com 的权威服务器委派，具体主机地址由该域权威服务器返回。

建议修改：重写为：递归解析器查缓存，必要时按根→TLD→域权威服务器迭代，再缓存结果。NS记录指向名称，不等于A记录（L191）。

依据：[RFC 1034](https://www.rfc-editor.org/rfc/rfc1034.html)。

### A101

**IPv4首部和IP报文的分片重组**

原文：[software/network/IPv4首部和IP报文的分片重组/index.md](<C:/Project/blog/software/network/IPv4首部和IP报文的分片重组/index.md>)。

记录日期：2024-06-14T10:21:16+08:00；状态：正文已核阅；有修改意见。

#### R163

**字词/链接 · 字词错误 · P3**

定位：[原文第 39 行](<C:/Project/blog/software/network/IPv4首部和IP报文的分片重组/index.md:39>)；待改表述／主题：` Differential Services；显示拥塞通告；已下 `。

原文定位行（节选）：` 用来表示服务的质量，由 8 bit 组成，用来表示优先度，延迟，吞吐，可靠性，由于 TOS 的实现控制非常复杂，导致其几乎没有被投入使用，后来 TOS 被拆分成两个段——DSCP（Differential Services Codepoint，差分服务代码点）以及 ECN（Explicit Congestion Notification，显示拥塞通告）。 `

问题：DSCP 的展开应为 Differentiated Services Code Point；Explicit 应译“显式”。

建议修改：改为“Differentiated Services Code Point”“显式拥塞通知”；L109改“以下”。

依据：[RFC 2474](https://www.rfc-editor.org/rfc/rfc2474.html)；[RFC 3168](https://www.rfc-editor.org/rfc/rfc3168.html)。

#### R164

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 75 行](<C:/Project/blog/software/network/IPv4首部和IP报文的分片重组/index.md:75>)；待改表述／主题：` 上层的协议（这里是运输层）…仅…目的地 `。

原文定位行（节选）：` 不同层的报文中都会出现这种类似的字段，表示上层的协议（这里是运输层），由 8 bit 组成，该字段仅在 IP 数据报到达了目的地时才会使用，它告诉程序应该将该报文交给哪一个运输层协议，例如，值为 6 表示交给 TCP，值为 17 则交给 UDP。 `

问题：Protocol 可指 ICMP、IP封装等，并非全是传输层；中间防火墙和路由设备也可能读取该字段。

建议修改：改为：标识封装的上层协议，例如 TCP=6、UDP=17、ICMP=1；删除“仅在目的地使用”。

依据：[www.iana.org · protocol-numbers](https://www.iana.org/assignments/protocol-numbers)。

#### R165

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 93 行](<C:/Project/blog/software/network/IPv4首部和IP报文的分片重组/index.md:93>)；待改表述／主题：` Options…仅在实验中使用 `。

原文定位行（节选）：` 长度可变，仅在实验中使用，由于长度的可变性，导致处理性能下降，复杂度上升，故在实践中几乎不使用。 `

问题：IPv4 选项并不只用于实验，标准有 Record Route、Timestamp、Router Alert 等。

建议修改：改为：可选字段，普通数据流中较少使用，处理/过滤受设备实现与策略影响。

依据：[RFC 791](https://www.rfc-editor.org/rfc/rfc791.html)；[RFC 2113](https://www.rfc-editor.org/rfc/rfc2113.html)。

### A102

**MAC地址和ARP协议**

原文：[software/network/MAC地址和ARP协议/index.md](<C:/Project/blog/software/network/MAC地址和ARP协议/index.md>)。

记录日期：2024-06-12T11:22:16+08:00；状态：正文已核阅；有修改意见。

#### R166

**字词/链接 · 字词错误 · P3**

定位：[原文第 17 行](<C:/Project/blog/software/network/MAC地址和ARP协议/index.md:17>)；待改表述／主题：` 文本意欲；在在 `。

原文定位行（节选）：` 在最初接触链路层寻址的时候，对于 MAC 地址还是有些疑惑，关于它和上层协议（网络层）的 IP 地址之间的关系和作用不甚了解，文本意欲理清它们的概念。 `

问题：改“本文意欲”；L100删除重复“在”。

建议修改：按以上两处修改。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R167

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 29 行](<C:/Project/blog/software/network/MAC地址和ARP协议/index.md:29>)；待改表述／主题：` 永远不变…EPROM（一种闪存） `。

原文定位行（节选）：` MAC 地址（Media Access Control Address），也可以称为 LAN 地址或物理地址，与 IP 地址拥有层次性的概念不同，MAC 地址的结构是扁平化的，它的地址长度是 48 位（6 字节）。并且它是不变的，即在网卡生产时，网络设备制造商会将一个唯一的 MAC 地址烧录到网卡的 EPROM （一种闪存芯片）中。 `

问题：MAC 可本地管理/随机化，不天然唯一不变；EPROM 不是 flash 的同义词。

建议修改：区分厂商分配的永久地址与实际使用的本地管理地址；删除烧录介质的绝对断言，EPROM 与 EEPROM/flash 区分。

依据：[RFC 7042](https://www.rfc-editor.org/rfc/rfc7042.html)。

#### R168

**事实/技术错误 · 示例错误 · P2**

定位：[原文第 78 行](<C:/Project/blog/software/network/MAC地址和ARP协议/index.md:78>)；待改表述／主题：` 33-33-33-33-33-33 `。

原文定位行（节选）：` | 192.168.0.113 | 33-33-33-33-33-33 | `

问题：首字节0x33最低位为1，表示组播地址，不适合作为普通主机单播MAC示例。

建议修改：用02开头的本地管理单播地址，例如02-00-00-00-00-03；示意值明确不是真实厂商分配。

依据：[RFC 7042](https://www.rfc-editor.org/rfc/rfc7042.html)。

#### R169

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 122 行](<C:/Project/blog/software/network/MAC地址和ARP协议/index.md:122>)；待改表述／主题：` 目标MAC…00-00-00-00-00-00 `。

原文定位行（节选）：` 需要注意的是，如果是 ARP 查询帧，由于此时目标的 MAC 地址未知，所以帧内容的目标 MAC 地址为 00-00-00-00-00-00。 `

问题：ARP 请求的目标硬件地址在请求中未知，RFC并未强制必须全部为0。

建议修改：改为：通常填零；接收方不应依赖该字段的某一固定值。

依据：[RFC 826](https://www.rfc-editor.org/rfc/rfc826.html)。

### A103

**宽带和带宽以及服务器上下行带宽**

原文：[software/network/宽带和带宽以及服务器上下行带宽/index.md](<C:/Project/blog/software/network/宽带和带宽以及服务器上下行带宽/index.md>)。

记录日期：2024-02-05T20:13:14+08:00；状态：草稿；正文已核阅；有修改意见。

#### R170

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 29 行](<C:/Project/blog/software/network/宽带和带宽以及服务器上下行带宽/index.md:29>)；待改表述／主题：` 1048576 个比特位 `。

原文定位行（节选）：` 所以，平时说的带宽有 1Mbps，指的是数据传输速率为 1 兆 bit 每秒，即一秒钟传输 1048576 个比特位。 `

问题：网络 Mbps 使用十进制兆。

建议修改：改为1 Mbps=1,000,000 bit/s；L107若单位KB按十进制，则455KB/s=3.64Mbps；若实为KiB/s，则约3.72736Mbps，明确截图软件计量方式。

依据：[NIST · metric-si-prefixes](https://www.nist.gov/pml/owm/metric-si-prefixes)。

#### R171

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 39 行](<C:/Project/blog/software/network/宽带和带宽以及服务器上下行带宽/index.md:39>)；待改表述／主题：` 2010…不到4M一概窄带 `。

原文定位行（节选）：` 宽带是一个名词，指的是带宽比较宽，因为还有一个概念——窄带，从 2010 年世界电信日(5.17)开始，带宽不到 4M 一概称为窄带，只有 4M 或以上才能被称为宽带。 `

问题：不存在跨国家、机构和时代通用的4Mbps宽带分界。

建议修改：删去“一概”的全球断言；需要阈值时注明具体机构、文件和年份。

依据：[www.itu.int · broadband](https://www.itu.int/itunews/issue/2001/06/broadband.html)。

#### R172

**事实/技术错误 · 概念混淆 · P2**

定位：[原文第 73 行](<C:/Project/blog/software/network/宽带和带宽以及服务器上下行带宽/index.md:73>)；待改表述／主题：` 吞吐量…req/s…不会超过带宽 `。

原文定位行（节选）：` 也就是说，这是两个指标，一个带宽不大的服务器，由于各方面优化的很到位，也可以拥有比较大的吞吐量（但不会超过带宽这个硬性的上限）。 `

问题：req/s是应用吞吐量；网络吞吐率按bit/s计。不同量纲不能直接比较。

建议修改：分开定义应用请求吞吐量与网络吞吐率；给定每请求数据量后才可估算带宽上限。

依据：[RFC 1242](https://www.rfc-editor.org/rfc/rfc1242.html)。

### A104

**局域网和以太网**

原文：[software/network/局域网和以太网/index.md](<C:/Project/blog/software/network/局域网和以太网/index.md>)。

记录日期：2024-06-10T16:02:16+08:00；状态：正文已核阅；有修改意见。

#### R173

**事实/技术错误 · 事实/字词错误 · P2**

定位：[原文第 63 行](<C:/Project/blog/software/network/局域网和以太网/index.md:63>)；待改表述／主题：` 1887…证明以太并不存在 `。

原文定位行（节选）：` 1887 年，物理学家迈克尔逊和爱德华·莫立证明了以太并不存在，但梅特卡夫认为以太这个名字很适合描述这个可以传递信号给计算机的新网络系统。 `

问题：实验没有检测到预期的以太风，单次实验不能概括成直接证明所有以太理论不存在。人名拼写也有误。

建议修改：改为“迈克耳孙—莫雷实验未检测到预期的以太风”；L49人名改 Robert Melancton Metcalfe；L57短矩离→短距离，L83同轴电联→同轴电缆。

依据：[美国物理学会历史资料 · Michelson](https://history.aip.org/exhibits/gap/Michelson/Michelson.html)；[ACM 图灵奖资料 · metcalfe_3968159.cfm](https://amturing.acm.org/award_winners/metcalfe_3968159.cfm)。

#### R174

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 91 行](<C:/Project/blog/software/network/局域网和以太网/index.md:91>)；待改表述／主题：` 没有必要再使用MAC协议（Multiple Access Control） `。

原文定位行（节选）：` 现代交换机是全双工的，并且每个端口的帧会被交换机准确的发送到目的地，所以并不会产生碰撞，也就没有必要再使用 MAC 协议了（Multiple Access Control，多路访问控制）。 `

问题：MAC 通常展开为 Media Access Control；全双工交换以太网不需要CSMA/CD争用，但仍有MAC子层、地址和帧格式。

建议修改：改为：全双工点对点链路不发生碰撞，无需CSMA/CD；MAC机制仍存在。

依据：[www.cisco.com · tr1904](https://www.cisco.com/en/US/docs/internetworking/troubleshooting/guide/tr1904.html)。

### A105

**GoAccess可视化Nginx日志**

原文：[software/nginx/GoAccess可视化Nginx日志/index.md](<C:/Project/blog/software/nginx/GoAccess可视化Nginx日志/index.md>)。

记录日期：2025-11-26T10:18:12；状态：正文已核阅；有修改意见。

#### R175

**事实/技术错误 · 配置复制错误 · P2**

定位：[原文第 219 行](<C:/Project/blog/software/nginx/GoAccess可视化Nginx日志/index.md:219>)；待改表述／主题：` 三个站点的try_files都指向第一份报告 `。

原文定位行（节选）：` try_files /report-djhx.site.html =404; `

问题：foo和bar的HTML入口仍读取report-djhx.site.html，与各自ExecStart生成的报告名不一致。

建议修改：219行改/report-foo.djhx.site.html；233行改/report-bar.djhx.site.html；逐一对应生成路径与HTML入口。

依据：[NGINX 官方文档 · ngx_http_core_module · try_files](https://nginx.org/en/docs/http/ngx_http_core_module.html#try_files)。

### A106

**Nginx上传文件大小的限制**

原文：[software/nginx/Nginx上传文件大小的限制/index.md](<C:/Project/blog/software/nginx/Nginx上传文件大小的限制/index.md>)。

记录日期：2025-07-21T10:20:00+08:00；状态：正文已核阅；有修改意见。

#### R176

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 58 行](<C:/Project/blog/software/nginx/Nginx上传文件大小的限制/index.md:58>)；待改表述／主题：` 必须加单位…否则单位是字节 `。

原文定位行（节选）：`` `client_max_body_size` 必须加单位（如 M、K），否则单位是字节； ``

问题：两句话互相矛盾；Nginx 允许不带单位的字节数。

建议修改：改为：可用字节数，或k/m后缀；0表示关闭该检查；配置修改一般reload即可，无需必须重启。

依据：[NGINX 官方文档 · ngx_http_core_module · client_max_body_size](https://nginx.org/en/docs/http/ngx_http_core_module.html#client_max_body_size)。

### A107

**Nginx中proxy_pass的斜杠问题**

原文：[software/nginx/Nginx中proxy_pass的斜杠问题/index.md](<C:/Project/blog/software/nginx/Nginx中proxy_pass的斜杠问题/index.md>)。

记录日期：2023-12-23T11:38:33+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A108

**Nginx中的sites Enabled和sites Available**

原文：[software/nginx/Nginx中的sites Enabled和sites Available/index.md](<C:/Project/blog/software/nginx/Nginx中的sites Enabled和sites Available/index.md>)。

记录日期：2024-02-08T10:08:50+08:00；状态：正文已核阅；有修改意见。

#### R177

**事实/技术错误 · 配置错误 · P2**

定位：[原文第 46 行](<C:/Project/blog/software/nginx/Nginx中的sites Enabled和sites Available/index.md:46>)；待改表述／主题：` include /etc/nginx/conf.d/*.conf `。

原文定位行（节选）：` include /etc/nginx/conf.d/*.conf `

问题：缺少指令末尾的分号。

建议修改：改为 include /etc/nginx/conf.d/*.conf;；L79“所有”改“所以”。

依据：[NGINX 官方文档 · ngx_core_module · include](https://nginx.org/en/docs/ngx_core_module.html#include)。

### A109

**Nginx的基础用法**

原文：[software/nginx/Nginx的基础用法/index.md](<C:/Project/blog/software/nginx/Nginx的基础用法/index.md>)。

记录日期：2023-08-05T09:53:00+08:00；状态：正文已核阅；有修改意见。

#### R178

**事实/技术错误 · 概念混淆 · P2**

定位：[原文第 43 行](<C:/Project/blog/software/nginx/Nginx的基础用法/index.md:43>)；待改表述／主题：` Servlet…交互协议 `。

原文定位行（节选）：` Client 和 Web Server 的交互信息是基于 HTTP 协议，那么 Web Server 和 Application Server 的交互也拥有自己的协议，最早的是叫 CGI（Common Gateway Interface），后来的改进版 FastCGI，基于 Java 的 Servlet（Server Applet），基于 Python 的 WSGI（Web Server Gateway Interface）。 `

问题：Servlet与WSGI是程序接口规范，不能与FastCGI一概当成网络通信协议。

建议修改：分别说明API/调用接口与进程间或网络协议；Web服务器也能通过模块/CGI处理动态内容，避免“力不从心”被理解为不支持动态内容。

依据：[Jakarta 规范 · 6.0](https://jakarta.ee/specifications/servlet/6.0/)；[Python PEP · pep-3333](https://peps.python.org/pep-3333/)。

#### R179

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 81 行](<C:/Project/blog/software/nginx/Nginx的基础用法/index.md:81>)；待改表述／主题：` 默认日志存在…没有起作用 `。

原文定位行（节选）：` 5. 重新打开 Nginx 的日志文件：Nginx -s reopen，该命令的作用是：当 Nginx 默认的日志文件没有的时候（被人挪走或改了名字），该命令会重新创建一个默认的 Nginx 日志文件，后续日志会写的刚创建的默认日志路径中。因此当 Nginx 默认的日志文件存在的时候，该命令没有起做用。 `

问题：reopen 会重新打开配置的日志文件，且可调整日志文件所有者；并非存在时无操作。

建议修改：写为：常用于日志轮转后让worker切换到新日志文件；reload为重载配置。

依据：[NGINX 官方文档 · control](https://nginx.org/en/docs/control.html)。

#### R180

**字词/链接 · 字词/链接错误 · P3**

定位：[原文第 121 行](<C:/Project/blog/software/nginx/Nginx的基础用法/index.md:121>)；待改表述／主题：` 192.168.41.180.80；imags；做用 `。

原文定位行（节选）：` * [http://192.168.41.180.80/linux/tutorial.html](http://192.168.41.180.80/linux/tutorial.html) `

问题：端口前应是冒号，images和作用拼错；L147URL含中文。

建议修改：改为192.168.41.180:80、images、作用；删链接目标中的“，但是默认”。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R181

**事实/技术错误 · 概念错误 · P2**

定位：[原文第 222 行](<C:/Project/blog/software/nginx/Nginx的基础用法/index.md:222>)；待改表述／主题：` 浏览器就是…正向代理 `。

原文定位行（节选）：` Nginx 的另一个常用的功能是反向代理，既然有反向代理，就有正向代理，正向代理面向的是用户，一个经典实例就是常用的浏览器，浏览器帮助我们解决 HTTP 协议的编解码，以及收到响应后的页面渲染，浏览器就是我们用户的正向代理，是架设在我们和网络内容之间的桥梁。 `

问题：浏览器通常是HTTP客户端，正向代理是替客户端转发请求的中间服务。

建议修改：用浏览器→正向代理→目标站点举例；反向代理隐藏上游只是拓扑效果，不能直接保证安全。

依据：[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#name-intermediaries)。

### A110

**SpringBoot埋点**

原文：[software/observability/SpringBoot埋点/index.md](<C:/Project/blog/software/observability/SpringBoot埋点/index.md>)。

记录日期：2026-07-01T16:36:41；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A111

**可观测性的概念**

原文：[software/observability/可观测性的概念/index.md](<C:/Project/blog/software/observability/可观测性的概念/index.md>)。

记录日期：2026-06-15T16:59:05；状态：草稿；正文已核阅；有修改意见。

#### R182

**字词/链接 · 字词错误 · P3**

定位：[原文第 81 行](<C:/Project/blog/software/observability/可观测性的概念/index.md:81>)；待改表述／主题：` 所有，建立；顺势状态 `。

原文定位行（节选）：` 所有，建立一个好的告警体系，首先需要了解实际用户接触的业务流程，要看用户依赖什么，针对这些方面优先建立告警，比如：支付、登录、下单是否能够成功，数据是否正确，响应延迟等。 `

问题：分别应为“所以，建立”“瞬时状态”（L101）。

建议修改：按这两处修改。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A112

**日志的结构化和分析**

原文：[software/observability/日志的结构化和分析/index.md](<C:/Project/blog/software/observability/日志的结构化和分析/index.md>)。

记录日期：2026-08-18T11:09:40；状态：正文已核阅；有修改意见。

#### R183

**事实/技术错误 · 术语错误 · P2**

定位：[原文第 76 行](<C:/Project/blog/software/observability/日志的结构化和分析/index.md:76>)；待改表述／主题：` 传统日志（Common Log Format, CLF） `。

原文定位行（节选）：` 非结构化就是传统的日志（Common Log Format, CLF），也就是上一节提到的案例。 `

问题：CLF 是特定的HTTP访问日志格式，并非任意纯文本应用日志的总称。

建议修改：改为自由格式文本日志；若介绍CLF，使用它的标准字段和示例。

依据：[httpd.apache.org · logs · common](https://httpd.apache.org/docs/2.4/logs.html#common)。

#### R184

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 140 行](<C:/Project/blog/software/observability/日志的结构化和分析/index.md:140>)；待改表述／主题：` 所有日志记录必填字段 `。

原文定位行（节选）：` 顶层字段必须要在所有记录中具有相同的语义，也是所有日志记录必填字段，例如：时间戳、日志级别等。 `

问题：OTel data model 明确顶层字段均为可选；语义统一不意味着每条记录都有值。

建议修改：改为：顶层字段有固定语义，缺失或无效时按规范处理；应用可以另外制定自己的必填字段规范。

依据：[opentelemetry.io · data-model](https://opentelemetry.io/docs/specs/otel/logs/data-model/)。

#### R185

**字词/链接 · 字词/格式错误 · P3**

定位：[原文第 177 行](<C:/Project/blog/software/observability/日志的结构化和分析/index.md:177>)；待改表述／主题：` protobub；(python-json-logger)[…] `。

原文定位行（节选）：` 为了实现 json 格式化，可以自己手动实现一个formatter,也可引入第三方的依赖——(python-json-logger)[https://pypi.org/project/python-json-logger/]。 `

问题：应为protobuf；Markdown链接括号方向错误；L11“触发”应为“出发”。

建议修改：改为Protobuf；链接改为 [python-json-logger](https://pypi.org/project/python-json-logger/)；“身体”译为日志正文（L155）。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A113

**SeaweedFS的搭建和示例**

原文：[software/oss/SeaweedFS的搭建和示例/index.md](<C:/Project/blog/software/oss/SeaweedFS的搭建和示例/index.md>)。

记录日期：2026-02-28T16:14:09；状态：正文已核阅；有修改意见。

#### R186

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 40 行](<C:/Project/blog/software/oss/SeaweedFS的搭建和示例/index.md:40>)；待改表述／主题：` 一个服务挂了不影响另外一个 `。

原文定位行（节选）：` 每个服务可以单独启动，也就是多个 service 文件，这样的好处是方便横向扩展，一个服务挂了不影响另外一个服务，具体步骤和 service 文件可以参考：[https://blog.csdn.net/weixin_51476622/article/details/148948939](https://blog.csdn.net/weixin_51476622/article/details/148948939) `

问题：进程独立不等于业务独立；filer/s3/volume/master之间存在依赖。

建议修改：改为：独立进程可单独管理和扩容，但某组件故障仍可能影响存储读写；需按组件和副本策略讨论可用性。

依据：[仓库源码：seaweedfs/seaweedfs · Components](https://github.com/seaweedfs/seaweedfs/wiki/Components)。

#### R187

**事实/技术错误 · 术语错误 · P2**

定位：[原文第 178 行](<C:/Project/blog/software/oss/SeaweedFS的搭建和示例/index.md:178>)；待改表述／主题：` aws 配置用户名和密码 `。

原文定位行（节选）：`` aws 配置用户名和密码，就是刚刚的 `s3.json` 里配置的用户： ``

问题：aws configure 的对应项是 Access Key ID / Secret Access Key，不是identities的name与密码。

建议修改：明确填s3.json.credentials中的accessKey/secretKey，不把用户名称当成Access Key。

依据：[仓库源码：seaweedfs/seaweedfs · Amazon-S3-API](https://github.com/seaweedfs/seaweedfs/wiki/Amazon-S3-API)。

### A114

**C的整型类型和占用大小**

原文：[software/program/c/C的整型类型和占用大小/index.md](<C:/Project/blog/software/program/c/C的整型类型和占用大小/index.md>)。

记录日期：2025-01-04T09:01:30+08:00；状态：草稿；正文已核阅；有修改意见。

#### R188

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 36 行](<C:/Project/blog/software/program/c/C的整型类型和占用大小/index.md:36>)；待改表述／主题：` Java…所有整型都是有符号 `。

原文定位行（节选）：` 不同的资料对于 C 的数据类型的说法都不尽相同，这是最开始让人很困惑的一点，因为它存在一些范围和底层机器硬件是相关的，不同于 Java 的强数据类型，在 Java 中，整型的范围和运行 Java 代码的机器无关，Java 的每个整型类型，在不同的机器上都是一致的（byte：1 字节，short：2 字节，int：4 字节，long：8 字节），并且 Java 不存在无符号（unsigned）的整型类型，所有整型都是有符号类型。 `

问题：Java 的 char 也是整数类型，是无符号16位UTF-16码元。

建议修改：限定byte/short/int/long为有符号；char范围0～65535。

依据：[Oracle／Java 官方文档 · jls-4](https://docs.oracle.com/javase/specs/jls/se17/html/jls-4.html)。

#### R189

**条件/版本澄清 · 实现/标准条件 · P2**

定位：[原文第 81 行](<C:/Project/blog/software/program/c/C的整型类型和占用大小/index.md:81>)；待改表述／主题：` unsigned 0-255；signed -128-127 `。

原文定位行（节选）：` 如果指定 unsigned 修饰符，那么范围就是 0 - 255，如果是 signed 修饰符，范围就是 -128 - 127，而 ASCII 的范围是 0 - 127，所以当使用 char 来表示，无论是 unsigned 还是 signed 都没问题。 `

问题：C char 为1个C字节，CHAR_BIT不一定8；旧标准signed char表示法也不能无条件断言-128。

建议修改：说明这些范围以CHAR_BIT=8、二补码有符号表示为前提。plain char、signed char、unsigned char是三个不同类型；plain char的符号性由实现决定。引用旧标准时保留其允许的表示差异。

依据：[www.open-std.org · n1570.pdf](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

#### R190

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 94 行](<C:/Project/blog/software/program/c/C的整型类型和占用大小/index.md:94>)；待改表述／主题：` 高位会被截掉 `。

原文定位行（节选）：` 这里的 'A' 就是字符常量，神奇的是，字符常量的类型总是 int，也就是说，'A' 对应的 65 是存储在 32 位（或者 16 位）的存储单元中，但是赋值的变量是 char 类型，32 位或者 16 位的字符常量存到 8 位的 char 类型的变量后，高位会被截掉，仅仅保留下了低 8 位（1 字节）的内容。 `

问题：数值转换不是普遍意义的“按位截断”；超出有符号类型范围时旧C标准结果依实现。

建议修改：区分代表ASCII A的值转换与超范围转换；写明目标编译器/标准版本；L75“却决”改“取决”。

依据：[www.open-std.org · n1570.pdf](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)。

### A115

**IDEA断点调试技巧**

原文：[software/program/java/IDEA断点调试技巧/index.md](<C:/Project/blog/software/program/java/IDEA断点调试技巧/index.md>)。

记录日期：2023-05-20T11:28:08+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A116

**Java中的比较和排序**

原文：[software/program/java/Java中的比较和排序/index.md](<C:/Project/blog/software/program/java/Java中的比较和排序/index.md>)。

记录日期：2021-05-27T12:04:15+08:00；状态：正文已核阅；有修改意见。

#### R191

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 27 行](<C:/Project/blog/software/program/java/Java中的比较和排序/index.md:27>)；待改表述／主题：` 未实现Comparable…TimSort `。

原文定位行（节选）：`` 2. 如果容器存储的是非自然排序的引用类型元素（即未实现 `Comparable` 接口），底层采用 “`TimSort`”。 ``

问题：选择TimSort还是ComparableTimSort取决于是否传入Comparator，不由类是否实现Comparable单独决定。

建议修改：将分类改为：按自然顺序/未传比较器与显式传比较器；同一类可走两种排序；算法描述注明所查OpenJDK版本。

依据：[仓库源码：openjdk/jdk8u · Arrays.java](https://github.com/openjdk/jdk8u/blob/master/jdk/src/share/classes/java/util/Arrays.java)。

#### R192

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 327 行](<C:/Project/blog/software/program/java/Java中的比较和排序/index.md:327>)；待改表述／主题：` Number 类型的 compareTo `。

原文定位行（节选）：`` 可以看出，`Number` 类型的 `compareTo` 都很直观，比较值的大小即可。但其他的类，就需要人为的定义规则了，比如日期是按照年、月、日顺序依次排序，字符串是按照字符（`String` 的底层是数组，JDK1.8 以及之前都是 char 数组，JDK1.9 之后是 byte 数组）逐个比较。 ``

问题：Number 基类没有compareTo，也不实现Comparable；Integer、Double等具体类实现。

建议修改：改为Integer/Double等数值包装类；自然顺序不是必然按某个数值升序，是类型定义的排序规则。

依据：[Oracle／Java 官方文档 · Number](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Number.html)。

#### R193

**字词/链接 · 字词错误 · P3**

定位：[原文第 460 行](<C:/Project/blog/software/program/java/Java中的比较和排序/index.md:460>)；待改表述／主题：` 简答；Array.sort；先，；不在赘述 `。

原文定位行（节选）：`` 不管是覆写还是直接继承，我们看到 `List.sort` 的方法内部还是调用了一开始就讲过的 `Arrays.sort()`，兜了一圈，又绕回到这个工具类了。`Array.sort()` 对于对象排序总共有四个重载方法： ``

问题：应为简单、Arrays.sort；L445末尾“先，”是残留；L763为不再。

建议修改：按以上位置修正。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A117

**Java基础之I／O流**

原文：[software/program/java/Java基础之I／O流/index.md](<C:/Project/blog/software/program/java/Java基础之I／O流/index.md>)。

记录日期：2023-02-18T14:55:18+08:00；状态：草稿；正文已核阅；有修改意见。

#### R194

**事实/技术错误 · 术语错误 · P2**

定位：[原文第 27 行](<C:/Project/blog/software/program/java/Java基础之I／O流/index.md:27>)；待改表述／主题：` NIO…Non-Blocking Input/Output `。

原文定位行（节选）：` 在 2002 年，NIO 伴随着 JDK1.4 发布，提供了 Non-Blocking Input/Output。 `

问题：NIO原意为New I/O，包含buffer/channel/selector等；部分channel支持非阻塞，不代表全部非阻塞。

建议修改：改为New I/O；明确FileChannel不提供这种非阻塞模式。

依据：[Oracle／Java 官方文档](https://docs.oracle.com/javase/8/docs/technotes/guides/io/index.html)。

#### R195

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 660 行](<C:/Project/blog/software/program/java/Java基础之I／O流/index.md:660>)；待改表述／主题：` Java…使用UTF-16…本地字符集 `。

原文定位行（节选）：` Java 平台使用 Unicode 存储字符，准确的说是使用 UTF-16 编码。字符流会自动将原始字节与本地字符集相互转换。关于 Unicode 的讲解，可以参考我之前的文章：[https://korilweb.cn/tech/%E8%81%8A%E8%81%8Aunicodeutf-8utf-16%E4%BB%A5%E5%8F%8Autf-32%E7%9A%84%E9%82%A3%E4%BA%9B%E4%BA%8B%E5%84%BF/](https://korilweb.… `

问题：char/Reader的逻辑单位为UTF-16码元；String物理存储和文件默认字符集并非一律UTF-16或本地字符集。

建议修改：按Java版本说明：Java9后compact strings可用字节数组，Java18后默认字符集通常UTF-8；文件读写建议显式指定编码。

依据：[仓库源码：openjdk/jdk · String.java](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/lang/String.java)；[Oracle／Java 官方文档 · Charset](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/charset/Charset.html)。

### A118

**Java基础之文件操作**

原文：[software/program/java/Java基础之文件操作/index.md](<C:/Project/blog/software/program/java/Java基础之文件操作/index.md>)。

记录日期：2023-02-18T14:55:48+08:00；状态：草稿；正文已核阅；有修改意见。

#### R196

**条件/版本澄清 · 字词/版本条件 · P2**

定位：[原文第 19 行](<C:/Project/blog/software/program/java/Java基础之文件操作/index.md:19>)；待改表述／主题：` 文档系统；Path.of `。

原文定位行（节选）：`` `Path` 是在 Java NIO2 更新时加入的（Java SE7），完全限定名称是：`java.nio.file.Path`。`Path` 用来表示文档系统中的路径。路径可以指向文档或目录。路径可以是绝对路径，也可以是相对路径。 ``

问题：文件系统不应写成文档系统；Path.of实际从Java11引入，接口从Java8支持静态方法不等于该API在Java8已存在。

建议修改：19、21行等文档系统/文档按语境改文件系统/文件；兼容性段明确Path.of要求Java11及以上。

依据：[Oracle／Java 官方文档 · Path · of(java.lang.String,java.lang.String...)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/nio/file/Path.html#of(java.lang.String,java.lang.String...))。

#### R197

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 134 行](<C:/Project/blog/software/program/java/Java基础之文件操作/index.md:134>)；待改表述／主题：` Path为空…返回当前Path `。

原文定位行（节选）：`` 1. 给定的 `Path` 为空，则返回当前 `Path`。 ``

问题：这里是empty path，不是null；null会抛NullPointerException。

建议修改：改为：参数表示空路径时返回原路径；参数为null会抛异常。

依据：[Oracle／Java 官方文档 · Path · resolve(java.nio.file.Path)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/nio/file/Path.html#resolve(java.nio.file.Path))。

#### R198

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 393 行](<C:/Project/blog/software/program/java/Java基础之文件操作/index.md:393>)；待改表述／主题：` 成功返回true，否则false `。

原文定位行（节选）：`` 和返回 void 的 delete 不同，`deleteIfExists` 返回一个布尔值，成功删除文件返回 true，否则返回 false，文件不存在，不会抛出异常。当有多个线程删除文件并且您不想仅仅因为一个线程先这样做而抛出异常时，静默失败（不抛异常）很有用。 ``

问题：false只表示文件不存在，权限/非空目录/其他I/O错误仍会抛异常。

建议修改：改为：删除成功true，不存在false；其余失败按异常处理。

依据：[Oracle／Java 官方文档 · Files · deleteIfExists(java.nio.file.Path)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/nio/file/Files.html#deleteIfExists(java.nio.file.Path))。

#### R199

**事实/技术错误 · 字词/代码错误 · P2**

定位：[原文第 538 行](<C:/Project/blog/software/program/java/Java基础之文件操作/index.md:538>)；待改表述／主题：` readAllByte；SKIP_SIBLING；BasicFileAttribute `。

原文定位行（节选）：` 3. 访问目录下的文件的操作：访问文件时调用，文件的 BasicFileAttribute 会传入该方法。 `

问题：正确名称分别为readAllBytes、SKIP_SIBLINGS、BasicFileAttributes（L610/L538）。

建议修改：修正名称；L603加入→假如，L409c:\User→与前文一致的C:\Users；文件系统不要译成文档系统。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A119

**Java基础之注解**

原文：[software/program/java/Java基础之注解/index.md](<C:/Project/blog/software/program/java/Java基础之注解/index.md>)。

记录日期：2023-09-09T11:13:55+08:00；状态：正文已核阅；有修改意见。

#### R200

**字词/链接 · 字词错误 · P3**

定位：[原文第 112 行](<C:/Project/blog/software/program/java/Java基础之注解/index.md:112>)；待改表述／主题：` SuppressWarning `。

原文定位行（节选）：`` Java 平台提供了一些官方注解，定义在 `java.lang` 包和 `java.lang.annotation` 包中。在之前的实例中，`Override` 和 `SuppressWarning` 都属于官方注解。当然也可以定义自己的注解，前面示例中的 `Author` 和 `EBook` 就属于自定义注解类型。 ``

问题：官方注解为SuppressWarnings。

建议修改：补末尾s；示例注解也同步检查。

依据：[Oracle／Java 官方文档 · SuppressWarnings](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/SuppressWarnings.html)。

### A120

**Java的异常和异常处理**

原文：[software/program/java/Java的异常和异常处理/index.md](<C:/Project/blog/software/program/java/Java的异常和异常处理/index.md>)。

记录日期：2023-09-02T09:09:37+08:00；状态：正文已核阅；有修改意见。

#### R201

**字词/链接 · 字词错误 · P3**

定位：[原文第 74 行](<C:/Project/blog/software/program/java/Java的异常和异常处理/index.md:74>)；待改表述／主题：` 早上的；推出；抱错；列子；一推；再合适 `。

原文定位行（节选）：`` 因为我们自己失误早上的异常，比如打电话，电话号码拨错了，这个异常就像是后面将要介绍的 `RuntimeException`，通常发生在 API 调用错误，或者参数错误，由程序员个人的编码不细致和粗心造成的。 ``

问题：分别应为造成的、退出、报错、例子、一堆、在合适（L396/L549/L765/L862/L937）。

建议修改：并统一try-with-resources（复数），修正FileReader/FileWriter示例描述不一致（L347）。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R202

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 112 行](<C:/Project/blog/software/program/java/Java的异常和异常处理/index.md:112>)；待改表述／主题：` 运行时系统将终止 `。

原文定位行（节选）：` foo 方法因为包含了对 tar 方法抛出的异常的处理器，可以称，foo 方法捕获了一个异常（catch the exception）。如果运行时系统，找遍了整个调用方法栈都没有发现合适的异常处理器，运行时系统将终止（terminate）。 `

问题：未捕获异常通常终止当前线程；不一定终止整个JVM/进程。

建议修改：改为：交给线程的未捕获异常处理器后，该线程终止；是否导致JVM退出取决于其他非守护线程等。

依据：[Oracle／Java 官方文档 · jls-11](https://docs.oracle.com/javase/specs/jls/se17/html/jls-11.html)。

#### R203

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 222 行](<C:/Project/blog/software/program/java/Java的异常和异常处理/index.md:222>)；待改表述／主题：` FileWrite…不存在的文件名…IOException `。

原文定位行（节选）：`` 第一个异常，FileWrite 构造函数如果给定了不存在的文件名，或者文件无法打开，会抛出 `IOException` 异常，该异常为受检异常。 ``

问题：FileWriter通常会创建不存在的目标文件；父目录不存在、无权限等才会失败。

建议修改：改为：目标是目录、父路径不存在或无写权限等会抛IOException；名称FileWrite改FileWriter。

依据：[Oracle／Java 官方文档 · FileWriter](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/FileWriter.html)。

#### R204

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 274 行](<C:/Project/blog/software/program/java/Java的异常和异常处理/index.md:274>)；待改表述／主题：` 每个try…至少一个catch `。

原文定位行（节选）：` 仅仅用 try 块包裹，还不够，因为我们必须提供受检异常的异常处理器，放在 catch 块中，也就是说，每个 try 块至少跟着一个 catch 块。 `

问题：try-finally可以没有catch；try-with-resources也可以没有catch。受检异常还可以由throws传播。

建议修改：限定当前需要在本方法处理IOException的示例，不当作Java语法通则。

依据：[Oracle／Java 官方文档 · jls-14 · jls-14.20](https://docs.oracle.com/javase/specs/jls/se17/html/jls-14.html#jls-14.20)。

#### R205

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 496 行](<C:/Project/blog/software/program/java/Java的异常和异常处理/index.md:496>)；待改表述／主题：` 总是与throw语句一起引发 `。

原文定位行（节选）：` 但在捕获异常之前，某处的某些代码必须抛出异常。任何代码都可能引发异常：自己的代码、其他人编写的包中的代码，例如 Java 平台附带的包或 Java 运行时环境。无论什幺引发异常，它总是与 throw 语句一起引发。 `

问题：空指针、数组越界等可由JVM隐式抛出，不需要源码出现throw。

建议修改：改为：异常可显式throw或由表达式求值/JVM检测隐式产生。

依据：[Oracle／Java 官方文档 · jls-11](https://docs.oracle.com/javase/specs/jls/se17/html/jls-11.html)。

#### R206

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 771 行](<C:/Project/blog/software/program/java/Java的异常和异常处理/index.md:771>)；待改表述／主题：` 没法…任何恢复…无法继续 `。

原文定位行（节选）：`` 空指针异常（`NullPointerException`）和除零异常（`ArithmeticException`）还有下标越界异常（`IndexOutOfBoundsException`）都是典型的 `RuntimeException`，我们没法从异常中，做出任何恢复行为，也无法继续执行下去了。 ``

问题：RuntimeException可捕获并让外层请求、任务或线程继续；“不应该恢复”是设计判断而非语言限制。

建议修改：改为：通常应修正调用/逻辑错误；有明确边界时可以隔离失败任务，不能称无法恢复。

依据：[Oracle／Java 官方文档 · jls-11](https://docs.oracle.com/javase/specs/jls/se17/html/jls-11.html)。

#### R207

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 963 行](<C:/Project/blog/software/program/java/Java的异常和异常处理/index.md:963>)；待改表述／主题：` FileNotFoundException没有后代 `。

原文定位行（节选）：`` 方法中可以针对特定的异常编写的特定的处理代码。`FileNotFoundException` 类没有后代，因此以下处理代码只能处理一种类型的异常： ``

问题：它不是final，用户可以继承，catch也会匹配其子类。Exception不是Throwable层级的顶端（L999）。

建议修改：改为：捕获FileNotFoundException及其子类；Throwable为顶层，Exception和Error是不同分支。

依据：[Oracle／Java 官方文档 · FileNotFoundException](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/FileNotFoundException.html)。

### A121

**Java获取两个时间的间隔天数**

原文：[software/program/java/Java获取两个时间的间隔天数/index.md](<C:/Project/blog/software/program/java/Java获取两个时间的间隔天数/index.md>)。

记录日期：2023-12-23T11:37:26+08:00；状态：正文已核阅；有修改意见。

#### R208

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 97 行](<C:/Project/blog/software/program/java/Java获取两个时间的间隔天数/index.md:97>)；待改表述／主题：` 时间戳相减除86400…正确 `。

原文定位行（节选）：`` 第一种，就是上面提到的，将 `LocalDate` 转换成对应的时间戳，相减，然后除以 86400 得到天数。 ``

问题：当地日期间隔遇到夏令时可含23/25小时；日期差与完整24小时段数不相同。

建议修改：固定无夏令时偏移下、两端均为当天零点时可得到示例结果；任意systemDefault时区并不保证。日期差优先ChronoUnit.DAYS.between(LocalDate,LocalDate)或toEpochDay差值；区分日期差和持续时间。

依据：[Oracle／Java 官方文档 · Period](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/Period.html)；[Oracle／Java 官方文档 · Duration](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/Duration.html)。

### A122

**跨平台的概念**

原文：[software/program/java/跨平台的概念/index.md](<C:/Project/blog/software/program/java/跨平台的概念/index.md>)。

记录日期：2026-07-18T15:13:01；状态：正文已核阅；有修改意见。

#### R209

**字词/链接 · 字词错误 · P3**

定位：[原文第 15 行](<C:/Project/blog/software/program/java/跨平台的概念/index.md:15>)；待改表述／主题：` 指的是是；加入；平台放上 `。

原文定位行（节选）：` 平台（Platform）可以指的是是硬件（CPU）平台，也可以是软件（OS）平台。硬件层面，CPU 有 ARM 架构和 X86 架构以及 RISC-V 架构，软件层面，操作系统有 Windows、Linux、MacOS、Android、iOS 等等。 `

问题：删重复是；L41加入→假如；L25→各个平台上运行。

建议修改：按这几处修改。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A123

**cachetools的使用**

原文：[software/program/python/cachetools的使用/index.md](<C:/Project/blog/software/program/python/cachetools的使用/index.md>)。

记录日期：2026-08-09T14:12:17；状态：草稿；正文已核阅；有修改意见。

#### R210

**字词/链接 · 字词错误 · P3**

定位：[原文第 276 行](<C:/Project/blog/software/program/python/cachetools的使用/index.md:276>)；待改表述／主题：` 冷问 `。

原文定位行（节选）：` 但是对于 LRU 而言，因为今年这个产品没有被访问过了（最后一次访问时间是在去年），那么该产品的重要性就远远低于一个刚刚被访问的冷问产品（历史访问次数可能非常少）。 `

问题：错字。

建议修改：改为冷门。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R211

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 341 行](<C:/Project/blog/software/program/python/cachetools的使用/index.md:341>)；待改表述／主题：` 一旦TTL到期…被删除 `。

原文定位行（节选）：` TTL 没有热点的概念，不管某个产品数据最近是否被频繁访问，历史访问频次是否最多，一旦 TTL 到期了，就会被删除，这种特性适合一些拥有固定生命周期的缓存数据，比如验证码之类的。 `

问题：TTLCache过期后不可访问，但底层内存可以直到修改操作或expire才被释放。

建议修改：改为逻辑过期与实际清除分离；并说明TTLCache和TLRUCache也含LRU容量淘汰策略。

依据：[cachetools.readthedocs.io](https://cachetools.readthedocs.io/en/stable/)。

### A124

**PEP282-日志系统-译文**

原文：[software/program/python/PEP282-日志系统-译文/index.md](<C:/Project/blog/software/program/python/PEP282-日志系统-译文/index.md>)。

记录日期：2025-07-05T14:00:00+08:00；状态：正文已核阅；有修改意见。

#### R212

**字词/链接 · 字词错误 · P3**

定位：[原文第 268 行](<C:/Project/blog/software/program/python/PEP282-日志系统-译文/index.md:268>)；待改表述／主题：` setlevel；对象门；配制；版本呢；(asctime)s `。

原文定位行（节选）：`` 当创建新的 `Logger` 时，它们会以表示“无级别”（no level）的级别进行初始化。可以使用 setlevel（）方法明确设置级别： ``

问题：应为setLevel、对象们、配置、版本；格式占位符缺%。

建议修改：L134/L190对象门→对象们；L136配制→配置；L27删除呢；L363补为%(asctime)s。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R213

**事实/技术错误 · 版本/事实说明 · P2**

定位：[原文第 383 行](<C:/Project/blog/software/program/python/PEP282-日志系统-译文/index.md:383>)；待改表述／主题：` 附加到根Logger的Filter `。

原文定位行（节选）：`` 默认行为允许使用 `Logger` 名称初始化 `Filter`。这将仅允许通过使用指定名称的 `Logger` 或其任何子 `Logger` 生成的事件。例如，使用“`A.B`”初始化的 `Filter` 将允许由“`A.B`”、“`A.B.C`”、“`A.B.C.D`”、“`A.B.D`”等 `Logger` 记录的事件，但不允许“`A.BB`”、“`B.A.B`”等 `Logger` 记录的事件。如果使用空字符串进行初始化，则 `Filter` 将允许所有事件通过。这种… ``

问题：原PEP保留该表述，但现代logging不会对从子logger传播的record执行祖先logger的filter。

建议修改：译文保留历史原文，加译者注：全局过滤应把Filter放到root的Handler；setRollover同样注明是历史提案API。

依据：[Python 官方文档 · logging](https://docs.python.org/3/library/logging.html)；[Python PEP · pep-0282](https://peps.python.org/pep-0282/)。

### A125

**Python中的多线程编程**

原文：[software/program/python/Python中的多线程编程/index.md](<C:/Project/blog/software/program/python/Python中的多线程编程/index.md>)。

记录日期：2024-11-24T09:12:14+08:00；状态：草稿；空提纲／参考资料；无实质技术正文。

只有提纲、前言标题或参考链接，缺少可核实的技术正文。本轮不把这种空提纲计作内容正确的技术文章。

### A126

**Python使用SMTP发送邮件**

原文：[software/program/python/Python使用SMTP发送邮件/index.md](<C:/Project/blog/software/program/python/Python使用SMTP发送邮件/index.md>)。

记录日期：2025-07-02T11:26:00+08:00；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A127

**Python压缩JPEG图片**

原文：[software/program/python/Python压缩JPEG图片/index.md](<C:/Project/blog/software/program/python/Python压缩JPEG图片/index.md>)。

记录日期：2023-05-20T10:41:51+08:00；状态：正文已核阅；有修改意见。

#### R214

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 48 行](<C:/Project/blog/software/program/python/Python压缩JPEG图片/index.md:48>)；待改表述／主题：` Defaults to80…For lossless…effort `。

原文定位行（节选）：` > Integer, 0-100, Defaults to 80. For lossy, 0 gives the smallest size and 100 the largest. For lossless, this parameter is the amount of effort put into the compression: 0 is the fastest, but gives larger files compared to the slowest, but… `

问题：引用的是WebP参数而不是JPEG；JPEG默认quality=75。

建议修改：替换为Pillow JPEG小节说明：默认75，通常避免>95；不要把lossless压缩努力程度套到JPEG。

依据：[pillow.readthedocs.io · image-file-formats · jpeg](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#jpeg)。

### A128

**Python复杂脚本的日志记录实践**

原文：[software/program/python/Python复杂脚本的日志记录实践/index.md](<C:/Project/blog/software/program/python/Python复杂脚本的日志记录实践/index.md>)。

记录日期：2025-07-09T16:00:00+08:00；状态：正文已核阅；有修改意见。

#### R215

**字词/链接 · 字词错误 · P3**

定位：[原文第 15 行](<C:/Project/blog/software/program/python/Python复杂脚本的日志记录实践/index.md:15>)；待改表述／主题：` 可能就够用了 `。

原文定位行（节选）：`` 与那些一次性的简单脚本不同，复杂场景下的脚本，比如一些定时任务，或者系统运维脚本的运行时间较长，代码较为复杂，这时候简单的 `basicConfig` 可能就够用了。 ``

问题：与下文转向dictConfig的理由相反，缺“不”字。

建议修改：改为“可能就不够用了”。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R216

**事实/技术错误 · 代码错误 · P1**

定位：[原文第 78 行](<C:/Project/blog/software/program/python/Python复杂脚本的日志记录实践/index.md:78>)；待改表述／主题：` app_logger.exception…smtp task failed `。

原文定位行（节选）：` app_logger.exception(f'smtp task failed: {e}') `

问题：告警发送失败又调用同一个配置了告警handler的logger，会递归提交告警；ntfy L103同样存在。

建议修改：使用仅文件/控制台handler的独立内部logger（propagate=False），或在handler失败时用安全fallback；增加有界队列/限流，防止失败风暴。

依据：[Python 官方文档 · logging](https://docs.python.org/3/library/logging.html)。

### A129

**Python多线程下载网络图片**

原文：[software/program/python/Python多线程下载网络图片/index.md](<C:/Project/blog/software/program/python/Python多线程下载网络图片/index.md>)。

记录日期：2020-04-17T16:16:12+08:00；状态：正文已核阅；有修改意见。

#### R217

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 167 行](<C:/Project/blog/software/program/python/Python多线程下载网络图片/index.md:167>)；待改表述／主题：` 多线程并不是运行在多核…单核CPU `。

原文定位行（节选）：` Python 的多线程并不是运行在多核上的，由于 GIL（Global Interpreter Lock，全局解释器锁）的存在，所以在每个时刻，单核 CPU，仅有一个线程在运行，可以说是并发而不是并行（并发和并行在宏观角度上都是在同一个时间段同时完成多个任务，但从微观角度来讲，同一时刻下，并发只是处理单个任务，并行才是真正运行在多核上，同时完成。） `

问题：GIL限制的是同一解释器同时执行Python字节码的线程数，不会把机器变成单核；释放GIL的扩展可以并行。

建议修改：限定到启用GIL的CPython纯Python计算；线程由OS调度且可用多个核心；补充3.13起可选free-threaded构建。

依据：[Python 官方文档 · threading](https://docs.python.org/3.13/library/threading.html)。

#### R218

**字词/链接 · 字词错误 · P3**

定位：[原文第 169 行](<C:/Project/blog/software/program/python/Python多线程下载网络图片/index.md:169>)；待改表述／主题：` 收到CPU限制；pyhton `。

原文定位行（节选）：` 对于 CPU 密集型的任务而言，pyhton 的多线程并没什么用，反而比单线程慢，由于创建线程，切换线程需要额外的开销，而同一时刻运行的又只有一个线程，所以如同鸡肋。应对 CPU 密集型的任务，可以采用 MultiProcess，多进程来进行处理，这样每个进程都有自己 GIL，互不干扰，达到并行的效果。 `

问题：应为受到、Python（L169）。

建议修改：按这两处修改。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A130

**Python的异常机制**

原文：[software/program/python/Python的异常机制/index.md](<C:/Project/blog/software/program/python/Python的异常机制/index.md>)。

记录日期：2025-07-31T10:10:00+08:00；状态：正文已核阅；有修改意见。

#### R219

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 23 行](<C:/Project/blog/software/program/python/Python的异常机制/index.md:23>)；待改表述／主题：` SyntaxError…不发生在程序运行时 `。

原文定位行（节选）：` 有一种异常比较特殊，它不是发生在运行时（RunTime），而是在 Python 解释器解析代码时可能会爆出的异常。 `

问题：运行中的程序调用compile/exec/eval或导入另一个模块时，也可能得到SyntaxError。

建议修改：改为：被解析的代码单元存在语法错误；直接运行一个语法错误的主脚本通常在执行脚本语句前失败。

依据：[Python 官方文档 · exceptions · SyntaxError](https://docs.python.org/3/library/exceptions.html#SyntaxError)。

#### R220

**字词/链接 · 字词错误 · P3**

定位：[原文第 55 行](<C:/Project/blog/software/program/python/Python的异常机制/index.md:55>)；待改表述／主题：` 语法违法 `。

原文定位行（节选）：` Python 是一种解释型语言，解释器在执行代码之前会先对代码进行语法检查，如果代码语法违法了 Python 语言的规则，就会抛出 SyntaxError。 `

问题：应为“语法违反了…”或“违反语法规则”。

建议修改：按原句改为“违反语法规则”。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R221

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 149 行](<C:/Project/blog/software/program/python/Python的异常机制/index.md:149>)；待改表述／主题：` 自动调用sys.exit() `。

原文定位行（节选）：`` 如果对于程序的异常没有做任何处理，那么，Python 会自动调用 `sys.exit()` 来终止程序的执行。 ``

问题：普通未处理异常不等于解释器自动调用sys.exit；主线程未处理异常调用sys.excepthook，sys.exit本身是抛出SystemExit。

建议修改：说明未处理异常终止相应执行路径；主线程通常打印回溯并退出，工作线程异常通常由threading.excepthook处理。

依据：[Python 官方文档 · sys · sys.excepthook](https://docs.python.org/3/library/sys.html#sys.excepthook)；[Python 官方文档 · threading · threading.excepthook](https://docs.python.org/3/library/threading.html#threading.excepthook)。

#### R222

**事实/技术错误 · 代码/解释错误 · P2**

定位：[原文第 206 行](<C:/Project/blog/software/program/python/Python的异常机制/index.md:206>)；待改表述／主题：` 服务器请求错误（404，500） `。

原文定位行（节选）：` 代码逻辑很简单，通过网络请求一个站点，然后把 HTTP 响应的 text body 写到本地的一个文件中，这个过程可能会有各种各样的异常，服务器请求错误（404，500），网络超时，文件无法打开，文件写入错误等等。 `

问题：本段requests.get没有raise_for_status，404/500会作为正常Response返回；裸except仍能用sys.exc_info获得异常详情。

建议修改：在199行后加response.raise_for_status()；208行改为示例没有输出异常细节，而非裸except无法获得细节。

依据：[Requests 文档／源码 · models](https://requests.readthedocs.io/en/latest/_modules/requests/models/)；[Python 官方文档 · sys · sys.exc_info](https://docs.python.org/3/library/sys.html#sys.exc_info)。

### A131

**Python的日志记录**

原文：[software/program/python/Python的日志记录/index.md](<C:/Project/blog/software/program/python/Python的日志记录/index.md>)。

记录日期：2024-10-01T10:00:00+08:00；状态：草稿；正文已核阅；有修改意见。

#### R223

**字词/链接 · 字词错误 · P3**

定位：[原文第 36 行](<C:/Project/blog/software/program/python/Python的日志记录/index.md:36>)；待改表述／主题：` 剩下；主要主要；显示；知道 `。

原文定位行（节选）：` logging 模块的作者是 Vinay Sajip，Python 官方的 logging 文档作者也是他，目前找到的可以参考的主要主要资料如下： `

问题：按上下文应为省下、主要、显式、直到。

建议修改：24行剩下→省下；36行删重复主要；139行输出是→输出时；401行显示→显式；484行向→像；528行知道→直到；582行一下→以下。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R224

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 234 行](<C:/Project/blog/software/program/python/Python的日志记录/index.md:234>)；待改表述／主题：` 必须先basicConfig…否则无效 `。

原文定位行（节选）：`` 这里有个坑，如果你要自己调用 `basicConfig`，那么一定要在使用 debug，info 等等这些记录方法前调用，否则无效， ``

问题：无效的条件是root已有handler；Python3.8起force=True可重新配置。stderr是否红色由显示环境决定。

建议修改：改写为root已有handler时普通basicConfig不生效，可以force=True；162行删去“一定”红色的断言。

依据：[Python 官方文档 · logging · logging.basicConfig](https://docs.python.org/3/library/logging.html#logging.basicConfig)。

#### R225

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 277 行](<C:/Project/blog/software/program/python/Python的日志记录/index.md:277>)；待改表述／主题：` basicConfig…无法接收encoding `。

原文定位行（节选）：`` 但这里有个很怪的地方，我以为 `basicConfig` 可以指定 encoding，但是 `basicConfig` 并不接收这个参数，`basicConfig` 默认调用的 `FileHandler` 的 `encoding` 参数默认值是 None，所以如果要指定 encoding，只能通过后面介绍的 `FileHandler` 来处理，这很奇怪，参考以下帖子： ``

问题：Python3.9起basicConfig支持encoding/errors，用于filename创建的FileHandler；本文引用3.12文档。

建议修改：改为：basicConfig(filename=..., encoding="utf-8")可指定文件编码；传入已有handlers时由各handler管理编码。

依据：[Python 官方文档 · logging · logging.basicConfig](https://docs.python.org/3/library/logging.html#logging.basicConfig)。

#### R226

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 530 行](<C:/Project/blog/software/program/python/Python的日志记录/index.md:530>)；待改表述／主题：` Handler未设置level…继承Logger `。

原文定位行（节选）：` 如果 handler 不设置 level，那么 handler 会从 logger 那继承 level。 `

问题：Handler默认级别是NOTSET，不继承Logger的有效级别；祖先Logger的level也不再次过滤传播记录。

建议修改：分别说明Logger有效级别沿父链查找、Handler级别独立判断，以及propagate的处理流程。

依据：[Python 官方文档 · logging · logging.Handler](https://docs.python.org/3/library/logging.html#logging.Handler)；[Python 官方文档 · logging · logging.Logger.propagate](https://docs.python.org/3/library/logging.html#logging.Logger.propagate)。

### A132

**Python的模块和包**

原文：[software/program/python/Python的模块和包/index.md](<C:/Project/blog/software/program/python/Python的模块和包/index.md>)。

记录日期：2025-09-19T14:52:00+08:00；状态：正文已核阅；有修改意见。

#### R227

**字词/链接 · 字词错误 · P3**

定位：[原文第 4 行](<C:/Project/blog/software/program/python/Python的模块和包/index.md:4>)；待改表述／主题：` 一场；制定；文件了 `。

原文定位行（节选）：` summary: "为了不要把所有代码都堆在一个文件了，我们有了模块和包的概念" `

问题：按上下文应为异常、指定、文件里。

建议修改：336行一场→异常；114行制定→指定；总结中的文件了→文件里。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R228

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 146 行](<C:/Project/blog/software/program/python/Python的模块和包/index.md:146>)；待改表述／主题：` PYTHONPATH…sys.path开头 `。

原文定位行（节选）：`` 设置后，Python 启动时会优先在这些目录里找模块（会把这些路径加在 `sys.path` 的开头）。 ``

问题：通常脚本所在目录或-m时的当前工作目录在PYTHONPATH目录之前。

建议修改：改为：PYTHONPATH所列目录加入模块搜索路径；首项行为由启动方式、-P/-I等选项决定。

依据：[Python 官方文档 · sys_path_init](https://docs.python.org/3/library/sys_path_init.html)。

#### R229

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 493 行](<C:/Project/blog/software/program/python/Python的模块和包/index.md:493>)；待改表述／主题：` 没有__all__…没有任何效果 `。

原文定位行（节选）：` 实际上，在包内导入所有元素是没有任何效果的： `

问题：from package import *会导入包命名空间中已有的公开名称（包括__init__.py定义或导入的名称）；不会自动扫描并加载全部子模块。

建议修改：限定本例空包的结果；补上普通包公开名称及__all__的实际规则。

依据：[Python 官方文档 · modules · importing-from-a-package](https://docs.python.org/3/tutorial/modules.html#importing-from-a-package)。

### A133

**Python简单脚本的日志记录实践**

原文：[software/program/python/Python简单脚本的日志记录实践/index.md](<C:/Project/blog/software/program/python/Python简单脚本的日志记录实践/index.md>)。

记录日期：2025-07-08T16:15:00+08:00；状态：正文已核阅；有修改意见。

#### R230

**事实/技术错误 · 代码错误 · P2**

定位：[原文第 67 行](<C:/Project/blog/software/program/python/Python简单脚本的日志记录实践/index.md:67>)；待改表述／主题：` if task_res `。

原文定位行（节选）：` if task_res: `

问题：task正常返回0时也被当成异常返回None。128篇的对应示例也应同步修改。

建议修改：改为if task_res is not None；或让异常与成功返回值分离，用明确的结果对象。

依据：[Python 官方文档 · stdtypes · truth-value-testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing)。

### A134

**Python解释器的-m参数**

原文：[software/program/python/Python解释器的-m参数/index.md](<C:/Project/blog/software/program/python/Python解释器的-m参数/index.md>)。

记录日期：2025-09-13T09:11:00+08:00；状态：正文已核阅；有修改意见。

#### R231

**事实/技术错误 · 代码错误 · P2**

定位：[原文第 37 行](<C:/Project/blog/software/program/python/Python解释器的-m参数/index.md:37>)；待改表述／主题：` import sys from pprint import pprint `。

原文定位行（节选）：` import sys from pprint import pprint `

问题：两条import语句误拼成一行，无法通过Python语法解析。

建议修改：拆为import sys和from pprint import pprint两行。

依据：[Python 官方文档 · simple_stmts · the-import-statement](https://docs.python.org/3/reference/simple_stmts.html#the-import-statement)。

#### R232

**事实/技术错误 · 概念/字词错误 · P2**

定位：[原文第 105 行](<C:/Project/blog/software/program/python/Python解释器的-m参数/index.md:105>)；待改表述／主题：` 内置模块uuid；变成 `。

原文定位行（节选）：` 这是最最常见的做法，Python 有很多实用的内置模块，在大部分变成场景下，这些模块都是以 import 的形式导入到我们的脚本文件中使用。 `

问题：uuid是标准库模块，而非通常所称的解释器内置模块；变成应为编程。

建议修改：改为“标准库uuid模块”“编程”。

依据：[Python 官方文档 · uuid](https://docs.python.org/3/library/uuid.html)；[Python 官方文档 · sys · sys.builtin_module_names](https://docs.python.org/3/library/sys.html#sys.builtin_module_names)。

### A135

**uv设置镜像源**

原文：[software/program/python/uv设置镜像源/index.md](<C:/Project/blog/software/program/python/uv设置镜像源/index.md>)。

记录日期：2025-10-25T12:00:00+08:00；状态：正文已核阅；有修改意见。

#### R233

**字词/链接 · 字词错误 · P3**

定位：[原文第 37 行](<C:/Project/blog/software/program/python/uv设置镜像源/index.md:37>)；待改表述／主题：` UV_DEFUALT_INDEX `。

原文定位行（节选）：` 可以把上面提到的 UV\_DEFUALT\_INDEX 写进 ~/.profile（或 ~/.bashrc、~/.zshrc）里。 `

问题：环境变量单词拼错，代码块UV_DEFAULT_INDEX是正确的。

建议修改：正文统一改为UV_DEFAULT_INDEX。

依据：[docs.astral.sh · environment · uv_default_index](https://docs.astral.sh/uv/reference/environment/#uv_default_index)。

### A136

**上下文管理器**

原文：[software/program/python/上下文管理器/index.md](<C:/Project/blog/software/program/python/上下文管理器/index.md>)。

记录日期：2025-12-09T16:35:05；状态：正文已核阅；有修改意见。

#### R234

**字词/链接 · 字词错误 · P3**

定位：[原文第 21 行](<C:/Project/blog/software/program/python/上下文管理器/index.md:21>)；待改表述／主题：` 及其耗时费心 `。

原文定位行（节选）：` 第一种场景就是管理资源，管理这些有限的资源是一个及其耗时费心的工作，往往我们随取随用，但是忘记编写清理资源的相关代码是一种常见的编程错误。 `

问题：这里“及其”应为程度副词“极其”。

建议修改：21行改为“极其耗时费心”。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R235

**事实/技术错误 · 概念错误 · P2**

定位：[原文第 173 行](<C:/Project/blog/software/program/python/上下文管理器/index.md:173>)；待改表述／主题：` __enter__返回值代表上下文管理器 `。

原文定位行（节选）：` __enter__ 的返回值很重要，返回值代表了上下文管理器，一般有两类返回值：返回自身或者相关对象。 `

问题：上下文管理器是with表达式求值得到的manager，__enter__的返回值赋给as目标，可以是其他对象甚至None。

建议修改：用manager和as target两个名称区分；149行__enter补齐为__enter__。

依据：[Python 官方文档 · compound_stmts · the-with-statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)。

### A137

**使用devpi搭建pypi缓存服务器**

原文：[software/program/python/使用devpi搭建pypi缓存服务器/index.md](<C:/Project/blog/software/program/python/使用devpi搭建pypi缓存服务器/index.md>)。

记录日期：2025-10-22T15:00:00+08:00；状态：正文已核阅；有修改意见。

#### R236

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 19 行](<C:/Project/blog/software/program/python/使用devpi搭建pypi缓存服务器/index.md:19>)；待改表述／主题：` pip…没有…完善的缓存 `。

原文定位行（节选）：` 1. pip 没有像 maven 一样，有很完善的缓存机制 `

问题：pip默认具有HTTP响应和wheel缓存；devpi的优势是共享代理缓存及索引管理，不能用pip没有缓存来解释。

建议修改：改为：pip有每客户端缓存；devpi可为多机器集中提供代理索引缓存。

依据：[pip.pypa.io · caching](https://pip.pypa.io/en/stable/topics/caching/)。

#### R237

**事实/技术错误 · 代码/字词错误 · P2**

定位：[原文第 131 行](<C:/Project/blog/software/program/python/使用devpi搭建pypi缓存服务器/index.md:131>)；待改表述／主题：` mirror.yourdomian.com…--trusted-host mirror.yourdomain.com `。

原文定位行（节选）：` python -m pip install -i http://mirror.yourdomian.com/root/pypi/+simple/ --trusted-host mirror.yourdomain.com requests `

问题：安装URL和trusted-host域名拼写不一致。

建议修改：统一为同一个实际域名；示例yourdomian改yourdomain。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A138

**使用uv和typer编写CLI工具的流程**

原文：[software/program/python/使用uv和typer编写CLI工具的流程/index.md](<C:/Project/blog/software/program/python/使用uv和typer编写CLI工具的流程/index.md>)。

记录日期：2025-11-19T16:48:46；状态：内容未完成；现有文本已核阅。

只有两个项目名，尚未提供标题所说的完整 CLI 编写与发布流程。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A139

**springboot接入prometheus**

原文：[software/prometheus/springboot接入prometheus/index.md](<C:/Project/blog/software/prometheus/springboot接入prometheus/index.md>)。

记录日期：2026-06-27T21:10:58；状态：正文已核阅；有修改意见。

#### R238

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 69 行](<C:/Project/blog/software/prometheus/springboot接入prometheus/index.md:69>)；待改表述／主题：` systemctl reload prometheus `。

原文定位行（节选）：` sudo systemctl reload prometheus `

问题：是否支持reload取决于unit是否定义ExecReload。Prometheus配置重载支持SIGHUP，或启用--web.enable-lifecycle后的/-/reload。

建议修改：与前文实际unit保持一致：有ExecReload时用systemctl reload；否则发送SIGHUP。

依据：[Prometheus 官方文档 · configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/)；[Prometheus 官方文档 · management_api](https://prometheus.io/docs/prometheus/latest/management_api/)。

### A140

**RabbitMQ的基本概念和使用**

原文：[software/rabbitmq/RabbitMQ的基本概念和使用/index.md](<C:/Project/blog/software/rabbitmq/RabbitMQ的基本概念和使用/index.md>)。

记录日期：2026-02-13T11:46:55；状态：草稿；正文已核阅；有修改意见。

#### R239

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 144 行](<C:/Project/blog/software/rabbitmq/RabbitMQ的基本概念和使用/index.md:144>)；待改表述／主题：` 消息…只会…一个消费者 `。

原文定位行（节选）：` 点对点是一种最基础的模式，生产者发送消息到队列，一个队列可以有一个或者多个消费者监听，但一条消息只会被其中一个消费者处理（竞争消费）。 `

问题：同一次投递通常交给一个消费者；连接故障、未确认或重新入队会使同一消息被再次投递。

建议修改：补充至少一次投递/重复处理的可能性，业务处理需考虑幂等；不能等同恰好一次。

依据：[RabbitMQ 官方文档 · reliability](https://www.rabbitmq.com/docs/reliability)。

#### R240

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 269 行](<C:/Project/blog/software/rabbitmq/RabbitMQ的基本概念和使用/index.md:269>)；待改表述／主题：` prefetch…channel `。

原文定位行（节选）：`` 消费者里的 `channel.basic_qos(prefetch_count=1)` 作用是限制一个 channel 最大的 unack message 数量，相当于告诉在我（consumer）没还给你（ACK）足够多的消息之前，别再给我发新的任务。 ``

问题：RabbitMQ在global=False时将prefetch_count分别应用于各consumer，并非整个channel共享的总额度。

建议修改：限定示例只有一个consumer；解释global=False与global=True的不同范围。

依据：[RabbitMQ 官方文档 · consumer-prefetch](https://www.rabbitmq.com/docs/consumer-prefetch)。

#### R241

**事实/技术错误 · 代码错误 · P1**

定位：[原文第 316 行](<C:/Project/blog/software/rabbitmq/RabbitMQ的基本概念和使用/index.md:316>)；待改表述／主题：` future完成后直接ACK `。

原文定位行（节选）：` def on_done(fut): `

问题：Future完成也可能是任务抛出异常；不检查结果就ACK，会确认尚未成功处理的消息。

建议修改：在on_done中调用fut.result()判断是否成功；成功才通过add_callback_threadsafe回到连接线程ACK，失败按重试/死信策略NACK。

依据：[Python 官方文档 · concurrent.futures · concurrent.futures.Future.result](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future.result)；[RabbitMQ 官方文档 · confirms](https://www.rabbitmq.com/docs/confirms)。

#### R242

**字词/链接 · 字词错误 · P3**

定位：[原文第 335 行](<C:/Project/blog/software/rabbitmq/RabbitMQ的基本概念和使用/index.md:335>)；待改表述／主题：` 点点对；计算计分 `。

原文定位行（节选）：` 点点对的模式适用于一个消息只被其中一个消费者消费，如果想要所有消费者消费同一个信息，那就需要使用广播（fanout）。 `

问题：应为点对点、计算积分。

建议修改：335行改点对点；100行改计算积分。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A141

**批量创建虚拟机**

原文：[software/vagrant/批量创建虚拟机/index.md](<C:/Project/blog/software/vagrant/批量创建虚拟机/index.md>)。

记录日期：2026-02-13T14:32:52；状态：正文已核阅；有修改意见。

#### R243

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 50 行](<C:/Project/blog/software/vagrant/批量创建虚拟机/index.md:50>)；待改表述／主题：` vagrant init…下载Box `。

原文定位行（节选）：` vagrant init debian/bookworm64 `

问题：init创建Vagrantfile，下载通常发生在vagrant up或vagrant box add；也不要求目录必须为空。

建议修改：按实际命令区分初始化配置、获取Box和启动虚拟机；38行删去空目录硬性要求。

依据：[developer.hashicorp.com · init](https://developer.hashicorp.com/vagrant/docs/cli/init)；[developer.hashicorp.com · up](https://developer.hashicorp.com/vagrant/docs/cli/up)。

### A142

**cookie和session**

原文：[software/web/backend/cookie和session/index.md](<C:/Project/blog/software/web/backend/cookie和session/index.md>)。

记录日期：2025-07-23T16:21:00+08:00；状态：正文已核阅；有修改意见。

#### R244

**事实/技术错误 · 字词/对象错误 · P2**

定位：[原文第 64 行](<C:/Project/blog/software/web/backend/cookie和session/index.md:64>)；待改表述／主题：` SessionId交给服务器；随即 `。

原文定位行（节选）：` 应用服务器在内存中维护一个键值对结构（Map），Key 是一个随即生成的 SessionId，Value 则是用户信息对象，服务器仅需要把 SessionId 交给服务器，这样用户信息存储在服务器端，安全性有了保障。 `

问题：这里应由服务器把SessionId交给浏览器；随即应为随机。

建议修改：改为“服务器生成随机SessionId并交给浏览器”。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R245

**事实/技术错误 · 概念错误 · P2**

定位：[原文第 109 行](<C:/Project/blog/software/web/backend/cookie和session/index.md:109>)；待改表述／主题：` JWT…解密 `。

原文定位行（节选）：` 2. CPU 压力高，每次请求响应涉及到 session 数据的解密和签名校验。 `

问题：常见签名JWT（JWS）进行解码和验签；只有使用JWE的加密JWT才涉及解密。

建议修改：区分签名、防篡改与加密、保密；Base64URL本身不提供保密性。

依据：[RFC 7519](https://www.rfc-editor.org/rfc/rfc7519.html)；[RFC 7515](https://www.rfc-editor.org/rfc/rfc7515.html)。

#### R246

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 124 行](<C:/Project/blog/software/web/backend/cookie和session/index.md:124>)；待改表述／主题：` 关闭浏览器…自动删除Cookie `。

原文定位行（节选）：` 会话 Cookie 仅在当前浏览器会话中有效，关闭浏览器就自动删除，这种 session cookie 常见于临时登陆，或者安全性较高的网站（比如：银行软件）。 `

问题：会话Cookie的会话结束由用户代理定义；浏览器会话恢复可能恢复它。Cookie Path也不是安全隔离边界（139行）。

建议修改：限定通常行为，并明确服务器侧会话过期；说明Path只控制发送路径，不能承担权限隔离。

依据：[RFC 6265](https://www.rfc-editor.org/rfc/rfc6265.html)；[MDN 文档 · Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie)。

### A143

**CORS的基础知识**

原文：[software/web/backend/CORS的基础知识/index.md](<C:/Project/blog/software/web/backend/CORS的基础知识/index.md>)。

记录日期：2023-11-19T09:43:04+08:00；状态：正文已核阅；有修改意见。

#### R247

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 40 行](<C:/Project/blog/software/web/backend/CORS的基础知识/index.md:40>)；待改表述／主题：` https…默认80 `。

原文定位行（节选）：`` | [https://baidu.com](https://baidu.com) | HTTPS | `baidu.com` | 80 | ``

问题：HTTPS默认端口是443，后文表格已写正确。

建议修改：40、41行统一为443；79行主机名(port)改主机名(host)。

依据：[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#section-4.2.2)。

#### R248

**字词/链接 · 链接错误 · P3**

定位：[原文第 49 行](<C:/Project/blog/software/web/backend/CORS的基础知识/index.md:49>)；待改表述／主题：` URL目标混入中文或单引号 `。

原文定位行（节选）：` 假设，客户端的 URL 是 [https://korilweb.cn，那么以下的](https://korilweb.cn，那么以下的) URL，其中部分存在跨源访问（也可以叫做：跨域访问）的问题。 `

问题：49行URL后含中文正文；164、168行链接目标末尾把引号带入了路径。

建议修改：49行目标只保留https://korilweb.cn；164、168行从URL目标中移除末尾单引号，将正文引号放在链接外。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R249

**事实/技术错误 · 事实错误 · P1**

定位：[原文第 77 行](<C:/Project/blog/software/web/backend/CORS的基础知识/index.md:77>)；待改表述／主题：` 同源策略防御CSRF…不允许跨域请求 `。

原文定位行（节选）：` 为了防御这种攻击，所有浏览器现在都实施同源策略。 `

问题：同源策略主要约束跨源读取等行为；表单、链接、部分资源请求可以跨源发出，不能据此防御CSRF。

建议修改：重写为限制跨源读取响应；CSRF需独立的令牌、SameSite及来源校验等机制。

依据：[MDN 文档 · Same-origin_policy](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy)。

#### R250

**条件/版本澄清 · 条件遗漏 · P2**

定位：[原文第 95 行](<C:/Project/blog/software/web/backend/CORS的基础知识/index.md:95>)；待改表述／主题：` 简单请求只看Method和Content-Type `。

原文定位行（节选）：` 必须是满足以下的要求，才能称为简单请求 `

问题：还涉及CORS safelisted请求头及其值等条件；GET携带Authorization或自定义header也会触发预检。

建议修改：补齐简单请求的请求头限制；214行补充带凭据请求不能使用Access-Control-Allow-Origin: *。

依据：[MDN 文档 · CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS)。

### A144

**Flask实现简单的登陆功能**

原文：[software/web/backend/Flask实现简单的登陆功能/index.md](<C:/Project/blog/software/web/backend/Flask实现简单的登陆功能/index.md>)。

记录日期：2025-07-27T08:43:00+08:00；状态：正文已核阅；有修改意见。

#### R251

**条件/版本澄清 · 字词/条件遗漏 · P2**

定位：[原文第 23 行](<C:/Project/blog/software/web/backend/Flask实现简单的登陆功能/index.md:23>)；待改表述／主题：` 受到；关闭浏览器自动删除 `。

原文定位行（节选）：` 浏览器受到 set-cookie 后，会自动在之后的请求中使用该 cookie 访问站点。 `

问题：受到应为收到；153行浏览器关闭删除Cookie需说明会话恢复例外。

建议修改：23行改收到；153行按会话Cookie定义补充条件。

依据：[MDN 文档 · Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie)。

#### R252

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 177 行](<C:/Project/blog/software/web/backend/Flask实现简单的登陆功能/index.md:177>)；待改表述／主题：` 非permanent…不设置Cookie `。

原文定位行（节选）：` 如果 session 是非持久化的，那么每次刷新页面都是一个 cookie，Flask 服务器是不会在 response 里面 set 新的 cookie，但如果 session 是持久化的，那么每次刷新页面，服务器都会 set 一个新的 cookie。 `

问题：Flask会在session被修改时保存Cookie，与permanent无必然等价关系；清空session也会删除Cookie。

建议修改：改为：modified触发保存；permanent且SESSION_REFRESH_EACH_REQUEST=True也可刷新未修改但非空的会话。

依据：[Flask 官方文档 · api · flask.sessions.SecureCookieSessionInterface.should_set_cookie](https://flask.palletsprojects.com/en/stable/api/#flask.sessions.SecureCookieSessionInterface.should_set_cookie)。

### A145

**Gunicorn+Flask的基本应用**

原文：[software/web/backend/Gunicorn+Flask的基本应用/index.md](<C:/Project/blog/software/web/backend/Gunicorn+Flask的基本应用/index.md>)。

记录日期：2024-12-08T10:38:22+08:00；状态：草稿；正文已核阅；有修改意见。

#### R253

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 55 行](<C:/Project/blog/software/web/backend/Gunicorn+Flask的基本应用/index.md:55>)；待改表述／主题：` FastAPI…WSGI `。

原文定位行（节选）：` Web 应用框架的代表：Django，Flask，FastAPI，它们处理业务逻辑，和数据库打交道，支持模板引擎，处理路由和函数的绑定，处理用户的会话和身份验证等功能，它们支持 WSGI 协议，并和 WSGI 服务器通讯。 `

问题：FastAPI基于ASGI；WSGI、ASGI是应用与服务器的接口规范。

建议修改：将FastAPI放在ASGI类别；区分应用接口、HTTP和uWSGI可选的uwsgi线协议。

依据：[FastAPI 官方文档 · manually](https://fastapi.tiangolo.com/deployment/manually/)；[Python PEP · pep-3333](https://peps.python.org/pep-3333/)。

#### R254

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 88 行](<C:/Project/blog/software/web/backend/Gunicorn+Flask的基本应用/index.md:88>)；待改表述／主题：` Werkzeug不支持多线程、多进程 `。

原文定位行（节选）：`` 2. 它缺乏像 Gunicorn 或 `uWSGI` 那样的多线程、多进程支持。 ``

问题：Werkzeug run_simple提供threaded和processes选项，只是二者不能同时启用。

建议修改：改为开发服务器支持线程或进程模式，但官方不建议用于生产部署。

依据：[Werkzeug 官方文档 · serving](https://werkzeug.palletsprojects.com/en/stable/serving/)。

#### R255

**事实/技术错误 · 实验归因错误 · P2**

定位：[原文第 147 行](<C:/Project/blog/software/web/backend/Gunicorn+Flask的基本应用/index.md:147>)；待改表述／主题：` Windows…单线程伪并发 `。

原文定位行（节选）：` Werkzeug 的单线程模型，使得它无法处理 CPU 密集型的任务，但对于 I/O 密集型的任务，如果数量少的话，表现尚可。 `

问题：Flask.run默认threaded=True，等待请求可由多个线程处理，两套系统都能出现这种现象。

建议修改：在147、219、260、264行统一说明worker/线程配置、time.sleep释放执行机会等条件；不能把Windows表现解释为单线程。

依据：[Flask 官方文档 · api · flask.Flask.run](https://flask.palletsprojects.com/en/stable/api/#flask.Flask.run)。

#### R256

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 266 行](<C:/Project/blog/software/web/backend/Gunicorn+Flask的基本应用/index.md:266>)；待改表述／主题：` 大于2*cores+1…性能降低；跨平台一致 `。

原文定位行（节选）：` Gunicorn 的 worker 是跨平台一致的设计，而 Windows 上的 Werkzeug 受益于底层特性，性能看似更好。 `

问题：Gunicorn给出的worker数是起点经验值，实际需测量；Gunicorn是UNIX/POSIX服务器，不能推出原生Windows也相同。

建议修改：把经验式写成调优起点；注明实验系统及worker类型；266行补POSIX适用范围，223行work改worker。

依据：[仓库源码：benoitc/gunicorn · design.rst](https://github.com/benoitc/gunicorn/blob/23.0.0/docs/source/design.rst)；[仓库源码：benoitc/gunicorn · README.rst](https://github.com/benoitc/gunicorn/blob/master/README.rst)。

### A146

**RBAC权限模型概述**

原文：[software/web/backend/RBAC权限模型概述/index.md](<C:/Project/blog/software/web/backend/RBAC权限模型概述/index.md>)。

记录日期：2025-01-30T10:35:00+08:00；状态：草稿；空提纲／参考资料；无实质技术正文。

只有提纲、前言标题或参考链接，缺少可核实的技术正文。本轮不把这种空提纲计作内容正确的技术文章。

### A147

**Servlet初探**

原文：[software/web/backend/Servlet初探/index.md](<C:/Project/blog/software/web/backend/Servlet初探/index.md>)。

记录日期：2023-05-21T10:40:45+08:00；状态：正文已核阅；有修改意见。

#### R257

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 89 行](<C:/Project/blog/software/web/backend/Servlet初探/index.md:89>)；待改表述／主题：` Apache/Nginx不能生成动态内容 `。

原文定位行（节选）：` 上面提到的静态页面，同样需要有服务器的某个软件提供支持，因为本质上，HTML，CSS，JS 还有图片这些资源，都是通过 HTTP 协议来传输和接收的，必然会有一个解析 HTTP 协议的程序，Apache 和 Nginx 都是最有名的 Web Server 软件，它们支持 HTTP 协议和传输静态资源文件，但是它们不能生成动态的页面，只是单纯的数据搬运工。 `

问题：Apache可通过CGI/模块处理动态内容，NGINX也有扩展能力；通常承担静态服务和代理不等于不能处理动态内容。

建议修改：限定本教程部署方式：由Nginx代理到Tomcat，由Servlet生成响应。

依据：[httpd.apache.org · cgi](https://httpd.apache.org/docs/2.4/howto/cgi.html)。

#### R258

**事实/技术错误 · 生命周期错误 · P2**

定位：[原文第 99 行](<C:/Project/blog/software/web/backend/Servlet初探/index.md:99>)；待改表述／主题：` 每个请求创建Servlet…destroy…垃圾回收 `。

原文定位行（节选）：`` 例如，Tomcat 接收到 Web Server 的请求后，解析出请求路径，找到具体访问的接口，然后创建与路径相对应的 `Servlet` 实现类对象，最后调用 `Servlet` 中的 `service` 方法。 ``

问题：Servlet实例通常由容器初始化并复用于多个请求，service可并发调用；destroy不等于对象立刻被GC。

建议修改：按实例化→init→多次service→destroy说明生命周期和共享实例状态。

依据：[Jakarta 规范 · jakarta-servlet-spec-6.0](https://jakarta.ee/specifications/servlet/6.0/jakarta-servlet-spec-6.0.html)。

#### R259

**事实/技术错误 · 概念/字词错误 · P2**

定位：[原文第 359 行](<C:/Project/blog/software/web/backend/Servlet初探/index.md:359>)；待改表述／主题：` ServletConfig类；的的；给给 `。

原文定位行（节选）：`` 在 `init` 方法的形参中，出现了 `ServletConfig` 类。 ``

问题：ServletConfig是接口；有重复字和误字。

建议修改：359行改接口；26行删重复的；38行考虑以下→考虑一下；361行删重复给。

依据：[Jakarta 规范 · servletconfig](https://jakarta.ee/specifications/servlet/6.0/apidocs/jakarta.servlet/jakarta/servlet/servletconfig)。

### A148

**Windows安装OpenSSH服务端**

原文：[software/web/backend/Windows安装OpenSSH服务端/index.md](<C:/Project/blog/software/web/backend/Windows安装OpenSSH服务端/index.md>)。

记录日期：2024-10-30T20:22:06+08:00；状态：正文已核阅；有修改意见。

#### R260

**事实/技术错误 · 命令错误 · P2**

定位：[原文第 49 行](<C:/Project/blog/software/web/backend/Windows安装OpenSSH服务端/index.md:49>)；待改表述／主题：` net user koril 123456 /active `。

原文定位行（节选）：` net user koril 123456 /active `

问题：/active选项需要yes或no值；原示例没有给出值。

建议修改：激活账户写net user koril /active:yes；创建账户的命令与激活命令分开说明。

依据：[learn.microsoft.com · net-user](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/net-user)。

### A149

**一个软件全量更新的简单方式**

原文：[software/web/backend/一个软件全量更新的简单方式/index.md](<C:/Project/blog/software/web/backend/一个软件全量更新的简单方式/index.md>)。

记录日期：2025-07-23T16:21:00+08:00；状态：正文已核阅；有修改意见。

#### R261

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 55 行](<C:/Project/blog/software/web/backend/一个软件全量更新的简单方式/index.md:55>)；待改表述／主题：` Windows不能关闭当前运行程序 `。

原文定位行（节选）：` 需要注意的是，网上的一些方案，是把更新程序和主程序捆绑，最后打包成一个 exe 文件，但是这样会导致“关闭主程序-更新-重启主程序”这个主要环节出现问题，Windows 是不能关闭当前正在运行的程序的，所以一些博客的方法是把“软件替换+重启软件”这个步骤通过 bat 文件来完成。 `

问题：问题通常是不能按一般方式覆写正在运行的EXE，Windows当然支持结束运行中的进程。

建议修改：改为：更新器等待主程序退出，再替换其EXE和依赖文件。

依据：[learn.microsoft.com · terminating-a-process](https://learn.microsoft.com/en-us/windows/win32/procthread/terminating-a-process)。

#### R262

**事实/技术错误 · 代码错误 · P1**

定位：[原文第 301 行](<C:/Project/blog/software/web/backend/一个软件全量更新的简单方式/index.md:301>)；待改表述／主题：` Content-Length默认0…EOF算完成 `。

原文定位行（节选）：` total_size = int(response.headers.get('Content-Length', 0)) `

问题：循环仅凭read返回空字节判完成，没有核对已下载大小/摘要；不完整文件可能进入替换流程。

建议修改：存在Content-Length时核对计数，另用受信任的摘要或签名确认内容完整性，验证失败不替换。

依据：[Python 官方文档 · http.client · http.client.HTTPResponse.read](https://docs.python.org/3/library/http.client.html#http.client.HTTPResponse.read)。

#### R263

**事实/技术错误 · 代码错误 · P1**

定位：[原文第 383 行](<C:/Project/blog/software/web/backend/一个软件全量更新的简单方式/index.md:383>)；待改表述／主题：` 先删除旧EXE，再移动新文件 `。

原文定位行（节选）：` os.remove(self.app_path) `

问题：移动失败时旧版本已被删除，更新失败会失去可运行版本。

建议修改：先把下载并验证的新文件放到同一文件系统的临时路径，保留备份，再替换并设计失败恢复；不要提前删除唯一旧版本。

依据：[Python 官方文档 · os · os.replace](https://docs.python.org/3/library/os.html#os.replace)；[Python 官方文档 · shutil · shutil.move](https://docs.python.org/3/library/shutil.html#shutil.move)。

#### R264

**事实/技术错误 · 代码错误 · P1**

定位：[原文第 426 行](<C:/Project/blog/software/web/backend/一个软件全量更新的简单方式/index.md:426>)；待改表述／主题：` len(sys.argv)<5却解包7个元素 `。

原文定位行（节选）：` if len(sys.argv) < 5: `

问题：传5或6个参数元素会通过检查，然后在432行解包时ValueError；用法提示也漏description和update_date。

建议修改：检查len(sys.argv)==7，补完整用法：update.exe <app_path> <current_version> <exe_url> <new_version> <description> <update_date>；完整版重复代码同步修改。

依据：[Python 官方文档 · sys · sys.argv](https://docs.python.org/3/library/sys.html#sys.argv)。

### A150

**一种直白有效的前缀匹配方案**

原文：[software/web/backend/一种直白有效的前缀匹配方案/index.md](<C:/Project/blog/software/web/backend/一种直白有效的前缀匹配方案/index.md>)。

记录日期：2024-10-20T12:12:04+08:00；状态：正文已核阅；有修改意见。

#### R265

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 136 行](<C:/Project/blog/software/web/backend/一种直白有效的前缀匹配方案/index.md:136>)；待改表述／主题：` 集合查找全是O(1) `。

原文定位行（节选）：` 集合是通过哈希表实现的，所以添加，删除，查找的复杂度都是 O(1)。 `

问题：Redis有序集合的ZRANK通常为O(log N)，ZRANGE通常O(log N+M)；不能将哈希集合查询套用于zset所有操作。

建议修改：给出本文实际使用命令的复杂度，说明编码和命令会影响代价。

依据：[Redis 官方文档 · zrank](https://redis.io/docs/latest/commands/zrank/)；[Redis 官方文档 · zrange](https://redis.io/docs/latest/commands/zrange/)。

#### R266

**条件/版本澄清 · 概念/条件遗漏 · P2**

定位：[原文第 156 行](<C:/Project/blog/software/web/backend/一种直白有效的前缀匹配方案/index.md:156>)；待改表述／主题：` 基于Unicode码值排序 `。

原文定位行（节选）：` 我们可以利用这一特性，来存储城市名称（中文也可以，因为是基于 Unicode 码值的字典序进行排序的）。 `

问题：Redis有序集合同分值成员按二进制字节字典序比较，不理解Unicode；良构UTF-8通常保持码点顺序，但不是语言学排序。

建议修改：注明成员编码与全体score相同的前提；Java char是UTF-16码元，不能把末位+1直接当任意Unicode字符的后继。

依据：[Redis 官方文档 · zrangebylex](https://redis.io/docs/latest/commands/zrangebylex/)。

#### R267

**事实/技术错误 · 代码错误 · P1**

定位：[原文第 291 行](<C:/Project/blog/software/web/backend/一种直白有效的前缀匹配方案/index.md:291>)；待改表述／主题：` query[-1]；zrank后直接zrange `。

原文定位行（节选）：` end_query = query[:len(query) - 1] + chr(ord(query[-1]) + 1) `

问题：空query会越界；不存在的前缀rank为None，Python版本随后调用zrange失败。Java版本虽检查rank为空，但仍会在空字符串时越界。

建议修改：入口处理空值/空前缀；不存在的rank返回空列表；明确支持的字符范围，或采用字节前缀边界的BYLEX方案。

依据：[Redis 官方文档 · zrank](https://redis.io/docs/latest/commands/zrank/)；[Redis 官方文档 · zrangebylex](https://redis.io/docs/latest/commands/zrangebylex/)。

### A151

**使用MMDB来获取客户端的IP信息**

原文：[software/web/backend/使用MMDB来获取客户端的IP信息/index.md](<C:/Project/blog/software/web/backend/使用MMDB来获取客户端的IP信息/index.md>)。

记录日期：2024-11-09T09:25:48+08:00；状态：正文已核阅；有修改意见。

#### R268

**事实/技术错误 · 概念错误 · P2**

定位：[原文第 37 行](<C:/Project/blog/software/web/backend/使用MMDB来获取客户端的IP信息/index.md:37>)；待改表述／主题：` GPS定位 `。

原文定位行（节选）：` 自从 James 和 Theresa Arnold 于 2011 年 3 月搬进他们在堪萨斯州巴特勒县租来的 623 英亩农场以来，他们看到“无数”执法官员和个人日夜出现在他们的农场，寻找与涉嫌盗窃和其他涉嫌犯罪的联系。所有这些人都是因为 GPS 位置的四舍五入错误而到达的，这会错误地将人们指向他们的农场。 `

问题：本文案例是IP地理数据库的估计或默认坐标，并非终端GPS测量。

建议修改：统一为IP地理定位；避免把数据库坐标直接解释为用户精确住址。

依据：[support.maxmind.com · maxmind-geolocation-accuracy](https://support.maxmind.com/knowledge-base/articles/maxmind-geolocation-accuracy)。

#### R269

**事实/技术错误 · 名称错误 · P2**

定位：[原文第 68 行](<C:/Project/blog/software/web/backend/使用MMDB来获取客户端的IP信息/index.md:68>)；待改表述／主题：` GeoIP2-ASN `。

原文定位行（节选）：` 3. GeoIP2-ASN：ASN（自治系统号码）数据库，包含 IP 地址归属的自治系统（ISP 或大型网络服务提供商）信息，适合网络分析和监控。 `

问题：免费产品叫GeoLite2 ASN；收费产品组合中对应的ISP信息不是名为GeoIP2-ASN的数据库。

建议修改：改为GeoLite2 ASN；收费/免费数据库更新频率按具体产品和日期描述，勿笼统全体比较。

依据：[dev.maxmind.com · databases](https://dev.maxmind.com/geoip/docs/databases/)。

#### R270

**事实/技术错误 · 代码错误 · P1**

定位：[原文第 252 行](<C:/Project/blog/software/web/backend/使用MMDB来获取客户端的IP信息/index.md:252>)；待改表述／主题：` 直接读取X-Forwarded-For `。

原文定位行（节选）：` ip = request.headers.get('X-Forwarded-For', request.remote_addr) `

问题：该header可包含逗号分隔的代理链，不能直接作为一个IP查询MMDB；也不能无条件信任客户端传入的内容。

建议修改：按已知可信代理层数配置ProxyFix或可信代理解析；查询前校验单个IP；260行remote_addr应为直接连接的代理地址，不一定127.0.0.1。

依据：[Werkzeug 官方文档 · proxy_fix](https://werkzeug.palletsprojects.com/en/stable/middleware/proxy_fix/)；[NGINX 官方文档 · ngx_http_proxy_module · var_proxy_add_x_forwarded_for](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#var_proxy_add_x_forwarded_for)。

### A152

**使用Redis实现分页和搜索的功能**

原文：[software/web/backend/使用Redis实现分页和搜索的功能/index.md](<C:/Project/blog/software/web/backend/使用Redis实现分页和搜索的功能/index.md>)。

记录日期：2024-12-07T14:51:04+08:00；状态：正文已核阅；有修改意见。

#### R271

**条件/版本澄清 · 用法边界澄清 · P2**

定位：[原文第 110 行](<C:/Project/blog/software/web/backend/使用Redis实现分页和搜索的功能/index.md:110>)；待改表述／主题：` 类似Python切片 `。

原文定位行（节选）：` 使用方式和 Python 的切片相似。 `

问题：“与Python切片相似”可作为类比，但没有说明end包含这一关键差别；容易导致实际分页多取一项。

建议修改：明确是闭区间start..end；分页end应为offset+page_size-1。

依据：[Redis 官方文档 · zrange](https://redis.io/docs/latest/commands/zrange/)。

#### R272

**字词/链接 · 字词错误 · P3**

定位：[原文第 316 行](<C:/Project/blog/software/web/backend/使用Redis实现分页和搜索的功能/index.md:316>)；待改表述／主题：` 当前page的的 `。

原文定位行（节选）：` 这样只需要一次请求，就可以拿到当前页面的的详细信息。 `

问题：重复字。

建议修改：删一个的。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A153

**在Tomcat中部署一个简单的Servlet**

原文：[software/web/backend/在Tomcat中部署一个简单的Servlet/index.md](<C:/Project/blog/software/web/backend/在Tomcat中部署一个简单的Servlet/index.md>)。

记录日期：2023-05-23T18:51:18+08:00；状态：正文已核阅；有修改意见。

#### R273

**字词/链接 · 链接错误 · P3**

定位：[原文第 98 行](<C:/Project/blog/software/web/backend/在Tomcat中部署一个简单的Servlet/index.md:98>)；待改表述／主题：` 本地演示URL包含中文正文 `。

原文定位行（节选）：` 然后打开 [http://localhost:8080/static-demo/，可以看到以下页面](http://localhost:8080/static-demo/，可以看到以下页面)： `

问题：98、183行Markdown链接目标混入“可以看到以下页面”等中文。

建议修改：分别只保留http://localhost:8080/static-demo/、http://localhost:8080/hello-servlet/hello。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R274

**事实/技术错误 · 术语错误 · P2**

定位：[原文第 114 行](<C:/Project/blog/software/web/backend/在Tomcat中部署一个简单的Servlet/index.md:114>)；待改表述／主题：` hello-servlet…根上下文 `。

原文定位行（节选）：` * <TOMCAT_HOME>/webapps/hello-servlet/：表示一个 web app 目录，下面放着一些资源文件，如 HTML，CSS，JS 文件，以及 Java 的 Class 文件和第三方库，这个目录也表示该 app 的整个上下文（root context）。 `

问题：hello-servlet目录对应/hello-servlet上下文；真正根上下文通常用ROOT目录或空context path。

建议修改：改为应用上下文/hello-servlet；80行webapps限定默认appBase布局。

依据：[tomcat.apache.org · context](https://tomcat.apache.org/tomcat-10.1-doc/config/context.html)。

#### R275

**条件/版本澄清 · 事实/部署条件 · P2**

定位：[原文第 116 行](<C:/Project/blog/software/web/backend/在Tomcat中部署一个简单的Servlet/index.md:116>)；待改表述／主题：` WEB-INF/src…Servlet API放lib `。

原文定位行（节选）：` * <TOMCAT_HOME>/webapps/hello-servlet/WEB-INF/src：存放 Java 程序的源代码文件，为了方便部署，最佳实践是将源代码文件和编译后的 classes 分开放。 `

问题：WEB-INF/src是教学自定目录；Servlet API由容器提供，不应作为应用依赖重复打进WEB-INF/lib。

建议修改：将src标为可选构建目录；用Tomcat lib下servlet-api.jar作编译类路径，构建工具依赖设为provided。

依据：[tomcat.apache.org · class-loader-howto](https://tomcat.apache.org/tomcat-10.1-doc/class-loader-howto.html)；[Jakarta 规范 · jakarta-servlet-spec-6.0](https://jakarta.ee/specifications/servlet/6.0/jakarta-servlet-spec-6.0.html)。

### A154

**拦截器和过滤器**

原文：[software/web/backend/拦截器和过滤器/index.md](<C:/Project/blog/software/web/backend/拦截器和过滤器/index.md>)。

记录日期：2023-11-04T09:56:41+08:00；状态：正文已核阅；有修改意见。

#### R276

**事实/技术错误 · 执行顺序错误 · P2**

定位：[原文第 28 行](<C:/Project/blog/software/web/backend/拦截器和过滤器/index.md:28>)；待改表述／主题：` Response按照过滤器链顺序返回 `。

原文定位行（节选）：`` 等 Servlet 工作完成后，Servlet 交付的 `Response` 又会按照过滤器链的顺序，依次返回给每个过滤器处理，最终交付到客户端。 ``

问题：chain.doFilter调用构成嵌套，正常返回时后置代码与请求进入顺序相反。

建议修改：例如请求F1→F2→Servlet，返回Servlet→F2→F1；说明异常/异步等情况另有生命周期规则。

依据：[Jakarta 规范 · jakarta-servlet-spec-6.0](https://jakarta.ee/specifications/servlet/6.0/jakarta-servlet-spec-6.0.html)。

#### R277

**字词/链接 · 字词错误 · P3**

定位：[原文第 596 行](<C:/Project/blog/software/web/backend/拦截器和过滤器/index.md:596>)；待改表述／主题：` preHandler/postHandler/DespatcherServlet `。

原文定位行（节选）：`` 拦截器提供了三个方法，`preHandler` 是在进入具体的 `Controller` 代码前执行，`postHandler` 是在 `Controller` 代码结束后，返回 ModelAndView 的时候执行，而 `afterCompletion` 用于请求结束后的一些操作，比如资源的清理和日志的记录。 ``

问题：接口方法名是preHandle、postHandle；DispatcherServlet拼错。

建议修改：596行改preHandle/postHandle；730行改DispatcherServlet、与请求路径匹配；24行分别不执行→分别执行；243行删重复的。

依据：[Spring 官方文档 · HandlerInterceptor](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/servlet/HandlerInterceptor.html)。

### A155

**用户系统设计下的通用概念**

原文：[software/web/backend/用户系统设计下的通用概念/index.md](<C:/Project/blog/software/web/backend/用户系统设计下的通用概念/index.md>)。

记录日期：2025-12-12T11:24:20；状态：正文已核阅；有修改意见。

#### R278

**事实/技术错误 · 概念错误 · P2**

定位：[原文第 42 行](<C:/Project/blog/software/web/backend/用户系统设计下的通用概念/index.md:42>)；待改表述／主题：` OAuth2作为Authentication方式 `。

原文定位行（节选）：` - OAuth2 `

问题：OAuth 2.0是授权框架，不能单独保证用户身份认证语义；基于它的OpenID Connect定义身份认证层。

建议修改：改为OpenID Connect/OAuth2配套身份认证协议；56行Hash加密改密码哈希存储。

依据：[RFC 6749](https://www.rfc-editor.org/rfc/rfc6749.html)；[openid.net · openid-connect-core-1_0](https://openid.net/specs/openid-connect-core-1_0.html)。

#### R279

**字词/链接 · 字词错误 · P3**

定位：[原文第 94 行](<C:/Project/blog/software/web/backend/用户系统设计下的通用概念/index.md:94>)；待改表述／主题：` 不同级别的人可以不同级别的文档 `。

原文定位行（节选）：` MAC 起源于军事和情报界，给一些文档打上了安全等级标签（公开 < 秘密 < 机密 < 绝密），不同级别的人可以不同级别的文档。 `

问题：句子缺谓语。

建议修改：改为不同级别的人可以按安全策略访问相应级别的文档。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A156

**登录注册体系的安全手段**

原文：[software/web/backend/登录注册体系的安全手段/index.md](<C:/Project/blog/software/web/backend/登录注册体系的安全手段/index.md>)。

记录日期：2025-08-19T10:30:00+08:00；状态：正文已核阅；有修改意见。

#### R280

**条件/版本澄清 · 标准更新建议 · P2**

定位：[原文第 27 行](<C:/Project/blog/software/web/backend/登录注册体系的安全手段/index.md:27>)；待改表述／主题：` 必须包含大小写字母数字特殊字符 `。

原文定位行（节选）：` 2. 必须包含大小写字母，数字，特殊字符。 `

问题：可以制定项目组合规则，本句不是语言层面的事实错误；如果希望对齐现行NIST指南，应更新策略：该指南不要求字符类别组合，单因素密码最低15字符，多因素可最低8字符。

建议修改：改为明确的项目策略或按所采用标准说明长度、泄露密码阻止清单、速率限制；不能把复杂度组合当必需条件。

依据：[NIST 指南 · authenticators](https://pages.nist.gov/800-63-4/sp800-63b/authenticators/)。

#### R281

**字词/链接 · 字词错误 · P3**

定位：[原文第 32 行](<C:/Project/blog/software/web/backend/登录注册体系的安全手段/index.md:32>)；待改表述／主题：` 收到撞库攻击；登陆 `。

原文定位行（节选）：` 用户往往会采用同一个密码，注册多个不同平台，这样就会导致一个风险：一旦某一个平台的数据库泄露，那么该用户的注册过的其他平台就有可能收到撞库攻击。 `

问题：按语义应为受到撞库攻击；登录作为计算机认证操作建议全文统一。

建议修改：32行收到→受到；统一计算机场景的登录用字。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R282

**事实/技术错误 · 概念错误 · P1**

定位：[原文第 38 行](<C:/Project/blog/software/web/backend/登录注册体系的安全手段/index.md:38>)；待改表述／主题：` 加密存储…哈希…日志记录密码 `。

原文定位行（节选）：` 加密存储的策略主要是哈希函数，哈希函数是一种**数据摘要**函数，可以把**任意长度的数据**映射成**固定长度的值**。 `

问题：密码哈希不是可逆加密；正常认证过程中服务端可能暂时处理明文，但不应记录密码或密码哈希到日志。

建议修改：区分TLS传输加密和服务端加盐密码哈希；日志中省略/脱敏密码字段，使用Argon2id等密码哈希实现。

依据：[Spring 官方文档 · password-storage](https://docs.spring.io/spring-security/reference/features/authentication/password-storage.html)；[OWASP 指南 · Password_Storage_Cheat_Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)。

### A157

**自制一个聚合搜索引擎的页面**

原文：[software/web/backend/自制一个聚合搜索引擎的页面/index.md](<C:/Project/blog/software/web/backend/自制一个聚合搜索引擎的页面/index.md>)。

记录日期：2022-08-16T11:29:09+08:00；状态：正文已核阅；有修改意见。

#### R283

**字词/链接 · 字词错误 · P3**

定位：[原文第 23 行](<C:/Project/blog/software/web/backend/自制一个聚合搜索引擎的页面/index.md:23>)；待改表述／主题：` 自制能力 `。

原文定位行（节选）：` 现在的算法和 AI 很厉害，总是能把一个功能本应该极简化的搜索页面搞成一个五颜六色，充斥着牛鬼蛇神的推荐页面（参考国内某些浏览器的主页），包括智能提示，历史搜索提示（对其他人可能很有用），我的注意力就会被吸引过去，然后恰好我的自制能力抵不住推荐算法的诱惑，就往往从搜索**Nginx 入门视频**不知不觉就变成了**你的背景被嘎子偷了**，**XXX 明星塌房**，**高燃混剪|进来看不后悔**之类的。。。 `

问题：应为自制力。

建议修改：改为自制力。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R284

**事实/技术错误 · 代码错误 · P2**

定位：[原文第 134 行](<C:/Project/blog/software/web/backend/自制一个聚合搜索引擎的页面/index.md:134>)；待改表述／主题：` window.open(dict[select] + content) `。

原文定位行（节选）：` window.open(dict[select] + content); `

问题：输入含&、#、+等字符时会改变查询参数或URL片段，结果不再是原搜索词。

建议修改：查询参数用URLSearchParams或encodeURIComponent；词典路径参数另作路径编码。

依据：[MDN 文档 · encodeURIComponent](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/encodeURIComponent)。

### A158

**阿里云短信认证服务的使用**

原文：[software/web/backend/阿里云短信认证服务的使用/index.md](<C:/Project/blog/software/web/backend/阿里云短信认证服务的使用/index.md>)。

记录日期：2025-11-12T11:02:00+08:00；状态：正文已核阅；有修改意见。

#### R285

**条件/版本澄清 · 条件遗漏 · P2**

定位：[原文第 127 行](<C:/Project/blog/software/web/backend/阿里云短信认证服务的使用/index.md:127>)；待改表述／主题：` 我们并不知道验证码 `。

原文定位行（节选）：` 验证码是阿里云平台随机生成的，我们并不知道，所以验证用户的验证码需要调用阿里云的核验验证码接口： `

问题：默认不返回验证码，但API支持ReturnVerifyCode，不能无条件说调用方无法获取。

建议修改：改为本例未启用ReturnVerifyCode，采用平台核验；186行该该删重复字。

依据：[help.aliyun.com · api-dypnsapi-2017-05-25-sendsmsverifycode](https://help.aliyun.com/zh/pnvs/developer-reference/api-dypnsapi-2017-05-25-sendsmsverifycode)。

### A159

**SPA和SSR**

原文：[software/web/frontend/SPA和SSR/index.md](<C:/Project/blog/software/web/frontend/SPA和SSR/index.md>)。

记录日期：2026-02-01T10:48:21；状态：正文已核阅；有修改意见。

#### R286

**事实/技术错误 · 概念错误 · P2**

定位：[原文第 15 行](<C:/Project/blog/software/web/frontend/SPA和SSR/index.md:15>)；待改表述／主题：` SPA和SSR两种方案；SPA等同CSR `。

原文定位行（节选）：` 自前后端分离流行以来，前端的主流方案有两种，一种叫 SPA，另一种叫 SSR，本文简述二者的概念与区别。 `

问题：SPA/MPA讨论导航与应用结构，CSR/SSR讨论渲染位置；SSR与SPA可以组合，传统模板引擎也属于服务端渲染。

建议修改：分两组概念说明；SSR不限定服务器执行JS；首次速度、SEO等属于实现条件相关的趋势。

依据：[vuejs.org · ssr](https://vuejs.org/guide/scaling-up/ssr.html)。

### A160

**自己动手写一个博客静态页面生成器**

原文：[software/web/frontend/自己动手写一个博客静态页面生成器/index.md](<C:/Project/blog/software/web/frontend/自己动手写一个博客静态页面生成器/index.md>)。

记录日期：2025-01-29T09:30:00+08:00；状态：正文已核阅；有修改意见。

#### R287

**事实/技术错误 · 字词/实现不符 · P2**

定位：[原文第 139 行](<C:/Project/blog/software/web/frontend/自己动手写一个博客静态页面生成器/index.md:139>)；待改表述／主题：` jinjia2；YAML手工按冒号解析 `。

原文定位行（节选）：` - jinjia2 `

问题：依赖名是Jinja2；手工split无法完整解析YAML的引号、多行文本、转义等，甚至会保留title两边引号。

建议修改：139行改jinja2；用规范YAML解析器处理front matter，或明确仅支持受限的key:value语法。

依据：[jinja.palletsprojects.com](https://jinja.palletsprojects.com/en/stable/)；[pyyaml.org · PyYAMLDocumentation](https://pyyaml.org/wiki/PyYAMLDocumentation)。

### A161

**Spring Boot 3+Spring Security+Thymeleaf的示例**

原文：[software/web/spring-security/Spring Boot 3+Spring Security+Thymeleaf的示例/index.md](<C:/Project/blog/software/web/spring-security/Spring Boot 3+Spring Security+Thymeleaf的示例/index.md>)。

记录日期：2024-11-10T10:56:08+08:00；状态：内容未完成；现有文本已核阅。

示例停在 DraftRepository，尚未提供前言预告的认证页面、CRUD 页面和部署流程。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A162

**Spring Security 初探**

原文：[software/web/spring-security/Spring Security 初探/index.md](<C:/Project/blog/software/web/spring-security/Spring Security 初探/index.md>)。

记录日期：2023-12-30T14:44:37+08:00；状态：正文已核阅；有修改意见。

#### R288

**事实/技术错误 · 接口识别错误 · P2**

定位：[原文第 192 行](<C:/Project/blog/software/web/spring-security/Spring Security 初探/index.md:192>)；待改表述／主题：` 默认认证用AuthenticationFilter `。

原文定位行（节选）：`` 对于身份的验证，就属于其中一个过滤器——`AuthenticationFilter`，`AuthenticationFilter` 将对身份验证的职责委派给 `AuthenticationManager`，它是认证的主要策略接口： ``

问题：示例默认Basic与表单认证分别使用BasicAuthenticationFilter和UsernamePasswordAuthenticationFilter，不由AuthenticationFilter统一接管。

建议修改：说明这几个具体filter及共同委托AuthenticationManager的关系。

依据：[Spring 官方文档 · architecture](https://docs.spring.io/spring-security/reference/servlet/authentication/architecture.html)；[Spring 官方文档 · basic](https://docs.spring.io/spring-security/reference/servlet/authentication/passwords/basic.html)。

#### R289

**事实/技术错误 · 接口契约错误 · P2**

定位：[原文第 200 行](<C:/Project/blog/software/web/spring-security/Spring Security 初探/index.md:200>)；待改表述／主题：` AuthenticationManager无法决定返回null `。

原文定位行（节选）：`` 如果验证通过，`AuthenticationManager` 会返回一个 `Authentication` 对象，如果认证失败则会抛出 `AuthenticationException` 异常，如果无法决定则返回 null。 ``

问题：允许返回null交由其他provider尝试的是AuthenticationProvider；AuthenticationManager成功返回认证对象，否则抛AuthenticationException。

建议修改：把两者的返回值契约分开，ProviderManager最终不能认证时抛相应异常。

依据：[Spring 官方文档 · AuthenticationManager](https://docs.spring.io/spring-security/site/docs/current/api/org/springframework/security/authentication/AuthenticationManager.html)；[Spring 官方文档 · architecture](https://docs.spring.io/spring-security/reference/servlet/authentication/architecture.html)。

#### R290

**事实/技术错误 · 接口识别错误 · P2**

定位：[原文第 219 行](<C:/Project/blog/software/web/spring-security/Spring Security 初探/index.md:219>)；待改表述／主题：` 委托给UserDetailsManager `。

问题：DaoAuthenticationProvider查询用户依赖UserDetailsService；UserDetailsManager是含增删改功能的扩展，并非认证必需。

建议修改：219行改UserDetailsService；660行账号锁定/凭据过期等也是认证状态检查，并非仅授权判定。

依据：[Spring 官方文档 · architecture](https://docs.spring.io/spring-security/reference/servlet/authentication/architecture.html)。

#### R291

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 395 行](<C:/Project/blog/software/web/spring-security/Spring Security 初探/index.md:395>)；待改表述／主题：` 自定义UserDetailsService必须提供PasswordEncoder `。

问题：默认存在DelegatingPasswordEncoder；使用正确的{id}前缀编码可以无需自定义PasswordEncoder Bean。示例无前缀密码失败不等于框架要求二者成对自定义。

建议修改：说明无前缀密码与所用encoder不匹配；教学可显式配置，实际密码按相应算法编码。

依据：[Spring 官方文档 · password-storage](https://docs.spring.io/spring-security/reference/features/authentication/password-storage.html)。

#### R292

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 425 行](<C:/Project/blog/software/web/spring-security/Spring Security 初探/index.md:425>)；待改表述／主题：` HTTP Basic安全性低 `。

原文定位行（节选）：`` Spring Security 默认使用 HTTP Basic 认证方式，但它安全性低，并不适用大部分的程序架构。想要重写授权配置，可以扩展 `WebSecurityConfigurerAdapter` 类，然后重写 configure(`HttpSecurity` HTTP) 方法： ``

问题：Basic的Base64不加密，需TLS；是否适用与凭据管理、客户端场景和传输保护有关，不能单凭这种认证方式作笼统结论。

建议修改：说明Basic传输的是可恢复的凭据，必须在TLS下使用，并交代项目为何选表单/令牌方案。

依据：[RFC 7617](https://www.rfc-editor.org/rfc/rfc7617.html)。

### A163

**Spring Security用户管理**

原文：[software/web/spring-security/Spring Security用户管理/index.md](<C:/Project/blog/software/web/spring-security/Spring Security用户管理/index.md>)。

记录日期：2026-07-14T10:32:10；状态：正文已核阅；有修改意见。

#### R293

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 126 行](<C:/Project/blog/software/web/spring-security/Spring Security用户管理/index.md:126>)；待改表述／主题：` 认证后确保擦除凭证 `。

原文定位行（节选）：`` 在 `ProviderManager` 调用完认证 Provider 后，会去调用 `eraseCredentials`，确保敏感信息完成认证后就擦除，而不是一直保存： ``

问题：ProviderManager默认eraseCredentialsAfterAuthentication=True，但可以配置关闭；是否擦除还取决于结果是否实现CredentialsContainer。

建议修改：补默认开关和对象接口条件；eraseCredentials不是清除数据库保存的密码哈希。

依据：[Spring 官方文档 · architecture](https://docs.spring.io/spring-security/reference/servlet/authentication/architecture.html)。

#### R294

**字词/链接 · 字词错误 · P3**

定位：[原文第 461 行](<C:/Project/blog/software/web/spring-security/Spring Security用户管理/index.md:461>)；待改表述／主题：` 到目前位置 `。

原文定位行（节选）：` 到目前位置，已经理清了 Spring Security 对于用户和权限抽象的两个接口： `

问题：应为到目前为止。

建议修改：改为到目前为止。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A164

**Spring Security认证过程**

原文：[software/web/spring-security/Spring Security认证过程/index.md](<C:/Project/blog/software/web/spring-security/Spring Security认证过程/index.md>)。

记录日期：2026-07-15T10:23:26；状态：正文已核阅；有修改意见。

#### R295

**事实/技术错误 · 类型概念错误 · P2**

定位：[原文第 50 行](<C:/Project/blog/software/web/spring-security/Spring Security认证过程/index.md:50>)；待改表述／主题：` Principal可以是UserDetails `。

原文定位行（节选）：`` 和之前提到的 `UserDetails` 不同，`UserDetails` 处于用户名密码体系下的一个更加具体的层次，而 `Principal` 更加通用。`Principal` 经过认证后，可以是 `UserDetails`，也可以表示 JWT 或者匿名用户等。`Principal` 表示当前正在登录或已经登录的那个主体。 ``

问题：Authentication继承java.security.Principal，但其getPrincipal返回Object；通常的UserDetails并不继承Principal。

建议修改：区分Java Principal接口、Authentication对象和getPrincipal中的业务身份载荷。

依据：[Spring 官方文档 · architecture](https://docs.spring.io/spring-security/reference/servlet/authentication/architecture.html)；[Spring 官方文档 · UserDetails](https://docs.spring.io/spring-security/site/docs/current/api/org/springframework/security/core/userdetails/UserDetails.html)。

#### R296

**事实/技术错误 · 概念/未完句 · P2**

定位：[原文第 773 行](<C:/Project/blog/software/web/spring-security/Spring Security认证过程/index.md:773>)；待改表述／主题：` Stateless不需要SecurityContextRepository；这又 `。

原文定位行（节选）：` stateless 既不创建 HttpSession 来保存 Spring Security 的认证信息，也不从已有 HttpSession 中恢复认证信息，所不需要 SecurityContextRepository，可以从源码看到，如果是 stateless 模式，就会创建一个 NullSecurityContextRepository。 `

问题：无状态通常仍配置NullSecurityContextRepository或请求级Repository，不依赖HttpSession不等于不存在该抽象。673行句子未完成。

建议修改：改为不需要跨请求的会话持久化，但仍可通过Repository抽象装载/保存请求级上下文；补完673行。

依据：[Spring 官方文档 · persistence](https://docs.spring.io/spring-security/reference/servlet/authentication/persistence.html)。

### A165

**Spring Security配置SecurityFilterChain**

原文：[software/web/spring-security/Spring Security配置SecurityFilterChain/index.md](<C:/Project/blog/software/web/spring-security/Spring Security配置SecurityFilterChain/index.md>)。

记录日期：2026-07-12T13:53:57；状态：正文已核阅；有修改意见。

#### R297

**事实/技术错误 · 版本错误 · P2**

定位：[原文第 23 行](<C:/Project/blog/software/web/spring-security/Spring Security配置SecurityFilterChain/index.md:23>)；待改表述／主题：` 5.x之前…WebSecurityConfigurerAdapter `。

原文定位行（节选）：`` 在 Spring Security 老版本（5.x）之前，使用 `WebSecurityConfigurerAdapter` 来配置（需要一个配置类继承该类），但该类在新版本已经废弃，新版本使用配置类和 `@Bean` 来进行自定义配置。 ``

问题：该类在5.x中仍被使用，5.7弃用，6.0移除；并非只有5.x之前才用。

建议修改：明确版本边界；本文新版本代码保留SecurityFilterChain Bean方式。

依据：[Spring 官方说明 · spring-security-without-the-websecurityconfigureradapter](https://spring.io/blog/2022/02/21/spring-security-without-the-websecurityconfigureradapter)。

#### R298

**字词/链接 · 字词错误 · P3**

定位：[原文第 243 行](<C:/Project/blog/software/web/spring-security/Spring Security配置SecurityFilterChain/index.md:243>)；待改表述／主题：` 显示；不用；最佳时间；本是 `。

原文定位行（节选）：`` 最佳时间是，如果有多个 `SecurityFilterChain`，那么 `@Order` 的顺序应该是从小范围的具体匹配到最后的最大范围的兜底。 ``

问题：分别应为显式、不同、最佳实践、本质。

建议修改：187行显示→显式；199行不用→不同；243行最佳时间→最佳实践；322行本是→本质。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A166

**Spring Security默认配置**

原文：[software/web/spring-security/Spring Security默认配置/index.md](<C:/Project/blog/software/web/spring-security/Spring Security默认配置/index.md>)。

记录日期：2026-07-11T15:01:06；状态：正文已核阅；有修改意见。

#### R299

**条件/版本澄清 · 条件遗漏 · P2**

定位：[原文第 53 行](<C:/Project/blog/software/web/spring-security/Spring Security默认配置/index.md:53>)；待改表述／主题：` 不传凭据访问所有接口都会401 `。

原文定位行（节选）：` 我们在引入 Spring Security 依赖以后，并没有编写任何配置，日志就打印了一个 uuid 密码，并且访问所有接口，如果不传递用户名密码，就会 401，这是因为自动配置的机制，我们没有提供配置，Spring Boot 就默认给了我们一个最基本的配置： `

问题：默认同时启用formLogin和httpBasic，根据请求内容协商/入口点可能重定向登录页，也可能401；129行已展示跳转。

建议修改：说明浏览器和curl的典型差异；397行所有端口改所有匹配请求/接口。

依据：[Spring 官方文档 · spring-security](https://docs.spring.io/spring-boot/reference/web/spring-security.html)。

#### R300

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 342 行](<C:/Project/blog/software/web/spring-security/Spring Security默认配置/index.md:342>)；待改表述／主题：` 所有configurer最后都会addFilter `。

原文定位行（节选）：`` `HttpSecurity` 在配置过程中添加的所有 configurer, 都有 `configure` 方法，最后一步都会调用 `http.addFilter`。 ``

问题：部分configurer配置共享对象或其他属性，不各自添加filter；HttpSecurityConfiguration配置的是configurer，不能说注入前已创建了全部filter。

建议修改：按配置器登记→build/init/configure→实际filter添加→排序的流程表述；195、396行也改为默认启用的配置项。

依据：[Spring 官方文档 · PortMapperConfigurer](https://docs.spring.io/spring-security/site/docs/current/api/org/springframework/security/config/annotation/web/configurers/PortMapperConfigurer.html)。

### A167

**Spring Boot 中 @Component 和 @Bean 的区别**

原文：[software/web/spring/Spring Boot 中 @Component 和 @Bean 的区别/index.md](<C:/Project/blog/software/web/spring/Spring Boot 中 @Component 和 @Bean 的区别/index.md>)。

记录日期：2026-07-10T10:11:47；状态：正文已核阅；有修改意见。

#### R301

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 15 行](<C:/Project/blog/software/web/spring/Spring Boot 中 @Component 和 @Bean 的区别/index.md:15>)；待改表述／主题：` @Bean用在第三方类 `。

原文定位行（节选）：`` `@Bean` 用在第三方框架里的类，特点就是你无法修改第三方的源码，你不能在源码类上面添加注解。 ``

问题：@Bean也可以用于自定义类；第三方类只是常见应用场景。

建议修改：改为@Bean显式定义对象构造/工厂方法，特别适合不能修改源码的第三方对象。

依据：[Spring 官方文档 · basic-concepts](https://docs.spring.io/spring-framework/reference/core/beans/java/basic-concepts.html)。

#### R302

**条件/版本澄清 · 概念/条件遗漏 · P2**

定位：[原文第 72 行](<C:/Project/blog/software/web/spring/Spring Boot 中 @Component 和 @Bean 的区别/index.md:72>)；待改表述／主题：` Controller/Service/Repository完全没区别；Configuration总代理 `。

原文定位行（节选）：`` `@Controller` 和 `@Service` 以及 `@Repository` 都是和 `@Component` 没区别，`@Configuration` 虽然也是 `@Component`，但是稍微特殊一些，Spring 扫描到 `@Configuration` 注解的类生成的是代理对象。 ``

问题：Controller供MVC识别，Repository可配合异常转换；@Configuration(proxyBeanMethods=false)不代理，prototype Bean调用也不能笼统说总返回已有单例。

建议修改：说明共同具有组件扫描语义，各有扩展语义；代理示例限定proxyBeanMethods=true和singleton作用域。

依据：[Spring 官方文档 · classpath-scanning](https://docs.spring.io/spring-framework/reference/core/beans/classpath-scanning.html)；[Spring 官方文档 · basic-concepts](https://docs.spring.io/spring-framework/reference/core/beans/java/basic-concepts.html)。

#### R303

**字词/链接 · 字词错误 · P3**

定位：[原文第 151 行](<C:/Project/blog/software/web/spring/Spring Boot 中 @Component 和 @Bean 的区别/index.md:151>)；待改表述／主题：` MySerivce；考虑一下的 `。

原文定位行（节选）：`` 只剩两条日志了，是因为在注册 MySerivce `Bean` 时，`MyConfig` 的代理类（`MyConfig$$SpringCGLIB$$0@b25b095`）拦截了 database()，发现容器已经存在 `Database` `Bean`，就不会创建新的 `Database` 对象。 ``

问题：类名拼错，句子误字。

建议修改：151行MySerivce改MyService；76行改考虑以下三个类。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A168

**Spring Boot 中 Session 的使用**

原文：[software/web/spring/Spring Boot 中 Session 的使用/index.md](<C:/Project/blog/software/web/spring/Spring Boot 中 Session 的使用/index.md>)。

记录日期：2026-07-02T11:04:46；状态：正文已核阅；未发现可确认的明显错误。

本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。

### A169

**Spring Boot+JPA的日志打印问题**

原文：[software/web/spring/Spring Boot+JPA的日志打印问题/index.md](<C:/Project/blog/software/web/spring/Spring Boot+JPA的日志打印问题/index.md>)。

记录日期：2023-08-12T10:55:46+08:00；状态：正文已核阅；有修改意见。

#### R304

**事实/技术错误 · 概念错误 · P2**

定位：[原文第 62 行](<C:/Project/blog/software/web/spring/Spring Boot+JPA的日志打印问题/index.md:62>)；待改表述／主题：` format_sql结构化打印 `。

原文定位行（节选）：` 如果需要结构化打印，需要额外增加一个配置项： `

问题：Hibernate format_sql只是格式化SQL缩进和换行，不等于JSON/字段化结构化日志。

建议修改：改为格式化/美化SQL，不等于字段化结构化日志。115行BasicBinder适用于Hibernate5；Hibernate6通常使用logging.level.org.hibernate.orm.jdbc.bind=TRACE，注明版本。

依据：[docs.jboss.org · Hibernate_User_Guide · settings-logging](https://docs.jboss.org/hibernate/orm/6.6/userguide/html_single/Hibernate_User_Guide.html#settings-logging)。

### A170

**Spring MVC 接收前端参数的 N 种方式**

原文：[software/web/spring/Spring MVC 接收前端参数的 N 种方式/index.md](<C:/Project/blog/software/web/spring/Spring MVC 接收前端参数的 N 种方式/index.md>)。

记录日期：2023-02-12T18:23:56+08:00；状态：正文已核阅；有修改意见。

#### R305

**字词/链接 · 链接错误 · P3**

定位：[原文第 54 行](<C:/Project/blog/software/web/spring/Spring MVC 接收前端参数的 N 种方式/index.md:54>)；待改表述／主题：` 豆瓣和路径参数示例URL含中文 `。

原文定位行（节选）：` 有时候请求一些页面需要加一些简单的，不敏感的参数，比如分页信息，传输页面编号和数量，又比如博客网站，需要传递一个文章编号，这些简单的信息可以用 GET 请求，把参数加在 URL 后面，比如豆瓣的一个链接：[https://movie.douban.com/top250?start=125&filter=，里面有两个参数一个是](https://movie.douban.com/top250?start=125&filter=，里面有两个参数一个是) start，另一个是 fi… `

问题：54、129行把链接后的解释句写入目标URL。

建议修改：54行目标只保留https://movie.douban.com/top250?start=125&filter=；129行只保留http://myblog/post/123。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

### A171

**telegram-bot入门**

原文：[software/web/telegram/telegram-bot入门/index.md](<C:/Project/blog/software/web/telegram/telegram-bot入门/index.md>)。

记录日期：2026-08-24T23:16:34；状态：正文已核阅；有修改意见。

#### R306

**字词/链接 · 字词错误 · P3**

定位：[原文第 89 行](<C:/Project/blog/software/web/telegram/telegram-bot入门/index.md:89>)；待改表述／主题：` 没有用户消息是 `。

原文定位行（节选）：` 长轮询在没有用户消息是，tg server 不会立即返回，而是保持这个 HTTP 连接一段时间： `

问题：应为没有用户消息时。

建议修改：89行是→时；50行删除重复的要么。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R307

**事实/技术错误 · 协议表述错误 · P2**

定位：[原文第 110 行](<C:/Project/blog/software/web/telegram/telegram-bot入门/index.md:110>)；待改表述／主题：` 每次请求重新创建HTTP连接 `。

原文定位行（节选）：` 等待的过程中，如果有用户的新消息，tg server 就会立即返回，然后 bot server 收到消息后，再继续创建新的 HTTP 连接。 `

问题：独立HTTP请求不必每次建立新TCP/TLS连接，连接可复用；长轮询是在一个请求上等待。

建议修改：将110行等新建HTTP连接改为发起下一次HTTP请求，区分请求生命周期和底层连接复用。

依据：[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#section-3.3)。

#### R308

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 127 行](<C:/Project/blog/software/web/telegram/telegram-bot入门/index.md:127>)；待改表述／主题：` 每个用户发消息update_id+1 `。

原文定位行（节选）：` 假设用户发了一个消息，消息的 update_id = 176，那么用户发的下一个消息，update_id 就是 177，update_id 是用户发一条消息，数值就变大 1。 `

问题：update_id属于bot的Update序列，包含多用户和多种事件；长时间无新Update后下一个ID可随机选择。

建议修改：按bot更新流维护max(update_id)+1游标；不是每用户独立消息计数。

依据：[Telegram Bot API · api · update](https://core.telegram.org/bots/api#update)。

#### R309

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 354 行](<C:/Project/blog/software/web/telegram/telegram-bot入门/index.md:354>)；待改表述／主题：` reply keyboard不允许随意输入 `。

原文定位行（节选）：` reply keyboard 会更改用户输入框，最简单的用法，就是类似下拉列表，提供给用户系统允许范围的可选值，避免用户输入错误。 `

问题：ReplyKeyboardMarkup只是提供输入按钮，用户仍可手工输入其他文本，不能替代服务端校验。

建议修改：说明仍需检查消息值；若需要明确的回调动作可用inline callback_data，但同样校验输入。

依据：[Telegram Bot API · api · replykeyboardmarkup](https://core.telegram.org/bots/api#replykeyboardmarkup)。

### A172

**使用Telegram机器人实现告警功能**

原文：[software/web/telegram/使用Telegram机器人实现告警功能/index.md](<C:/Project/blog/software/web/telegram/使用Telegram机器人实现告警功能/index.md>)。

记录日期：2026-03-12T10:24:49；状态：正文已核阅；有修改意见。

#### R310

**字词/链接 · 字词错误 · P3**

定位：[原文第 23 行](<C:/Project/blog/software/web/telegram/使用Telegram机器人实现告警功能/index.md:23>)；待改表述／主题：` 按一下顺序 `。

原文定位行（节选）：`` 首先需要建立一个机器人，在 `@BotFather` 下按一下顺序建立好机器人： ``

问题：应为按以下顺序。

建议修改：改为按以下顺序。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R311

**事实/技术错误 · 依赖遗漏 · P2**

定位：[原文第 112 行](<C:/Project/blog/software/web/telegram/使用Telegram机器人实现告警功能/index.md:112>)；待改表述／主题：` application.job_queue.run_repeating `。

原文定位行（节选）：` job_queue.run_repeating(check_memory_job, interval=10, first=0) `

问题：JobQueue是可选依赖，普通安装python-telegram-bot可能使job_queue为None，示例会失败。

建议修改：补安装python-telegram-bot[job-queue]的命令；说明告警定时任务与接收Update的polling互不等价。

依据：[docs.python-telegram-bot.org · telegram.ext.jobqueue](https://docs.python-telegram-bot.org/en/stable/telegram.ext.jobqueue.html)。

#### R312

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 128 行](<C:/Project/blog/software/web/telegram/使用Telegram机器人实现告警功能/index.md:128>)；待改表述／主题：` webhook性能一定比轮询更好 `。

原文定位行（节选）：` 回调函数的性能比轮询更好，节省资源，但缺点是需要配置了 HTTPS 的公网域名。 `

问题：长轮询不会不断制造无意义的短轮询请求；两种方案的资源/延迟受连接、流量与托管方式影响，不能无条件排名。

建议修改：比较长轮询与webhook适用部署条件；66行明确库默认通常使用长轮询。

依据：[Telegram Bot API · api · getupdates](https://core.telegram.org/bots/api#getupdates)。

### A173

**关于前后端接口规范的讨论**

原文：[software/web/关于前后端接口规范的讨论/index.md](<C:/Project/blog/software/web/关于前后端接口规范的讨论/index.md>)。

记录日期：2026-02-26T16:29:54；状态：正文已核阅；有修改意见。

#### R313

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 19 行](<C:/Project/blog/software/web/关于前后端接口规范的讨论/index.md:19>)；待改表述／主题：` HTTP Code怎么用从来没有统一标准 `。

原文定位行（节选）：` 其实只要是做 web 开发的，无论前端还是后端，只要换的公司数量够多，或者看过的开源框架数量够多，都会碰到这个问题，因为对于 HTTP Code 该不该用，该怎么用，从来都没有一个统一的标准，有的团队坚持 RESTful，有的团队坚持只有 GET+POST，足够宽松的 HTTP 协议并没有对前后端通信中产生的业务问题做出什么约束，所以大家各行其道。 `

问题：HTTP状态码语义由RFC定义，具体业务错误映射可由团队约定。引用中的所有4xx都无重试意义也有429等反例。

建议修改：区分协议标准与业务映射规范；给引文加注：429可按Retry-After重试，5xx也不是全部可无条件重试。RFC7807已有RFC9457替代。

依据：[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html)；[RFC 6585](https://www.rfc-editor.org/rfc/rfc6585.html#section-4)；[RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html)。

### A174

**请求外部接口需要做的准备**

原文：[software/web/请求外部接口需要做的准备/index.md](<C:/Project/blog/software/web/请求外部接口需要做的准备/index.md>)。

记录日期：2026-08-28T21:06:03；状态：正文已核阅；有修改意见。

#### R314

**字词/链接 · 字词错误 · P3**

定位：[原文第 22 行](<C:/Project/blog/software/web/请求外部接口需要做的准备/index.md:22>)；待改表述／主题：` Server Internal Error；受到；ConnctionError；不可以 `。

原文定位行（节选）：` - 对方服务状态不可控，随时可能 Server Internal Error（status code == 500）。 `

问题：HTTP常用名称为Internal Server Error；其余按上下文为收到、ConnectionError、不可用。

建议修改：22行改Internal Server Error；35/408行受到→收到；236行ConnctionError→ConnectionError；503行不可以→不可用。

依据：[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.6.1)。

#### R315

**事实/技术错误 · 异常类型错误 · P2**

定位：[原文第 78 行](<C:/Project/blog/software/web/请求外部接口需要做的准备/index.md:78>)；待改表述／主题：` 把Timeout画成ConnectTimeout的子类 `。

原文定位行（节选）：` │       └── Timeout `

问题：ConnectTimeout同时继承ConnectionError和Timeout，Timeout并非ConnectTimeout的子类；JSONDecodeError也存在兼容JSON异常的多继承。

建议修改：将树图改为带多父类标注的关系图，或列类与直接父类表；至少更正78行的继承方向。

依据：[Requests 文档／源码 · exceptions](https://requests.readthedocs.io/en/latest/_modules/requests/exceptions/)。

#### R316

**条件/版本澄清 · 适用条件 · P2**

定位：[原文第 402 行](<C:/Project/blog/software/web/请求外部接口需要做的准备/index.md:402>)；待改表述／主题：` time.monotonic加流读取可硬限制总时长 `。

原文定位行（节选）：` 如果想硬性限制整个请求的总时长，requests 的 timeout 做不到，得在应用代码层面通过 time.monotonic() 计时，主动在流读取过程中处理超时终止。 `

问题：仅在读取间隙检查计时无法中断当前阻塞读取，还受DNS和单次socket等待等影响。

建议修改：区分协作式截止时间和可取消的硬期限；将剩余预算传递到每一步，或使用有总deadline/取消能力的客户端和执行机制。

依据：[Requests 文档／源码 · advanced · timeouts](https://requests.readthedocs.io/en/latest/user/advanced/#timeouts)；[Python 官方文档 · time · time.monotonic](https://docs.python.org/3/library/time.html#time.monotonic)。

#### R317

**事实/技术错误 · 事实错误 · P2**

定位：[原文第 408 行](<C:/Project/blog/software/web/请求外部接口需要做的准备/index.md:408>)；待改表述／主题：` raise_for_status针对所有非2xx `。

原文定位行（节选）：` requests 受到响应后，如果响应的 status code 不是 2xx, 并不会抛出 HTTPError 的异常，如果想要在非 2xx 的情况下抛出 HTTPError,需要调用 raise\_for\_status() 的方法。 `

问题：Requests仅对400～599范围状态码抛HTTPError，3xx等不因这个方法失败。

建议修改：改为4xx/5xx；若业务要求严格2xx，应另做200<=status_code<300判断。

依据：[Requests 文档／源码 · models](https://requests.readthedocs.io/en/latest/_modules/requests/models/)。

### A175

**我的技术小结-2025**

原文：[software/我的技术小结-2025/index.md](<C:/Project/blog/software/我的技术小结-2025/index.md>)。

记录日期：2025-11-22T09:37:54；状态：正文已核阅；有修改意见。

#### R318

**字词/链接 · 字词错误 · P3**

定位：[原文第 31 行](<C:/Project/blog/software/我的技术小结-2025/index.md:31>)；待改表述／主题：` 旳；21世界；人力成文 `。

原文定位行（节选）：` 21 世界的敲着键盘的程序员，从某些角度来看和那些踩着缝纫机的纺织工人是没啥两样的，有一点不一样的是，现在并没有太多人反对 AI 结对编程，更别提“打砸烧毁”机器，我们恨不得购买更多的显卡和 API tokens 来让 AI 为我们工作。可以预见在不远的将来，除了创意性的工作（绘画，影视，音乐，书籍，编码，新闻等等）会交给 AI 之外，配置了 AI 的人形机器人，会开着车，送着快递和外卖。 `

问题：分别应为的、21世纪、人力成本。

建议修改：29行旳→的；31行世界→世纪；91行成文→成本。

依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。

#### R319

**条件/版本澄清 · 术语条件澄清 · P2**

定位：[原文第 57 行](<C:/Project/blog/software/我的技术小结-2025/index.md:57>)；待改表述／主题：` 孤独症蔓延在社交网络之中 `。

原文定位行（节选）：` - 社会变得更加冷漠，人人自危，焦虑、抑郁和孤独症蔓延在热闹繁华的社交网络之中。 `

问题：孤独症通常指自闭症谱系障碍，不是孤独感的同义词；此处若意指社交环境中的孤独情绪，用词会误导。

建议修改：如意指loneliness，改为孤独感；如果确实讨论自闭症谱系障碍，应单独提供其流行病学证据，不能从社会感受推定。

依据：[WHO 资料 · autism-spectrum-disorders](https://www.who.int/news-room/fact-sheets/detail/autism-spectrum-disorders)。

#### R320

**事实/技术错误 · 技术断言错误 · P2**

定位：[原文第 89 行](<C:/Project/blog/software/我的技术小结-2025/index.md:89>)；待改表述／主题：` 不可以在CPU密集型任务使用CPython `。

原文定位行（节选）：` 每个语言都有自己擅长的地方，就像是你不可以在一个 CPU 密集型的任务里面使用 CPython，你也用不着在一个 IO 密集型的应用里纠结那 1% 的性能优化，你不必在一个简单脚本的 JSON 解析里面，用冗长的 Java 代码来折磨自己，在没有成熟团队的支持下，一些较小规模的项目，也不要硬上分布式和微服务，而对于业务复杂，抽象和建模比较重要的场景下，也不要用过程式的代码堆出一座巨大的屎山，折磨阅读你代码的每一个人。 `

问题：CPython可执行CPU密集任务；NumPy等释放GIL的原生扩展、多进程或适当工作量都可使用。

建议修改：改为纯Python字节码CPU密集任务的多线程受GIL约束，需按库实现和性能预算选方案。

依据：[Python 官方文档 · threading · gil-and-performance-considerations](https://docs.python.org/3/library/threading.html#gil-and-performance-considerations)。

## 验证与复核记录

本地针对性验证 **18 项通过、1 项跳过**。环境为 Python 3.13.5、SQLite 3.49.1；验证了 SQLite NULL 主键及自增元数据、logging 过滤与 QueueHandler 行为、JSON 截断、导入语法、Future 失败结果、更新器参数检查、搜索参数编码和截断 HTTP 响应读取等。

本地未安装 Requests，因此对应本地探针跳过；`raise_for_status()` 和异常多继承关系改由 Requests 官方源码核对。探针验证的是具体行为，不能代替整篇示例的端到端运行。结果：[probe-results.json](<C:/Project/MyProject/blogger/docs/blog-audit-2026-10-02/probe-results.json>)。

复核撤回了以下候选，未计入 320 条意见：

- SQLite CLI 接受 `.headers` 的无歧义前缀 `.header`，不能判为无效命令。
- 防火墙教程已展示 `--permanent` 和 reload，不能概括成文章所有运行时修改均不生效。
- SHA-512 与 SHA-256 的性能受实现和硬件影响，缺少对照数据的速度判断未列为确认错误。
- BusyBox 恢复 rpm 的文章是特定静态构建的个人实践，已给出静态前提，不能凭工具功能边界否定该经历。

Redis 大偏移分页的候选也未列入：原文实际使用 score 范围分页，偏移扫描成本的说明成立。

便于后续逐条修订的结构化清单：[findings.json](<C:/Project/MyProject/blogger/docs/blog-audit-2026-10-02/findings.json>)；覆盖、状态和原文 SHA-256 快照：[coverage.json](<C:/Project/MyProject/blogger/docs/blog-audit-2026-10-02/coverage.json>)。

原文 Git HEAD：`882620b614f45d2873a372926993120cee6e663f`。交付前检查原文工作树无改动。行号以此次本地快照为准；今后修改原文后应重新定位。
