# PDF 按章节切割工具

这个工具可以根据 PDF 文档的书签（大纲）自动将文档切割成多个独立的章节文件。

## 功能特点

- 自动读取 PDF 书签信息
- 按顶级章节切割文档
- 自动生成规范的文件名
- 保留原始文档格式和内容

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
python split_pdf_by_chapters.py <PDF文件路径>
```

例如：
```bash
python split_pdf_by_chapters.py docs/ts_124501v181200p.pdf
```

### 自定义输出目录

```bash
python split_pdf_by_chapters.py <PDF文件路径> <输出目录>
```

例如：
```bash
python split_pdf_by_chapters.py docs/document.pdf output/chapters/
```

## 输出结果

默认情况下，切割后的章节文件会保存到：
```
<PDF文件目录>/chapters/<PDF文件名>/
```

例如，处理 `docs/ts_124501v181200p.pdf` 后，输出文件在：
```
docs/chapters/ts_124501v181200p/
├── 01_Intellectual Property Rights.pdf
├── 02_Legal Notice.pdf
├── 03_Modal verbs terminology.pdf
├── 04_Foreword.pdf
├── 05_1 Scope.pdf
├── 06_2 References.pdf
...
```

## 已处理文档

- `ts_124501v181200p.pdf` - 已切割成 21 个章节文件

## 注意事项

- 此工具依赖于 PDF 文档中的书签信息
- 如果 PDF 没有书签，工具将无法自动切割
- 文件名会自动清理非法字符，确保兼容性

## 依赖项

- Python 3.7+
- pypdf >= 4.0.0
