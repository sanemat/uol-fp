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

---

## Reframing Discussion: Classification vs QA vs Document IE

### What proto2 actually does

proto2 assigns one of four labels to every sentence in the paper. This is **text classification**. The implicit assumption is: the correct answer to "what is the TechnicalMethod?" is somewhere in the list of sentences the model assigns to TechnicalMethod.

This assumption has a structural problem. The model sees all 200+ sentences and scores each one independently. There is no mechanism to say "this is the primary TechnicalMethod of the paper, not a mentioned method from a related paper." The result is high recall, unknown precision, and unmanageable output volume (MapReduce: 151 TechnicalMethod sentences).

### Why QA is a better framing

The real task is: **given a paper, return a short term that names the TechnicalMethod / Task / Dataset / EvaluationMetric**.

This is a question-answering task:

- Question: "What is the technical method used in this paper?"
- Context: paper text (or key sections)
- Answer: "Transformer" (a short span or generated string)

QA models return one answer, not a ranked list of all candidates. Evaluation is also simpler: does the answer match the gold term? This is what I wanted proto2 to do but it could not, because classification does not commit to one answer.

**Approach A — Extractive QA (no API cost)**

Use a pre-trained QA model (e.g. DeBERTa fine-tuned on SQuAD) with:
- Question: "What is the technical method used in this paper?"
- Context: abstract + method section text

The model returns a span from the context. No labeled methodology data is needed (the QA model is trained on Wikipedia/news SQuAD, not methodology). Same domain mismatch risk as proto2, but the output is one span rather than 100 sentences.

**Approach B — Generative LLM QA (higher quality, API cost)**

Send abstract + method section to an LLM with:

```
Extract the following from the paper:
- TechnicalMethod: the main method, model, or algorithm
- Task: the research task or problem
- Dataset: the dataset used for training or evaluation
- EvaluationMetric: the metric used to report results
Return as JSON.
```

The LLM reads the section as a unit and generates a structured answer. This naturally handles the authorship problem: the LLM understands "we propose X" vs "X was proposed by Y". No hypothesis engineering needed.

**Approach C — Section-level NLI + top-1 (minimal change from proto2)**

Keep NLI but only on Abstract + Method sections, return the single top-scoring sentence per role. This is essentially proto3 Stage 1–3 already described above. It does not fix the framing problem (still classification, not extraction) but reduces output volume significantly.

### Why document / section IE matters

Jain et al. (SciREX) argue that methodology information requires document-level analysis: "a significant amount of information can only be gleaned from analyzing the full document." A sentence in isolation may not contain enough context to identify the methodology role. Section-level IE respects this: it passes a section (not a single sentence) to the model.

proto3 Stage 4 (LLM term extraction) is already a step toward section-level IE — it passes the top sentences together to the LLM as context, not individually.

### Evaluation-first design rationale

proto2's evaluation weakness: substring match on any accepted sentence is easy to pass when the output is 100+ sentences. MapReduce 151 TechnicalMethod sentences will almost certainly contain "MapReduce" somewhere. The score (10/12) overstates the usefulness of the output.

proto3 should define evaluation before choosing an approach:

1. **Top-1 precision**: is the single returned answer (or top-1 sentence) correct?
2. **Gold comparison**: exact term match against manually verified gold labels
3. **Paper coverage**: does the approach work on ML papers only, or also on systems papers?

The evaluation metric drives the approach choice. If top-1 precision is the target, a QA model that returns one answer is directly aligned. If the target is coverage across paper types, an LLM QA approach may generalize better.

---

## Deadline Constraint and Decision

The preliminary report deadline is 29 June 2026. proto3 is not ready and cannot be submitted in time.

**Decision: submit proto2 as-is for the preliminary.**

proto2 is a working prototype. The evaluation result (10/12 recall) and the known limitations (precision unknown, output volume too large) are already documented in Chapter 4. The preliminary report correctly identifies the improvements planned for next iterations.

**What to add to the preliminary report (Chapter 4 §5):**

Add 1–2 sentences noting the text classification → QA reframing as a planned direction:

> A longer-term improvement is to reframe the task as question answering rather than sentence classification. Instead of classifying every sentence, a QA model would take a question ("What is the technical method used in this paper?") and a section of the paper as context, and return a single answer span. This directly addresses the output volume problem and produces a more precise output.

This does not require any code change to proto2 and fits within Chapter 4 §5's existing "Improvements" framing.

**Post-submission: build proto3**

After 29 June, implement proto3 properly with evaluation-first design. The pipeline structure is already drafted in this memo. The key decision remaining is which LLM to use for Stage 4 (Approach B above is the recommended direction).
