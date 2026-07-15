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

**Selected: Gemini (`gemini-2.5-flash`, via the `google-genai` SDK).** Easiest to set up from Google Colab: the API key is read from Colab's built-in secret manager (`google.colab.userdata`), no separate `.env` or `getpass` flow, and no other API account is needed beyond the Google account already used for Colab.

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

For each of the four roles below, return:
- "answer": the shortest identifying term (e.g. "Transformer", not "a novel attention-based model")
- "evidence": one sentence quoted directly from the paper that supports the answer

Roles:
- TechnicalMethod: the main method, model, algorithm, or system proposed by the authors
- Task: the research task or problem being addressed
- Dataset: the dataset used for training or evaluation
- EvaluationMetric: the metric used to report results

Rules:
- Use the authors' own method, not methods cited from prior work.
- If a field is not present in the paper, return null for both answer and evidence.
- For each evidence, return the section heading and one sentence quoted verbatim from the paper.
- Return only the JSON object, no explanation.

Paper text:
{paper_text}
```

---

## Implementation status

Stage 0–2 are implemented in `proto3/3pipeline.ipynb` (Colab notebook), through sending the
prompt to Gemini and parsing the JSON response. Not yet implemented: the 3-axis evaluation
below, the Related Work ablation, and batch processing across `proto3/previouswork/`.

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

- ~~**Which LLM?**~~ Resolved: Gemini (`gemini-2.5-flash`), chosen for the simplest Colab setup (see Selected note above).
- **Evidence verbatim check**: automatic (string search in paper text) or manual? Automatic is feasible; implement as part of the evaluation script.

---

## What happened to Stage 0–4 (NLI + first-person filter)

The earlier proto3 design kept NLI but added a first-person filter, top-N selection, and LLM term extraction as a final step. This is an improvement over proto2 but does not change the fundamental framing — it is still sentence classification. The first-person filter reduces authorship noise but misses passive or impersonal primary claims ("BERT is pre-trained on BooksCorpus..."). The LLM in Stage 4 only sees the top sentences selected by NLI, so it cannot recover anything Stage 1–3 missed.

Document-level LLM extraction removes this dependency chain. The LLM reads the full paper and decides what is the primary method. The authorship problem is handled by the LLM's language understanding, not by heuristic filters.
