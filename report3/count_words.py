"""
Count words per chapter in report.md.

Excluded from count:
  - <figure> blocks (includes <figcaption>)
  - <pre> blocks
  - Markdown table rows (lines starting and ending with |)
  - Table/Figure caption lines: "Table N:", "Table B1:", "*Table 2 ...*" etc.
  - Code fences (``` ... ```)
  - Horizontal rules (---)
  - Word count annotations like (1240 words)

Usage:
    python3 report3/count_words.py
"""
import re
import sys
from pathlib import Path

report_path = Path(__file__).parent / "report.md"
text = report_path.read_text()

text = re.sub(r"<style>.*?</style>", "", text, flags=re.DOTALL)


def count_words(chunk: str) -> int:
    # Remove <figure>...</figure> blocks (includes figcaption)
    chunk = re.sub(r"<figure>.*?</figure>", "", chunk, flags=re.DOTALL)
    # Remove <pre>...</pre> blocks
    chunk = re.sub(r"<pre>.*?</pre>", "", chunk, flags=re.DOTALL)
    # Strip remaining HTML tags
    chunk = re.sub(r"<[^>]+>", " ", chunk)
    # Remove markdown table rows
    chunk = re.sub(r"^\|.*\|$", "", chunk, flags=re.MULTILINE)
    # Remove code fences
    chunk = re.sub(r"```.*?```", "", chunk, flags=re.DOTALL)
    # Remove Table/Figure caption lines (plain or italic, with any label like B1, A3)
    chunk = re.sub(r"^\s*\*?(Table|Figure)\s+[A-Za-z]?\d+[^\n]*\*?\s*$", "", chunk, flags=re.MULTILINE)
    # Remove horizontal rules
    chunk = re.sub(r"^---+$", "", chunk, flags=re.MULTILINE)
    # Remove citation markers like [5], [2, 3], [D6], [D1]
    chunk = re.sub(r"\[[A-Za-z]?\d+[^\]]*\]", "", chunk)
    # Remove word count annotations like (1240 words)
    chunk = re.sub(r"\(\d+ words\)", "", chunk)
    # Strip markdown formatting characters
    chunk = re.sub(r"[*_`]", "", chunk)
    # Strip heading markers (## ### etc.) but keep heading text
    chunk = re.sub(r"^#{1,4}\s+", "", chunk, flags=re.MULTILINE)
    return len(chunk.split())


markers = [
    ("Chapter 1", "## Chapter 1:"),
    ("Chapter 2", "## Chapter 2:"),
    ("Chapter 3", "## Chapter 3:"),
    ("Chapter 4", "## Chapter 4:"),
    ("Chapter 5", "## Chapter 5:"),
    ("Chapter 6", "## Chapter 6:"),
]
end_marker = "\n## References"

starts = {name: text.index(m) for name, m in markers}
order = [name for name, _ in markers]

limits = {
    "Chapter 1": 1000,
    "Chapter 2": 2500,
    "Chapter 3": 2000,
    "Chapter 4": 2000,
    "Chapter 5": 2500,
    "Chapter 6": 1000,
}
total_limit = 9500

counts = {}
ok = True
for i, name in enumerate(order):
    start = starts[name]
    end = starts[order[i + 1]] if i + 1 < len(order) else text.index(end_marker)
    counts[name] = count_words(text[start:end])
    flag = "OK" if counts[name] <= limits[name] else "OVER"
    if flag == "OVER":
        ok = False
    print(f"{name}: {counts[name]:>5}  (limit {limits[name]})  {flag}")

total = sum(counts.values())
total_flag = "OK" if total <= total_limit else "OVER"
if total_flag == "OVER":
    ok = False
print(f"{'Total':>9}: {total:>5}  (limit {total_limit})  {total_flag}")

sys.exit(0 if ok else 1)
