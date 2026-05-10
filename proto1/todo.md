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

### T — ResearchDesign hierarchy + TechnicalMethod rename

Grounded in Oates (2006) and Pilkington & Pretorius.

- Replaced flat `DesignType` with `DesignFamily` / `PrimaryDesignType` / `DesignSubtype`
- Added `ResearchDesign` dataclass with `family`, `primary_type`, `subtype`, `secondary_types`
- `detect_design()` returns MIXED family when non-empirical primary + experiment both detected
- Renamed `method` → `technical_method` to separate from Oates/Pilkington "Research Method"
- Output key: `"Design"` → `"ResearchDesign"`, `"Method"` → `"TechnicalMethod"`

---

### T11 — End-to-end test on "Attention is All You Need"

Run full pipeline with GROBID TEI XML as input.

All 6 conditions met:
- No tokens longer than 40 chars in candidate output (longest: "English-to-German", 17 chars)
- TechnicalMethod list contains `Transformer`, `attention` ✅
- Evaluation list contains `BLEU` ✅
- Task list contains `translation` ✅
- Candidate log shows readable source sentences with correct section names ✅
- ResearchDesign: `family=mixed`, `primary_type=design_and_creation`, `secondary_types=[experiment]` ✅

---

### Fix Cell 8 heading

Changed heading from "SciBERT NER" to "Regex" to match the actual regex-based implementation.

---

## 🔲 Next

Two parallel tracks. Pipeline track first; literature track can run alongside.

---

### Pipeline track (T12 → T13, in order)

#### T12 — Run pipeline on all 6 dataset papers

Run the full pipeline on all 6 XML files. This is a smoke test — no quality bar yet.

Papers:
- Attention Is All You Need (Transformer)
- BERT
- Deep Residual Learning (ResNet)
- MapReduce
- ImageNet Classification (AlexNet)
- The Anatomy of a Large-Scale Hypertextual Web Search Engine (PageRank)

**Done when:** Each paper produces a structured output JSON without errors.

---

#### T13 — Reduce candidate extraction noise (precision improvement)

*Requires T12 done first.*

Related: [issue #31](https://github.com/sanemat/uol-fp/issues/31)

Run pipeline on all 6 papers. Classify failures into:
- **Noisy** — extracted but not methodology-related → tighten regex, add stopwords, add section filter
- **Missing** — term not extracted → fix regex or expand patterns
- **Wrong role** — extracted but wrong role → fix classifier rules

**Done when (Transformer paper):**

Must contain:
- TechnicalMethod: `Transformer`, `self-attention`
- Evaluation: `BLEU`
- Task: `translation`

Must NOT contain (in any list):
- `and`, `but`, `solely`, `being`, `while`, `two`, `more`, `less`

TechnicalMethod list ≤ 30 items.

---

### Literature track (T14 → T15 → T16, independent of pipeline)

#### T14 — Create notes.md for must-have papers

*Start here. Highest value: forces careful reading of the closest prior work.*

Write a `notes.md` next to each TEI XML in `previouswork/` for the must-have papers.
Use the template in `memo.md` → "notes.md Template" section (8 headings).

Papers:
- Ghosh 2023a (Extracting Methodology Components...)
- Ghosh 2023b (Enhancing AI Research Paper Analysis...)
- Ma 2023 (From "what" to "how"...)
- Oates 2005 (one shared notes.md for ch8, ch9, ch10)
- Pilkington & Pretorius 2015

**Done when:** Each of the 5 files above has a `notes.md` with all 8 headings filled.

---

#### T15 — Acquire SciBERT TEI XML

*After T14.*

Obtain PDF and TEI XML for Beltagy et al. 2019 (arXiv:1903.10676) via GROBID.
Add both files to `previouswork/`. Write `notes.md` using the template.

---

#### T16 — Acquire GROBID paper TEI XML

*After T15.*

Obtain PDF and TEI XML for Lopez 2009 (ECDL 2009) via GROBID.
Add both files to `previouswork/`. Write `notes.md` using the template.

---

## Later (not this branch)

- Annotate a small gold dataset (10–20 papers)
- Run error analysis — classify failures into missing / noisy / wrong role
- Improve based on analysis results
- Create `previouswork/project/annotation-guideline.md` — annotation rules for the gold set (inter-annotator agreement, boundary cases)
- Create `previouswork/project/evaluation-policy.md` — scoring rules for partial matches in ResearchDesign profiles
- Trim `literaturesurvey.md` to ~2,500 words before final submission (currently ~3,287)
