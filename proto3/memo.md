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
`response_json_schema=MethodologyProfile.model_json_schema()`, passed to
`client.models.generate_content` via `GenerateContentConfig`. Google's SDK docs note
that duplicating the schema in the prompt can hurt quality, so the prompt now only
states rules the schema itself cannot express (authorship, verbatim quoting).
`MethodologyProfile` also carries a `model_validator` that rejects a response where
`answer` and `evidence` are not both null or both present — a correlation the plain
JSON Schema subset Gemini accepts cannot express on its own.

Note on `response_schema` vs `response_json_schema`: the SDK's `response_schema`
field (accepting a Pydantic model class directly) converts to Google's own `Schema`
proto, a restricted OpenAPI 3.0 subset that does **not** support
`additionalProperties`. Since `extra="forbid"` on the Pydantic models produces
`additionalProperties: false` in their JSON Schema, `response_schema=MethodologyProfile`
fails with `400 INVALID_ARGUMENT ... Unknown name "additional_properties"`.
`response_json_schema` accepts a real JSON Schema dict and explicitly supports
`additionalProperties`, so `MethodologyProfile.model_json_schema()` is passed there
instead. `model_validate_json(response.text)` still does the Pydantic-side parsing,
so this only changes what is sent to the API, not the class used to parse the result.

Note: an earlier version of this prompt said "evidence" was a single quoted sentence, but
also told the model to "return the section heading and one sentence quoted verbatim" —
an internally inconsistent instruction. In testing on Attention Is All You Need, Gemini
resolved the ambiguity by returning `evidence` as one flat string with the heading
prepended (e.g. `"## Introduction In this work we propose..."`), not the nested
`{section, quote}` object the top-of-file example shows. The prompt above makes the
nested shape explicit so `evidence.section` and `evidence.quote` are reliably separate
fields for the evaluation checks below. That nested shape is now structurally
guaranteed by `response_json_schema`, not just prompt-requested, so this class of bug
can no longer recur.

Structured output guarantees syntactic validity (valid JSON, the four keys present,
correct types, no extra keys) and the answer/evidence null-correlation above. It does
not guarantee semantic correctness — the answer being right, the quote actually
appearing in the paper, or the section being accurate. Those still require the
evaluation checks below.

---

## Implementation status

Stage 0–2 are implemented in `proto3/3pipeline.ipynb` (Colab notebook), through sending the
prompt to Gemini with structured output (`response_json_schema=MethodologyProfile.model_json_schema()`)
and parsing the response with Pydantic. Stage 3's gold-label match (P/R/F1 against
`GOLD_LABELS` and the frozen `proto3/baseline/*.json` outputs) is also implemented and tested.
Not yet implemented, in priority order: a real (≥5-run) variance study with logged outputs,
confidence intervals on the P/R/F1 estimates, a consolidated manual review pass (including a
quote-in-source check, folded into that manual pass rather than a separate script), and (lower
priority) the Related Work ablation. See "Evaluation plan" below.

Correction: an earlier version of this file said "batch processing across
`proto3/previouswork/`" was pending. That was a misunderstanding — that directory holds
background/survey PDFs used for the literature review, not additional target papers. Retracted,
not a to-do.

`proto3/baseline/*.json` is the sole frozen reference (no separate `baseline.ipynb` — it only
ever duplicated `3pipeline.ipynb`'s Stage 0-2c with no distinct method). Git history records
what code produced it, if reproducibility is ever needed.

---

## Evaluation plan

Reconsidered from scratch (2026-07-20) — the earlier "3 axes" list below was a brainstorm
("maybe do this"), not a decision. This replaces it with a prioritized plan, given a ~3-week
budget before report3 is due. Same 6 papers and gold labels as proto2 throughout (6 papers × 4
roles = 24 items; `GOLD_LABELS` hardcoded in the notebook, no separate file).

**What's actually implemented today: only gold-label match (below).** Everything else in this
section is planned, not done.

### Gold label match — implemented and tested

Does `answer` contain the gold label as a substring (normalized, case/whitespace-insensitive,
either direction)? Scored as a classification problem (TP/FP/FN/TN, `null` handled as a real
value): a wrong-but-present answer costs both precision and recall; a hallucinated answer where
gold is `null` is a false positive. Implemented in `proto3/src/uol_fp/scoring.py` (13 passing
tests), scored in `3pipeline.ipynb` Stage 3 against `GOLD_LABELS` and the frozen
`proto3/baseline/*.json` outputs.

Current per-role F1 (baseline outputs):

| Role | TP | FP | FN | TN | P | R | F1 |
|---|---|---|---|---|---|---|---|
| TechnicalMethod | 5 | 1 | 1 | 0 | 0.83 | 0.83 | 0.83 |
| Task | 2 | 4 | 4 | 0 | 0.33 | 0.33 | 0.33 |
| Dataset | 4 | 1 | 2 | 0 | 0.80 | 0.67 | 0.73 |
| EvaluationMetric | 4 | 1 | 2 | 0 | 0.80 | 0.67 | 0.73 |
| **Micro** (pool tp/fp/fn) | 15 | 7 | 9 | — | 0.68 | 0.62 | **0.65** |
| **Macro** (mean of 4 F1s) | — | — | — | — | — | — | **0.655** |

**Micro vs macro decision: report both, headline macro.** The 4 roles are fixed, equally
mandatory fields of one schema, not a frequency distribution — a user needs all four, not
"whichever role has more support," so macro (equal weight per role) matches how the tool is
actually used. State explicitly that micro (0.65) and macro (0.655) are close here only because
every role happens to have n=6 in the current 6-paper set — a coincidence of this dataset, not
a property of the method. Don't let a single "Overall" number imply uniform performance: Task
(0.33) is less than half of TechnicalMethod (0.83).

**Sample size decision: keep n=6, state it honestly with real numbers, don't try to grow the
corpus for statistical power.** Wilson 95% CIs at n=6: TechnicalMethod recall 0.83 → **[0.44,
0.97]**; Task recall 0.33 → **[0.10, 0.70]** — these substantially overlap, which undercuts any
claim that TechnicalMethod is reliably "solved" while Task is reliably "broken." Meaningfully
tightening these intervals would need ~30-40 gold-labeled papers per role, not the 6-10 reachable
in 3 weeks with no second annotator to check labels against — poor ROI. Report the CI numbers
directly instead of a vague "small sample" caveat.

**Known measurement-instrument artifact, not just a model failure:** MapReduce's Task slot —
gold `"distributed"`, system answer `"automatic parallelization and distribution of large-scale
computations"` — fails the substring rule (`"distributed"` is not a literal substring of
`"distribution"`) despite being arguably correct. Task's low F1 (0.33) is partly a property of
the blunt substring-match rule, not purely a pipeline failure. Worth stating in the report to
separate "the pipeline is wrong" from "the metric is blunt."

### Priority for what to add next (given ~3 weeks total for the whole report, not just Evaluation)

**P0 (~3-3.5 days) — do these:**
1. **Real variance study.** The single existing "run-to-run variance" table below rests on n=2
   reruns that were never logged to disk (only an ephemeral in-Colab-kernel dict) — not a
   defensible variance claim. Log every Stage-2 run to `proto3/results/runs/run_<n>.json`, run
   ≥5 times, report per-role mean/range F1. If only 3-4 runs are reached before time runs out,
   say so explicitly rather than implying a fuller study.
2. **Confidence intervals** on the P/R/F1 estimates (Wilson interval) — already computed above
   for 2 roles; extend to all 4 and report alongside the aggregate table.
3. **One consolidated manual review pass** (replaces the old separate "human check" and
   "evidence support/authorship check" — same person reading the same 6 papers once, not three
   times): per (paper, role) — plausibly correct? evidence supports answer? authors' own work,
   not prior work? **Does the quote actually appear in the source text?** (folded in here rather
   than a separate script — the reviewer is already reading the source to judge support/
   authorship, so checking the quote is real costs nothing extra at this scale; a dedicated
   automated verbatim-check script was considered and dropped as mostly redundant with this pass
   for only 24 slots. Note it's a weaker check than it sounds either way — a verbatim-real quote
   can still be the *wrong* evidence, e.g. a genuine Related Work sentence cited as the paper's
   own method; that's exactly what "evidence supports answer" and "authors' own work" above are
   for.) Include the MapReduce/Task example above as a concrete illustration. Note: this pass has
   the same single-annotator bias as the gold labels themselves — say so once, don't present it
   as more objective.

**P1 (~2.5-3 days total, three items competing for it) — only if P0 finishes with time to spare;
if only one item fits, do #4 first, not the ablation:**
4. **Decomposed-extraction pilot (variant B vs A)** — see "Architecture reconsideration" below.
   4 independent role-specific calls per paper instead of 1 joint call, scored with the existing
   `scoring.py` unchanged. ~1-1.5 days. Promoted ahead of the ablation because it directly
   targets Task's known weakness (F1 0.33, the lowest of the 4 roles) rather than a general
   robustness check, and is more central to "technical challenge"/"critical evaluation" than the
   ablation.
5. Related Work ablation (see below) — the one item here that's a genuine controlled experiment,
   not a QA check, but not required to prove the core claims of report3. ~1-1.5 days.
6. Explicit proto2 → proto3 "fixed / not fixed" synthesis against proto2's three named failure
   modes (output volume, authorship attribution, recall-only scoring) — near-free once the P0
   data exists, mostly a writing task.

**P2 / optional stretch:** one unscored non-ML-benchmark paper (e.g. HCI) as a qualitative case
study of schema fit, not added to the 24-slot statistics; a diagnostic (not a shipped metric
change) on whether relaxed/stemmed matching would change the Task conclusion.

**Explicitly out of scope — defer to the Conclusion's "further work," don't attempt in 3 weeks:**
growing the gold-label corpus for statistical power; a formal inter-annotator-agreement study (no
second annotator exists on this solo project); a full multi-model comparison (Gemini vs Claude
Haiku vs Llama 3.1 — belongs in the Design chapter's model-choice discussion, not Evaluation);
any variance claim stronger than what the actual run count supports; **the consolidation pass
(variant C) and the full A/B/C three-way comparison** (see "Architecture reconsideration" below)
— designing and debugging a consolidation prompt plus a 5th call per paper is real new scope that
competes directly with the ~14-15 days needed to write all 6 chapters; report3's "work need not be
complete" allowance covers stating this as a planned next step instead.

**Risks to state in the report regardless of how much of P1/P2 gets reached:** the substring-match
rule has construct-validity problems independent of pipeline quality (can both under- and
over-credit, see MapReduce example); the frozen baseline JSON is not "ground truth" — it's one
earlier frozen sample, equally subject to non-determinism as any other run, and is already
correctly distinct from `GOLD_LABELS` in the code (keep that distinction equally clear in prose).

**Original n=2 observation (superseded by the P0 variance study above once it exists — kept here
for the raw numbers, not as the final claim):**

| Role | Baseline F1 | Pipeline run 1 | Pipeline run 2 |
|---|---|---|---|
| TechnicalMethod | 0.83 | 0.83 | 0.83 |
| Task | 0.33 | 0.33 | 0.33 |
| Dataset | 0.73 | 0.80 | 0.91 |
| EvaluationMetric | 0.73 | 0.67 | 0.50 |
| Overall (micro) | 0.65 | 0.65 | 0.64 |

TechnicalMethod and Task scored identically across baseline and both pipeline runs. Dataset and
EvaluationMetric changed between runs despite unchanged code, `temperature=0`, and `seed=0` —
Gemini does not guarantee bit-for-bit reproducibility across sessions. This asymmetry (2 roles
stable, 2 roles not) is itself worth investigating in the real variance study (P0 item 1), not
just noting anecdotally.

---

## Architecture reconsideration: joint vs decomposed extraction (2026-07-20)

**Current design (variant A, implemented): joint extraction.** One prompt, one Gemini call per
paper, returns all 4 roles at once (Stage 2, see "Pipeline" above). Justified originally by Jain
et al./SciREX's document-level argument: extraction can exploit cross-role relationships within
one context — e.g. recognizing "Transformer"/"WMT"/"BLEU" together in the same sentence
("We evaluate the Transformer on WMT using BLEU") links TechnicalMethod, Dataset, and
EvaluationMetric jointly, which four fully-independent extractors would each see in isolation.

**Proposed alternative, not yet implemented:**

- **Variant B — decomposed extraction.** 4 independent calls per paper, one per role, each with
  a role-specific prompt naming that role's specific failure pattern (e.g. TechnicalMethod:
  "distinguish the primary method from components and prior work"; Dataset: "do not return
  datasets mentioned only in prior work"). Justified by Khot et al. 2022 ("Decomposed Prompting":
  arXiv:2210.02406) — decomposing a complex task into independently-optimizable subtasks can beat
  a single joint few-shot prompt on several reasoning tasks.
- **Variant C — decomposed + consolidation.** Variant B's 4 outputs, plus their evidence, passed
  to a 5th call: "Are these four outputs mutually consistent with the evidence? Do not introduce
  new values. Correct only contradictions or role confusion." Aims to recover the cross-role
  relationship joint extraction has natively, without needing one prompt to do everything.

**Why the 4 roles genuinely differ in what they ask the model to judge** (motivates
per-role-tailored prompts under B/C):

| Role | Core judgment |
|---|---|
| TechnicalMethod | Primary method vs. component vs. prior work |
| Task | What problem the paper is actually solving |
| Dataset | What data was actually used, not just mentioned |
| EvaluationMetric | What metric was actually used to report results |

**Predicted outcome (a hypothesis to test empirically, not a settled finding — no paper
directly shows 4-role methodology extraction specifically favors decomposition; the literature
supports both directions for different reasons):**

```
per-role extraction accuracy:      B or C > A
cross-role consistency:            C > A > B
```

**Status and priority:** this design rationale (the table above, the two citations, the A/B/C
framing) is written up now for report3's Design chapter at zero implementation cost — it shows
the current joint design was a considered choice. Variant B (decomposed only) is P1 item 4 above
— promoted ahead of the Related Work ablation because it targets Task's known weakness (F1 0.33)
directly. Variant C (consolidation) and the full 3-way A/B/C comparison are explicitly out of
scope for report3 (see the out-of-scope list above) — real new prompt-design and debugging work,
deferred to further work after report3, not attempted under the current time budget.

If variant B is actually run: reuse `scoring.py` unchanged (each independent call still produces
one `RoleExtraction`, scored the same way as today); the interesting comparison is per-role F1,
A vs B, especially for Task and Dataset (the two roles most likely to benefit from a role-specific
failure-pattern instruction).

---

## Research framing

This project uses a long-context LLM as a schema-guided document-level information extractor. The input is a full research paper; the output is a structured JSON profile of the methodology. The output is evaluated against gold labels and validated with supporting evidence quoted from the source text. This framing is more testable and more academically defensible than submitting the paper to an LLM and reporting whatever it returns.

---

## Ablation

**Status: P1 (optional) — see "Evaluation plan" above.** Not required to prove report3's core
claims; attempt only if the P0 evaluation items finish with time to spare.

**Related Work inclusion**

Main setting: keep Related Work in the input text.
Ablation: exclude Related Work and compare results.

Rationale: Related Work may help the model understand the contribution of the paper in context. If it causes attribution errors, these are detectable through `evidence.section` — a TechnicalMethod claim citing a Related Work sentence is a visible signal. Keeping Related Work as the main setting gives the model more document context. The ablation tests whether this extra context introduces noise.

---

## Open questions

- ~~**Which LLM?**~~ Resolved: Gemini (`gemini-3.5-flash`), chosen for the simplest Colab setup (see Selected note above).
- ~~**Evidence verbatim check**: automatic or manual, separate script or not?~~ Resolved: no
  separate script — a verbatim match only proves instruction-following, not evidence quality, so
  it's folded into the manual review pass (P0 item 3) as one more thing to check while already
  reading the source text, rather than built as standalone tooling.
- **Still open:** how much of P1/P2 (ablation, proto2→proto3 synthesis, HCI case study) is
  reachable depends on how long the P0 items (variance study, CIs, manual review) actually take —
  re-assess after P0 is done, don't commit to P1 scope in advance.

---

## What happened to Stage 0–4 (NLI + first-person filter)

The earlier proto3 design kept NLI but added a first-person filter, top-N selection, and LLM term extraction as a final step. This is an improvement over proto2 but does not change the fundamental framing — it is still sentence classification. The first-person filter reduces authorship noise but misses passive or impersonal primary claims ("BERT is pre-trained on BooksCorpus..."). The LLM in Stage 4 only sees the top sentences selected by NLI, so it cannot recover anything Stage 1–3 missed.

Document-level LLM extraction removes this dependency chain. The LLM reads the full paper and decides what is the primary method. The authorship problem is handled by the LLM's language understanding, not by heuristic filters.
