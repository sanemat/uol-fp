# proto3 Design Memo

## What proto3 does

Input: TEI XML of one computing research paper

Output: one answer per role, with supporting evidence

```json
{
  "TechnicalMethod": {
    "answer": "Transformer",
    "evidence": {
      "section": "Model Architecture",
      "quote": "The Transformer is the first transduction model relying entirely on self-attention to compute representations of its input and output without using sequence-aligned RNNs or convolution."
    }
  },
  "Task": {
    "answer": "machine translation",
    "evidence": {
      "section": "Abstract",
      "quote": "We evaluate on the WMT 2014 English-German and English-French translation tasks."
    }
  },
  "Dataset": {
    "answer": "WMT 2014 English-German",
    "evidence": {
      "section": "Abstract",
      "quote": "We evaluate on the WMT 2014 English-German and English-French translation tasks."
    }
  },
  "EvaluationMetric": {
    "answer": "BLEU",
    "evidence": {
      "section": "Results",
      "quote": "Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task."
    }
  }
}
```

Approach: **schema-guided document-level information extraction with a long-context LLM**

The LLM reads the full paper as one document and returns structured JSON.
This is not "send paper to LLM and trust the answer."
The output includes evidence so each answer can be validated against the source text.

---

## Why proto2's approach fails

proto2 classifies every sentence into one of four roles with NLI.
This is text classification, not information extraction.

Problems:
- Output volume: MapReduce produced 151 TechnicalMethod sentences. Not usable.
- No mechanism to distinguish the authors' own method from methods cited from prior work.
- Evaluation was recall-only: 10/12 means the gold term appeared somewhere in 100+ sentences.
- Threshold 0.5 is arbitrary; no principled way to cut the output.

The real task is: given a paper, what is the primary TechnicalMethod? This is closer to QA or IE than sentence classification.

---

## Why document-level and why full paper

Jain et al. (SciREX) argue: "a significant amount of information can only be gleaned from analyzing the full document." Dataset and EvaluationMetric typically appear only in the Experiment section, not the Abstract or Method. Sending only a subset recreates the recall gap that document-level IE was designed to avoid.

A typical computing paper in plain text is 4,000–20,000 tokens. Modern long-context LLMs can usually handle this range without chunking:

| Model | Context | Cost |
|---|---|---|
| Gemini Flash | 1M tokens | cheap API |
| Claude Haiku | 200k tokens | cheap API |
| Llama 3.1 8B Instruct | 128k tokens | free (Colab GPU) |

For the selected papers in this project, the cleaned full text is expected to fit within the context window of modern long-context LLMs. Therefore, chunking is not used in the main pipeline.

**Selected: Gemini (`gemini-3.5-flash`, via the `google-genai` SDK).** Easiest to set up from Google Colab: the API key is read from Colab's built-in secret manager (`google.colab.userdata`), no separate `.env` or `getpass` flow, and no other API account is needed beyond the Google account already used for Colab.

Note: `gemini-2.5-flash` was tried first but returned a 404 (`This model ... is no longer available to new users`) as of July 2026. Gemini model IDs rotate over time — if `gemini-3.5-flash` later stops working, check `https://ai.google.dev/gemini-api/docs/models` for the current stable flash-tier model ID and update `MODEL_NAME` in the notebook.

---

## Pipeline

```
XML
  ↓ Stage 0: parse sections (GROBID, same as proto2)
  ↓ Stage 1: extract and concatenate section texts (skip References, Acknowledgements)
  ↓ Stage 2: LLM extraction with schema-guided prompt
Output: MethodologyProfile JSON (answer + evidence per role)
```

### Stage 0 — Parse XML

Same as proto2. Extract Abstract and body sections from TEI XML via GROBID.
Skip: References, Acknowledgements.
Keep: Related Work (main setting). See Ablation below.

### Stage 1 — Text extraction

Concatenate section texts in reading order (Abstract first, then body sections).
No sentence-level filtering. The LLM sees everything except excluded sections.

### Stage 2 — LLM extraction

Prompt:

```
You are extracting research methodology from a computing research paper.

For each of the four roles below, return an object with:
- "answer": the shortest identifying term (e.g. "Transformer", not "a novel attention-based model")
- "evidence": an object with "section" (the section heading) and "quote" (one sentence quoted verbatim from the paper that supports the answer)

Roles:
- TechnicalMethod: the main method, model, algorithm, or system proposed by the authors
- Task: the research task or problem being addressed
- Dataset: the dataset used for training or evaluation
- EvaluationMetric: the metric used to report results

Rules:
- Use the authors' own method, not methods cited from prior work.
- Return null when a role is not present in the paper.
- Evidence quotes must be copied verbatim from the paper, not paraphrased.

Paper text:
{paper_text}
```

The output shape (four keys, nested `evidence.section`/`evidence.quote`, `null`
handling) is no longer described in the prompt text. It is enforced by Gemini's
structured-output config instead: `response_mime_type="application/json"` and
`response_schema=MethodologyProfile` (a Pydantic model), passed to
`client.models.generate_content` via `GenerateContentConfig`. Google's SDK docs note
that duplicating the schema in the prompt can hurt quality, so the prompt now only
states rules the schema itself cannot express (authorship, verbatim quoting).
`MethodologyProfile` also carries a `model_validator` that rejects a response where
`answer` and `evidence` are not both null or both present — a correlation the plain
JSON Schema subset Gemini accepts cannot express on its own.

Note: an earlier version of this prompt said "evidence" was a single quoted sentence, but
also told the model to "return the section heading and one sentence quoted verbatim" —
an internally inconsistent instruction. In testing on Attention Is All You Need, Gemini
resolved the ambiguity by returning `evidence` as one flat string with the heading
prepended (e.g. `"## Introduction In this work we propose..."`), not the nested
`{section, quote}` object the top-of-file example shows. The prompt above makes the
nested shape explicit so `evidence.section` and `evidence.quote` are reliably separate
fields for the evaluation checks below. That nested shape is now structurally
guaranteed by `response_schema`, not just prompt-requested, so this class of bug can no
longer recur.

Structured output guarantees syntactic validity (valid JSON, the four keys present,
correct types, no extra keys) and the answer/evidence null-correlation above. It does
not guarantee semantic correctness — the answer being right, the quote actually
appearing in the paper, or the section being accurate. Those still require the
evaluation checks below.

---

## Implementation status

Stage 0–2 are implemented in `proto3/3pipeline.ipynb` (Colab notebook), through sending the
prompt to Gemini with structured output (`response_schema=MethodologyProfile`) and parsing
the response with Pydantic. Not yet implemented: the 3-axis evaluation below, the Related
Work ablation, and batch processing across `proto3/previouswork/`.

---

## Evaluation (3 axes)

Same 6 papers as proto2. Gold labels: same as proto2 (6 papers × 4 roles = 24 items).

**1. Gold label match**
Does `answer` contain the gold label as a substring?
Same method as proto2, but now applied to one answer per role, not 100+ sentences.
A correct answer with one sentence is much harder to pass than recall over 151 sentences.

**2. Human precision check**
Is `answer` plausibly correct by human judgment?
Catches cases where the answer is not in the gold labels but is still valid (or where it is wrong despite matching a substring).

**3. Evidence check**
For each returned answer:
- Does `evidence.quote` appear verbatim in the paper text?
- Does `evidence.quote` support `answer`?
- Is `evidence.section` consistent with the quote's actual location in the paper?
- Is the evidence about the authors' own work, not prior work?

The `section` field makes Related Work attribution visible without needing to exclude that section entirely. If the LLM cites a Related Work sentence as evidence for TechnicalMethod, the error is detectable. This check catches hallucination (fabricated evidence) and attribution errors.

---

## Research framing

This project uses a long-context LLM as a schema-guided document-level information extractor. The input is a full research paper; the output is a structured JSON profile of the methodology. The output is evaluated against gold labels and validated with supporting evidence quoted from the source text. This framing is more testable and more academically defensible than submitting the paper to an LLM and reporting whatever it returns.

---

## Ablation

**Related Work inclusion**

Main setting: keep Related Work in the input text.
Ablation: exclude Related Work and compare results.

Rationale: Related Work may help the model understand the contribution of the paper in context. If it causes attribution errors, these are detectable through `evidence.section` — a TechnicalMethod claim citing a Related Work sentence is a visible signal. Keeping Related Work as the main setting gives the model more document context. The ablation tests whether this extra context introduces noise.

---

## Open questions

- ~~**Which LLM?**~~ Resolved: Gemini (`gemini-3.5-flash`), chosen for the simplest Colab setup (see Selected note above).
- **Evidence verbatim check**: automatic (string search in paper text) or manual? Automatic is feasible; implement as part of the evaluation script.

---

## What happened to Stage 0–4 (NLI + first-person filter)

The earlier proto3 design kept NLI but added a first-person filter, top-N selection, and LLM term extraction as a final step. This is an improvement over proto2 but does not change the fundamental framing — it is still sentence classification. The first-person filter reduces authorship noise but misses passive or impersonal primary claims ("BERT is pre-trained on BooksCorpus..."). The LLM in Stage 4 only sees the top sentences selected by NLI, so it cannot recover anything Stage 1–3 missed.

Document-level LLM extraction removes this dependency chain. The LLM reads the full paper and decides what is the primary method. The authorship problem is handled by the LLM's language understanding, not by heuristic filters.
