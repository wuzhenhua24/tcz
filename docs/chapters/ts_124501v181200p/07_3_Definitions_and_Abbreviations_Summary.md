# 07_3 Definitions and Abbreviations 章节总结分析

## 文档基本信息

- **文档编号**: 3GPP TS 24.501
- **版本**: version 18.12.0 Release 18
- **发布日期**: 2025-10
- **章节**: 第 3 章 Definitions and abbreviations

## 章节概述

本章节定义了 3GPP TS 24.501 规范中使用的术语和缩略语，是理解 5G 系统 NAS 协议的基础。章节包含两个主要部分：
- **3.1 Definitions（定义）**：详细定义了本规范使用的专业术语
- **3.2 Abbreviations（缩略语）**：列出了所有缩略语及其全称

**优先级原则**：本文档中定义的术语优先于 3GPP TR 21.905 中的同名术语定义。

---

## 3.1 Definitions（定义）核心内容分析

### 1. UE 状态和模式定义

#### 5GMM 模式
- **5GMM-IDLE mode**: UE 空闲模式，可用于 3GPP 或非 3GPP 接入
  - **5GMM-IDLE mode over 3GPP access**: 3GPP 接入上的空闲模式（无 N1 NAS 信令连接）
  - **5GMM-IDLE mode over non-3GPP access**: 非 3GPP 接入上的空闲模式

- **5GMM-CONNECTED mode**: UE 连接模式，可用于 3GPP 或非 3GPP 接入
  - **5GMM-CONNECTED mode over 3GPP access**: 3GPP 接入上的连接模式（存在 N1 NAS 信令连接）
  - **5GMM-CONNECTED mode over non-3GPP access**: 非 3GPP 接入上的连接模式

**对应关系**：这些术语对应于 TS 23.501 中的 CM-IDLE 和 CM-CONNECTED 状态。

#### N1 模式变体
- **N1 mode**: UE 允许通过 5G 接入网络访问 5G 核心网络的模式
- **NB-N1 mode**: 通过 NB-IoT 连接到 5GCN 的 E-UTRA 提供网络服务
- **WB-N1 mode**: E-UTRA 连接到 5GCN 但不在 NB-N1 模式
- **WB-N1/CE mode**: CE 模式 B 能力的 UE 在 WB-N1 模式下运行 CE 模式 A 或 B

### 2. 安全相关定义

#### 加密和完整性算法
- **5G-EA (5GS Encryption Algorithms)**: 5GS 加密算法
  - 包括：5G-EA0, 128-5G-EA1, 128-5G-EA2, 128-5G-EA3, 5G-EA4, 5G-EA5, 5G-EA6, 5G-EA7
  - 对应 TS 33.501 中的 NEA 系列

- **5G-IA (5GS Integrity Algorithms)**: 5GS 完整性算法
  - 包括：5G-IA0, 128-5G-IA1, 128-5G-IA2, 128-5G-IA3, 5G-IA4, 5G-IA5, 5G-IA6, 5G-IA7
  - 对应 TS 33.501 中的 NIA 系列

#### 信息元素安全
- **Cleartext IEs**: 可以在初始 NAS 消息中不加密发送的信息元素
- **Non-cleartext IEs**: 非明文信息元素

### 3. 接入层连接定义

**Access stratum connection**: 点对点接入层连接，根据接入类型不同包括：
- **3GPP 接入**: UE 与 NG-RAN 之间（通过 Uu 参考点的 RRC 连接）
- **不可信非 3GPP 接入**: UE 与 N3IWF 之间（IKE_SA_INIT 交换完成）
- **可信非 3GPP 接入（UE 使用）**: UE 与 TNGF 之间
- **可信非 3GPP 接入（N5CW 设备使用）**: TWIF 代表 N5CW 设备
- **有线接入（5G-RG 使用）**: 5G-RG 与 W-AGF 之间（W-CP 协议栈）
- **有线接入（FN-RG 使用）**: W-AGF 代表 FN-RG
- **有线接入（N5GC 设备使用）**: W-AGF 代表 N5GC 设备

### 4. 网络切片相关定义

#### NSSAI 相关术语
- **Alternative NSSAI**: 被替换的 S-NSSAI 和替代 S-NSSAI 之间的映射信息列表
- **Default S-NSSAI**: 标记为默认的订阅 S-NSSAI
- **HPLMN S-NSSAI**: 在 HPLMN 中无需进一步映射即可应用的 S-NSSAI
- **Mapped S-NSSAI**: HPLMN 或订阅 SNPN 的订阅 S-NSSAI，注册 PLMN 的 S-NSSAI 映射到该 S-NSSAI
- **On-demand S-NSSAI**: UE 仅在需要建立 PDU 会话时才允许请求的 S-NSSAI
- **Partially rejected NSSAI**: 在某些 TA 中被拒绝但不是所有 TA 的 S-NSSAI

#### Rejected NSSAI（被拒 NSSAI）类型
- **Rejected NSSAI for the current PLMN or SNPN**: 当前 PLMN/SNPN 不可用
- **Rejected NSSAI for the current registration area**: 当前注册区域不可用
- **Rejected NSSAI for the failed or revoked NSSAA**: 由于 NSSAA 失败或撤销而不可用
- **Rejected NSSAI for the maximum number of UEs reached**: 达到最大 UE 数量

#### 网络切片信息
**Network slicing information**: UE 存储的信息，包括：
- 默认配置 NSSAI、配置 NSSAI
- NSSRG 信息、S-NSSAI 位置有效性信息、S-NSSAI 时间有效性信息
- 映射的 S-NSSAI、待处理 NSSAI、被拒 NSSAI
- 每种接入类型的：允许 NSSAI、替代 NSSAI、按需 NSSAI
- 3GPP 接入类型的：NSAG 信息、部分允许 NSSAI、部分被拒 NSSAI

### 5. PDU 会话相关定义

#### PDU 会话类型
- **Always-on PDU session**: 每次从 5GMM-IDLE 转换到 5GMM-CONNECTED 时都必须建立用户面资源的 PDU 会话
- **Emergency PDU session**: 使用"初始紧急请求"或"现有紧急 PDU 会话"请求类型建立的 PDU 会话
- **Non-emergency PDU session**: 任何非紧急 PDU 会话
- **Persistent PDU session**: 持久性 PDU 会话（包含特定 QoS 流的非紧急会话或紧急会话）
- **PDU session for LADN**: 与 LADN 关联的 DNN 的 PDU 会话
- **PDU session with suspended user-plane resources**: 用户面资源已建立但数据无线承载被挂起的 PDU 会话
- **N6 PDU session**: UE 与 UPF 之间传输 IP/Ethernet/非结构化数据的 PDU 会话
- **NEF PDU session**: UE 与 NEF 之间传输非结构化数据的 PDU 会话

#### DNN 相关定义
- **DNN determined by the AMF**: AMF 根据订阅信息或本地策略确定的 DNN
- **DNN requested by the UE**: UE 显式请求并包含在 NAS 请求消息中的 DNN
- **DNN selected by the network**: 网络选择的 DNN（考虑 DNN 替换）

#### PDU 会话资源
- **User-plane resources**: UE 和 UPF 之间建立的资源，根据接入类型包括：
  - 3GPP 接入：用户面无线承载（Uu）+ N3 隧道 + N9 隧道
  - 不可信非 3GPP 接入：IPsec 隧道（NWu）+ N3 隧道 + N9 隧道
  - 可信非 3GPP 接入：IPsec 隧道（NWt）或 L2 连接 + N3 隧道 + N9 隧道
  - 有线接入：W-UP 资源（Y4）或 L-W-UP 资源（Y5）+ N3 隧道 + N9 隧道

### 6. 注册相关定义

#### 注册类型
- **Initial registration for emergency services**: 使用"紧急注册"类型进行的注册
- **Initial registration for onboarding services in SNPN**: 使用"SNPN 入网注册"类型进行的注册
- **Initial registration for disaster roaming services**: 使用"灾难漫游初始注册"类型进行的注册
- **Mobility registration for disaster roaming services**: 使用"灾难漫游移动性注册更新"类型进行的注册

#### 注册状态
- **Registered for emergency services**: 成功完成紧急服务初始注册的 UE
- **Registered for onboarding services in SNPN**: 成功完成 SNPN 入网服务初始注册的 UE
- **Registered for disaster roaming services**: 成功完成灾难漫游服务注册的 UE
- **Registered PLMN**: UE 执行最后一次成功注册的 PLMN（通过 5G-GUTI 的 GUAMI 字段提供）

### 7. SNPN 相关定义

- **SNPN access operation mode**: UE 仅选择 SNPN 的操作模式（等同于 TS 23.501 中的"SNPN 接入模式"）
- **Access to SNPN services via a PLMN**: UE 使用 PLMN 的 3GPP 接入连接到 SNPN 的 5GCN
- **Globally-unique SNPN identity**: NID 的分配模式不设置为 1 的 SNPN 身份
- **Non-globally-unique SNPN identity**: NID 的分配模式设置为 1 的 SNPN 身份
- **Onboarding SUPI**: SNPN 接入操作模式下的 UE 从默认 UE 凭证派生的 SUPI
- **Onboarding SUCI**: 从入网 SUPI 派生的 SUCI

### 8. CAG（封闭接入组）相关定义

- **CAG cell**: 只有 CAG 成员可以获得正常服务的小区
- **CAG-ID**: PLMN 范围内唯一标识 CAG 的标识符
- **CAG restrictions**: 应用于 UE 接入 PLMN 5GCN 的限制
  - 通过非 CAG 小区（如果 UE 仅允许通过 CAG 小区访问）
  - 通过 CAG 小区（如果 CAG-ID 未经授权）
- **Non-CAG Cell**: 不广播任何 CAG 身份的 NR 小区或连接到 5GCN 的 E-UTRA 小区

### 9. CIoT 5GS 优化定义

- **Control plane CIoT 5GS optimization**: 通过 AMF 在控制面传输用户数据（IP、Ethernet、非结构化或 SMS）的信令优化
- **User plane CIoT 5GS optimization**: 通过用户面传输用户数据（IP、Ethernet 或非结构化）的信令优化
- **UE supporting CIoT 5GS optimizations**: 支持控制面或用户面 CIoT 5GS 优化的 UE
- **Registered for 5GS services with control plane CIoT 5GS optimization**: 网络接受控制面 CIoT 优化的 UE
- **Registered for 5GS services with user plane CIoT 5GS optimization**: 网络接受用户面 CIoT 优化的 UE

### 10. 拥塞控制定义

- **General NAS level congestion control**: 移动性管理级别的通用拥塞控制
- **DNN based congestion control**: 基于 DNN 的会话管理级别拥塞控制
- **S-NSSAI based congestion control**: 基于 S-NSSAI 的会话管理级别拥塞控制

### 11. 特殊 UE 类型定义

- **MUSIM UE**: 具有多个有效 USIM 的 UE，能够使用这些 USIM 的身份和凭证同时维护独立的注册状态
- **MBSR-UE**: 作为 MBSR 运行并支持本规范中 UE NAS 功能的 UE
- **UE supporting UAS services**: 支持无人机系统（UAS）服务的 UE
- **N5CW device**: 不能通过 WLAN 接入网络支持 5GCN NAS 信令的设备
- **N5CW device supporting 3GPP access**: 支持作为 3GPP 接入中的 UE 的 N5CW 设备

### 12. 小区和网络类型定义

- **NG-RAN cell**: 具有 NG-RAN 接入技术或卫星 NG-RAN 接入技术的小区
- **Satellite NG-RAN cell**: 具有卫星 NG-RAN 接入技术的小区
- **Non-satellite NG-RAN cell**: 具有 NG-RAN 接入技术的小区
- **Satellite NG-RAN RAT type**: 卫星 NG-RAN 接入的 RAT 类型（NR(LEO)、NR(MEO)、NR(GEO)）

### 13. 其他重要定义

- **N1 NAS signalling connection**: UE 和 AMF 之间的点对点 N1 模式连接
- **Initial NAS message**: 可以触发建立 N1 NAS 信令连接的 NAS 消息
- **Procedure transaction identity**: UE 为 UE 请求的 5GSM 过程动态分配的身份
- **Current TAI**: UE 驻留小区广播的选定 PLMN 的 TAI
- **Last visited registered TAI**: UE 注册到网络的注册区域中最后访问的 TAI
- **Mapped 5G-GUTI**: 从 MME 先前分配的 4G-GUTI 映射的 5G-GUTI
- **Native 5G-GUTI**: AMF 先前分配的 5G-GUTI
- **NITZ information**: 网络身份和时区信息（包括网络全名、短名、时区等）
- **Home country**: HPLMN 所在的国家
- **Local release**: 无 UE 和网络之间端到端信令的 PDU 会话释放

### 14. 引用其他规范的定义

本规范还引用了大量其他 3GPP 规范中的定义，包括：
- **TS 22.261**: Non-public network, Disaster Roaming, satellite NG-RAN
- **TS 23.003**: 5G-GUTI, SUPI, SUCI, IMSI, IMEI 等标识符
- **TS 23.122**: PLMN 选择、SNPN 选择、CAG 选择等
- **TS 23.501**: 5G 系统架构相关术语（Network slice, PDU session, QoS flow 等）
- **TS 24.301**: EPS 相关术语
- **TS 33.501**: 安全上下文相关术语
- **TS 23.256**: UAS（无人机系统）相关术语
- **TS 24.554**: 5G ProSe 相关术语
- **TS 24.587**: V2X 相关术语

---

## 3.2 Abbreviations（缩略语）核心内容分析

### 缩略语统计

本节包含 **200+ 个缩略语**，涵盖 5G 系统的各个方面。

### 按功能域分类的主要缩略语

#### 1. 核心系统标识和架构（30+ 个）

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| 5GCN | 5G Core Network | 5G 核心网络 |
| 5GS | 5G System | 5G 系统 |
| 5GMM | 5GS Mobility Management | 5GS 移动性管理 |
| 5GSM | 5GS Session Management | 5GS 会话管理 |
| 5G-GUTI | 5G-Globally Unique Temporary Identifier | 5G 全球唯一临时标识符 |
| 5G-RG | 5G Residential Gateway | 5G 住宅网关 |
| AMF | Access and Mobility Management Function | 接入和移动性管理功能 |
| SMF | Session Management Function | 会话管理功能 |
| UPF | User Plane Function | 用户面功能 |
| AUSF | Authentication Server Function | 认证服务器功能 |
| UDM | Unified Data Management | 统一数据管理 |
| PCF | Policy Control Function | 策略控制功能 |
| NEF | Network Exposure Function | 网络开放功能 |

#### 2. 网络切片相关（15+ 个）

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| NSSAI | Network Slice Selection Assistance Information | 网络切片选择辅助信息 |
| S-NSSAI | Single NSSAI | 单个 NSSAI |
| NSSAA | Network slice-specific authentication and authorization | 网络切片特定认证和授权 |
| NSSAAF | Network Slice-Specific and SNPN authentication and authorization Function | 网络切片和 SNPN 认证授权功能 |
| NSAC | Network Slice Admission Control | 网络切片准入控制 |
| NSACF | Network Slice Admission Control Function | 网络切片准入控制功能 |
| NSAG | Network slice AS group | 网络切片 AS 组 |
| NS-AoS | Network slice area of service | 网络切片服务区域 |
| NSSRG | Network Slice Simultaneous Registration Group | 网络切片同时注册组 |

#### 3. PDU 会话和 QoS（20+ 个）

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| PDU | Protocol Data Unit | 协议数据单元 |
| DNN | Data Network Name | 数据网络名称 |
| APN | Access Point Name | 接入点名称 |
| QoS | Quality of Service | 服务质量 |
| 5QI | 5G QoS Identifier | 5G QoS 标识符 |
| QFI | QoS Flow Identifier | QoS 流标识符 |
| QRI | QoS Rule Identifier | QoS 规则标识符 |
| AMBR | Aggregate Maximum Bit Rate | 聚合最大比特率 |
| GFBR | Guaranteed Flow Bit Rate | 保证流比特率 |
| MFBR | Maximum Flow Bit Rate | 最大流比特率 |
| RQA | Reflective QoS Attribute | 反射 QoS 属性 |
| RQI | Reflective QoS Indication | 反射 QoS 指示 |
| LADN | Local Area Data Network | 本地区域数据网络 |
| MA PDU | Multi-Access PDU | 多接入 PDU |

#### 4. 安全相关（15+ 个）

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| AKA | Authentication and Key Agreement | 认证和密钥协商 |
| AKMA | Authentication and Key Management for Applications | 应用认证和密钥管理 |
| A-KID | AKMA Key Identifier | AKMA 密钥标识符 |
| A-TID | AKMA Temporary Identifier | AKMA 临时标识符 |
| ABBA | Anti-Bidding down Between Architectures | 架构间防降级 |
| EAP-AKA' | Improved EAP method for 3rd generation AKA | 改进的 EAP-AKA 方法 |
| SUPI | Subscription Permanent Identifier | 订阅永久标识符 |
| SUCI | Subscription Concealed Identifier | 订阅隐藏标识符 |
| KSI | Key Set Identifier | 密钥集标识符 |
| MAC | Message Authentication Code | 消息认证码 |
| ECIES | Elliptic Curve Integrated Encryption Scheme | 椭圆曲线集成加密方案 |

#### 5. 无线接入网络（15+ 个）

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| NG-RAN | Next Generation Radio Access Network | 下一代无线接入网 |
| NR | New Radio | 新空口 |
| E-UTRAN | Evolved Universal Terrestrial Radio Access Network | 演进的通用陆地无线接入网 |
| RAN | Radio Access Network | 无线接入网 |
| TA | Tracking Area | 跟踪区 |
| TAC | Tracking Area Code | 跟踪区码 |
| TAI | Tracking Area Identity | 跟踪区标识 |
| CGI | Cell Global Identity | 小区全球标识 |
| LEO | Low Earth Orbit | 低地球轨道 |
| MEO | Medium Earth Orbit | 中地球轨道 |
| GEO | Geostationary Orbit | 地球静止轨道 |
| IAB | Integrated access and backhaul | 集成接入和回传 |

#### 6. 用户和设备标识（15+ 个）

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| IMSI | International Mobile Subscriber Identity | 国际移动用户识别码 |
| IMEI | International Mobile station Equipment Identity | 国际移动设备识别码 |
| IMEISV | IMEI and Software Version number | IMEI 和软件版本号 |
| PEI | Permanent Equipment Identifier | 永久设备标识符 |
| GUAMI | Globally Unique AMF Identifier | 全球唯一 AMF 标识符 |
| 5G-S-TMSI | 5G S-Temporary Mobile Subscription Identifier | 5G S-临时移动用户标识 |
| 5G-TMSI | 5G Temporary Mobile Subscription Identifier | 5G 临时移动用户标识 |
| NAI | Network Access Identifier | 网络接入标识符 |
| GLI | Global Line Identifier | 全局线路标识符 |
| GCI | Global Cable Identifier | 全局电缆标识符 |

#### 7. SNPN 和 NPN 相关（10+ 个）

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| SNPN | Stand-alone Non-Public Network | 独立非公共网络 |
| NPN | Non-public network | 非公共网络 |
| PNI-NPN | Public Network Integrated Non-Public Network | 公共网络集成非公共网络 |
| ON-SNPN | Onboarding Standalone Non-Public Network | 入网独立非公共网络 |
| NID | Network identifier | 网络标识符 |
| CAG | Closed access group | 封闭接入组 |
| GIN | Group ID for Network Selection | 网络选择组 ID |

#### 8. IoT 和优化相关（10+ 个）

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| CIoT | Cellular IoT | 蜂窝物联网 |
| N5CW | Non-5G-Capable over WLAN | 非 5G 能力通过 WLAN |
| N5GC | Non-5G Capable | 非 5G 能力 |
| MICO | Mobile Initiated Connection Only | 仅移动发起连接 |
| eDRX | Extended DRX cycle | 扩展 DRX 周期 |
| WUS | Wake-up signal | 唤醒信号 |
| SDT | Small Data Transmission | 小数据传输 |
| DDX | Downlink Data Expected | 预期下行数据 |

#### 9. V2X 和 ProSe 相关（10+ 个）

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| V2X | Vehicle-to-Everything | 车联万物 |
| V2XP | V2X policy | V2X 策略 |
| ProSe | Proximity based Services | 邻近服务 |
| ProSeP | 5G ProSe policy | 5G ProSe 策略 |
| PIN | Personal IoT Network | 个人物联网 |
| PINE | PIN Element | PIN 元素 |
| PEGC | PIN Element with Gateway Capability | 具有网关能力的 PIN 元素 |
| PEMC | PIN Element with Management Capability | 具有管理能力的 PIN 元素 |

#### 10. UAS（无人机系统）相关（10+ 个）

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| UAS | Uncrewed Aerial System | 无人机系统 |
| UAV | Uncrewed Aerial Vehicle | 无人机 |
| UAV-C | Uncrewed Aerial Vehicle-Controller | 无人机控制器 |
| USS | UAS Service Supplier | UAS 服务供应商 |
| UUAA | USS UAV Authorization/Authentication | USS UAV 授权/认证 |
| A2X | Aircraft-to-Everything | 飞机到万物 |
| A2XP | A2X policy | A2X 策略 |

#### 11. 边缘计算相关（10+ 个）

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| EAS | Edge Application Server | 边缘应用服务器 |
| EASDF | Edge Application Server Discovery Function | 边缘应用服务器发现功能 |
| ECS | Edge Configuration Server | 边缘配置服务器 |
| ECSP | Edge Computing Service Provider | 边缘计算服务提供商 |
| EDC | Edge DNS Client | 边缘 DNS 客户端 |
| EEC | Edge Enabler Client | 边缘使能客户端 |

#### 12. 时间敏感网络（TSN）相关（8+ 个）

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| TSN | Time-Sensitive Networking | 时间敏感网络 |
| TSC | Time Sensitive Communication | 时间敏感通信 |
| TSCTSF | Time Sensitive Communication and Time Synchronization Function | 时间敏感通信和时间同步功能 |
| DS-TT | Device-Side TSN Translator | 设备侧 TSN 转换器 |
| PTP | Precision Time Protocol | 精密时间协议 |

#### 13. MBS（组播/广播服务）相关（5+ 个）

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| MBS | Multicast/Broadcast Services | 组播/广播服务 |
| MBSR | Mobile Base Station Relay | 移动基站中继 |
| MSK | MBS Service Key | MBS 服务密钥 |
| MTK | MBS Traffic Key | MBS 流量密钥 |
| TMGI | Temporary Mobile Group Identity | 临时移动组标识 |

#### 14. 定位服务相关（8+ 个）

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| LCS | LoCation Services | 定位服务 |
| LCS-UPP | Location Services User Plane Protocol | 定位服务用户面协议 |
| LMF | Location Management Function | 定位管理功能 |
| LPP | LTE Positioning Protocol | LTE 定位协议 |
| SLPP | SideLink Positioning Protocol | 侧行定位协议 |
| UPP-CMI | User Plane Positioning Connection Management Information | 用户面定位连接管理信息 |
| RSLPP | Ranging and Sidelink Positioning Protocol | 测距和侧行定位协议 |

#### 15. 策略和配置相关（10+ 个）

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| URSP | UE Route Selection Policy | UE 路由选择策略 |
| UPDS | UE policy delivery service | UE 策略传递服务 |
| UPSI | UE Policy Section Identifier | UE 策略段标识符 |
| UPSC | UE Policy Section Code | UE 策略段代码 |
| PCO | Protocol Configuration Option | 协议配置选项 |
| ANDSP | Access Network Discovery and Selection Policy | 接入网发现和选择策略 |
| SOR | Steering of Roaming | 漫游引导 |
| SOR-CMCI | Steering of Roaming Connected Mode Control Information | 漫游引导连接模式控制信息 |
| PG | PLMN Generic | PLMN 通用 |
| VPS | VPLMN Specific | VPLMN 特定 |

#### 16. 接入技术和互通（10+ 个）

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| N3IWF | Non-3GPP Inter-Working Function | 非 3GPP 互通功能 |
| TNGF | Trusted Non-3GPP Gateway Function | 可信非 3GPP 网关功能 |
| TWIF | Trusted WLAN Interworking Function | 可信 WLAN 互通功能 |
| W-AGF | Wireline Access Gateway Function | 有线接入网关功能 |
| ePDG | Evolved Packet Data Gateway | 演进的分组数据网关 |
| WLAN | Wireless Local Area Network | 无线局域网 |
| AUN3 | Authenticable Non-3GPP | 可认证的非 3GPP |
| NAUN3 | Non-Authenticable Non-3GPP | 不可认证的非 3GPP |

#### 17. 流量和拥塞控制（8+ 个）

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| ATSSS | Access Traffic Steering, Switching and Splitting | 接入流量引导、切换和分流 |
| SGC | Service Gap Control | 服务间隙控制 |
| EAC | Early Admission Control | 早期准入控制 |
| RFSP | RAT Frequency Selection Priority | RAT 频率选择优先级 |
| MINT | Minimization of Service Interruption | 服务中断最小化 |

#### 18. 配置和管理（8+ 个）

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| ACS | Auto-Configuration Server | 自动配置服务器 |
| PVS | Provisioning Server | 配置服务器 |
| PMF | Performance Measurement Function | 性能测量功能 |
| RACS | Radio Capability Signalling Optimisation | 无线能力信令优化 |
| OS Id | OS Identity | 操作系统标识 |

#### 19. 其他重要缩略语（20+ 个）

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| MUSIM | Multi-USIM | 多 USIM |
| NITZ | Network Identity and Time Zone | 网络身份和时区 |
| PTI | Procedure Transaction Identity | 过程事务标识 |
| EPD | Extended Protocol Discriminator | 扩展协议鉴别器 |
| FQDN | Fully Qualified Domain Name | 完全限定域名 |
| DNS | Domain Name System | 域名系统 |
| IP-CAN | IP-Connectivity Access Network | IP 连接接入网 |
| RG | Residential Gateway | 住宅网关 |
| FN-RG | Fixed Network RG | 固定网络 RG |
| RTT | Round Trip Time | 往返时间 |
| RSN | Redundancy Sequence Number | 冗余序列号 |
| NCR-MT | Network Controlled Repeater - Mobile Termination | 网络控制中继器 - 移动终端 |

#### 20. 数据速率单位

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| Mbps | Megabits per second | 兆比特每秒 |
| Gbps | Gigabits per second | 千兆比特每秒 |
| Tbps | Terabits per second | 太比特每秒 |

---

## 总结

### 章节重要性

本章节是理解整个 3GPP TS 24.501 规范的**基础和字典**，包含了：

1. **200+ 个专业术语定义**：涵盖 UE 状态、网络切片、PDU 会话、安全、注册等各个方面
2. **200+ 个缩略语**：系统性地定义了 5G 系统中使用的所有缩略语

### 核心特点

1. **层次分明**：
   - 按功能域清晰分类（移动性管理、会话管理、安全、网络切片等）
   - 相关术语组织在一起，便于理解

2. **引用广泛**：
   - 引用了 20+ 个其他 3GPP 规范的定义
   - 确保术语在整个 3GPP 标准体系中的一致性

3. **版本演进**：
   - 包含 4G/5G 互通相关术语（Mapped 5G-GUTI、Native 5G-GUTI）
   - 包含新技术术语（UAS、V2X、ProSe、TSN、边缘计算）

4. **覆盖全面**：
   - 从基本概念（IDLE/CONNECTED 模式）到高级特性（网络切片、CIoT 优化）
   - 从公共网络到专网（SNPN、NPN）
   - 从地面网络到卫星网络

### 关键术语域

1. **移动性管理**：5GMM 状态、注册类型、TAI 管理
2. **会话管理**：PDU 会话类型、DNN 管理、QoS 控制
3. **网络切片**：NSSAI 管理、切片选择、切片认证
4. **安全**：加密/完整性算法、密钥管理、认证
5. **特殊应用**：IoT、V2X、UAS、ProSe、边缘计算
6. **网络类型**：PLMN、SNPN、CAG、卫星网络

### 使用建议

- **初学者**：先掌握基本术语（5GMM 模式、PDU 会话、NSSAI）
- **开发者**：重点关注与具体功能相关的术语和缩略语
- **测试人员**：理解状态定义和消息类型相关术语
- **系统设计**：全面了解网络架构和功能域的术语

本章节是阅读后续技术章节的**必备参考**，建议在阅读规范其他部分时经常回查本章节。
