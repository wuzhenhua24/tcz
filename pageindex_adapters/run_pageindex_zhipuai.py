"""
PageIndex with ZhipuAI GLM-4 Flash Support
Modified version to use ZhipuAI API instead of OpenAI
"""

import argparse
import os
import json
import sys

# Monkey patch to use ZhipuAI utils
# CRITICAL: We must inject the replacement utils into sys.modules BEFORE
# pageindex.page_index is imported, because page_index.py does 'from .utils import *'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# STEP 1: Remove any cached pageindex modules to ensure clean import
# This is necessary if pageindex was previously imported
modules_to_remove = [key for key in sys.modules.keys() if key.startswith('pageindex')]
for module in modules_to_remove:
    del sys.modules[module]

# STEP 2: Import the ZhipuAI adapter
from pageindex import utils_zhipuai as utils_replacement

# STEP 3: Inject the replacement utils into sys.modules BEFORE importing page_index
# This ensures that when page_index.py executes 'from .utils import *',
# it imports from our ZhipuAI adapter instead of the original utils
sys.modules['pageindex.utils'] = utils_replacement

# STEP 4: Now import the functions - they will automatically use the ZhipuAI adapter
from pageindex.page_index import page_index_main
from pageindex.page_index_md import md_to_tree

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Process PDF or Markdown document with ZhipuAI GLM-4 Flash'
    )
    parser.add_argument('--pdf_path', type=str, help='Path to the PDF file')
    parser.add_argument('--md_path', type=str, help='Path to the Markdown file')

    parser.add_argument(
        '--model',
        type=str,
        default='glm-4-flash',
        help='ZhipuAI model to use (default: glm-4-flash)'
    )

    parser.add_argument('--toc-check-pages', type=int, default=20,
                      help='Number of pages to check for table of contents (PDF only)')
    parser.add_argument('--max-pages-per-node', type=int, default=10,
                      help='Maximum number of pages per node (PDF only)')
    parser.add_argument('--max-tokens-per-node', type=int, default=20000,
                      help='Maximum number of tokens per node (PDF only)')

    parser.add_argument('--if-add-node-id', type=str, default='yes',
                      help='Whether to add node id to the node')
    parser.add_argument('--if-add-node-summary', type=str, default='yes',
                      help='Whether to add summary to the node')
    parser.add_argument('--if-add-doc-description', type=str, default='no',
                      help='Whether to add doc description to the doc')
    parser.add_argument('--if-add-node-text', type=str, default='no',
                      help='Whether to add text to the node')

    # Markdown specific arguments
    parser.add_argument('--if-thinning', type=str, default='no',
                      help='Whether to apply tree thinning for markdown (markdown only)')
    parser.add_argument('--thinning-threshold', type=int, default=5000,
                      help='Minimum token threshold for thinning (markdown only)')
    parser.add_argument('--summary-token-threshold', type=int, default=200,
                      help='Token threshold for generating summaries (markdown only)')
    args = parser.parse_args()

    # Validate that exactly one file type is specified
    if not args.pdf_path and not args.md_path:
        raise ValueError("Either --pdf_path or --md_path must be specified")
    if args.pdf_path and args.md_path:
        raise ValueError("Only one of --pdf_path or --md_path can be specified")

    # Check for ZhipuAI API key
    if not os.getenv("ZHIPUAI_API_KEY"):
        print("=" * 70)
        print("ERROR: ZHIPUAI_API_KEY not found!")
        print("=" * 70)
        print("\n请设置智谱AI API key:")
        print("  选项1: 创建 .env 文件:")
        print("    echo 'ZHIPUAI_API_KEY=your-key-here' > .env")
        print("\n  选项2: 设置环境变量:")
        print("    export ZHIPUAI_API_KEY='your-key-here'")
        print("\n获取API key: https://open.bigmodel.cn/usercenter/apikeys")
        print("=" * 70)
        sys.exit(1)

    print("=" * 70)
    print("PageIndex with ZhipuAI GLM-4 Flash")
    print("=" * 70)
    print(f"Model: {args.model}")
    api_key = os.getenv('ZHIPUAI_API_KEY')
    print(f"API Key: {api_key[:20]}..." if api_key else "Not set")
    print("=" * 70)

    if args.pdf_path:
        # Validate PDF file
        if not args.pdf_path.lower().endswith('.pdf'):
            raise ValueError("PDF file must have .pdf extension")
        if not os.path.isfile(args.pdf_path):
            raise FileNotFoundError(f"PDF file not found: {args.pdf_path}")

        print(f"\n正在处理 PDF: {args.pdf_path}")
        print(f"预计需要 20-40 分钟（取决于文档大小）...")
        print(f"使用模型: {args.model}")
        print("=" * 70)

        # Process PDF with ZhipuAI
        # Create opt configuration object (SimpleNamespace to allow dot notation)
        from types import SimpleNamespace
        opt = SimpleNamespace(
            model=args.model,
            toc_check_page_num=args.toc_check_pages,
            max_page_num_each_node=args.max_pages_per_node,
            max_token_num_each_node=args.max_tokens_per_node,
            if_add_node_id=args.if_add_node_id,
            if_add_node_summary=args.if_add_node_summary,
            if_add_doc_description=args.if_add_doc_description,
            if_add_node_text=args.if_add_node_text
        )

        result = page_index_main(args.pdf_path, opt)

        # Save result
        os.makedirs('results', exist_ok=True)
        output_file = f"results/{os.path.basename(args.pdf_path).replace('.pdf', '_tree_zhipuai.json')}"

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print("\n" + "=" * 70)
        print(f"✅ 成功! 树形结构已保存到: {output_file}")
        print("=" * 70)

        # Print summary
        def count_nodes(node):
            count = 1
            if 'children' in node and node['children']:
                for child in node['children']:
                    count += count_nodes(child)
            return count

        total_nodes = count_nodes(result)
        print(f"\n摘要:")
        print(f"  - 总节点数: {total_nodes}")
        print(f"  - 根标题: {result.get('title', 'N/A')}")
        print(f"  - 根页码: {result.get('pages', 'N/A')}")
        if 'children' in result:
            print(f"  - 第一级章节数: {len(result['children'])}")

    elif args.md_path:
        # Validate Markdown file
        if not args.md_path.lower().endswith('.md'):
            raise ValueError("Markdown file must have .md extension")
        if not os.path.isfile(args.md_path):
            raise FileNotFoundError(f"Markdown file not found: {args.md_path}")

        print(f"\n正在处理 Markdown: {args.md_path}")
        print(f"使用模型: {args.model}")
        print("=" * 70)

        # Process Markdown with ZhipuAI (async)
        import asyncio

        result = asyncio.run(md_to_tree(
            md_path=args.md_path,
            model=args.model,
            if_thinning=(args.if_thinning.lower() == 'yes'),
            thinning_threshold=args.thinning_threshold,
            summary_token_threshold=args.summary_token_threshold,
            if_add_node_id=(args.if_add_node_id.lower() == 'yes'),
            if_add_node_summary=(args.if_add_node_summary.lower() == 'yes')
        ))

        # Save result
        os.makedirs('results', exist_ok=True)
        output_file = f"results/{os.path.basename(args.md_path).replace('.md', '_tree_zhipuai.json')}"

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print("\n" + "=" * 70)
        print(f"✅ 成功! 树形结构已保存到: {output_file}")
        print("=" * 70)
