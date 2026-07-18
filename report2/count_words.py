"""
Count words per section in prototype.md.

Excluded from count:
  - Code fences (``` ... ```)
  - Markdown table rows (lines starting and ending with |)
  - Horizontal rules (---)
  - Heading markers (## etc.), formatting characters (*_`)

References and Appendix do not count toward the word limit, per the
assignment's own carve-out for "additional pages of images or references."

Usage:
    python3 report2/count_words.py
"""
import re
import sys
from pathlib import Path

report_path = Path(__file__).parent / "prototype.md"
text = report_path.read_text()


def count_words(chunk: str) -> int:
    # Remove code fences
    chunk = re.sub(r"```.*?```", "", chunk, flags=re.DOTALL)
    # Remove markdown table rows
    chunk = re.sub(r"^\|.*\|$", "", chunk, flags=re.MULTILINE)
    # Remove horizontal rules
    chunk = re.sub(r"^---+$", "", chunk, flags=re.MULTILINE)
    # Remove image syntax: ![alt](src)
    chunk = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", chunk)
    # Strip markdown formatting characters
    chunk = re.sub(r"[*_`]", "", chunk)
    # Strip heading markers (## ### etc.) but keep heading text
    chunk = re.sub(r"^#{1,4}\s+", "", chunk, flags=re.MULTILINE)
    return len(chunk.split())


markers = [
    ("1. Template Statement", "## 1. Template Statement"),
    ("2. Project Overview and Fit", "## 2. Project Overview and Fit"),
    ("3. Features Implemented", "## 3. Features Implemented"),
    ("4. Algorithms, Techniques and Methods", "## 4. Algorithms, Techniques and Methods"),
    ("5. Code Explanation", "## 5. Code Explanation"),
    ("6. Visual Representation / Demonstration", "## 6. Visual Representation / Demonstration"),
    ("7. Evaluation and Improvement", "## 7. Evaluation and Improvement"),
]
end_marker = "\n## References"

starts = {name: text.index(m) for name, m in markers}
order = [name for name, _ in markers]

total_limit = 2000

counts = {}
for i, name in enumerate(order):
    start = starts[name]
    end = starts[order[i + 1]] if i + 1 < len(order) else text.index(end_marker)
    counts[name] = count_words(text[start:end])
    print(f"{name}: {counts[name]:>5}")

total = sum(counts.values())
flag = "OK" if total <= total_limit else "OVER"
print(f"{'Total':>42}: {total:>5}  (limit {total_limit})  {flag}")

whole_doc_total = count_words(text)
print(f"{'Whole document':>42}: {whole_doc_total:>5}  (exclude: References, Appendix)")

sys.exit(0 if flag == "OK" else 1)
