# PageIndex Python版本要求

## 📋 最低版本要求

**Python 3.8 或更高版本**

推荐使用：**Python 3.8+**（测试环境使用Python 3.11.14）

## 🔍 依赖包Python版本要求分析

### 核心依赖

| 包 | 版本 | 最低Python要求 | 说明 |
|---|------|--------------|------|
| **openai** | 1.101.0 | Python 3.7.1+ | OpenAI官方SDK |
| **tiktoken** | 0.11.0 | Python 3.8+ | Token计数工具 |
| **pymupdf** | 1.26.4 | Python 3.8+ | PDF处理库 |
| **PyPDF2** | 3.0.1 | Python 3.6+ | PDF操作库 |
| **python-dotenv** | 1.1.0 | Python 3.8+ | 环境变量管理 |
| **pyyaml** | 6.0.2 | Python 3.6+ | YAML解析 |

### 适配器额外依赖

| 包 | 最低Python要求 | 说明 |
|---|--------------|------|
| **google-generativeai** | Python 3.9+ | Gemini API |
| **zhipuai** | Python 3.7+ | 智谱AI SDK |

## ✅ 推荐配置

### 最佳实践

```bash
# 推荐使用 Python 3.8 - 3.11
Python 3.8  ✅ 支持
Python 3.9  ✅ 支持（推荐）
Python 3.10 ✅ 支持（推荐）
Python 3.11 ✅ 支持（推荐，当前测试环境）
Python 3.12 ⚠️  大部分支持（部分依赖可能需要更新）
```

### 不同操作系统的安装

**macOS:**
```bash
# 使用 Homebrew
brew install python@3.11

# 或使用 pyenv
brew install pyenv
pyenv install 3.11.0
pyenv global 3.11.0
```

**Ubuntu/Debian:**
```bash
# Ubuntu 20.04+ 自带 Python 3.8+
sudo apt update
sudo apt install python3.11 python3.11-pip

# 设置默认版本
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
```

**Windows:**
```bash
# 从官网下载安装
# https://www.python.org/downloads/

# 或使用 Chocolatey
choco install python --version=3.11.0
```

## 🧪 验证Python版本

### 检查当前版本

```bash
python3 --version
# 输出应该是: Python 3.8.x 或更高
```

### 检查是否满足PageIndex要求

```bash
python3 << 'EOF'
import sys

print(f"当前Python版本: {sys.version}")
print(f"版本信息: {sys.version_info}")

major, minor = sys.version_info[:2]
if major == 3 and minor >= 8:
    print(f"✅ Python {major}.{minor} 满足PageIndex要求 (>= 3.8)")
elif major == 3 and minor == 7:
    print(f"⚠️  Python {major}.{minor} 可能可以运行，但推荐升级到 3.8+")
else:
    print(f"❌ Python {major}.{minor} 版本过低，请升级到 3.8+")
EOF
```

## 📦 虚拟环境设置（推荐）

### 使用venv（Python内置）

```bash
# 创建虚拟环境
python3 -m venv pageindex_env

# 激活虚拟环境
# Linux/macOS:
source pageindex_env/bin/activate

# Windows:
pageindex_env\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 退出虚拟环境
deactivate
```

### 使用conda

```bash
# 创建环境并指定Python版本
conda create -n pageindex python=3.11

# 激活环境
conda activate pageindex

# 安装依赖
pip install -r requirements.txt

# 退出环境
conda deactivate
```

## 🐛 常见版本问题

### 问题1: Python版本过低

**错误信息:**
```
SyntaxError: invalid syntax
或
ModuleNotFoundError: No module named 'xxx'
```

**解决方法:**
```bash
# 升级Python到3.8+
# 或在虚拟环境中使用正确版本
python3.11 -m venv env
source env/bin/activate
```

### 问题2: tiktoken安装失败

**错误信息:**
```
ERROR: Could not build wheels for tiktoken
```

**原因:** Python版本低于3.8

**解决方法:**
```bash
# 升级Python到3.8+
# 或使用预编译wheel
pip install tiktoken --prefer-binary
```

### 问题3: google-generativeai要求Python 3.9+

**错误信息:**
```
ERROR: Package requires a different Python: 3.8.x not in '>=3.9'
```

**解决方法:**
```bash
# 升级到Python 3.9+
# 或不使用Gemini适配器，改用智谱AI或OpenAI
```

## 🔧 不同Python版本的兼容性测试

### Python 3.8

```bash
✅ OpenAI SDK - 支持
✅ Tiktoken - 支持
✅ PyMuPDF - 支持
❌ Google Generative AI - 不支持（需要3.9+）
✅ ZhipuAI - 支持
```

**建议:** 可以使用，但无法使用Gemini适配器

### Python 3.9+

```bash
✅ 所有依赖包完全支持
✅ 可以使用所有适配器（Gemini/智谱AI/OpenAI）
```

**建议:** **推荐使用**

### Python 3.12

```bash
⚠️  大部分包支持
⚠️  部分依赖可能需要最新版本
⚠️  可能遇到兼容性问题
```

**建议:** 建议使用3.9-3.11，更稳定

## 📊 测试结果总结

| Python版本 | PageIndex核心 | Gemini适配器 | 智谱AI适配器 | 推荐度 |
|-----------|-------------|-------------|------------|--------|
| 3.7 | ⚠️ 部分支持 | ❌ | ✅ | ❌ 不推荐 |
| 3.8 | ✅ | ❌ | ✅ | ⚠️  可用但受限 |
| 3.9 | ✅ | ✅ | ✅ | ✅ 推荐 |
| 3.10 | ✅ | ✅ | ✅ | ✅ 推荐 |
| 3.11 | ✅ | ✅ | ✅ | ✅✅ 强烈推荐 |
| 3.12 | ⚠️ | ⚠️ | ⚠️ | ⚠️  谨慎使用 |

## 🎯 建议

### 新项目

如果你正在开始一个新项目：
- **首选**: Python 3.11（最新稳定版，完全支持）
- **备选**: Python 3.10 或 3.9

### 现有项目

如果你的系统已经有Python：
- **Python 3.8+**: 可以直接使用（Gemini适配器除外）
- **Python 3.7**: 建议升级到3.9+
- **Python 3.6-**: 必须升级

### 生产环境

对于生产部署：
- **推荐**: Python 3.10 或 3.11
- **原因**: 性能好、稳定、包支持完整

## 📚 参考资源

- **Python官网**: https://www.python.org/downloads/
- **OpenAI Python SDK**: https://github.com/openai/openai-python
- **PyPI包信息**: https://pypi.org/
- **PageIndex GitHub**: https://github.com/VectifyAI/PageIndex

## 📝 更新日志

- **2025-11-17**: 初始版本
  - 确认最低要求 Python 3.8+
  - 推荐 Python 3.9-3.11
  - 测试环境使用 Python 3.11.14
