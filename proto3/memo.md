# proto3 Design Memo

## What proto3 does

Input: TEI XML of one computing research paper

Output: one short term per role

```json
{
  "TechnicalMethod": "Transformer",
  "Task": "machine translation",
  "Dataset": "WMT 2014 English-German",
  "EvaluationMetric": "BLEU"
}
```

Approach: **document-level IE with a long-context LLM**

Send the cleaned paper text (all sections except References) to an LLM.
The LLM reads the full paper as a unit and returns structured JSON.

---

## Why not proto2's approach

proto2 classifies every sentence into one of four roles with NLI.
This is text classification, not extraction.

Problems:
- Output volume: MapReduce produced 151 TechnicalMethod sentences. Not usable.
- No mechanism to distinguish "the paper's own method" from "a method cited from prior work."
- Evaluation was recall-only: 10/12 means the gold term appeared somewhere in 100+ sentences.
- Threshold 0.5 is arbitrary; no principled way to cut the output.

The real task is: **given a paper, what is the primary TechnicalMethod?** This is a QA problem, not sentence classification.

---

## Why document-level matters

Jain et al. (SciREX) argue: "a significant amount of information can only be gleaned from analyzing the full document." Dataset and EvaluationMetric typically appear in the Experiment section, not the Abstract or Method. Sending only a subset of the paper recreates the recall gap that document-level IE was designed to avoid.

---

## Context window

A typical computing paper in plain text is 4,000–20,000 tokens. Modern long-context LLMs handle this:

| Model | Context | Cost |
|---|---|---|
| Gemini 1.5 Flash | 1M tokens | cheap API |
| Claude Haiku | 200k tokens | cheap API |
| Llama 3.1 8B Instruct | 128k tokens | free (Colab GPU) |

The full paper fits. Chunking is not needed.

---

## Pipeline

```
XML
  ↓ Stage 0: parse sections (GROBID, same as proto2)
  ↓ Stage 1: extract text from all sections except References/Acknowledgements
  ↓ Stage 2: send to LLM with extraction prompt
Output: MethodologyProfile JSON
```

### Stage 0 — Parse XML

Same as proto2. Extract Abstract and body sections from TEI XML via GROBID.
Skip: References, Acknowledgements, Related Work.

### Stage 1 — Text extraction

Concatenate section texts in order (Abstract first, then body sections).
No sentence-level filtering. The LLM sees everything that is not References.

### Stage 2 — LLM extraction

Prompt:

```
You are extracting research methodology from a computing research paper.
Return a JSON object with exactly these four fields:

{
  "TechnicalMethod": "the main method, model, algorithm, or system proposed by the authors",
  "Task": "the research task or problem being addressed",
  "Dataset": "the dataset used for training or evaluation",
  "EvaluationMetric": "the metric used to report results"
}

Rules:
- Use the authors' own method, not methods cited from prior work.
- Return the shortest identifying term (e.g. "Transformer", not "a novel attention-based model").
- If a field is not present in the paper, return null.
- Return only the JSON object, no explanation.

Paper text:
{paper_text}
```

---

## Evaluation

Same gold labels as proto2 (6 papers × 4 roles = 24 role-paper pairs).

Metrics:
- **Top-1 match**: does the returned term contain the gold label as a substring? (same as proto2)
- **Top-1 precision**: is the returned term plausibly correct by human judgment? (new; manual check)

This measures something proto2 could not: precision on a single answer, not recall over 100+ sentences.

---

## Open questions

- Which LLM to use? (Llama 3.1 8B avoids API cost; Claude Haiku is more reliable)
- Does "Related Work" need to be excluded? (it describes prior methods; may confuse the LLM)
- How to handle papers with no clear method section heading?

---

## What happened to Stage 0–4 (NLI + first-person filter)

The original proto3 design kept NLI but added a first-person filter, top-N selection, and LLM term extraction as a final step. This is an improvement over proto2 but does not change the fundamental framing — it is still sentence classification. The first-person filter reduces noise but misses passive or impersonal primary claims ("BERT is pre-trained on..."). The LLM in Stage 4 only sees the top sentences selected by NLI, so it cannot recover anything Stage 1–3 missed.

Document-level LLM extraction avoids this dependency chain. The LLM reads the full paper and decides what is the primary method. The authorship problem ("we propose X" vs "X was proposed by Y") is handled by the LLM's language understanding, not by heuristic filters.
