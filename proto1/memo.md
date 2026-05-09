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

* **ResearchDesign** → hierarchical research design grounded in Oates (2006) and Pilkington & Pretorius. Fields: `family` (empirical / non_empirical / mixed), `primary_type` (survey / experiment / case_study / action_research / ethnography / design_and_creation / model_or_theory_building), `subtype` (algorithm_development / system_development / model_building / theory_building), `secondary_types`
* **TechnicalMethod** → model, algorithm, or technique (e.g. BERT, CNN). Separated from Oates/Pilkington "Research Method" (interviews, observations, questionnaires).
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
  "ResearchDesign": {
    "family": "mixed",
    "primary_type": "design_and_creation",
    "subtype": "algorithm_development",
    "secondary_types": ["experiment"]
  },
  "TechnicalMethod": ["Transformer", "self-attention"],
  "Task": ["machine translation"],
  "Optional": {
    "Data": ["WMT 2014 English-German"],
    "Evaluation": ["BLEU"]
  }
}
```

---

### Step 5: Consistency Checking

Apply simple validation rules:

* Experiment or DesignAndCreation without Task → weak
* Experiment or DesignAndCreation without TechnicalMethod → weak
* TechnicalMethod without Task → incomplete

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

---

## TEI XML Format (GROBID output)

GROBID version: **0.8.1** (`lfoppiano/grobid:0.8.1` Docker image)

Namespace: `http://www.tei-c.org/ns/1.0` (always needed for ElementTree queries)

Key paths used for parsing:

| Content | XPath |
|---------|-------|
| Title | `.//tei:titleStmt/tei:title` |
| Abstract | `.//tei:abstract` (use `itertext()` to get full text) |
| Body sections | `.//tei:body//tei:div` |
| Section heading | `div/tei:head` |
| Section paragraphs | `div/tei:p` (use `itertext()` — `p.text` misses inline elements like `<ref>`, `<formula>`) |

`itertext()` pattern (required — `element.text` alone is wrong):

```python
NS = {"tei": "http://www.tei-c.org/ns/1.0"}

def _text(element) -> str:
    return " ".join(element.itertext()).strip()
```

GROBID automatically:
- Separates references into `<listBibl>` (not in body)
- Assigns section headings from paper structure
- Handles multi-column layouts

---

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

See `todo.md` for task tracking.
