# 11_7 Handling of Unknown, Unforeseen, and Erroneous Protocol Data 章节总结分析

## 文档基本信息

- **文档编号**: 3GPP TS 24.501
- **版本**: version 18.12.0 Release 18
- **发布日期**: 2025-10
- **章节**: 第 7 章 Handling of unknown, unforeseen, and erroneous protocol data

## 章节概述

本章节定义了 5G 系统（5GS）中处理未知、未预见和错误协议数据的程序。这些程序不仅提供错误情况的恢复机制，还为协议的未来扩展定义了兼容性机制。这是确保协议健壮性和向后兼容性的关键部分。

## 7.1 总体规则（General）

### 核心原则

1. **优先级顺序**：子条款 7.1 到 7.8 应按优先级顺序应用
2. **实现依赖性**：网络中的详细错误处理程序是实现依赖的，可能因 PLMN 而异
3. **强制性要求**：
   - 开发协议扩展时，网络需要具备标记为"shall"的强制错误处理
   - 还应具备标记为"should"的强烈推荐的错误处理
4. **错误阈值**：仅当专用连接期间未达到特定错误阈值时，网络错误处理才被视为强制或强烈推荐

### 错误定义

- **语义错误**和**语法错误**的定义参考 3GPP TS 24.007 [11], subclause 11.4.2

## 7.2 消息长度问题（Message too short or too long）

### 7.2.1 消息过短

**处理规则**：
- 当接收到的消息过短，无法包含完整的消息类型信息元素时
- **处理方式**：应忽略该消息
- 参考：3GPP TS 24.007 [11]

### 7.2.2 消息过长

**最大消息大小规范**：
- **NR 连接到 5GCN**：3GPP TS 38.323 [29]
- **E-UTRA 连接到 5GCN**：3GPP TS 36.323 [25]
- **非 3GPP 接入连接到 5GCN**：3GPP TS 24.502 [18]

## 7.3 未知或未预见的过程事务标识符或 PDU 会话标识符

### 7.3.1 过程事务标识符（PTI）处理

#### 网络侧处理程序

**a) PTI 不匹配的响应消息**：
- 适用消息：PDU SESSION MODIFICATION COMPLETE、PDU SESSION RELEASE COMPLETE、PDU SESSION MODIFICATION COMMAND REJECT
- 条件：PTI 值（已分配或未分配）不匹配任何正在使用的 PTI
- **处理**：响应 5GSM STATUS 消息，原因 #47 "PTI mismatch"

**b) 无效的 PTI 值（已分配值）**：
- 适用消息：PDU SESSION AUTHENTICATION COMPLETE、SERVICE-LEVEL AUTHENTICATION COMPLETE
- 条件：PTI 值为已分配值
- **处理**：响应 5GSM STATUS 消息，原因 #81 "invalid PTI value"

**c) 无效的 PTI 值（未分配值）**：
- 适用消息：PDU SESSION ESTABLISHMENT REQUEST、PDU SESSION MODIFICATION REQUEST、PDU SESSION RELEASE REQUEST
- 条件：PTI 值为未分配值
- **处理**：响应 5GSM STATUS 消息，原因 #81 "invalid PTI value"

**d) 保留的 PTI 值**：
- 条件：PTI 值为保留值
- **处理**：忽略该消息

#### UE 侧处理程序

**a) PDU SESSION MODIFICATION 消息中的 PTI 不匹配**：
- 适用消息：PDU SESSION MODIFICATION COMMAND、PDU SESSION MODIFICATION REJECT
- 条件：PTI 值不匹配任何正在使用的 PTI
- **处理**：
  1. 如果是已接受请求的网络重传 → 响应 PDU SESSION MODIFICATION COMPLETE
  2. 如果是已拒绝请求的网络重传 → 响应 PDU SESSION MODIFICATION COMMAND REJECT
  3. 否则 → 响应 5GSM STATUS 消息，原因 #47 "PTI mismatch"

**b) PDU SESSION RELEASE 消息中的 PTI 不匹配**：
- 适用消息：PDU SESSION RELEASE COMMAND、PDU SESSION RELEASE REJECT
- 条件：PTI 值不匹配任何正在使用的 PTI
- **处理**：
  1. 如果是已接受请求的网络重传 → 响应 PDU SESSION RELEASE COMPLETE
  2. 否则 → 响应 5GSM STATUS 消息，原因 #47 "PTI mismatch"

**c) PDU SESSION ESTABLISHMENT 消息中的 PTI 不匹配**：
- 适用消息：PDU SESSION ESTABLISHMENT ACCEPT、PDU SESSION ESTABLISHMENT REJECT
- 条件：PTI 值不匹配任何正在使用的 PTI
- **处理**：响应 5GSM STATUS 消息，原因 #47 "PTI mismatch"

**d) 认证消息中的无效 PTI**：
- 适用消息：PDU SESSION AUTHENTICATION COMMAND、PDU SESSION AUTHENTICATION RESULT、SERVICE-LEVEL AUTHENTICATION COMMAND
- 条件：PTI 值为已分配值
- **处理**：响应 5GSM STATUS 消息，原因 #81 "invalid PTI value"

**e) 未分配 PTI 值的消息**：
- 适用消息：PDU SESSION ESTABLISHMENT ACCEPT、PDU SESSION ESTABLISHMENT REJECT、PDU SESSION MODIFICATION REJECT、PDU SESSION RELEASE REJECT
- 条件：PTI 值为未分配值
- **处理**：忽略该消息

**f) 保留 PTI 值**：
- **处理**：忽略该消息

### 7.3.2 PDU 会话标识符处理

#### 网络侧处理程序

**a) 修改请求中的无效 PDU 会话标识符**：
- 适用消息：PDU SESSION MODIFICATION REQUEST
- 条件：PDU 会话标识符值为未分配或保留值
- **处理**：响应 PDU SESSION MODIFICATION REJECT，原因 #43 "invalid PDU session identity"

**b) 释放请求中的无效 PDU 会话标识符**：
- 适用消息：PDU SESSION RELEASE REQUEST
- 条件：PDU 会话标识符值为未分配或保留值
- **处理**：响应 PDU SESSION RELEASE REJECT，原因 #43 "invalid PDU session identity"

**c) UL NAS TRANSPORT 消息处理**：
- 适用消息：UL NAS TRANSPORT
- **处理**：
  1. 如果 Request type IE 设置为"initial request"或"initial emergency request"且包含保留 PDU 会话标识符 → 响应 DL NAS TRANSPORT，原因 #90 "payload was not forwarded"
  2. 否则，如果包含未分配或保留 PDU 会话标识符 → 响应 DL NAS TRANSPORT，原因 #90 "payload was not forwarded"

**d) 其他消息中的无效 PDU 会话标识符**：
- 条件：包含保留 PDU 会话标识符或不匹配现有 PDU 会话的已分配值
- **处理**：忽略该消息

#### UE 侧处理程序

**a) 未分配或保留的 PDU 会话标识符**：
- **处理**：忽略该消息

**b) PDU SESSION INACTIVE 状态的会话**：
- 条件：PDU 会话标识符属于 UE 中处于 PDU SESSION INACTIVE 状态的 PDU 会话
- **处理**：响应 5GSM STATUS 消息，原因 #43 "invalid PDU session identity"

## 7.4 未知或未预见的消息类型（Unknown or unforeseen message type）

### UE 侧处理

- 条件：接收到扩展协议鉴别符（EPD）未定义或接收方未实现的消息类型
- **处理**：返回状态消息（5GMM STATUS 或 5GSM STATUS，取决于 EPD），原因 #97 "message type non-existent or not implemented"

**不兼容协议状态的消息**：
- **处理**：返回状态消息，原因 #98 "message type not compatible with protocol state"

### 网络侧处理

- 条件：在协议状态下从 UE 接收到给定 EPD 的非请求消息不可预见时
- **处理**：实现依赖
- 其他情况：应忽略该消息，但建议返回状态消息，原因 #97

**不兼容协议状态的消息**：
- **处理**：实现依赖

### 注意事项

- EPD 给定方向未定义的消息类型被接收方视为该 EPD 未定义的消息类型
- 参考：3GPP TS 24.007 [11]

## 7.5 非语义强制信息元素错误

### 7.5.1 通用程序

#### 错误类型

当接收到消息时，诊断出以下错误或包含以下内容：
- **a)** "imperative message part" 错误
- **b)** "missing mandatory IE" 错误
- **a)** 语法不正确的强制 IE
- **b)** 在消息中未知但编码为"需要理解"的 IEI
- **c)** 编码为"需要理解"的乱序 IE

#### UE 处理

- 如果消息不是子条款 7.5.3 中列出的消息
- **处理**：返回状态消息（5GMM STATUS 或 5GSM STATUS），原因 #96 "invalid mandatory information"

#### 网络处理

- 如果消息不是子条款 7.5.3 中列出的消息
- **处理**（两者之一）：
  1. 尝试处理消息（具体后续操作是实现依赖的）
  2. 忽略消息，但应返回状态消息，原因 #96 "invalid mandatory information"

### 7.5.2 5GS 移动性管理

- **特殊情况**：5GS 移动性管理消息没有描述例外情况
- **EPS NAS 消息容器**：对 REGISTRATION REQUEST 消息中的 EPS NAS 消息容器信息元素，除了存在性和长度之外，不进行其他语义或语法诊断

### 7.5.3 5GS 会话管理

#### UE 侧处理程序

**a) PDU SESSION ESTABLISHMENT ACCEPT**：
- **处理**：通过发送 PDU SESSION RELEASE REQUEST 消息启动 PDU 会话释放程序，原因 #96 "invalid mandatory information"

**b) Void**

**c) PDU SESSION RELEASE COMMAND**：
- **处理**：返回 PDU SESSION RELEASE COMPLETE 消息，原因 #96 "invalid mandatory information"

#### 网络侧处理程序

**a) PDU SESSION ESTABLISHMENT REQUEST**：
- **处理**：返回 PDU SESSION ESTABLISHMENT REJECT 消息，原因 #96 "invalid mandatory information"

**b) PDU SESSION MODIFICATION REQUEST**：
- **处理**：返回 PDU SESSION MODIFICATION REJECT 消息，原因 #96 "invalid mandatory information"

**c) PDU SESSION RELEASE REQUEST**：
- **处理**：返回 PDU SESSION RELEASE REJECT 消息，原因 #96 "invalid mandatory information"

## 7.6 非强制消息部分中的未知和未预见 IE

### 7.6.1 消息中的未知 IEI

- **UE 处理**：忽略消息中所有未知的、未编码为"需要理解"的 IE
- **网络处理**：采用相同方法

### 7.6.2 乱序 IE

- **UE 处理**：忽略消息中所有未编码为"需要理解"的乱序 IE
- **网络处理**：应采用相同方法

### 7.6.3 重复的 IE

#### 处理规则

**未指定重复的情况**：
- 如果格式为 T、TV、TLV 或 TLV-E 的信息元素在消息中重复，但在第 8 章和第 9 章中未指定重复
- **处理**：仅处理首次出现的信息元素内容，忽略所有后续重复

**指定重复的情况**：
- 仅处理指定的重复信息元素内容
- 如果超出信息元素的重复限制，仅处理首次出现的信息元素内容直到重复限制，忽略所有后续重复

**网络处理**：应遵循相同程序

### 7.6.4 Type 6 IE 容器信息元素中的未知和未预见 IE

#### 7.6.4.1 Type 6 IE 容器中的未知 IEI

- **UE 处理**：忽略 Type 6 IE 容器信息元素中所有未知的、未编码为"需要理解"的 IE
- **网络处理**：采用相同方法

**注意**：
- Type 6 IE 容器信息元素定义的 IEI 集合独立于消息其他部分定义的 IEI 集合
- 因此，即使消息其他部分中存在相同 IEI 的已知 IE，该 IE 在 Type 6 IE 容器中也可能是未知的，反之亦然

#### 7.6.4.2 乱序 IE

- **UE 处理**：忽略 Type 6 IE 容器信息元素中所有未编码为"需要理解"的乱序 IE
- **网络处理**：应采用相同方法

#### 7.6.4.3 重复的 IE

**处理规则**（与 7.6.3 类似）：
- 如果格式为 TLV-E 的信息元素在 Type 6 IE 容器中重复，但未指定重复
- **处理**：仅处理首次出现的内容，忽略所有后续重复
- 如果超出重复限制，处理首次出现的内容直到限制，忽略后续重复

**网络处理**：应遵循相同程序

## 7.7 非强制消息部分错误

### 错误类别

包括：
- **a)** 语法不正确的可选 IE
- **b)** 条件 IE 错误

### 7.7.1 语法不正确的可选 IE

- **UE 处理**：将消息中所有语法不正确的可选 IE 视为在消息中不存在
- **网络处理**：采用相同方法

### 7.7.2 条件 IE 错误

#### UE 处理

当接收到 5GMM 或 5GSM 消息时，UE 诊断出：
- "missing conditional IE" 错误
- "unexpected conditional IE" 错误
- 至少一个语法不正确的条件 IE

**处理**：
- 忽略该消息
- 返回状态消息（5GMM STATUS 或 5GSM STATUS），原因 #100 "conditional IE error"

#### 网络处理

当网络接收到消息并诊断出上述错误时：
- **处理**（两者之一）：
  1. 尝试处理消息（具体后续操作是实现依赖的）
  2. 忽略消息，但应返回状态消息，原因 #100 "conditional IE error"

## 总结

### 核心设计原则

1. **分层错误处理**：从消息长度到消息类型，从强制 IE 到可选 IE，建立了完整的错误处理层次
2. **向后兼容性**：通过定义未知 IE 和消息类型的处理方式，确保协议可扩展性
3. **网络灵活性**：网络侧处理在许多情况下是实现依赖的，允许不同 PLMN 采用不同策略
4. **明确的错误原因码**：每种错误情况都有对应的 5GSM 原因值，便于问题诊断

### 关键错误原因码

- **#43**: "invalid PDU session identity" - 无效的 PDU 会话标识符
- **#47**: "PTI mismatch" - PTI 不匹配
- **#81**: "invalid PTI value" - 无效的 PTI 值
- **#90**: "payload was not forwarded" - 有效载荷未转发
- **#96**: "invalid mandatory information" - 无效的强制信息
- **#97**: "message type non-existent or not implemented" - 消息类型不存在或未实现
- **#98**: "message type not compatible with protocol state" - 消息类型与协议状态不兼容
- **#100**: "conditional IE error" - 条件 IE 错误

### 处理策略差异

#### UE 侧（用户设备）
- 通常采用严格的错误处理
- 大多数错误情况需要发送状态消息
- 明确定义的响应行为

#### 网络侧
- 更灵活的实现依赖处理
- 可以选择尝试处理或拒绝错误消息
- 考虑错误阈值和 PLMN 差异

### 实际意义

1. **协议健壮性**：确保即使在错误情况下，系统仍能正常运行
2. **互操作性**：不同厂商设备可以通过这些规则实现互操作
3. **可维护性**：清晰的错误处理使问题定位和解决更容易
4. **演进能力**：支持协议在不破坏现有实现的情况下进行扩展

### 特殊处理场景

1. **消息重传检测**：UE 能够识别网络重传并作出适当响应
2. **Type 6 IE 容器**：独立的 IEI 命名空间，允许更灵活的扩展
3. **会话状态感知**：根据 PDU 会话状态（如 INACTIVE）采取不同处理
4. **"理解要求"编码**：区分必须理解的 IE 和可忽略的 IE

## 应用建议

### 对实现者

1. **严格遵守强制规则**：所有"shall"标记的要求必须实现
2. **考虑推荐规则**：实现"should"标记的建议以提高互操作性
3. **测试边界情况**：确保各种错误场景都经过充分测试
4. **日志记录**：详细记录错误处理情况以便问题诊断

### 对网络运营商

1. **监控错误率**：跟踪各类错误的发生频率
2. **设定阈值**：定义何时需要采取纠正措施
3. **测试新设备**：验证新 UE 的错误处理行为
4. **兼容性规划**：在升级网络时考虑向后兼容性

### 对测试人员

1. **覆盖所有错误类型**：确保测试用例涵盖本章所有场景
2. **验证状态消息**：检查是否返回正确的原因码
3. **压力测试**：测试错误情况下的系统稳定性
4. **互操作测试**：验证不同厂商设备间的兼容性
