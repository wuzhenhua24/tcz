#!/usr/bin/env python3
"""
测试脚本：验证 utils_gemini_rest.py 能否被正确导入和注入
"""
import sys
import os

print("=" * 70)
print("测试 PageIndex Gemini 适配器导入")
print("=" * 70)

# 设置路径（模拟 run_pageindex_gemini.py 的路径设置）
script_dir = os.path.dirname(os.path.abspath(__file__))
pageindex_adapters_dir = os.path.join(script_dir, "pageindex_adapters")

print(f"\n1. 脚本目录: {script_dir}")
print(f"2. pageindex_adapters 目录: {pageindex_adapters_dir}")

# 插入路径
sys.path.insert(0, pageindex_adapters_dir)
print(f"\n3. sys.path 已更新")
print(f"   sys.path[0] = {sys.path[0]}")

# 尝试导入 utils_gemini_rest
print("\n4. 尝试导入 pageindex.utils_gemini_rest...")
try:
    from pageindex import utils_gemini_rest as utils_replacement
    print("   ✓ 导入成功！")
    print(f"   模块位置: {utils_replacement.__file__}")

    # 检查是否包含 ChatGPT_API 函数
    if hasattr(utils_replacement, 'ChatGPT_API'):
        print("   ✓ 包含 ChatGPT_API 函数")
    else:
        print("   ✗ 缺少 ChatGPT_API 函数！")

    # 检查是否包含完整的工具函数
    required_funcs = [
        'ChatGPT_API', 'ChatGPT_API_async', 'ChatGPT_API_with_finish_reason',
        'count_tokens', 'structure_to_list', 'extract_json', 'ConfigLoader'
    ]

    missing = []
    for func_name in required_funcs:
        if not hasattr(utils_replacement, func_name):
            missing.append(func_name)

    if missing:
        print(f"   ✗ 缺少函数: {', '.join(missing)}")
    else:
        print(f"   ✓ 所有必需函数都存在")

except ImportError as e:
    print(f"   ✗ 导入失败！")
    print(f"   错误: {e}")
    print("\n调试信息：")
    print(f"   pageindex_adapters 存在？ {os.path.exists(pageindex_adapters_dir)}")

    pageindex_dir = os.path.join(pageindex_adapters_dir, "pageindex")
    print(f"   pageindex 目录存在？ {os.path.exists(pageindex_dir)}")

    utils_file = os.path.join(pageindex_dir, "utils_gemini_rest.py")
    print(f"   utils_gemini_rest.py 存在？ {os.path.exists(utils_file)}")

    if os.path.exists(pageindex_dir):
        files = os.listdir(pageindex_dir)
        print(f"   pageindex 目录内容: {files}")

    sys.exit(1)

# 尝试注入到 sys.modules
print("\n5. 注入到 sys.modules...")
sys.modules['pageindex.utils'] = utils_replacement
print("   ✓ 注入完成")

# 验证注入是否成功
print("\n6. 验证 sys.modules['pageindex.utils']...")
if 'pageindex.utils' in sys.modules:
    print("   ✓ pageindex.utils 存在于 sys.modules")
    utils_module = sys.modules['pageindex.utils']
    print(f"   模块: {utils_module}")
    print(f"   是否与 utils_replacement 相同? {utils_module is utils_replacement}")
else:
    print("   ✗ pageindex.utils 不在 sys.modules 中！")

print("\n" + "=" * 70)
print("测试完成")
print("=" * 70)
