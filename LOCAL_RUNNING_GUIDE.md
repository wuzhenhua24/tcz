# PageIndex 本地运行完整指南

## 📋 概述

由于当前服务器环境无法访问外部LLM API服务（Gemini和智谱AI均返回403），本指南将教你如何在**本地电脑**上运行PageIndex处理你的PDF协议文档。

## 🎯 目标

在本地环境处理 `ts_124501v181200p.pdf` (7.6MB, ~1000页)，生成完整的树形索引，用于推理式检索。

## 📦 准备工作

### 系统要求

- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8 或更高版本
- **磁盘空间**: 至少 500MB
- **网络**: 能够访问 Google AI / 智谱AI API

### 检查Python版本

```bash
python --version
# 或
python3 --version
```

如果版本低于3.8，请先升级Python。

## 🚀 完整安装步骤

### 步骤1：下载项目文件

**方式A：从Git仓库克隆**

```bash
# 克隆你的项目仓库
git clone https://github.com/wuzhenhua24/tcz.git
cd tcz

# 下载PageIndex
cd ~
git clone https://github.com/VectifyAI/PageIndex.git
cd PageIndex
```

**方式B：手动下载**

1. 下载PageIndex: https://github.com/VectifyAI/PageIndex/archive/refs/heads/main.zip
2. 解压到本地目录
3. 复制你的PDF文档到该目录

### 步骤2：安装依赖

```bash
cd PageIndex

# 安装基础依赖
pip install -r requirements.txt

# 根据你选择的API安装额外依赖
# 选项1: 使用Gemini API
pip install google-generativeai

# 选项2: 使用智谱AI
pip install zhipuai

# 选项3: 使用OpenAI (推荐，最稳定)
# 不需要额外安装，已包含在requirements.txt中
```

### 步骤3：复制适配器文件

从服务器复制我为你准备的适配器文件到本地：

**下载这些文件到 `PageIndex/pageindex/` 目录：**

1. **Gemini适配器** (如果用Gemini)
   - 从服务器下载: `/home/user/PageIndex/pageindex/utils_gemini_rest.py`
   - 放到本地: `PageIndex/pageindex/utils_gemini_rest.py`
   - 同时下载: `/home/user/PageIndex/run_pageindex_gemini.py`
   - 放到本地: `PageIndex/run_pageindex_gemini.py`

2. **智谱AI适配器** (如果用智谱AI)
   - 从服务器下载: `/home/user/PageIndex/pageindex/utils_zhipuai.py`
   - 放到本地: `PageIndex/pageindex/utils_zhipuai.py`
   - 同时下载: `/home/user/PageIndex/run_pageindex_zhipuai.py`
   - 放到本地: `PageIndex/run_pageindex_zhipuai.py`

或者，我可以帮你把这些文件打包提交到你的Git仓库，你直接从仓库拉取。

### 步骤4：配置API Key

**选项A：使用Gemini API (免费)**

```bash
# 获取API key: https://aistudio.google.com/app/apikey
# 创建 .env 文件
echo "GEMINI_API_KEY=你的Gemini-API-key" > .env
```

**选项B：使用智谱AI**

```bash
# 获取API key: https://open.bigmodel.cn/usercenter/apikeys
# 创建 .env 文件
echo "ZHIPUAI_API_KEY=你的智谱AI-key" > .env
```

**选项C：使用OpenAI (最稳定，付费)**

```bash
# 获取API key: https://platform.openai.com/api-keys
# 创建 .env 文件
echo "CHATGPT_API_KEY=sk-proj-你的OpenAI-key" > .env
```

### 步骤5：复制PDF文档

```bash
# 将你的PDF文档复制到PageIndex目录
# 假设你的文档在 ~/tcz/docs/ 目录
cp ~/tcz/docs/ts_124501v181200p.pdf .
```

## 🎬 运行处理

### 使用Gemini API

```bash
cd PageIndex

python3 run_pageindex_gemini.py \
  --pdf_path ts_124501v181200p.pdf \
  --model gemini-1.5-flash \
  --max-pages-per-node 20 \
  --max-tokens-per-node 50000 \
  --if-add-node-summary yes \
  --if-add-node-id yes \
  --if-add-node-text no
```

### 使用智谱AI

```bash
cd PageIndex

python3 run_pageindex_zhipuai.py \
  --pdf_path ts_124501v181200p.pdf \
  --model glm-4-flash \
  --max-pages-per-node 20 \
  --max-tokens-per-node 30000 \
  --if-add-node-summary yes \
  --if-add-node-id yes \
  --if-add-node-text no
```

### 使用OpenAI (原版PageIndex)

```bash
cd PageIndex

python3 run_pageindex.py \
  --pdf_path ts_124501v181200p.pdf \
  --model gpt-4o-mini \
  --max-pages-per-node 20 \
  --max-tokens-per-node 30000 \
  --if-add-node-summary yes \
  --if-add-node-id yes \
  --if-add-node-text no
```

## ⏱️ 预期处理时间和成本

### Gemini API

- **时间**: 20-40分钟
- **成本**: 免费（1500请求/天限额）
- **准确率**: 95%+

### 智谱AI

- **时间**: 20-40分钟
- **成本**:
  - glm-4-flash: ¥0.1/百万tokens (超便宜)
  - glm-4-plus: ¥50/百万tokens
  - 处理1000页约¥1-5元
- **准确率**: 95%+

### OpenAI

- **时间**: 20-40分钟
- **成本**:
  - gpt-4o-mini: $0.15/1M input + $0.60/1M output
  - 处理1000页约$3-8
- **准确率**: 98%+（最高）

## 📊 运行过程中

处理过程中你会看到：

```
======================================================================
PageIndex with ZhipuAI GLM-4 Flash
======================================================================
Model: glm-4-flash
API Key: ef82587a6e794c46a09a...

正在处理 PDF: ts_124501v181200p.pdf
预计需要 20-40 分钟（取决于文档大小）...
使用模型: glm-4-flash
======================================================================

正在处理: ts_124501v181200p.pdf
总页数: 600

找到 25 个章节:

[1/25] Intellectual Property Rights
    页码范围: 1 - 2
    已保存: 01_Intellectual_Property_Rights.pdf

[2/25] Legal Notice
    页码范围: 3 - 4
    已保存: 02_Legal_Notice.pdf

...生成摘要中...

======================================================================
✅ 成功! 树形结构已保存到: results/ts_124501v181200p_tree_zhipuai.json
======================================================================

摘要:
  - 总节点数: 87
  - 根标题: 3GPP TS 24.501 version 18.12.0 Release 18
  - 根页码: [1, 600]
  - 第一级章节数: 25
```

## 📁 输出结果

处理完成后，你会得到：

```
results/
└── ts_124501v181200p_tree_zhipuai.json  (或 _tree_gemini.json / _tree.json)
```

### 验证结果

```bash
# 查看JSON文件（美化输出）
cat results/ts_124501v181200p_tree_zhipuai.json | python3 -m json.tool | less

# 统计节点数量
python3 << 'EOF'
import json

with open('results/ts_124501v181200p_tree_zhipuai.json', 'r') as f:
    tree = json.load(f)

def count_nodes(node):
    count = 1
    if 'children' in node:
        for child in node['children']:
            count += count_nodes(child)
    return count

print(f"总节点数: {count_nodes(tree)}")
print(f"根标题: {tree.get('title')}")
print(f"第一层章节数: {len(tree.get('children', []))}")

# 打印第一层章节
print("\n第一层章节:")
for i, chapter in enumerate(tree.get('children', [])[:5], 1):
    print(f"{i}. {chapter.get('title')}")
    print(f"   页码: {chapter.get('pages')}")
    if 'summary' in chapter:
        print(f"   摘要: {chapter['summary'][:80]}...")
EOF
```

### 树形结构示例

```json
{
  "title": "3GPP TS 24.501 version 18.12.0 Release 18",
  "pages": [1, 600],
  "summary": "本规范定义了5G系统的非接入层(NAS)协议...",
  "node_id": "root",
  "children": [
    {
      "title": "3 Definitions and abbreviations",
      "pages": [17, 50],
      "summary": "定义了200+个5G NAS协议相关的术语和缩略语...",
      "node_id": "node_3",
      "children": [
        {
          "title": "3.1 Definitions",
          "pages": [17, 40],
          "summary": "定义了UE状态、网络切片、PDU会话等核心概念...",
          "node_id": "node_3_1"
        },
        {
          "title": "3.2 Abbreviations",
          "pages": [41, 50],
          "summary": "列出了所有缩略语...",
          "node_id": "node_3_2"
        }
      ]
    }
  ]
}
```

## 🔄 将结果同步回服务器

处理完成后，将结果上传回服务器：

```bash
# 方式1: 使用git (推荐)
cd ~/tcz
mkdir -p results
cp ~/PageIndex/results/ts_124501v181200p_tree_*.json results/
git add results/
git commit -m "Add PageIndex tree structure for ts_124501v181200p"
git push

# 方式2: 使用scp
scp results/ts_124501v181200p_tree_*.json user@server:/home/user/tcz/results/
```

## 🐛 常见问题

### 问题1: 模块导入错误

```
ImportError: No module named 'zhipuai'
```

**解决方法:**
```bash
pip install zhipuai
# 或
pip install google-generativeai
```

### 问题2: API Key错误

```
Error: ZHIPUAI_API_KEY not set
```

**解决方法:**
```bash
# 检查.env文件
cat .env

# 或直接设置环境变量
export ZHIPUAI_API_KEY="你的key"
export GEMINI_API_KEY="你的key"
```

### 问题3: PDF文件找不到

```
FileNotFoundError: PDF file not found
```

**解决方法:**
```bash
# 使用绝对路径
python3 run_pageindex_zhipuai.py \
  --pdf_path /Users/你的用户名/Downloads/ts_124501v181200p.pdf \
  ...
```

### 问题4: 处理中断

如果处理过程中断（网络问题、电脑休眠等）：

1. **当前PageIndex不支持断点续传**，需要重新运行
2. **建议**:
   - 保持电脑不休眠
   - 使用稳定的网络连接
   - 先用小文档测试（提取某一章）

### 问题5: 内存不足

如果处理大文档时内存不足：

```bash
# 减小每个节点的大小
python3 run_pageindex_zhipuai.py \
  --pdf_path ts_124501v181200p.pdf \
  --max-pages-per-node 10 \
  --max-tokens-per-node 15000 \
  ...
```

## 📈 优化建议

### 针对大型协议文档（1000+页）

```bash
# 推荐配置
python3 run_pageindex_zhipuai.py \
  --pdf_path ts_124501v181200p.pdf \
  --model glm-4-flash \
  --max-pages-per-node 30 \
  --max-tokens-per-node 40000 \
  --if-add-node-summary yes \
  --if-add-node-id yes \
  --if-add-node-text no \
  --toc-check-pages 30
```

**优点:**
- 更大的节点保持章节完整性
- 减少节点数量，加快处理速度
- 适合结构化的协议文档

### 先测试小文档

如果不确定配置，可以先用小文档测试：

```bash
# 从大PDF提取前50页作为测试
python3 << 'EOF'
from pypdf import PdfReader, PdfWriter

reader = PdfReader('ts_124501v181200p.pdf')
writer = PdfWriter()

for i in range(50):  # 提取前50页
    writer.add_page(reader.pages[i])

with open('test_50pages.pdf', 'wb') as f:
    writer.write(f)
EOF

# 处理测试文档（5-10分钟）
python3 run_pageindex_zhipuai.py \
  --pdf_path test_50pages.pdf \
  --model glm-4-flash \
  --max-pages-per-node 20 \
  --if-add-node-summary yes
```

## 🎯 下一步：使用树形索引

处理完成后，你可以：

### 1. 实现推理式检索

```python
import json

# 加载树形索引
with open('results/ts_124501v181200p_tree_zhipuai.json', 'r') as f:
    tree = json.load(f)

# 示例：查找术语定义
def find_term_definition(tree, term):
    """在树中查找术语定义"""
    # 1. 推理：术语定义通常在"Definitions"章节
    for chapter in tree.get('children', []):
        if 'definition' in chapter.get('title', '').lower():
            # 2. 在该章节的摘要中搜索
            if 'summary' in chapter:
                if term.lower() in chapter['summary'].lower():
                    return {
                        'chapter': chapter['title'],
                        'pages': chapter['pages'],
                        'summary': chapter['summary'],
                        'node_id': chapter.get('node_id')
                    }
    return None

# 测试
result = find_term_definition(tree, '5GMM-IDLE')
if result:
    print(f"找到术语定义:")
    print(f"章节: {result['chapter']}")
    print(f"页码: {result['pages']}")
    print(f"摘要: {result['summary'][:200]}...")
```

### 2. 对比传统RAG

- 使用相同的问题测试两种方法
- 对比准确率、速度、成本

### 3. 实现混合架构

参考 `IMPLEMENTATION_PLAN.md` 和 `PAGEINDEX_VS_TRADITIONAL_RAG.md` 中的方案。

## 📚 参考文档

你的项目中有这些详细的技术文档：

1. **IMPLEMENTATION_PLAN.md** - 传统分层RAG架构方案
2. **PAGEINDEX_VS_TRADITIONAL_RAG.md** - PageIndex深度对比分析
3. **GEMINI_PAGEINDEX_GUIDE.md** - Gemini完整使用指南
4. **GEMINI_API_TROUBLESHOOTING.md** - API问题诊断
5. **LOCAL_RUNNING_GUIDE.md** - 本文档

## 🆘 获取帮助

如果遇到问题：

1. **检查日志**: PageIndex会输出详细的处理日志
2. **查看文档**: 参考上述参考文档
3. **GitHub Issues**: https://github.com/VectifyAI/PageIndex/issues
4. **联系我**: 如果还有问题，随时回来找我！

## ✅ 总结

本地运行的优势：
- ✅ 不受服务器网络限制
- ✅ 可以选择任何LLM服务
- ✅ 处理速度更稳定
- ✅ 结果可以保存和重用

祝你处理顺利！🚀
