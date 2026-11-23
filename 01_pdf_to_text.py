"""第 1 步：PDF 转纯文本。
用法: uv run --with pypdf python 01_pdf_to_text.py <PDF目录> <输出目录>
每个 PDF 输出同名 .txt（UTF-8），并清除控制字符。
ponytail: pypdf 会拆碎公式、压平表格；正式流程改用 GROBID 等工具后替换本步骤。
"""
import re, sys
from pathlib import Path
import pypdf

CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")

def pdf_to_text(pdf: Path) -> str:
    pages = pypdf.PdfReader(pdf).pages
    return CTRL.sub("", "\n".join(p.extract_text() or "" for p in pages))

if __name__ == "__main__":
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    dst.mkdir(parents=True, exist_ok=True)
    for pdf in sorted(src.glob("*.pdf")):
        text = pdf_to_text(pdf)
        (dst / f"{pdf.stem}.txt").write_text(text, encoding="utf-8")
        print(f"{len(text):>7} 字符  {pdf.name}")
