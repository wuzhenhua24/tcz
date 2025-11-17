# Modal Verbs Terminology 情态动词术语总结分析

## 文档信息
- **文档编号**: 3GPP TS 24.501 version 18.12.0 Release 18
- **发布日期**: 2025-10
- **页码**: 第2页
- **所属章节**: 前言部分（Legal Notice 之后）

## 核心内容：情态动词术语规范

### 定义与解释标准
本文档规定了技术规范中情态动词的标准化解释方法，这些术语应按照 **ETSI Drafting Rules 第 3.2 条款**（"Verbal forms for the expression of provisions" - 条款表达的动词形式）进行解释。

### 规范的情态动词清单

文档中规定以下情态动词应被标准化解释：

1. **shall** (应当) - 表示强制性要求
2. **shall not** (不应当) - 表示强制性禁止
3. **should** (应该) - 表示推荐
4. **should not** (不应该) - 表示不推荐
5. **may** (可以) - 表示允许/可选
6. **need not** (无需) - 表示不必要
7. **will** (将) - 表示未来确定性
8. **will not** (将不) - 表示未来确定性的否定
9. **can** (能够) - 表示能力/可能性
10. **cannot** (不能) - 表示能力/可能性的否定

### 禁用词汇

**重要声明**：
- **"must"** 和 **"must not"** 在 ETSI 交付物中**不被允许**使用
- **唯一例外**：当这些词语用于直接引用时才可以使用

## 相关章节内容

### 知识产权声明

#### 基本专利 (Essential Patents)
- 已向 ETSI 声明的基本或潜在基本知识产权可在 ETSI SR 000 314 中查询
- ETSI 成员和非成员均可公开访问这些声明
- 最新更新可在 **ETSI IPR online database** 查询
- **免责声明**：ETSI 未进行 IPR 基本性调查，不保证不存在其他未被引用的 IPR

#### 商标 (Trademarks)
文档中列出的 ETSI 注册商标包括：
- **DECT™, PLUGTESTS™, UMTS™** 和 **ETSI logo** - 为 ETSI 成员利益注册
- **3GPP™, LTE™ 和 5G™ logo** - 为 ETSI 成员和 3GPP 组织合作伙伴利益注册
- **oneM2M™ logo** - 为 ETSI 成员和 oneM2M 合作伙伴利益注册
- **GSM®** 和 **GSM logo** - 由 GSM 协会注册并拥有

### 法律声明 (Legal Notice)
- 本技术规范由 **ETSI 3rd Generation Partnership Project (3GPP)** 制作
- 文档可能使用 3GPP 标识符引用技术规范或报告，这些应被解释为相应的 ETSI 交付物
- 3GPP 和 ETSI 标识符之间的交叉引用可在官方链接查询

## 技术意义与应用

### 为什么需要情态动词规范？

1. **标准化要求等级**
   - 明确区分强制性要求（shall）和推荐性要求（should）
   - 确保全球技术人员对规范的理解一致

2. **法律清晰度**
   - 在符合性测试和认证中提供明确的判定标准
   - 避免因语言模糊导致的合规性争议

3. **国际协调**
   - 与国际标准化组织（如 ETSI、ITU 等）的通用实践保持一致
   - 便于多语言翻译时保持语义精确

### 实际应用示例

| 情态动词 | 强度等级 | 典型用法场景 |
|---------|---------|-------------|
| shall | 强制性 | 必须实现的核心功能 |
| shall not | 强制禁止 | 绝对不允许的行为 |
| should | 推荐 | 最佳实践建议 |
| may | 可选 | 可选实现的增强特性 |
| cannot | 不可能 | 技术上不可行的场景 |

## 对开发者和实现者的意义

1. **合规性判断标准**
   - "shall" 和 "shall not" 的要求必须在产品中实现，否则无法通过认证
   - "should" 和 "may" 的要求可根据产品定位选择性实现

2. **测试规范编写**
   - 测试用例应针对所有 "shall" 要求进行验证
   - "should" 要求通常作为可选测试项

3. **互操作性保障**
   - 统一的术语解释确保不同厂商的实现能够互操作
   - 减少因理解差异导致的兼容性问题

## 文档结构预览

文档后续包含的主要章节（从目录可见）：
- Foreword（前言）
- 1. Scope（范围）
- 2. References（参考文献）
- 3. Definitions and abbreviations（定义和缩写）
- 4. General（总则）
- 5. Elementary procedures for 5GS mobility management（5GS 移动性管理基本流程）
- 6. Elementary procedures for 5GS session management（5GS 会话管理基本流程）
- 7-10. 其他技术章节

## 关键要点总结

1. **标准化术语体系** - 建立了明确的情态动词解释框架，适用于整个技术规范
2. **强制性与推荐性区分** - 清晰区分了必须实现和建议实现的功能
3. **禁用词汇规定** - 明确禁止使用 "must" 和 "must not"，避免术语混淆
4. **参考 ETSI 规则** - 所有解释基于 ETSI Drafting Rules 第 3.2 条款
5. **全文适用** - 这些规则适用于 3GPP TS 24.501 整个文档的 1200+ 页内容

## 实践建议

- **阅读规范时**：特别关注含有 "shall" 的条款，这些是强制性要求
- **实现功能时**：优先实现所有 "shall" 要求，再考虑 "should" 和 "may" 要求
- **测试验证时**：确保所有 "shall" 和 "shall not" 要求都有相应的测试用例
- **撰写文档时**：遵循相同的情态动词使用规范，确保表达准确

## 参考链接
- ETSI Drafting Rules: <https://portal.etsi.org/Services/editHelp!/Howtostart/ETSIDraftingRules.aspx>
- ETSI IPR online database: 可通过 ETSI 官网访问
