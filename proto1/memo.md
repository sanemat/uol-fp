# Task: Build a Simple System for Methodology Extraction

## Background

Research papers use the word **methodology**, but the meaning is not consistent.

* Some papers use "method" to mean a model (e.g. BERT)
* Some use it to mean research design (e.g. experiment)
* Some parts are clearly written, others are not

Because of this, it is hard to extract methodology automatically.

---

## Key Idea

We do NOT try to find the perfect definition.

Instead, we define a **simple and practical structure** that can be extracted from text.

Methodology = 3 main parts + optional details:

* **Design** → overall research design (experiment, survey, case study)
* **Method** → model, algorithm, or technique (e.g. BERT, CNN)
* **Task** → research task or problem (e.g. question answering, image classification)

Optional:

* **Data** → dataset or source (e.g. MNIST, SQuAD)
* **Evaluation** → metrics (accuracy, F1)

These parts are usually **explicitly written** in papers.

---

## Goal

Build a simple pipeline that:

1. reads a research paper text
2. extracts methodology candidates
3. classifies each candidate into a role
4. detects research design
5. outputs a structured result
6. validates consistency

---

## Approach

We do not need a perfect model.

We build a **simple working prototype**, then improve based on error analysis.

### Step 1: Candidate Extraction

* Use SciBERT to extract methodology-related phrases (sentence-by-sentence, max_length=128)
* Targets: model names, algorithm names, dataset names, metric names
* Save each candidate with its context: `{candidate, sentence, section, source_paper}`

The `section` field is best-effort (heuristic heading detection). Falls back to `"unknown"`.

---

### Step 2: Role Classification

* Rule-based for baseline: hard-coded term lists + context regex
* Input: candidate string only (for now)
* Log: full `{candidate, sentence, section, role}` saved for error analysis

---

### Step 3: Design Detection

* Rule-based: regex pattern matching on abstract or first ~2000 chars

---

### Step 4: Build Output

Output format:

```json
{
  "Design": "experiment",
  "Method": ["BERT"],
  "Task": ["question answering"],
  "Optional": {
    "Data": ["SQuAD"],
    "Evaluation": ["F1"]
  }
}
```

---

### Step 5: Consistency Checking

Apply simple validation rules:

* Experiment without Task → weak
* Experiment without Method → weak
* Method without Task → incomplete
* Theoretical design with benchmark-style Evaluation → possible mismatch

---

## Input Length Constraints

Both BERT-based models and LLMs have input length limits.
Full paper text cannot be processed at once.

Solution: sentence-level splitting.

* SciBERT processes each sentence with `max_length=128` (or 256 — compare in experiments)
* LLM receives only the candidate list (or candidate + sentence + section), not the full paper

Role of each model:

| Step | Model | Input |
|------|-------|-------|
| Candidate extraction | SciBERT + regex | sentence (max 128 tokens) |
| Role classification | rule-based → LLM later | candidate (+ sentence + section when needed) |
| Design detection | regex → LLM later | abstract text |
| Integration | rules | classified candidates |

---

## Error Analysis Strategy

Run the prototype first. Check the log output. Classify failures into 3 types:

1. **Missing candidate** — term is in the paper but not extracted
2. **Noisy candidate** — extracted but not methodology-related
3. **Wrong role** — extracted with correct role potential, but classified wrong

Then decide improvements:

| Failure type | Next action |
|--------------|-------------|
| Missing | Fix regex, NER, max_length, or section range |
| Noisy | Add stoplist, section filter, or candidate scoring |
| Wrong role | Pass `sentence` + `section` to LLM (no restructuring needed) |

In the report:

> The first prototype uses sentence-level candidate extraction and passes only the candidate
> list to the classifier. This simple design is used as a baseline. If role classification
> is inaccurate, an error analysis will determine whether additional context (source sentence,
> section name) is needed.

---

## Internal Data Structure

From the beginning, each candidate is stored as:

```json
{
  "candidate": "BERT",
  "sentence": "We fine-tune BERT on the SST-2 dataset.",
  "section": "Method",
  "source_paper": "paper_id_001"
}
```

The LLM receives only `candidate` at first. `sentence` and `section` are added later if
error analysis shows role classification is wrong.

---

## Important Notes

* Focus on **working system**, not perfect accuracy
* Keep implementation simple
* Avoid complex training
* This is a prototype for later improvement

---

## TODO

### ✅ T1 — Text quality check cell

Confirmed: 407 words > 25 chars on Transformer paper. pdfplumber breaks word spacing throughout the entire PDF. Root cause identified.

---

### ✅ T2 — Section filter cell

Implemented: cuts off References section, removes figure/table caption lines. Produces `filtered_text`.

---

### ✅ T3 — CandidateWithContext dataclass

Implemented: `candidate`, `sentence`, `section`, `source_paper`.

---

### ✅ T4 — Update extract_candidates

Implemented: returns `list[CandidateWithContext]`, min=3, max=40, expanded stop words.

---

### ✅ T5 — Update Step 2 to use CandidateWithContext

Implemented: iterates over `CandidateWithContext`, passes `cwc.sentence` as context.

---

### ✅ T6 — Logging cell

Implemented: prints each candidate with role + source sentence as JSON.

---

### T8 — Compare PDF extraction: PyMuPDF vs GROBID

**Background:** T1 confirmed that pdfplumber breaks word spacing on academic PDFs. The real fix is scholarly document parsing, not text filtering.

Priority order:
1. GROBID — academic paper specialist, outputs TEI XML with section names, body, references separated
2. PyMuPDF blocks — quicker to try, better than pdfplumber, uses `get_text("blocks", sort=True)`

Add a comparison cell to the notebook:

**Approach A — PyMuPDF:**
```python
import fitz  # pip install pymupdf
blocks = page.get_text("blocks", sort=True)  # type 0 = text block
```

**Approach B — GROBID (public HuggingFace server, no Docker needed):**
```python
# POST PDF to https://kermitt2-grobid.hf.space/api/processFulltextDocument
# Parse TEI XML: abstract, body sections, references (already separated)
```

Check both outputs on the Transformer paper. Evaluate:
- Spaces correct?
- Sentence order natural?
- References removed?
- Section names available?
- Tables separated from body?

**Done when:** First 20 sentences of both outputs are printed and checked against the 5 criteria above.

---

### T9 — Replace pdfplumber with the winning approach

Based on T8 comparison, update the PDF extraction cell (`id=7f1f6cbb`) to use the chosen approach.

If GROBID: remove `filter_paper_text()` — References separation is built-in. Update Step 1 to use section-aware text.

If PyMuPDF: keep `filter_paper_text()` as-is. Update extraction to use `get_text("blocks", sort=True)`.

**Done when:** `paper_text` (or structured equivalent) has no words > 25 chars and no References content.

---

### T10 — End-to-end test on a real paper

Run the full pipeline on "Attention is All You Need" with the new extraction.

Check:
- No tokens longer than 40 chars in candidate output
- Method list contains `Transformer`, `attention`
- Evaluation list contains `BLEU`
- Task list contains `translation`
- Candidate log shows readable source sentences

**Done when:** Output JSON is clean and candidate log sentences are readable English.

---

### Later (not this branch)

- Annotate a small gold dataset (10–20 papers)
- Run error analysis — classify failures into missing / noisy / wrong role
- Improve based on analysis results
