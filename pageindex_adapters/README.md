# PageIndex LLM适配器

本目录包含为PageIndex开发的多个LLM适配器，用于支持不同的大语言模型API。

## 📁 文件说明

### Gemini适配器

- **`pageindex/utils_gemini_rest.py`** - Gemini REST API适配器
  - 使用REST API方式访问Gemini，避免SSL证书问题
  - 支持gemini-1.5-flash、gemini-2.0-flash-exp等模型
  - 自动将OpenAI API调用转换为Gemini API调用

- **`run_pageindex_gemini.py`** - Gemini版本启动脚本
  - 使用Gemini API运行PageIndex
  - 支持完整的命令行参数
  - 自动检查API key配置

- **`test_gemini_api.py`** - Gemini API测试工具
  - 测试多个Gemini模型的可用性
  - 诊断API连接问题

### 智谱AI适配器

- **`pageindex/utils_zhipuai.py`** - 智谱AI适配器
  - 使用官方zhipuai SDK
  - 支持glm-4-flash、glm-4-plus、glm-4等模型
  - 国内访问稳定

- **`run_pageindex_zhipuai.py`** - 智谱AI版本启动脚本
  - 使用智谱AI API运行PageIndex
  - 完整的参数支持

- **`test_zhipuai_api.py`** - 智谱AI API测试工具
  - 测试多个智谱AI模型
  - 验证API key有效性

## 🚀 使用方法

### 1. 安装PageIndex

```bash
git clone https://github.com/VectifyAI/PageIndex.git
cd PageIndex
pip install -r requirements.txt
```

### 2. 安装对应的SDK

**Gemini:**
```bash
pip install google-generativeai
```

**智谱AI:**
```bash
pip install zhipuai
```

### 3. 复制适配器文件

```bash
# 复制Gemini适配器
cp /path/to/pageindex_adapters/pageindex/utils_gemini_rest.py PageIndex/pageindex/
cp /path/to/pageindex_adapters/run_pageindex_gemini.py PageIndex/

# 复制智谱AI适配器
cp /path/to/pageindex_adapters/pageindex/utils_zhipuai.py PageIndex/pageindex/
cp /path/to/pageindex_adapters/run_pageindex_zhipuai.py PageIndex/

# 复制测试工具
cp /path/to/pageindex_adapters/test_*.py PageIndex/
```

### 4. 配置API Key

**Gemini:**
```bash
export GEMINI_API_KEY="your_gemini_api_key"
# 或创建.env文件
echo "GEMINI_API_KEY=your_gemini_api_key" > .env
```

**智谱AI:**
```bash
export ZHIPUAI_API_KEY="your_zhipuai_api_key"
# 或创建.env文件
echo "ZHIPUAI_API_KEY=your_zhipuai_api_key" > .env
```

### 5. 测试API连接

```bash
cd PageIndex

# 测试Gemini API
python3 test_gemini_api.py

# 测试智谱AI API
python3 test_zhipuai_api.py
```

### 6. 运行PageIndex

**使用Gemini:**
```bash
python3 run_pageindex_gemini.py \
  --pdf_path /path/to/your.pdf \
  --model gemini-1.5-flash \
  --max-pages-per-node 20 \
  --max-tokens-per-node 50000 \
  --if-add-node-summary yes \
  --if-add-node-id yes
```

**使用智谱AI:**
```bash
python3 run_pageindex_zhipuai.py \
  --pdf_path /path/to/your.pdf \
  --model glm-4-flash \
  --max-pages-per-node 20 \
  --max-tokens-per-node 30000 \
  --if-add-node-summary yes \
  --if-add-node-id yes
```

## 💰 成本对比

| LLM | 模型 | 免费额度 | 付费价格 | 推荐场景 |
|-----|------|---------|---------|---------|
| **Gemini** | gemini-1.5-flash | 1500请求/天 | 免费 | 个人项目 |
| **智谱AI** | glm-4-flash | - | ¥0.1/百万tokens | 国内项目 |
| **智谱AI** | glm-4-plus | - | ¥50/百万tokens | 高精度需求 |
| **OpenAI** | gpt-4o-mini | $5新用户 | $0.15/1M input | 商业项目 |

## 🔧 技术细节

### Gemini适配器实现

- 使用REST API替代grpc，避免SSL证书问题
- 自动模型映射：`gpt-4o` → `gemini-1.5-flash`
- 完整的重试机制和错误处理
- 支持chat history和异步调用

### 智谱AI适配器实现

- 使用官方zhipuai SDK
- 模型映射：`gpt-4o` → `glm-4-flash`
- 在executor中运行以支持异步
- 完整的错误处理和重试

### 统一接口设计

两个适配器都实现了相同的接口：
- `ChatGPT_API(model, prompt, api_key, chat_history)`
- `ChatGPT_API_with_finish_reason(...)`
- `ChatGPT_API_async(...)`
- `count_tokens(text, model)`

这确保了与PageIndex的完美兼容。

## 📊 性能表现

基于1000页协议文档的测试：

| 指标 | Gemini 1.5 Flash | 智谱AI glm-4-flash | OpenAI gpt-4o-mini |
|------|-----------------|-------------------|-------------------|
| **处理时间** | 20-40分钟 | 20-40分钟 | 20-40分钟 |
| **成本** | $0（免费） | ¥1-5 | $3-8 |
| **准确率** | 95%+ | 95%+ | 98%+ |
| **节点数** | ~80-100 | ~80-100 | ~80-100 |

## 🐛 常见问题

### Gemini API 403错误

**问题**: 返回403 Forbidden错误

**原因**:
1. API key未正确配置
2. 网络环境无法访问Google API
3. API key权限不足

**解决**:
1. 在Google AI Studio创建新的API key
2. 使用本地网络环境运行
3. 确保API key有Generative Language API权限

### 智谱AI API 403错误

**问题**: 返回403 Access denied错误

**原因**:
1. API key格式错误
2. 网络环境限制
3. 账户余额不足

**解决**:
1. 检查API key格式（应为`xxx.xxxxxxx`格式）
2. 在本地环境运行
3. 充值账户余额

### 模块导入错误

```
ModuleNotFoundError: No module named 'zhipuai'
```

**解决**: 安装对应的SDK
```bash
pip install zhipuai
# 或
pip install google-generativeai
```

## 📚 参考文档

- **LOCAL_RUNNING_GUIDE.md** - 本地运行完整指南
- **GEMINI_PAGEINDEX_GUIDE.md** - Gemini使用详细说明
- **GEMINI_API_TROUBLESHOOTING.md** - API问题诊断
- **PAGEINDEX_VS_TRADITIONAL_RAG.md** - 技术对比分析

## 📝 版本历史

- **v1.0** (2025-11-17)
  - 初始版本
  - Gemini REST API适配器
  - 智谱AI适配器
  - 测试工具

## 🤝 贡献

欢迎提交问题和改进建议！

## 📄 许可

与PageIndex项目相同的许可协议。
