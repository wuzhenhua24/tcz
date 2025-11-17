#!/usr/bin/env python3
"""ZhipuAI API测试工具"""

import os
import sys
from zhipuai import ZhipuAI

def test_zhipuai_api(api_key):
    """测试ZhipuAI API连接"""

    print("=" * 70)
    print("智谱AI API 测试工具")
    print("=" * 70)
    print(f"\n✅ API Key: {api_key[:20]}...{api_key[-5:]}")
    print(f"   长度: {len(api_key)} 字符")

    # 测试不同的模型
    models = [
        "glm-4-flash",
        "glm-4-plus",
        "glm-4",
    ]

    for model_name in models:
        print(f"\n{'='*70}")
        print(f"测试模型: {model_name}")
        print(f"{'='*70}")

        try:
            client = ZhipuAI(api_key=api_key)

            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "user", "content": "测试：请简单回复OK"}
                ],
                temperature=0,
            )

            text = response.choices[0].message.content
            finish_reason = response.choices[0].finish_reason

            print(f"✅ 成功!")
            print(f"响应: {text}")
            print(f"Finish reason: {finish_reason}")
            return model_name

        except Exception as e:
            print(f"❌ 失败: {e}")

    return None

if __name__ == "__main__":
    api_key = os.getenv("ZHIPUAI_API_KEY")

    if not api_key:
        print("错误: ZHIPUAI_API_KEY 环境变量未设置")
        print("\n使用方法:")
        print("  export ZHIPUAI_API_KEY='your-key-here'")
        print("  python3 test_zhipuai_api.py")
        sys.exit(1)

    result = test_zhipuai_api(api_key)

    if result:
        print(f"\n✅ 找到可用模型: {result}")
        print("\n现在可以运行PageIndex了:")
        print(f"  python3 run_pageindex_zhipuai.py \\")
        print(f"    --pdf_path /path/to/your.pdf \\")
        print(f"    --model {result} \\")
        print(f"    --max-pages-per-node 20 \\")
        print(f"    --if-add-node-summary yes")
    else:
        print("\n❌ 所有模型测试都失败了")
        print("\n建议：")
        print("1. 检查API key是否正确")
        print("2. 访问 https://open.bigmodel.cn/usercenter/apikeys 验证key")
        print("3. 确保账户有足够的余额")
