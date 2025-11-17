#!/bin/bash
# 一键修复 PageIndex Gemini 适配器

set -e  # 遇到错误立即退出

echo "========================================="
echo "一键修复 PageIndex Gemini 适配器"
echo "========================================="

TCZ_DIR="$HOME/Documents/gitpro/tcz"
PAGEINDEX_DIR="$HOME/Documents/gitpro/PageIndex"

# 检查目录是否存在
if [ ! -d "$TCZ_DIR" ]; then
    echo "错误: tcz 目录不存在: $TCZ_DIR"
    exit 1
fi

if [ ! -d "$PAGEINDEX_DIR" ]; then
    echo "错误: PageIndex 目录不存在: $PAGEINDEX_DIR"
    exit 1
fi

echo ""
echo "步骤 1: 进入 tcz 目录"
cd "$TCZ_DIR"
pwd

echo ""
echo "步骤 2: 拉取最新代码"
git pull origin claude/fix-pageindex-parameters-01GvibUzzJwgRVwaHacJGL5A

echo ""
echo "步骤 3: 复制 utils_gemini_rest.py"
cp -v pageindex_adapters/pageindex/utils_gemini_rest.py "$PAGEINDEX_DIR/pageindex/"

echo ""
echo "步骤 4: 复制 run_pageindex_gemini.py"
cp -v pageindex_adapters/run_pageindex_gemini.py "$PAGEINDEX_DIR/"

echo ""
echo "步骤 5: 验证文件"
echo ""
echo "utils_gemini_rest.py:"
ls -lh "$PAGEINDEX_DIR/pageindex/utils_gemini_rest.py"
WC1=$(wc -l < "$PAGEINDEX_DIR/pageindex/utils_gemini_rest.py")
echo "行数: $WC1 (应该是 718)"

echo ""
echo "run_pageindex_gemini.py:"
ls -lh "$PAGEINDEX_DIR/run_pageindex_gemini.py"
WC2=$(wc -l < "$PAGEINDEX_DIR/run_pageindex_gemini.py")
echo "行数: $WC2 (应该是 189)"

echo ""
echo "========================================="
echo "✅ 修复完成！"
echo "========================================="
echo ""
echo "现在可以运行："
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
