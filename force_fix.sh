#!/bin/bash
# 强制修复 PageIndex Gemini 适配器问题

set -e

echo "==========================================="
echo "强制修复 PageIndex Gemini 适配器"
echo "==========================================="
echo ""

TCZ_DIR="$HOME/Documents/gitpro/tcz"
PAGEINDEX_DIR="$HOME/Documents/gitpro/PageIndex"

# 检查目录
if [ ! -d "$TCZ_DIR" ]; then
    echo "❌ 错误: tcz 目录不存在"
    exit 1
fi

if [ ! -d "$PAGEINDEX_DIR" ]; then
    echo "❌ 错误: PageIndex 目录不存在"
    exit 1
fi

echo "步骤 1: 清除所有 Python 缓存"
echo "-------------------------------------------"
cd "$PAGEINDEX_DIR"

if [ -d "pageindex/__pycache__" ]; then
    echo "删除 pageindex/__pycache__"
    rm -rf pageindex/__pycache__
fi

if [ -d "__pycache__" ]; then
    echo "删除 __pycache__"
    rm -rf __pycache__
fi

# 删除所有 .pyc 文件
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

echo "✓ 缓存已清除"
echo ""

echo "步骤 2: 进入 tcz 目录并拉取最新代码"
echo "-------------------------------------------"
cd "$TCZ_DIR"
pwd

echo "拉取最新代码..."
git pull origin claude/fix-pageindex-parameters-01GvibUzzJwgRVwaHacJGL5A

echo "✓ 代码已更新"
echo ""

echo "步骤 3: 强制复制 utils_gemini_rest.py"
echo "-------------------------------------------"

if [ ! -f "pageindex_adapters/pageindex/utils_gemini_rest.py" ]; then
    echo "❌ 错误: 源文件不存在: pageindex_adapters/pageindex/utils_gemini_rest.py"
    exit 1
fi

cp -fv pageindex_adapters/pageindex/utils_gemini_rest.py "$PAGEINDEX_DIR/pageindex/"

LINES1=$(wc -l < "$PAGEINDEX_DIR/pageindex/utils_gemini_rest.py")
echo "已复制，行数: $LINES1"

if [ "$LINES1" -ne 718 ]; then
    echo "❌ 警告: 行数不对！应该是718行"
else
    echo "✓ 文件正确（718行）"
fi

echo ""

echo "步骤 4: 强制复制 run_pageindex_gemini.py"
echo "-------------------------------------------"

if [ ! -f "pageindex_adapters/run_pageindex_gemini.py" ]; then
    echo "❌ 错误: 源文件不存在: pageindex_adapters/run_pageindex_gemini.py"
    exit 1
fi

cp -fv pageindex_adapters/run_pageindex_gemini.py "$PAGEINDEX_DIR/"

LINES2=$(wc -l < "$PAGEINDEX_DIR/run_pageindex_gemini.py")
echo "已复制，行数: $LINES2"

if [ "$LINES2" -ne 189 ]; then
    echo "❌ 警告: 行数不对！应该是189行"
else
    echo "✓ 文件正确（189行）"
fi

echo ""

echo "步骤 5: 验证文件内容"
echo "-------------------------------------------"

echo "检查 run_pageindex_gemini.py 第120行:"
LINE120=$(sed -n '120p' "$PAGEINDEX_DIR/run_pageindex_gemini.py")
echo "  $LINE120"

if echo "$LINE120" | grep -q "page_index_main"; then
    echo "  ✓ 第120行正确"
else
    echo "  ❌ 第120行内容不对！"
fi

echo ""
echo "检查 utils_gemini_rest.py 是否包含完整函数:"

if grep -q "def structure_to_list" "$PAGEINDEX_DIR/pageindex/utils_gemini_rest.py"; then
    echo "  ✓ 包含 structure_to_list"
else
    echo "  ❌ 缺少 structure_to_list"
fi

if grep -q "def ChatGPT_API" "$PAGEINDEX_DIR/pageindex/utils_gemini_rest.py"; then
    echo "  ✓ 包含 ChatGPT_API"
else
    echo "  ❌ 缺少 ChatGPT_API"
fi

echo ""

echo "步骤 6: 再次清除缓存（确保使用新文件）"
echo "-------------------------------------------"
cd "$PAGEINDEX_DIR"
rm -rf pageindex/__pycache__ __pycache__
find . -name "*.pyc" -delete 2>/dev/null || true

echo "✓ 缓存已清除"
echo ""

echo "==========================================="
echo "✅ 修复完成！"
echo "==========================================="
echo ""
echo "文件摘要:"
echo "  utils_gemini_rest.py: $LINES1 行"
echo "  run_pageindex_gemini.py: $LINES2 行"
echo ""
echo "下一步："
echo ""
echo "cd $PAGEINDEX_DIR"
echo ""
echo "python run_pageindex_gemini.py \\"
echo "  --pdf_path ts_124501v181200p.pdf \\"
echo "  --model gemini-2.5-flash \\"
echo "  --max-pages-per-node 20 \\"
echo "  --max-tokens-per-node 50000 \\"
echo "  --if-add-node-summary yes \\"
echo "  --if-add-node-id yes"
echo ""
echo "如果仍然报错，请运行: bash diagnose_issue.sh"
echo ""
