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

### T1 — Text quality check cell

Add a debug cell immediately after the PDF extraction cell.

Print:
- First 1000 chars of `paper_text`
- Count of words longer than 25 chars (indicates broken PDF spacing)
- First 10 such words

**Done when:** Running the cell shows the raw text sample and flags concatenated words.

---

### T2 — Section filter cell

Add a `filter_paper_text(text)` function and a cell that runs it before Step 1.

Rules:
- Cut off everything from `References` / `Bibliography` heading onward (regex on line start)
- Remove figure/table caption lines (`Figure N`, `Fig. N`, `Table N`)

Store result in `filtered_text`. All later cells use `filtered_text` instead of `paper_text`.

**Done when:** `filtered_text` is shorter than `paper_text` on a real paper (References removed), and caption lines are gone.

---

### T3 — CandidateWithContext dataclass

Add to the models cell (alongside `MethodologyProfile`):

```python
@dataclass
class CandidateWithContext:
    candidate: str
    sentence: str
    section: str = "unknown"
    source_paper: str = ""
```

**Done when:** Dataclass is defined and importable in later cells.

---

### T4 — Update extract_candidates

Change signature: `extract_candidates(text: str) -> list[CandidateWithContext]`

Changes:
- For each regex match, record which sentence it came from
- Min length: 3 (was 2)
- Max length: 40 (reject broken PDF concatenations)
- Expand stop word list (add: At, By, As, Of, Be, Are, Was, Has, Have, From, With, That, Which, These, Those, Also, Such, Both, Each)

**Done when:** No candidate in the output is longer than 40 chars or in the stop word list.

---

### T5 — Update Step 2 to use CandidateWithContext

Change Step 2 to iterate over `list[CandidateWithContext]` and pass `cwc.sentence` as context to `classify_role`.

**Done when:** `classified` dict is populated from `CandidateWithContext` list.

---

### T6 — Logging cell

Add a cell after Step 2 that prints each candidate with role + source sentence as JSON:

```json
[
  {
    "candidate": "BERT",
    "role": "Method",
    "sentence": "We fine-tune BERT on the SST-2 dataset.",
    "section": "unknown"
  }
]
```

**Done when:** Running the cell outputs valid JSON with `candidate`, `role`, `sentence`, `section` for every candidate.

---

### T7 — End-to-end test on a real paper

Run the full pipeline on a known paper (e.g., "Attention is All You Need").

Check:
- Candidate count is lower than before
- No tokens longer than 40 chars in output
- Method list contains `Transformer`, `attention`, `BLEU`
- Task list contains `translation`
- Logging cell shows source sentences

**Done when:** Output JSON looks clean and logging cell shows readable sentences.

---

### Later (not this branch)

- Annotate a small gold dataset (10–20 papers)
- Run error analysis — classify failures into missing / noisy / wrong role
- Improve based on analysis results
