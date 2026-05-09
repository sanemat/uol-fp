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

## Pipeline Architecture (revised)

PDF parsing is preprocessing, not part of the research pipeline.

```
Local:
  PDF → GROBID (Docker) → TEI XML

Colab:
  upload TEI XML
  → parse sections (abstract, body divs, skip references)
  → sentence splitting
  → candidate extraction
  → role classification
  → design detection
  → output JSON
```

GROBID provides section structure for free:
- abstract
- section heading + body text
- references separated (not included in body)

TEI XML is kept as-is (not converted to JSON). Colab reads the XML directly using ElementTree.

## Input Length Constraints

Both BERT-based models and LLMs have input length limits.
Full paper text cannot be processed at once.

Solution: sentence-level splitting within each section.

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

### ✅ T8 — Compare PDF extraction: PyMuPDF vs GROBID

PyMuPDF: 39497 chars, 1 long word — spaces correct.
GROBID HuggingFace public server: failed (cold start issue).
GROBID tested locally via Docker: works correctly. Returns structured TEI XML with 24 sections, references excluded.

**Decision: use GROBID locally. TEI XML is the hand-off format to Colab.**

---

### T9 — Local GROBID script: PDF → TEI XML

Write `proto1/pdf_to_xml.py` — CLI script that sends a PDF to local GROBID and saves TEI XML.

```
docker run -d --rm -p 8070:8070 lfoppiano/grobid:0.8.1
python pdf_to_xml.py paper.pdf          # saves paper.xml
python pdf_to_xml.py paper.pdf --out out.xml
```

The script:
- POSTs PDF to `http://localhost:8070/api/processFulltextDocument`
- Saves raw TEI XML response to file
- Prints summary: title, abstract length, section count

**Done when:** Running on Transformer paper PDF produces a `.xml` file. Title, abstract, and section headings are visible in the summary output.

---

### T10 — Update Colab pipeline to read TEI XML

Replace the PDF upload cell with a TEI XML upload cell.

New cell:
- Uploads `.xml` file from local
- Parses with ElementTree
- Extracts abstract + body sections (heading + paragraph text)
- Skips References / Acknowledgements divs
- Produces `sections: list[dict]` with `heading` and `text`
- `CandidateWithContext.section` is populated from actual GROBID section headings

Remove from pipeline:
- pdfplumber cell
- PyMuPDF comparison cells
- `filter_paper_text()` (GROBID already excludes References)
- Text Quality Check cell (no longer needed)

**Done when:** Uploading the Transformer paper XML produces candidate log with readable sentences and correct section names (e.g. `"Model Architecture"`, `"Training"`).

---

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

### Later (not this branch)

- Annotate a small gold dataset (10–20 papers)
- Run error analysis — classify failures into missing / noisy / wrong role
- Improve based on analysis results
