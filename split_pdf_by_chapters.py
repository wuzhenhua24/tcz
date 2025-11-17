#!/usr/bin/env python3
"""
PDF 按章节切割工具
根据 PDF 书签（大纲）将文档切割成多个独立的章节文件
"""

import os
import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter


def get_chapter_ranges(pdf_reader):
    """
    从 PDF 书签中提取章节信息
    返回格式: [(章节名称, 起始页码, 结束页码), ...]
    """
    outlines = pdf_reader.outline
    total_pages = len(pdf_reader.pages)

    if not outlines:
        print("警告: PDF 没有书签信息，无法自动按章节切割")
        return []

    chapters = []

    def extract_bookmarks(bookmarks, level=0):
        """递归提取书签信息"""
        for item in bookmarks:
            if isinstance(item, list):
                # 嵌套的书签
                extract_bookmarks(item, level + 1)
            else:
                # 单个书签
                title = item.title
                page_num = pdf_reader.get_destination_page_number(item)
                chapters.append((title, page_num, level))

    extract_bookmarks(outlines)

    # 计算每个章节的页面范围
    chapter_ranges = []
    for i, (title, start_page, level) in enumerate(chapters):
        # 只处理顶级章节（level 0）
        if level == 0:
            # 找到下一个同级或更高级的章节
            end_page = total_pages - 1
            for j in range(i + 1, len(chapters)):
                next_title, next_page, next_level = chapters[j]
                if next_level <= level:
                    end_page = next_page - 1
                    break

            chapter_ranges.append((title, start_page, end_page))

    return chapter_ranges


def sanitize_filename(filename):
    """清理文件名，移除非法字符"""
    # 替换非法字符
    illegal_chars = '<>:"/\\|?*'
    for char in illegal_chars:
        filename = filename.replace(char, '_')

    # 移除前后空格
    filename = filename.strip()

    # 限制长度
    if len(filename) > 100:
        filename = filename[:100]

    return filename


def split_pdf_by_chapters(pdf_path, output_dir=None):
    """
    按章节切割 PDF 文件

    Args:
        pdf_path: PDF 文件路径
        output_dir: 输出目录，默认为 PDF 文件同目录下的 'chapters' 文件夹
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        print(f"错误: 文件不存在 - {pdf_path}")
        return

    # 设置输出目录
    if output_dir is None:
        output_dir = pdf_path.parent / "chapters" / pdf_path.stem
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"正在处理: {pdf_path}")
    print(f"输出目录: {output_dir}")

    # 读取 PDF
    reader = PdfReader(pdf_path)
    print(f"总页数: {len(reader.pages)}")

    # 获取章节范围
    chapter_ranges = get_chapter_ranges(reader)

    if not chapter_ranges:
        print("无法提取章节信息，尝试其他方法...")
        print("\n提示: 可以手动指定章节页码范围")
        return

    print(f"\n找到 {len(chapter_ranges)} 个章节:\n")

    # 切割每个章节
    for idx, (title, start_page, end_page) in enumerate(chapter_ranges, 1):
        print(f"[{idx}/{len(chapter_ranges)}] {title}")
        print(f"    页码范围: {start_page + 1} - {end_page + 1}")

        # 创建新的 PDF
        writer = PdfWriter()

        # 添加页面
        for page_num in range(start_page, end_page + 1):
            writer.add_page(reader.pages[page_num])

        # 生成文件名
        safe_title = sanitize_filename(title)
        output_filename = f"{idx:02d}_{safe_title}.pdf"
        output_path = output_dir / output_filename

        # 保存文件
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        print(f"    已保存: {output_filename}")

    print(f"\n完成! 所有章节已保存到: {output_dir}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python split_pdf_by_chapters.py <PDF文件路径> [输出目录]")
        print("\n示例:")
        print("  python split_pdf_by_chapters.py docs/document.pdf")
        print("  python split_pdf_by_chapters.py docs/document.pdf output/")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    split_pdf_by_chapters(pdf_path, output_dir)


if __name__ == "__main__":
    main()
