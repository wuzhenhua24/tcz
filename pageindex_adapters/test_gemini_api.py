#!/usr/bin/env python3
"""Gemini API诊断工具"""

import os
import requests
import sys

def test_gemini_api(api_key):
    """测试Gemini API连接"""

    print("=" * 70)
    print("Gemini API 诊断工具")
    print("=" * 70)
    print(f"\n✅ API Key: {api_key[:20]}...{api_key[-5:]}")
    print(f"   长度: {len(api_key)} 字符")

    # 测试不同的API版本和模型
    tests = [
        ("v1beta", "gemini-pro"),
        ("v1beta", "gemini-1.5-flash"),
        ("v1beta", "gemini-2.0-flash-exp"),
        ("v1", "gemini-pro"),
        ("v1", "gemini-1.5-flash"),
    ]

    for api_version, model_name in tests:
        print(f"\n{'='*70}")
        print(f"测试: {api_version}/models/{model_name}")
        print(f"{'='*70}")

        url = f"https://generativelanguage.googleapis.com/{api_version}/models/{model_name}:generateContent"

        payload = {
            "contents": [{
                "parts": [{"text": "测试"}]
            }]
        }

        try:
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                params={"key": api_key},
                json=payload,
                timeout=10
            )

            print(f"状态码: {response.status_code}")

            if response.status_code == 200:
                print("✅ 成功!")
                result = response.json()
                if "candidates" in result:
                    text = result["candidates"][0]["content"]["parts"][0]["text"]
                    print(f"响应: {text[:100]}")
                    return (api_version, model_name)
            elif response.status_code == 403:
                print("❌ 403 Forbidden - API未授权")
            elif response.status_code == 404:
                print("⚠️  404 Not Found - 模型不存在")
            elif response.status_code == 429:
                print("⚠️  429 Rate Limit - 超过速率限制")
            else:
                print(f"❌ 错误: {response.status_code}")
                print(f"   响应: {response.text[:200]}")
        except Exception as e:
            print(f"❌ 异常: {e}")

    return None

if __name__ == "__main__":
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("错误: GEMINI_API_KEY 环境变量未设置")
        sys.exit(1)

    result = test_gemini_api(api_key)

    if result:
        print(f"\n✅ 找到可用配置: {result[0]}/models/{result[1]}")
    else:
        print("\n❌ 所有测试都失败了")
        print("\n建议：在Google AI Studio重新创建API key")
        print("https://aistudio.google.com/app/apikey")
