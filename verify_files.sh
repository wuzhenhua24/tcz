#!/bin/bash
# 验证 PageIndex 适配器文件是否正确复制

echo "========================================="
echo "验证 PageIndex Gemini 适配器文件"
echo "========================================="

PAGEINDEX_DIR="$HOME/Documents/gitpro/PageIndex"

echo ""
echo "1. 检查 run_pageindex_gemini.py"
if [ -f "$PAGEINDEX_DIR/run_pageindex_gemini.py" ]; then
    LINES=$(wc -l < "$PAGEINDEX_DIR/run_pageindex_gemini.py")
    echo "   ✓ 文件存在"
    echo "   行数: $LINES (应该是 189 行)"

    # 检查关键标记
    if grep -q "STEP 1: Remove any cached pageindex modules" "$PAGEINDEX_DIR/run_pageindex_gemini.py"; then
        echo "   ✓ 包含模块缓存清理代码（最新版本）"
    else
        echo "   ✗ 缺少模块缓存清理代码（旧版本！）"
    fi

    # 显示第120行内容
    echo "   第120行内容:"
    sed -n '120p' "$PAGEINDEX_DIR/run_pageindex_gemini.py" | sed 's/^/     /'
else
    echo "   ✗ 文件不存在！"
fi

echo ""
echo "2. 检查 utils_gemini_rest.py"
if [ -f "$PAGEINDEX_DIR/pageindex/utils_gemini_rest.py" ]; then
    LINES=$(wc -l < "$PAGEINDEX_DIR/pageindex/utils_gemini_rest.py")
    SIZE=$(du -h "$PAGEINDEX_DIR/pageindex/utils_gemini_rest.py" | cut -f1)
    echo "   ✓ 文件存在"
    echo "   行数: $LINES (应该是 718 行)"
    echo "   大小: $SIZE (应该约 28-30KB)"

    # 检查是否包含完整的工具函数
    if grep -q "def structure_to_list" "$PAGEINDEX_DIR/pageindex/utils_gemini_rest.py"; then
        echo "   ✓ 包含完整工具函数"
    else
        echo "   ✗ 缺少工具函数（不完整！）"
    fi
else
    echo "   ✗ 文件不存在！这是问题的关键！"
fi

echo ""
echo "3. 检查原始 utils.py（用于对比）"
if [ -f "$PAGEINDEX_DIR/pageindex/utils.py" ]; then
    echo "   ✓ 原始 utils.py 存在（这是正常的）"
else
    echo "   ✗ 原始 utils.py 不存在"
fi

echo ""
echo "========================================="
echo "修复建议："
echo "========================================="
echo ""
echo "cd ~/Documents/gitpro/tcz"
echo ""
echo "# 1. 拉取最新代码"
echo "git pull origin claude/fix-pageindex-parameters-01GvibUzzJwgRVwaHacJGL5A"
echo ""
echo "# 2. 复制文件到 PageIndex"
echo "cp pageindex_adapters/pageindex/utils_gemini_rest.py ~/Documents/gitpro/PageIndex/pageindex/"
echo "cp pageindex_adapters/run_pageindex_gemini.py ~/Documents/gitpro/PageIndex/"
echo ""
echo "# 3. 验证复制成功"
echo "ls -lh ~/Documents/gitpro/PageIndex/pageindex/utils_gemini_rest.py"
echo "ls -lh ~/Documents/gitpro/PageIndex/run_pageindex_gemini.py"
echo ""
