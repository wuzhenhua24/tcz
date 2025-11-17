#!/bin/bash
# 诊断 PageIndex Gemini 适配器问题

set -e

echo "==========================================="
echo "PageIndex Gemini 适配器问题诊断"
echo "==========================================="
echo ""

PAGEINDEX_DIR="$HOME/Documents/gitpro/PageIndex"

echo "1. 检查 run_pageindex_gemini.py 文件"
echo "-------------------------------------------"
if [ -f "$PAGEINDEX_DIR/run_pageindex_gemini.py" ]; then
    echo "✓ 文件存在"

    LINES=$(wc -l < "$PAGEINDEX_DIR/run_pageindex_gemini.py")
    echo "  行数: $LINES"

    if [ "$LINES" -eq 189 ]; then
        echo "  ✓ 行数正确 (189行)"
    else
        echo "  ✗ 行数错误！应该是189行，实际是${LINES}行"
        echo "  这说明文件是旧版本！"
    fi

    echo ""
    echo "  检查第120行内容："
    LINE120=$(sed -n '120p' "$PAGEINDEX_DIR/run_pageindex_gemini.py")
    echo "  $LINE120"

    if echo "$LINE120" | grep -q "page_index_main"; then
        echo "  ✓ 第120行包含 page_index_main"
    else
        echo "  ✗ 第120行不包含 page_index_main！"
    fi

    echo ""
    echo "  检查是否包含模块缓存清理代码："
    if grep -q "STEP 1: Remove any cached pageindex modules" "$PAGEINDEX_DIR/run_pageindex_gemini.py"; then
        echo "  ✓ 包含缓存清理代码"
    else
        echo "  ✗ 缺少缓存清理代码！文件是旧版本！"
    fi
else
    echo "✗ 文件不存在！"
fi

echo ""
echo "2. 检查 utils_gemini_rest.py 文件"
echo "-------------------------------------------"
if [ -f "$PAGEINDEX_DIR/pageindex/utils_gemini_rest.py" ]; then
    echo "✓ 文件存在"

    LINES=$(wc -l < "$PAGEINDEX_DIR/pageindex/utils_gemini_rest.py")
    SIZE=$(du -h "$PAGEINDEX_DIR/pageindex/utils_gemini_rest.py" | awk '{print $1}')

    echo "  行数: $LINES"
    echo "  大小: $SIZE"

    if [ "$LINES" -eq 718 ]; then
        echo "  ✓ 行数正确 (718行)"
    else
        echo "  ✗ 行数错误！应该是718行，实际是${LINES}行"
    fi

    echo ""
    echo "  检查是否包含完整工具函数："

    if grep -q "def structure_to_list" "$PAGEINDEX_DIR/pageindex/utils_gemini_rest.py"; then
        echo "  ✓ 包含 structure_to_list 函数"
    else
        echo "  ✗ 缺少 structure_to_list 函数"
    fi

    if grep -q "def generate_summaries_for_structure" "$PAGEINDEX_DIR/pageindex/utils_gemini_rest.py"; then
        echo "  ✓ 包含 generate_summaries_for_structure 函数"
    else
        echo "  ✗ 缺少 generate_summaries_for_structure 函数"
    fi
else
    echo "✗ 文件不存在！这是问题的关键原因！"
fi

echo ""
echo "3. 检查 Python 缓存文件"
echo "-------------------------------------------"
if [ -d "$PAGEINDEX_DIR/pageindex/__pycache__" ]; then
    echo "✓ 发现 __pycache__ 目录"
    echo "  缓存文件列表:"
    ls -lh "$PAGEINDEX_DIR/pageindex/__pycache__/" | grep "utils"
    echo ""
    echo "  建议：删除缓存文件以确保使用最新代码"
    echo "  命令: rm -rf '$PAGEINDEX_DIR/pageindex/__pycache__'"
else
    echo "  没有 __pycache__ 目录"
fi

echo ""
echo "4. 检查 PageIndex 安装"
echo "-------------------------------------------"
cd "$PAGEINDEX_DIR"
if python -c "import pageindex" 2>/dev/null; then
    echo "✓ pageindex 可以导入"
    PAGEINDEX_PATH=$(python -c "import pageindex; print(pageindex.__file__)")
    echo "  pageindex 位置: $PAGEINDEX_PATH"
else
    echo "✗ 无法导入 pageindex"
fi

echo ""
echo "==========================================="
echo "诊断总结"
echo "==========================================="
echo ""

# 总结建议
NEED_COPY=0
NEED_CLEAR_CACHE=0

if [ ! -f "$PAGEINDEX_DIR/pageindex/utils_gemini_rest.py" ]; then
    echo "❌ 关键问题：utils_gemini_rest.py 不存在！"
    NEED_COPY=1
fi

RUN_LINES=$(wc -l < "$PAGEINDEX_DIR/run_pageindex_gemini.py" 2>/dev/null || echo "0")
if [ "$RUN_LINES" -ne 189 ]; then
    echo "❌ 关键问题：run_pageindex_gemini.py 不是最新版本！"
    NEED_COPY=1
fi

if [ -d "$PAGEINDEX_DIR/pageindex/__pycache__" ]; then
    NEED_CLEAR_CACHE=1
fi

echo ""
if [ $NEED_COPY -eq 1 ] || [ $NEED_CLEAR_CACHE -eq 1 ]; then
    echo "🔧 修复步骤："
    echo ""

    if [ $NEED_CLEAR_CACHE -eq 1 ]; then
        echo "步骤 1: 清除 Python 缓存"
        echo "  rm -rf '$PAGEINDEX_DIR/pageindex/__pycache__'"
        echo "  rm -rf '$PAGEINDEX_DIR/__pycache__'"
        echo ""
    fi

    if [ $NEED_COPY -eq 1 ]; then
        echo "步骤 2: 重新复制文件"
        echo "  cd ~/Documents/gitpro/tcz"
        echo "  git pull origin claude/fix-pageindex-parameters-01GvibUzzJwgRVwaHacJGL5A"
        echo "  cp pageindex_adapters/pageindex/utils_gemini_rest.py '$PAGEINDEX_DIR/pageindex/'"
        echo "  cp pageindex_adapters/run_pageindex_gemini.py '$PAGEINDEX_DIR/'"
        echo ""
    fi

    echo "步骤 3: 验证复制成功"
    echo "  bash verify_files.sh"
    echo ""
else
    echo "✅ 所有文件看起来都正常"
    echo ""
    echo "如果仍然报错，请："
    echo "1. 重启 Python 解释器"
    echo "2. 确保没有其他 Python 进程在使用 PageIndex"
    echo "3. 检查是否在正确的虚拟环境中"
fi

echo ""
