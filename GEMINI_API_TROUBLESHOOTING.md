# Gemini API 403错误诊断和解决方案

## 🔍 问题诊断

你提供的Gemini API key遇到了403 Forbidden错误：

```
Error 403: Your client does not have permission to get URL
/v1/models/gemini-1.5-flash:generateContent from this server
```

## 📋 可能的原因

### 1. API未启用（最可能）

Google Gemini API需要在Google AI Studio或Google Cloud中明确启用。

### 2. API Key限制

API key可能被限制为特定的API或有IP限制。

### 3. 免费配额限制

虽然不太可能，但可能达到了某些限制。

## ✅ 解决方案

### 方案1：使用Google AI Studio创建的API Key（推荐）

1. **访问Google AI Studio**
   - URL: https://aistudio.google.com/app/apikey
   - 使用你的Google账号登录

2. **创建新的API Key**
   - 点击 "Create API key"
   - 选择"Create API key in new project"（在新项目中创建）
   - 等待几秒钟，API key创建完成

3. **复制新的API Key**
   - 格式应该是：`AIzaSy...`（39个字符）
   - **重要**：这个key会自动启用Gemini API

4. **测试新的API Key**
   ```bash
   export GEMINI_API_KEY="你的新key"
   curl "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=$GEMINI_API_KEY" \
     -H 'Content-Type: application/json' \
     -d '{"contents":[{"parts":[{"text":"测试"}]}]}'
   ```

### 方案2：在Google Cloud Console中启用API

如果你的key是从Google Cloud Console创建的：

1. **访问Google Cloud Console**
   - URL: https://console.cloud.google.com/

2. **启用Generative Language API**
   - 进入"APIs & Services" > "Library"
   - 搜索"Generative Language API"
   - 点击"Enable"

3. **验证API Key权限**
   - 进入"APIs & Services" > "Credentials"
   - 找到你的API key
   - 检查"API restrictions"
   - 确保"Generative Language API"在允许列表中

### 方案3：使用OpenAI API（备选方案）

如果Gemini API仍然有问题，我们可以回退到OpenAI API：

**免费试用选项：**
1. **OpenAI免费试用**
   - 新账号有$5免费额度
   - 足够处理你的1000页文档

2. **使用其他免费LLM服务**
   - Hugging Face Inference API
   - Anthropic Claude（有免费额度）

## 🧪 诊断脚本

保存为 `test_gemini_api.py` 并运行：

```python
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
                    return True
            elif response.status_code == 403:
                print("❌ 403 Forbidden - API未授权")
                print("   原因: API key没有权限访问此模型")
                print("   解决: 请在Google AI Studio重新创建API key")
            elif response.status_code == 404:
                print("⚠️  404 Not Found - 模型不存在")
            elif response.status_code == 429:
                print("⚠️  429 Rate Limit - 超过速率限制")
            else:
                print(f"❌ 错误: {response.status_code}")
                print(f"   响应: {response.text[:200]}")
        except Exception as e:
            print(f"❌ 异常: {e}")

    return False

def main():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("错误: GEMINI_API_KEY 环境变量未设置")
        print("\n使用方法:")
        print("  export GEMINI_API_KEY='your-key-here'")
        print("  python3 test_gemini_api.py")
        sys.exit(1)

    success = test_gemini_api(api_key)

    if not success:
        print("\n" + "=" * 70)
        print("💡 建议")
        print("=" * 70)
        print("\n1. 在Google AI Studio重新创建API key:")
        print("   https://aistudio.google.com/app/apikey")
        print("\n2. 确保选择'Create API key in new project'")
        print("\n3. 使用新创建的key重新测试")
        print("\n4. 如果仍然失败，考虑使用OpenAI API作为替代")

if __name__ == "__main__":
    main()
```

运行诊断：
```bash
export GEMINI_API_KEY="AIzaSyAnbyFnQgtk96Goy_lX9dg6WvJ2IC-v_ro"
python3 test_gemini_api.py
```

## 📝 下一步行动

### 选项A：获取新的Gemini API Key（推荐）

1. 访问：https://aistudio.google.com/app/apikey
2. 创建新的API key
3. 提供给我，我立即测试并运行

### 选项B：使用OpenAI API

如果Gemini持续有问题：

1. **获取OpenAI API key**
   - 访问：https://platform.openai.com/api-keys
   - 新账号有$5免费额度
   - 足够处理你的文档

2. **使用原版PageIndex**
   ```bash
   export CHATGPT_API_KEY="sk-proj-your-openai-key"
   cd /home/user/PageIndex
   python3 run_pageindex.py \
     --pdf_path /home/user/tcz/docs/ts_124501v181200p.pdf \
     --max-pages-per-node 20 \
     --if-add-node-summary yes
   ```

### 选项C：探索其他免费LLM选项

1. **Claude API** (Anthropic)
   - 有免费额度
   - 需要注册：https://console.anthropic.com/

2. **Hugging Face**
   - 免费Inference API
   - 多种开源模型可选

## 🤔 你想怎么做？

1. **立即重新获取Gemini API key**
   - 最快最简单
   - 完全免费
   - 我帮你测试并运行

2. **改用OpenAI API**
   - 有$5免费额度
   - 更成熟稳定
   - 成本约$5-10处理1000页

3. **探索其他方案**
   - 我可以继续诊断
   - 或者研究其他免费API

请告诉我你的选择，我会立即执行！🚀
