# macOS使用uv运行PageIndex完整指南

## 🎯 目标

在macOS上使用uv创建Python 3.11虚拟环境，运行PageIndex处理PDF文档。

## 📋 准备工作

### 系统要求
- macOS 10.15+ (Catalina或更高)
- 终端/iTerm2
- 网络连接

### uv简介

[uv](https://github.com/astral-sh/uv) 是一个极速的Python包管理和项目管理工具，由Astral（ruff的开发团队）开发：

**优势**：
- ⚡ 比pip快10-100倍
- 🔒 可靠的依赖解析
- 🐍 自动管理Python版本
- 💾 统一的缓存机制

## 🚀 步骤1：安装uv

### 方式A：使用官方安装脚本（推荐）

```bash
# 使用curl安装
curl -LsSf https://astral.sh/uv/install.sh | sh

# 重启终端或刷新环境变量
source $HOME/.cargo/env
```

### 方式B：使用Homebrew

```bash
brew install uv
```

### 验证安装

```bash
uv --version
# 输出类似: uv 0.4.x
```

## 📦 步骤2：创建项目目录

```bash
# 创建项目目录
mkdir -p ~/pageindex-test
cd ~/pageindex-test

# 克隆PageIndex
git clone https://github.com/VectifyAI/PageIndex.git
cd PageIndex

# 或者如果已经clone过
# cd ~/PageIndex
```

## 🐍 步骤3：使用uv创建Python 3.11环境

### 方式A：自动安装Python 3.11

```bash
# uv会自动下载并安装Python 3.11
uv venv --python 3.11

# 激活虚拟环境
source .venv/bin/activate
```

### 方式B：使用系统Python

```bash
# 如果已经安装了Python 3.11
uv venv --python python3.11

# 激活虚拟环境
source .venv/bin/activate
```

### 验证环境

```bash
# 检查Python版本
python --version
# 应该输出: Python 3.11.x

# 检查pip
which python
# 应该输出: /Users/你的用户名/pageindex-test/PageIndex/.venv/bin/python
```

## 📥 步骤4：安装依赖

### 安装PageIndex基础依赖

```bash
# 确保在虚拟环境中（命令行前面有(.venv)）
# 使用uv安装依赖（极快）
uv pip install -r requirements.txt
```

### 安装适配器依赖

根据你想使用的LLM选择安装：

**选项1：智谱AI（推荐，国内稳定）**
```bash
uv pip install zhipuai
```

**选项2：Gemini（免费）**
```bash
uv pip install google-generativeai
```

**选项3：OpenAI（最稳定）**
```bash
# 已包含在requirements.txt中，无需额外安装
```

## 📂 步骤5：复制适配器文件

### 从你的Git仓库获取适配器

```bash
# 克隆你的项目仓库
cd ~/pageindex-test
git clone https://github.com/wuzhenhua24/tcz.git

# 复制适配器文件到PageIndex
cd tcz
cp pageindex_adapters/pageindex/*.py ~/pageindex-test/PageIndex/pageindex/
cp pageindex_adapters/*.py ~/pageindex-test/PageIndex/

# 验证文件已复制
ls -l ~/pageindex-test/PageIndex/pageindex/utils_*.py
ls -l ~/pageindex-test/PageIndex/run_pageindex_*.py
```

### 复制PDF文档

```bash
# 复制你的PDF文档
cp docs/ts_124501v181200p.pdf ~/pageindex-test/PageIndex/
```

## 🔑 步骤6：配置API Key

### 创建.env文件

```bash
cd ~/pageindex-test/PageIndex

# 根据你选择的LLM创建.env文件
cat > .env << 'EOF'
# 智谱AI (选择这个如果用智谱AI)
ZHIPUAI_API_KEY=你的智谱AI-key

# Gemini (选择这个如果用Gemini)
# GEMINI_API_KEY=你的Gemini-API-key

# OpenAI (选择这个如果用OpenAI)
# CHATGPT_API_KEY=sk-proj-你的OpenAI-key
EOF
```

或者直接导出环境变量：

```bash
# 智谱AI
export ZHIPUAI_API_KEY="你的智谱AI-key"

# 或Gemini
# export GEMINI_API_KEY="你的key"

# 或OpenAI
# export CHATGPT_API_KEY="sk-proj-你的key"
```

## 🧪 步骤7：测试API连接

### 测试智谱AI

```bash
cd ~/pageindex-test/PageIndex
python test_zhipuai_api.py
```

**预期输出：**
```
======================================================================
智谱AI API 测试工具
======================================================================

✅ API Key: ef82587a6e794c46a09a...49L43
   长度: 49 字符

======================================================================
测试模型: glm-4-flash
======================================================================
✅ 成功!
响应: OK
Finish reason: stop

✅ 找到可用模型: glm-4-flash
```

### 测试Gemini

```bash
python test_gemini_api.py
```

## 🎬 步骤8：运行PageIndex

### 使用智谱AI（推荐）

```bash
cd ~/pageindex-test/PageIndex

# 确保虚拟环境已激活
source .venv/bin/activate

# 运行处理
python run_pageindex_zhipuai.py \
  --pdf_path ts_124501v181200p.pdf \
  --model glm-4-flash \
  --max-pages-per-node 20 \
  --max-tokens-per-node 30000 \
  --if-add-node-summary yes \
  --if-add-node-id yes \
  --if-add-node-text no
```

### 使用Gemini

```bash
python run_pageindex_gemini.py \
  --pdf_path ts_124501v181200p.pdf \
  --model gemini-1.5-flash \
  --max-pages-per-node 20 \
  --max-tokens-per-node 50000 \
  --if-add-node-summary yes \
  --if-add-node-id yes
```

### 使用OpenAI

```bash
python run_pageindex.py \
  --pdf_path ts_124501v181200p.pdf \
  --model gpt-4o-mini \
  --max-pages-per-node 20 \
  --max-tokens-per-node 30000 \
  --if-add-node-summary yes \
  --if-add-node-id yes
```

## ⏱️ 处理过程

**预计时间**：20-40分钟（1000页文档）

**运行中你会看到：**
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

检测文档目录结构...
找到 25 个章节

生成节点摘要 [1/87]...
生成节点摘要 [2/87]...
...
```

**建议**：
- ☕ 去喝杯咖啡，等待处理完成
- 💻 保持电脑不休眠
- 📡 保持网络连接稳定

## 📊 步骤9：查看结果

### 处理完成后

```bash
# 结果保存在results目录
ls -lh results/

# 查看JSON文件（美化输出）
cat results/ts_124501v181200p_tree_zhipuai.json | python -m json.tool | less

# 或使用jq（如果已安装）
brew install jq
cat results/ts_124501v181200p_tree_zhipuai.json | jq '.' | less
```

### 统计信息

```bash
python << 'EOF'
import json

with open('results/ts_124501v181200p_tree_zhipuai.json', 'r') as f:
    tree = json.load(f)

def count_nodes(node):
    count = 1
    if 'children' in node:
        for child in node['children']:
            count += count_nodes(child)
    return count

print(f"✅ 处理完成!")
print(f"总节点数: {count_nodes(tree)}")
print(f"根标题: {tree.get('title')}")
print(f"第一层章节数: {len(tree.get('children', []))}")

# 打印前5个章节
print("\n前5个章节:")
for i, chapter in enumerate(tree.get('children', [])[:5], 1):
    print(f"\n{i}. {chapter.get('title')}")
    print(f"   页码: {chapter.get('pages')}")
    if 'summary' in chapter:
        summary = chapter['summary'][:100] + "..." if len(chapter['summary']) > 100 else chapter['summary']
        print(f"   摘要: {summary}")
EOF
```

## 🔄 步骤10：上传结果到服务器

### 方式A：使用Git

```bash
cd ~/pageindex-test/tcz

# 创建results目录（如果不存在）
mkdir -p results

# 复制结果
cp ~/pageindex-test/PageIndex/results/ts_124501v181200p_tree_*.json results/

# 提交到Git
git add results/
git commit -m "Add PageIndex tree structure generated locally on macOS"
git push
```

### 方式B：使用scp（如果有服务器访问权限）

```bash
scp results/ts_124501v181200p_tree_*.json user@server:/home/user/tcz/results/
```

## 💡 uv常用命令

### 虚拟环境管理

```bash
# 创建虚拟环境
uv venv --python 3.11

# 激活虚拟环境
source .venv/bin/activate

# 退出虚拟环境
deactivate

# 删除虚拟环境
rm -rf .venv
```

### 包管理

```bash
# 安装包（极快）
uv pip install package-name

# 从requirements.txt安装
uv pip install -r requirements.txt

# 列出已安装的包
uv pip list

# 卸载包
uv pip uninstall package-name

# 查看包信息
uv pip show package-name
```

### 项目同步

```bash
# 同步到requirements.txt中的精确版本
uv pip sync requirements.txt

# 编译requirements.txt（从pyproject.toml）
uv pip compile pyproject.toml -o requirements.txt
```

## 🐛 常见问题

### 问题1: uv安装失败

**解决方法：**
```bash
# 使用Homebrew安装
brew install uv

# 或手动下载二进制文件
curl -LsSf https://github.com/astral-sh/uv/releases/latest/download/uv-installer.sh | sh
```

### 问题2: Python 3.11下载慢

**解决方法：**
```bash
# 先手动安装Python 3.11
brew install python@3.11

# 然后使用系统Python创建环境
uv venv --python python3.11
```

### 问题3: 虚拟环境未激活

**症状：**
```bash
# 命令行前面没有 (.venv)
```

**解决方法：**
```bash
source .venv/bin/activate

# 验证
which python
# 应该显示虚拟环境路径
```

### 问题4: API key不生效

**解决方法：**
```bash
# 检查.env文件
cat .env

# 或直接在终端导出
export ZHIPUAI_API_KEY="你的key"

# 验证
echo $ZHIPUAI_API_KEY
```

### 问题5: 权限问题

**解决方法：**
```bash
# 不要使用sudo安装uv或包
# uv设计为用户级工具

# 如果遇到权限问题，检查文件所有权
ls -la .venv/
```

## 📝 完整的命令清单

### 一键设置脚本

保存为 `setup_pageindex.sh`:

```bash
#!/bin/bash
set -e

echo "🚀 开始设置PageIndex环境..."

# 1. 安装uv（如果未安装）
if ! command -v uv &> /dev/null; then
    echo "📦 安装uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# 2. 创建项目目录
echo "📂 创建项目目录..."
mkdir -p ~/pageindex-test
cd ~/pageindex-test

# 3. 克隆仓库
if [ ! -d "PageIndex" ]; then
    echo "📥 克隆PageIndex..."
    git clone https://github.com/VectifyAI/PageIndex.git
fi

if [ ! -d "tcz" ]; then
    echo "📥 克隆tcz..."
    git clone https://github.com/wuzhenhua24/tcz.git
fi

# 4. 创建虚拟环境
cd PageIndex
echo "🐍 创建Python 3.11虚拟环境..."
uv venv --python 3.11

# 5. 激活虚拟环境
source .venv/bin/activate

# 6. 安装依赖
echo "📦 安装依赖..."
uv pip install -r requirements.txt
uv pip install zhipuai

# 7. 复制适配器
echo "📋 复制适配器文件..."
cp ../tcz/pageindex_adapters/pageindex/*.py pageindex/
cp ../tcz/pageindex_adapters/*.py .

# 8. 复制PDF
echo "📄 复制PDF文档..."
cp ../tcz/docs/ts_124501v181200p.pdf .

echo "✅ 设置完成!"
echo ""
echo "下一步："
echo "1. 配置API key: echo 'ZHIPUAI_API_KEY=你的key' > .env"
echo "2. 测试连接: python test_zhipuai_api.py"
echo "3. 运行处理: python run_pageindex_zhipuai.py --pdf_path ts_124501v181200p.pdf"
```

**使用方法：**
```bash
chmod +x setup_pageindex.sh
./setup_pageindex.sh
```

## 🎯 下一步

处理完成后，你可以：

1. **分析结果**
   - 查看树形结构
   - 验证章节划分
   - 检查摘要质量

2. **实现查询系统**
   - 参考 `IMPLEMENTATION_PLAN.md`
   - 构建混合架构
   - 实现推理检索

3. **分享结果**
   - 上传到Git仓库
   - 与团队分享
   - 编写技术文档

## 📚 相关文档

- **LOCAL_RUNNING_GUIDE.md** - 通用本地运行指南
- **PYTHON_VERSION_REQUIREMENTS.md** - Python版本要求
- **SESSION_SUMMARY.md** - 完整会话总结
- **pageindex_adapters/README.md** - 适配器使用说明

## 🌟 总结

使用uv的优势：
- ⚡ **快速**: 依赖安装比pip快10-100倍
- 🔒 **可靠**: 确定性的依赖解析
- 🐍 **便捷**: 自动管理Python版本
- 💾 **高效**: 统一的缓存机制

祝你处理顺利！🚀
