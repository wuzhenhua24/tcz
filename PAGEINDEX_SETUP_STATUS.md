# PageIndex 快速试用 - 设置状态

## ✅ 已完成

1. **克隆PageIndex仓库**
   - 位置: `/home/user/PageIndex`
   - 版本: 最新main分支

2. **安装依赖**
   ```
   ✅ openai==1.101.0
   ✅ pymupdf==1.26.4
   ✅ PyPDF2==3.0.1
   ✅ python-dotenv==1.1.0
   ✅ tiktoken==0.11.0
   ✅ pyyaml==6.0.2
   ```

3. **准备配置模板**
   - 已创建: `/home/user/PageIndex/.env.template`

## ⏸️ 待配置：OpenAI API Key

PageIndex需要OpenAI API key才能运行（使用GPT-4o进行文档分析和摘要生成）。

### 配置方法

**选项1: 使用.env文件（推荐）**
```bash
cd /home/user/PageIndex
cp .env.template .env
# 编辑 .env 文件，填入你的API key：
# CHATGPT_API_KEY=sk-proj-your-actual-key-here
```

**选项2: 设置环境变量**
```bash
export CHATGPT_API_KEY="sk-proj-your-actual-key-here"
```

### 获取API Key

1. 访问: https://platform.openai.com/api-keys
2. 登录/注册OpenAI账号
3. 点击"Create new secret key"
4. 复制生成的key（格式: `sk-proj-...`）

## 📊 下一步：处理你的协议文档

配置API key后，运行以下命令处理TS 24.501文档：

```bash
cd /home/user/PageIndex

python3 run_pageindex.py \
  --pdf_path /home/user/tcz/docs/ts_124501v181200p.pdf \
  --model gpt-4o-2024-11-20 \
  --max-pages-per-node 20 \
  --max-tokens-per-node 25000 \
  --if-add-node-summary yes \
  --if-add-node-id yes
```

### 预期结果

**处理时间**: 约20-40分钟（取决于文档大小和API速度）

**输出文件**: `./results/ts_124501v181200p_tree.json`

**树形结构示例**:
```json
{
  "title": "3GPP TS 24.501",
  "pages": [1, 600],
  "summary": "5G NAS协议规范...",
  "children": [
    {
      "title": "1 Scope",
      "pages": [10, 15],
      "summary": "本规范定义了...",
      "node_id": "node_1"
    },
    {
      "title": "3 Definitions and abbreviations",
      "pages": [16, 45],
      "summary": "定义了200+个术语和缩略语...",
      "children": [
        {
          "title": "3.1 Definitions",
          "pages": [16, 35],
          "node_id": "node_3_1"
        },
        {
          "title": "3.2 Abbreviations",
          "pages": [36, 45],
          "node_id": "node_3_2"
        }
      ]
    }
  ]
}
```

## 💰 成本估算

处理一个1000页的PDF文档（TS 24.501约7.6MB）：

**使用GPT-4o（默认模型）:**
- 输入token: ~500K tokens (生成摘要需要读取内容)
- 输出token: ~50K tokens (节点摘要)
- 预估成本: $5-10 USD

**成本组成:**
- 检测文档结构: ~$0.50
- 生成节点摘要: ~$4-9 (取决于节点数量)

💡 **提示**: 处理一次后，生成的树形索引可以重复使用，无需再次付费

## 🔍 处理后的验证

运行成功后，你可以：

1. **查看树形结构**
   ```bash
   cat results/ts_124501v181200p_tree.json | python3 -m json.tool | less
   ```

2. **统计节点数量**
   ```bash
   cat results/ts_124501v181200p_tree.json | jq '[.. | objects | select(has("node_id"))] | length'
   ```

3. **查看第一层节点**
   ```bash
   cat results/ts_124501v181200p_tree.json | jq '.children[] | {title, pages, node_id}'
   ```

## 📝 参数说明

| 参数 | 默认值 | 说明 | 建议值（协议文档）|
|------|--------|------|-------------------|
| `--max-pages-per-node` | 10 | 每个节点最大页数 | 20（协议章节较长）|
| `--max-tokens-per-node` | 20000 | 每个节点最大token数 | 25000 |
| `--if-add-node-summary` | yes | 是否生成节点摘要 | yes（推理检索需要）|
| `--if-add-node-id` | yes | 是否添加节点ID | yes（便于引用）|
| `--if-add-node-text` | no | 是否包含原文 | no（节省空间）|
| `--model` | gpt-4o-2024-11-20 | 使用的模型 | 保持默认 |

## ⚠️ 注意事项

1. **网络连接**: 需要稳定的网络连接到OpenAI API
2. **API限制**: 如果遇到rate limit，可能需要等待或升级账号tier
3. **中断恢复**: 目前PageIndex不支持断点续传，如果中断需要重新开始
4. **成本控制**: 可以先用小文档测试，确认成本后再处理大文档

## 🎯 你的当前状态

```
✅ PageIndex已安装
✅ 依赖已就绪
✅ PDF文档准备好 (ts_124501v181200p.pdf, 7.6MB)
⏸️ 需要配置OpenAI API key

下一步: 配置API key，然后运行处理命令
```
