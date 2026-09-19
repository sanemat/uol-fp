"""
Convert a Markdown file to PDF (Python port of the md-to-pdf setup).

Uses Python-Markdown for HTML, Pygments for code highlighting (GitHub-like
style) and WeasyPrint for PDF. Inline <style> blocks in the Markdown
(e.g. @page rules) are kept and applied.

Usage:
    python3 report4/md_to_pdf.py [input.md] [output.pdf]

Defaults: report4/report.md -> report4/report.pdf
"""
import sys
from pathlib import Path

import markdown
from pygments.formatters import HtmlFormatter
from weasyprint import HTML

BASE_CSS = """
@page { size: A4; margin: 18mm; }
body { font-family: sans-serif; }
pre { background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 4px;
      padding: 0.6em 0.8em; white-space: pre-wrap; word-break: break-word; }
table { border-collapse: collapse; }
th, td { border: 1px solid #d0d7de; padding: 0.3em 0.6em; }
"""


def convert(src: Path, dst: Path) -> None:
    body = markdown.markdown(
        src.read_text(encoding="utf-8"),
        extensions=["fenced_code", "codehilite", "tables", "md_in_html", "toc"],
        extension_configs={"codehilite": {"guess_lang": False, "css_class": "hl"}},
    )
    highlight_css = HtmlFormatter(style="default").get_style_defs(".hl")
    # Base CSS comes first so the document's own <style> block can override it.
    html = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<style>{BASE_CSS}{highlight_css}</style></head>"
        f"<body>{body}</body></html>"
    )
    HTML(string=html, base_url=str(src.parent)).write_pdf(dst)


if __name__ == "__main__":
    here = Path(__file__).parent
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else here / "report.md"
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".pdf")
    convert(src, dst)
    print(f"Wrote {dst}")
