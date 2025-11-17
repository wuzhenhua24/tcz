# 大型通信协议PDF处理实现方案

## 项目背景

处理3GPP等通信协议规范文档（1000+页），解决超上下文限制问题。

当前已有功能：
- ✅ 按章节切割PDF
- ✅ 生成章节摘要

## 架构设计

### 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    用户查询接口                          │
└──────────────────┬──────────────────────────────────────┘
                   │
         ┌─────────▼──────────┐
         │   智能查询路由      │
         │  (问题分类+意图识别) │
         └─────────┬──────────┘
                   │
    ┌──────────────┼──────────────┬────────────┐
    ▼              ▼              ▼            ▼
┌────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│术语查询│  │精确检索  │  │向量检索  │  │全章节读取│
│  索引  │  │(消息/IE) │  │  (RAG)   │  │(流程分析)│
└────────┘  └──────────┘  └──────────┘  └──────────┘
    │              │              │            │
    └──────────────┼──────────────┴────────────┘
                   │
         ┌─────────▼──────────┐
         │   答案生成/聚合     │
         └────────────────────┘
```

### 数据处理流程

```
PDF文档
  │
  ├─> 1. 章节切割 (已完成)
  │     └─> chapters/XX_Title.pdf
  │
  ├─> 2. 内容解析 (待实现)
  │     ├─> 提取文本
  │     ├─> 识别表格
  │     ├─> 提取图片
  │     └─> 保留格式
  │
  ├─> 3. 元数据提取 (待实现)
  │     ├─> 章节层次结构
  │     ├─> 消息定义位置
  │     ├─> IE字段位置
  │     ├─> 术语/缩略语位置
  │     └─> Cause值位置
  │
  ├─> 4. 智能分块 (待实现)
  │     ├─> 保持语义完整性
  │     ├─> 添加上下文标记
  │     └─> 500-1000 tokens/chunk
  │
  └─> 5. 多索引构建 (待实现)
        ├─> 向量索引 (Embedding)
        ├─> 术语索引 (JSON/SQLite)
        ├─> 结构化索引 (消息/IE/Cause)
        └─> 章节树索引
```

## 核心组件设计

### 1. 增强的文档解析器

```python
class ProtocolDocumentParser:
    """
    通信协议文档专用解析器
    识别协议文档特有的结构（消息格式、IE定义等）
    """

    def parse_chapter(self, pdf_path):
        """解析单个章节"""
        return {
            'text': ...,           # 纯文本
            'tables': [...],       # 表格内容（消息格式、IE定义）
            'figures': [...],      # 流程图
            'metadata': {
                'chapter_num': '5',
                'chapter_title': 'GMM procedures',
                'page_range': (50, 150),
                'content_type': ['procedures', 'messages']
            }
        }

    def extract_message_definitions(self, chapter):
        """提取消息定义"""
        # 识别 "8.2.X Message_Name" 格式
        # 提取消息类型、方向、IEs列表
        pass

    def extract_ie_definitions(self, chapter):
        """提取信息元素定义"""
        # 识别 "9.X.X IE_Name" 格式
        # 提取字段格式、长度、编码
        pass

    def extract_cause_values(self, chapter):
        """提取Cause值定义"""
        # 识别 "Annex A Cause values" 等
        # 提取错误码、含义、处理建议
        pass
```

### 2. 多层索引系统

```python
class ProtocolIndexer:
    """多层索引构建器"""

    def __init__(self):
        self.vector_store = None      # Chroma/FAISS
        self.term_index = {}          # 术语索引
        self.message_index = {}       # 消息索引
        self.ie_index = {}           # IE索引
        self.cause_index = {}        # Cause值索引
        self.chapter_tree = {}       # 章节树

    def build_vector_index(self, chunks):
        """构建向量索引"""
        # 使用OpenAI embedding或本地模型
        embeddings = OpenAIEmbeddings()
        self.vector_store = Chroma.from_documents(
            chunks,
            embeddings,
            collection_metadata={
                "hnsw:space": "cosine"
            }
        )

    def build_term_index(self, chapter_3_content):
        """从第3章构建术语索引"""
        # 解析 "3.1 Definitions" 和 "3.2 Abbreviations"
        # 格式: {term: {definition: ..., location: ...}}
        pass

    def build_message_index(self, message_chapters):
        """构建消息索引"""
        # 格式: {
        #   "REGISTRATION REQUEST": {
        #     "chapter": "8.2.6",
        #     "page": 125,
        #     "direction": "UE->AMF",
        #     "ies": [...]
        #   }
        # }
        pass
```

### 3. 智能查询路由

```python
class QueryRouter:
    """查询路由器 - 根据问题类型选择最优检索策略"""

    QUERY_PATTERNS = {
        'term_definition': [
            r'什么是 (.+)',
            r'(.+) 的定义',
            r'(.+) 是什么意思',
            r'解释 (.+)',
        ],
        'message_format': [
            r'(.+) 消息格式',
            r'(.+) message',
            r'(.+) 包含哪些字段',
            r'(.+) 的IEs',
        ],
        'cause_value': [
            r'cause.* (#?\d+)',
            r'错误码 (#?\d+)',
            r'拒绝原因 (#?\d+)',
        ],
        'procedure': [
            r'(.+) 流程',
            r'如何 (.+)',
            r'(.+) 过程',
            r'(.+) procedure',
        ]
    }

    def classify_query(self, question: str) -> dict:
        """
        分类查询类型
        返回: {
            'type': 'term_definition' | 'message_format' | 'cause_value' | 'procedure' | 'general',
            'entities': [...],  # 提取的实体
            'confidence': 0.95
        }
        """
        # 1. 规则匹配
        for query_type, patterns in self.QUERY_PATTERNS.items():
            for pattern in patterns:
                if match := re.search(pattern, question, re.I):
                    return {
                        'type': query_type,
                        'entities': list(match.groups()),
                        'confidence': 0.9
                    }

        # 2. LLM分类（可选）
        return {'type': 'general', 'entities': [], 'confidence': 0.5}

    def route(self, question: str, indexer: ProtocolIndexer):
        """路由到最优检索策略"""
        query_info = self.classify_query(question)

        if query_info['type'] == 'term_definition':
            # 直接查术语索引
            term = query_info['entities'][0]
            return indexer.term_index.get(term)

        elif query_info['type'] == 'message_format':
            # 查消息索引 + 读取完整定义
            msg_name = query_info['entities'][0]
            msg_info = indexer.message_index.get(msg_name)
            if msg_info:
                # 读取该消息的完整章节
                full_content = load_chapter(msg_info['chapter'])
                return full_content

        elif query_info['type'] == 'cause_value':
            # 查cause索引
            cause_code = query_info['entities'][0]
            return indexer.cause_index.get(cause_code)

        elif query_info['type'] == 'procedure':
            # 混合检索：向量搜索 + 完整章节加载
            # 1. 向量搜索找到相关章节
            relevant_docs = indexer.vector_store.similarity_search(
                question, k=3,
                filter={'content_type': 'procedure'}
            )
            # 2. 加载完整章节（避免截断流程描述）
            chapters = set(doc.metadata['chapter'] for doc in relevant_docs)
            full_chapters = [load_chapter(ch) for ch in chapters]
            return full_chapters

        else:  # general
            # 标准RAG
            return indexer.vector_store.similarity_search(question, k=5)
```

### 4. 上下文感知的分块策略

```python
class ProtocolChunker:
    """协议文档专用分块器"""

    def chunk_chapter(self, chapter_content, metadata):
        """
        智能分块，保持语义完整性
        """
        chunks = []

        # 策略1: 消息定义不拆分
        if metadata.get('content_type') == 'message_definition':
            # 一个消息定义作为一个chunk（即使超过1000 tokens）
            chunks.append({
                'content': chapter_content,
                'metadata': {
                    **metadata,
                    'chunk_type': 'complete_message',
                    'preserve_integrity': True
                }
            })

        # 策略2: 流程描述按步骤分块
        elif metadata.get('content_type') == 'procedure':
            # 识别步骤（"Step 1:", "a)", "1)"等）
            steps = self.split_by_steps(chapter_content)
            for i, step in enumerate(steps):
                chunks.append({
                    'content': step,
                    'metadata': {
                        **metadata,
                        'step_num': i + 1,
                        'total_steps': len(steps),
                        'chunk_type': 'procedure_step'
                    }
                })

        # 策略3: 术语定义按术语分块
        elif metadata.get('content_type') == 'definitions':
            terms = self.split_definitions(chapter_content)
            for term, definition in terms:
                chunks.append({
                    'content': f"{term}: {definition}",
                    'metadata': {
                        **metadata,
                        'term': term,
                        'chunk_type': 'term_definition'
                    }
                })

        # 策略4: 通用内容按语义边界分块
        else:
            # 使用语义边界（段落、小节标题）
            semantic_chunks = self.split_by_semantics(
                chapter_content,
                max_tokens=800
            )
            for chunk in semantic_chunks:
                chunks.append({
                    'content': chunk,
                    'metadata': {
                        **metadata,
                        'chunk_type': 'semantic'
                    }
                })

        # 添加上下文信息
        for chunk in chunks:
            chunk['metadata']['chapter_title'] = metadata.get('chapter_title')
            chunk['metadata']['chapter_path'] = metadata.get('chapter_path')
            # 添加前后文引用（帮助LLM理解上下文）
            chunk['context_hint'] = f"[{metadata.get('chapter_path')}]"

        return chunks
```

## 实现路线图

### Phase 1: 基础增强 (1-2周)

- [ ] **任务1.1**: 增强PDF解析
  - 集成 `pdfplumber` 或 `pypdf` + `pdfminer.six`
  - 提取表格（消息格式表、IE定义表）
  - 保留文本格式（缩进、列表）

- [ ] **任务1.2**: 构建术语索引
  - 解析第3章 Definitions and Abbreviations
  - 构建JSON索引: `{term: definition, location}`
  - 实现术语查询API

- [ ] **任务1.3**: 智能分块
  - 实现 ProtocolChunker
  - 按内容类型分块（消息/流程/定义/通用）
  - 添加元数据标记

### Phase 2: RAG系统 (2-3周)

- [ ] **任务2.1**: 向量数据库
  - 选择: Chroma (本地) 或 Pinecone (云端)
  - 集成 OpenAI Embeddings 或开源模型
  - 构建向量索引

- [ ] **任务2.2**: 实现查询路由
  - 问题分类（规则 + LLM）
  - 多索引查询接口
  - 结果聚合

- [ ] **任务2.3**: 检索优化
  - 混合检索（向量 + 关键词）
  - Re-ranking（提高精度）
  - 上下文扩展（返回相邻chunks）

### Phase 3: 高级功能 (3-4周)

- [ ] **任务3.1**: 消息/IE索引
  - 自动识别消息定义章节
  - 提取消息格式（表格解析）
  - 构建结构化索引

- [ ] **任务3.2**: 流程分析
  - 识别流程描述章节
  - 提取状态机/流程图
  - 多步骤推理支持

- [ ] **任务3.3**: 交叉引用
  - 构建引用图谱
  - 自动补充相关定义
  - 支持"深入查看"功能

### Phase 4: 优化和扩展 (持续)

- [ ] **任务4.1**: 性能优化
  - 缓存常见查询
  - 索引增量更新
  - 并行处理

- [ ] **任务4.2**: 多文档支持
  - 处理多个TS文档（如TS 24.501 + TS 23.501）
  - 跨文档引用解析
  - 版本管理

- [ ] **任务4.3**: 用户界面
  - Web UI (Streamlit/Gradio)
  - 聊天界面
  - 可视化（高亮原文位置）

## 技术栈建议

### 核心库

```python
# PDF处理
pypdf>=4.0.0          # 基础PDF操作（已有）
pdfplumber>=0.10.0    # 表格提取
pdfminer.six>=20221105 # 深度PDF解析

# 文本处理
langchain>=0.1.0      # RAG框架
tiktoken>=0.5.0       # Token计数

# 向量数据库（选一个）
chromadb>=0.4.0       # 本地部署，简单
# pinecone-client     # 云端，性能好
# qdrant-client       # 开源，功能强

# Embedding（选一个）
openai>=1.0.0         # OpenAI API（推荐）
# sentence-transformers # 本地模型

# 数据库
sqlite3               # 结构化索引（Python内置）
# or PostgreSQL+pgvector  # 生产环境

# LLM集成
openai>=1.0.0         # GPT-4/GPT-3.5
# anthropic           # Claude
# ollama              # 本地部署

# 工具库
regex>=2023.0.0       # 高级正则表达式
beautifulsoup4>=4.12.0 # HTML解析（如果需要）
```

### 架构选型

#### 方案A: 全本地部署（成本低，隐私好）

```
- Embedding: sentence-transformers (all-MiniLM-L6-v2)
- 向量DB: Chroma (本地文件)
- LLM: Ollama (Llama 3 / Mistral)
- 优点: 无API成本，数据不出本地
- 缺点: 效果稍差，需要GPU
```

#### 方案B: 混合方案（推荐）

```
- Embedding: OpenAI text-embedding-3-small ($0.02/1M tokens)
- 向量DB: Chroma (本地)
- LLM: OpenAI GPT-4 Turbo (按需调用)
- 优点: 平衡效果和成本
- 缺点: 需要API key
```

#### 方案C: 全云端（效果好，成本高）

```
- Embedding: OpenAI text-embedding-3-large
- 向量DB: Pinecone (云端)
- LLM: GPT-4 Turbo / Claude 3 Opus
- 优点: 最佳效果，无需维护
- 缺点: 成本较高，数据上云
```

## 成本估算（方案B）

假设处理 TS 24.501 (7.6MB, ~1000页, ~50万tokens):

```
1. 一次性索引构建:
   - Embedding: 50万 tokens ÷ 1M × $0.02 = $0.01

2. 日常查询 (100次/天):
   - Embedding查询: 100次 × 20 tokens ÷ 1M × $0.02 ≈ $0.0004/天
   - LLM调用: 100次 × (输入2000 + 输出500) tokens × $0.01/1K ≈ $2.5/天

3. 月成本: ~$75 (假设每天100次查询)

优化建议:
- 缓存常见查询 -> 减少50% LLM调用
- 使用GPT-3.5 Turbo处理简单查询 -> 成本降低10倍
- 直接索引查询（术语/消息）-> 0成本
```

## 示例代码

### 快速开始示例

```python
# main.py
from protocol_rag import ProtocolRAG

# 1. 初始化系统
rag = ProtocolRAG(
    pdf_path="docs/ts_124501v181200p.pdf",
    index_dir="indexes/",
    use_gpu=False
)

# 2. 构建索引（首次运行）
rag.build_indexes()

# 3. 查询
questions = [
    "什么是5GMM-IDLE模式?",
    "REGISTRATION REQUEST消息包含哪些IE?",
    "5GMM cause值#7是什么意思?",
    "网络切片选择流程是怎样的?"
]

for q in questions:
    print(f"\nQ: {q}")
    answer = rag.query(q)
    print(f"A: {answer.text}")
    print(f"来源: {answer.sources}")
```

### 高级使用示例

```python
# 自定义检索参数
answer = rag.query(
    "PDU session建立流程",
    search_type="hybrid",      # 混合检索
    top_k=10,                  # 检索10个chunks
    rerank=True,               # 启用重排序
    include_context=True,      # 包含上下文chunks
    return_full_chapter=True   # 返回完整章节
)

# 流式输出（适合长文本）
for chunk in rag.query_stream("详细解释网络切片"):
    print(chunk, end='', flush=True)

# 多轮对话（带历史记录）
conversation = rag.create_conversation()
conversation.ask("什么是NSSAI?")
conversation.ask("它和S-NSSAI有什么区别?")  # 带上下文
conversation.ask("在注册流程中如何使用?")    # 继续上下文
```

## 性能指标

### 目标指标

```
- 索引构建时间: <10分钟 (1000页文档)
- 查询延迟:
  - 术语查询: <100ms
  - 向量检索: <500ms
  - 复杂分析: <5s
- 准确率:
  - 术语定义: >95%
  - 消息格式: >90%
  - 流程理解: >85%
- 召回率: >90% (相关信息被检索到)
```

### 评估方法

```python
# 构建测试集
test_cases = [
    {
        "question": "什么是5G-GUTI?",
        "expected_chapter": "3.1",
        "expected_keywords": ["Globally Unique Temporary Identifier", "GUAMI", "5G-TMSI"]
    },
    # ... 更多测试用例
]

# 运行评估
evaluator = RAGEvaluator(rag, test_cases)
metrics = evaluator.run()
print(f"准确率: {metrics.accuracy}")
print(f"召回率: {metrics.recall}")
print(f"平均响应时间: {metrics.avg_latency}ms")
```

## 扩展方向

### 1. 多模态支持

```python
# 处理流程图、状态机图
- 使用OCR提取图片文字
- 使用GPT-4V理解图表
- 将图表转换为文本描述

# 示例
answer = rag.query("展示注册流程图")
# 返回: 流程图图片 + 文字描述
```

### 2. 代码生成

```python
# 根据协议规范生成实现代码
rag.generate_code(
    "生成REGISTRATION REQUEST消息的编码函数",
    language="python",
    include_tests=True
)
```

### 3. 协议对比

```python
# 对比不同版本
rag.compare_versions(
    "TS 24.501 v18.12.0 vs v17.0.0",
    focus="REGISTRATION REQUEST消息"
)

# 对比不同协议
rag.compare_protocols(
    "5G NAS vs 4G NAS",
    focus="注册流程"
)
```

### 4. 测试用例生成

```python
# 根据协议自动生成测试用例
rag.generate_test_cases(
    "注册流程异常场景",
    format="pytest"
)
```

## 总结

这个方案的核心优势：

1. **分层处理**: 章节切割 -> 智能分块 -> 多索引
2. **智能路由**: 根据问题类型选择最优检索策略
3. **保留结构**: 充分利用协议文档的结构化特点
4. **可扩展**: 易于添加新功能（代码生成、对比分析等）
5. **高效**: 直接索引查询 + RAG，平衡速度和准确性

关键是要**利用协议文档的结构化特点**，而不是盲目使用通用RAG方案。
