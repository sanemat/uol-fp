"""
Convert a Markdown file to PDF (Python port of the md-to-pdf setup).

Uses Python-Markdown for HTML, Pygments for code highlighting (GitHub-like
style) and WeasyPrint for PDF. Inline <style> blocks in the Markdown
(e.g. @page rules) are kept and applied.

```mermaid blocks are rendered to SVG with mermaid-cli (installed from
package.json with `npm ci`, run as `npm run mmdc`) and embedded as images, because WeasyPrint does
not run JavaScript.

Usage:
    python3 report4/md_to_pdf.py [input.md] [output.pdf]

Defaults: report4/report.md -> report4/report.pdf
"""
import base64
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown
from pygments.formatters import HtmlFormatter
from weasyprint import HTML

BASE_CSS = """
@page { size: A4; margin: 18mm; }
body { font-family: sans-serif; }
pre { background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 4px;
      padding: 0.6em 0.8em; white-space: pre-wrap; word-break: break-word;
      overflow-wrap: anywhere; }
pre code, pre span { overflow-wrap: anywhere; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #d0d7de; padding: 0.3em 0.6em;
         overflow-wrap: anywhere; }
img.mermaid { display: block; margin: 0 auto; max-width: 100%;
              max-height: 200mm; }
figure:has(img.mermaid) { break-inside: avoid; }
"""

HERE = Path(__file__).parent
MERMAID_RE = re.compile(r"^```mermaid\n(.*?)^```$", re.DOTALL | re.MULTILINE)
# WeasyPrint cannot draw <foreignObject>, so labels must be plain SVG text.
MERMAID_CONFIG = {
    "htmlLabels": False,
    "flowchart": {"htmlLabels": False, "wrappingWidth": 260},
}


def render_mermaid(md: str) -> str:
    """Replace each ```mermaid block with an <img> holding the rendered SVG."""
    with tempfile.TemporaryDirectory() as tmp:
        config = Path(tmp) / "config.json"
        config.write_text(json.dumps(MERMAID_CONFIG))

        def to_img(match: re.Match) -> str:
            src = Path(tmp) / "diagram.mmd"
            out = Path(tmp) / "diagram.svg"
            src.write_text(match.group(1), encoding="utf-8")
            subprocess.run(
                ["npm", "run", "--silent", "mmdc", "--",
                 "-i", str(src), "-o", str(out), "-c", str(config), "-q"],
                cwd=HERE,
                check=True,
            )
            data = base64.b64encode(out.read_bytes()).decode("ascii")
            return f'<img class="mermaid" src="data:image/svg+xml;base64,{data}">'

        return MERMAID_RE.sub(to_img, md)


def convert(src: Path, dst: Path) -> None:
    body = markdown.markdown(
        render_mermaid(src.read_text(encoding="utf-8")),
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
