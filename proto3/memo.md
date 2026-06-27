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

# Long-Context LLM for Methodology Extraction

## Main Idea

The project should not only send a paper to a black-box LLM and trust the answer.

Instead, the project can treat the LLM as a **document-level information extraction tool**.

The input is one full research paper.
The output is a short JSON profile:

```json
{
  "TechnicalMethod": "Transformer",
  "Task": "machine translation",
  "Dataset": "WMT 2014 English-German",
  "EvaluationMetric": "BLEU"
}
```

## Why Full Paper Context Matters

In the earlier design, the system classified each sentence.

This caused several problems:

* It produced too many candidate sentences.
* It could not clearly separate the authors' own method from prior work.
* It measured recall, but not whether the final answer was useful.
* It depended on an arbitrary threshold.

The real question is not:

> Which sentences look relevant?

The real question is:

> What is the main method, task, dataset, and evaluation metric of this paper?

This is closer to a question-answering or information extraction task.

## Why Long-Context LLMs Are Useful

A normal computing paper is often small enough to fit into a modern long-context LLM.

This means the system may not need to split the paper into many chunks.

Instead, it can send the cleaned full paper text to the model.

The system should remove parts that may confuse the model, such as:

* References
* Acknowledgements
* Possibly Related Work

Then the model can read the paper as one document.

## Related Work Direction

There are several useful areas of prior work:

### 1. Document-Level Information Extraction

SciREX is useful because it argues that some scientific information needs the full document.

This supports the idea that methodology extraction should not only use the abstract or a few sentences.

### 2. LLM-Based Scientific Information Extraction

Recent studies use LLMs to extract structured information from scientific papers.

These studies are useful because they show that LLMs can produce structured outputs such as JSON.

### 3. Schema-Guided Extraction

The project should give the LLM a clear schema.

For example:

```json
{
  "TechnicalMethod": "...",
  "Task": "...",
  "Dataset": "...",
  "EvaluationMetric": "..."
}
```

This makes the task more controlled than simply asking the LLM to “summarise the paper”.

### 4. Validation of Black-Box LLMs

A black-box LLM is difficult to trust.

Therefore, the project should not only check the final answer.
It should also ask the model to give evidence from the paper.

For example:

```json
{
  "TechnicalMethod": {
    "answer": "Transformer",
    "evidence": "The Transformer is the first transduction model relying entirely on self-attention..."
  }
}
```

This makes the output easier to check.

## Evaluation Plan

The system can be evaluated in three ways.

### 1. Gold Label Evaluation

Use a small set of papers with gold labels.

For example:

```text
6 papers × 4 roles = 24 items
```

The four roles are:

* TechnicalMethod
* Task
* Dataset
* EvaluationMetric

The system returns one answer for each role.

Then the answer is compared with the gold label.

### 2. Human Precision Check

A human checks whether the returned answer is reasonable.

This is important because a substring match may not always be enough.

For example, the model may return a term that is not exactly the gold label but is still correct.

### 3. Evidence Check

Each answer should include a short supporting passage.

The check asks:

* Does the evidence appear in the paper?
* Does the evidence support the answer?
* Is the answer about the authors' own work, not prior work?

## Stronger Research Framing

The project should not be described as:

> Send the paper to an LLM and use the answer.

A stronger framing is:

> This project uses a long-context LLM as a schema-guided document-level information extractor. The output is evaluated against gold labels and checked with supporting evidence.

This makes the project more testable and less dependent on blind trust in the LLM.

## Main Conclusion

Using the full cleaned paper is a reasonable new design.

The key point is that the project must still evaluate the output.

Long context solves the input-size problem, but it does not solve the trust problem.

Therefore, the project should combine:

* full-paper input,
* a clear JSON schema,
* gold-label evaluation,
* human precision checking,
* and evidence-based validation.
