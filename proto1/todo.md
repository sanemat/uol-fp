# TODO

## ✅ Done

### T1 — Text quality check cell

Confirmed: 407 words > 25 chars on Transformer paper. pdfplumber breaks word spacing throughout the entire PDF. Root cause identified.

---

### T2 — Section filter cell

Implemented: cuts off References section, removes figure/table caption lines. Produces `filtered_text`.

---

### T3 — CandidateWithContext dataclass

Implemented: `candidate`, `sentence`, `section`, `source_paper`.

---

### T4 — Update extract_candidates

Implemented: returns `list[CandidateWithContext]`, min=3, max=40, expanded stop words.

---

### T5 — Update Step 2 to use CandidateWithContext

Implemented: iterates over `CandidateWithContext`, passes `cwc.sentence` as context.

---

### T6 — Logging cell

Implemented: prints each candidate with role + source sentence as JSON.

---

### T8 — Compare PDF extraction: PyMuPDF vs GROBID

PyMuPDF: 39497 chars, 1 long word — spaces correct.
GROBID HuggingFace public server: failed (cold start issue).
GROBID tested locally via Docker: works correctly. Returns structured TEI XML with 24 sections, references excluded.

**Decision: use GROBID locally. TEI XML is the hand-off format to Colab.**

---

### T9 — Local GROBID script: PDF → TEI XML

`proto1/pdf_to_xml.py` written. Converts PDF to TEI XML via local GROBID Docker.

```
python pdf_to_xml.py paper.pdf          # saves paper.xml
python pdf_to_xml.py paper.pdf --out out.xml
```

All 6 dataset papers converted:
- Attention Is All You Need.xml (24 sections)
- BERT Pre-training.xml (27 sections)
- Deep Residual Learning.xml (12 sections)
- MapReduce.xml (42 sections)
- ImageNet / AlexNet.xml (16 sections)
- Google PageRank.xml (16 sections)

---

### T10 — Update Colab pipeline to read TEI XML

Replaced PDF upload cell with TEI XML upload cell. Pipeline now:
- Uploads `.xml` file from local
- Parses with ElementTree
- Extracts abstract + body sections (heading + paragraph text)
- Skips References / Acknowledgements divs
- Produces `sections: list[dict]` with `heading` and `text`
- `CandidateWithContext.section` populated from actual GROBID section headings

Removed: pdfplumber cell, PyMuPDF comparison cells, `filter_paper_text()`, Text Quality Check cell.

---

## 🔲 Next

### T11 — End-to-end test on "Attention is All You Need"

Run full pipeline with GROBID TEI XML as input.

Check:
- No tokens longer than 40 chars in candidate output
- Method list contains `Transformer`, `attention`
- Evaluation list contains `BLEU`
- Task list contains `translation`
- Candidate log shows readable source sentences with correct section names

**Done when:** Output JSON is clean and candidate log shows readable sentences with section names.

---

### T12 — Run pipeline on all 6 dataset papers

After T10 and T11 pass, run the full pipeline on all 6 XML files.

Papers:
- Attention Is All You Need (Transformer)
- BERT
- Deep Residual Learning (ResNet)
- MapReduce
- ImageNet Classification (AlexNet)
- The Anatomy of a Large-Scale Hypertextual Web Search Engine (PageRank)

**Done when:** Each paper produces a structured output JSON without errors.

---

## Later (not this branch)

- Annotate a small gold dataset (10–20 papers)
- Run error analysis — classify failures into missing / noisy / wrong role
- Improve based on analysis results
- Fix Cell 8 heading: says "SciBERT NER" but implementation is regex-based
