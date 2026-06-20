# proto3 Pipeline Design

## Goal

Input: TEI XML of one computing research paper
Output: one or more primary items per role (TOP_N, default 3)

```
TechnicalMethod:  ["Transformer"]
Task:             ["machine translation"]
Dataset:          ["WMT 2014", "WMT 2014 English-French"]
EvaluationMetric: ["BLEU", "accuracy"]
```

---

## Why a new design

The proto2 pipeline classifies every sentence in the paper with NLI.
This produces hundreds of results and does not answer the real question:
"What is THE primary method / task / dataset / metric of this paper?"

The problem is closer to QA than sentence classification.

Constraint: Abstract alone misses Dataset and EvaluationMetric (often only in Experiments).
Full paper does not fit in LLM context.

---

## Pipeline

```
XML
  ↓ Stage 0: parse sections
  ↓ Stage 1: candidate extraction (first-person filter + keep Abstract)
  ↓ Stage 2: NLI role classification on candidates only
  ↓ Stage 3: top-N per role by score × section_weight
  ↓ Stage 4: LLM term extraction (RAG-style)
Output: MethodologyProfile with short terms
```

---

## Stage 0 — Parse XML

Same as proto2.
Extract Abstract and body sections from TEI XML via GROBID.
Skip: References, Acknowledgements, Related Work.

---

## Stage 1 — Candidate Extraction

Replace "classify all sentences" with a targeted filter.
Expected output: ~15–40 sentences (down from 200+ in proto2).

### a) First-person active verb filter

Keep sentences that contain:

```
we propose, we introduce, we present, we use, we train, we evaluate,
we implement, we adopt, we employ, we develop,
our model, our approach, our method, our system,
in this paper, in this work
```

Implementation: case-insensitive regex.

Effect: removes prior-work noise naturally.
- "ELMo uses BiLSTM" → no "we" → excluded
- "We propose the Transformer" → included

### b) Keep Abstract regardless

Abstract sentences are always included, even without first-person verbs.
Abstract is short and contains the primary contribution summary.

### c) Section priority weight

Assign a weight per section heading (used in Stage 3, not for filtering):

```python
SECTION_WEIGHT = {
    "abstract": 1.5,
    "model": 1.3,
    "method": 1.3,
    "approach": 1.3,
    "architecture": 1.3,
    "experiment": 1.0,
    "result": 1.0,
    "evaluation": 1.0,
    "introduction": 0.6,
    "default": 0.8,
}
```

Matching: case-insensitive substring match on section heading.

### Known limitation

Passive or third-person primary claims are missed:
- "BERT is pre-trained on BooksCorpus and Wikipedia." → no "we" → excluded

Mitigation: Abstract inclusion covers most such cases.

---

## Stage 2 — Role Classification (NLI)

Apply NLI only to Stage 1 candidates.
Model: `cross-encoder/nli-deberta-v3-small`
Hypothesis template: `"{}"`  (label string used as-is)

Use best hypothesis set from proto2 comparison experiment (TBD).

```python
result = classifier(
    sentence,
    candidate_labels=LABELS,
    hypothesis_template="{}",
)
role = LABEL_TO_ROLE[result["labels"][0]]
score = result["scores"][0]
```

Output per candidate: `(sentence, role, score, section_weight)`

---

## Stage 3 — Top-N Selection per Role

Sort candidates per role by: `score × section_weight`
Take top N.

```python
TOP_N = 3

for role in Role:
    candidates_for_role = [(s, sc, w) for s, r, sc, w in all_candidates if r == role]
    top = sorted(candidates_for_role, key=lambda x: x[1] * x[2], reverse=True)[:TOP_N]
```

Output: up to TOP_N sentences per role (up to 12 sentences total).

---

## Stage 4 — Term Extraction (LLM, RAG-style)

Pass top sentences from Stage 3 to LLM.
Input: ≤12 sentences → always fits in context window.
Captures terms from any section (body sections included via Stage 3).

Prompt structure:

```
For each sentence below, extract the key term or name that represents
the methodology role. Return only the term, not the full sentence.

TechnicalMethod: "We propose the Transformer, a model architecture..."
→ Transformer

Task: "The task is English-to-German machine translation."
→ machine translation

Dataset: "We train on the WMT 2014 English-German dataset."
→ WMT 2014 English-German

EvaluationMetric: "We report BLEU score on the test set."
→ BLEU
```

Which LLM to use: decided separately (Claude API, HF model, etc.).

---

## Design Decisions

| Decision | Rationale |
|---|---|
| First-person filter before NLI | Removes prior-work noise; reduces NLI calls |
| Keep Abstract regardless | High recall; short enough to include safely |
| score × section_weight | Combines NLI confidence with positional importance |
| Top-N per role | Primary elements, not all mentions; N is configurable |
| RAG for term extraction | Abstract alone misses body-only info; full paper too large for LLM |

---

## Known Limitations

- Passive/third-person claims missed by first-person filter
- Section weight heuristic may not generalize to all paper styles
- Term extraction quality depends on LLM choice
- No gold labels for evaluation yet

---

## Open Questions

- Which hypothesis set from proto2 to use? (compare verbose_v1/v2/v3 results first)
- Which LLM for Stage 4? (Claude API requires key; HF models vary in quality)
- TOP_N = 3 appropriate? May need tuning per paper type
