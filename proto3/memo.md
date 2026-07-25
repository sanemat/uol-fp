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
Done as of 2026-07-22: a real 5-run variance study, logged to `proto3/results/run{1..5}/*.json`
and aggregated by `proto3/aggregate_runs.py` (`proto3/results/aggregate.json`), including pooled
Wilson 95% CIs on Precision and Recall for all 4 roles. See "Run-logging + variance study" under
"Evaluation plan" below.

Not yet implemented, in priority order: a consolidated manual review pass (including a
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

**What's actually implemented today: gold-label match, and (2026-07-22) the 5-run variance study
with pooled Wilson CIs (below).** The manual review pass and the Related Work ablation are still
planned, not done.

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
directly instead of a vague "small sample" caveat. (An informal AI-based cross-check exists — see
"NotebookLM cross-check" below — but it is not a substitute for a second human annotator.)

**Correction (2026-07-20): Wilson CI applies to Precision and Recall only, not F1.** Precision
(`TP/(TP+FP)`) and Recall (`TP/(TP+FN)`) are each a simple proportion (successes / trials), which
is exactly what a Wilson interval is for. F1 is the harmonic mean of the two — not a proportion —
so a Wilson interval on F1 directly is not statistically meaningful. Report Wilson 95% CI on P and
R for all 4 roles; report F1 as a point estimate only, with a one-line note that a proper F1
interval would need paper-level bootstrap resampling, which isn't worth adding at n=6 given the
deadline. The two CIs already computed above (TechnicalMethod/Task recall) are exactly this —
recall CIs — and can be used as-is; just don't extend the same treatment to the F1 column.

**Known measurement-instrument artifact, not just a model failure:** MapReduce's Task slot —
gold `"distributed"`, system answer `"automatic parallelization and distribution of large-scale
computations"` — fails the substring rule (`"distributed"` is not a literal substring of
`"distribution"`) despite being arguably correct. Task's low F1 (0.33) is partly a property of
the blunt substring-match rule, not purely a pipeline failure. Worth stating in the report to
separate "the pipeline is wrong" from "the metric is blunt."

### Run-logging + variance study — implemented and tested (2026-07-22)

5 full Stage-2 runs, logged to `proto3/results/run{1..5}/*.json` (6 papers each), scored against
`GOLD_LABELS` by `proto3/aggregate_runs.py` (reuses `scoring.py`'s `score_profile` and
`precision_recall_f1`, unchanged). Output written to `proto3/results/aggregate.json`; console
report cross-checked against each run's pre-existing `run.txt` capture (exact match — confirms the
JSON-based recomputation agrees with the earlier console output).

**Per-role F1 across the 5 runs:**

| Role | F1 mean | F1 min | F1 max | F1 range |
|---|---|---|---|---|
| TechnicalMethod | 0.83 | 0.83 | 0.83 | 0.00 |
| Task | 0.33 | 0.33 | 0.33 | 0.00 |
| Dataset | 0.91 | 0.91 | 0.91 | 0.00 |
| EvaluationMetric | 0.57 | 0.33 | 0.67 | 0.33 |

TechnicalMethod, Task, and Dataset scored identically on every one of the 5 runs — zero variance
across 5 real repetitions, not just the earlier n=2 anecdote. EvaluationMetric is the only role
that moved (F1 ranged 0.33–0.67 across runs; 3 of 5 runs landed at 0.67, one at 0.50, one at 0.33),
confirming the earlier n=2 observation that Gemini does not guarantee bit-for-bit reproducibility,
and narrowing the instability to one role rather than two (the earlier n=2 table also showed
Dataset moving; at n=5, Dataset is stable and only EvaluationMetric is not).

**Pooled Wilson 95% CI on Precision and Recall, all 4 roles** (tp/fp/fn summed across the 5 runs,
n=30 trials/role):

| Role | TP | FP | FN | P | P 95% CI | R | R 95% CI |
|---|---|---|---|---|---|---|---|
| TechnicalMethod | 25 | 5 | 5 | 0.83 | [0.66, 0.93] | 0.83 | [0.66, 0.93] |
| Task | 10 | 20 | 20 | 0.33 | [0.19, 0.51] | 0.33 | [0.19, 0.51] |
| Dataset | 25 | 0 | 5 | 1.00 | [0.87, 1.00] | 0.83 | [0.66, 0.93] |
| EvaluationMetric | 17 | 13 | 13 | 0.57 | [0.39, 0.73] | 0.57 | [0.39, 0.73] |

**Caveat, stated honestly:** the 30 trials/role pooled here are 5 repetitions of the same 6
papers, not 30 independent papers — so these intervals are narrower than a true 30-independent-
sample would give, and should not be presented as if they were. They still supersede the earlier
n=6 single-baseline CIs (TechnicalMethod recall [0.44, 0.97], Task recall [0.10, 0.70]) with a
tighter estimate backed by real repeated measurement, and the report should show both: the
looser, more defensible n=6-independent-paper figure and the tighter, non-independent n=30-pooled
figure, explaining what each does and doesn't prove. Even with the tighter pooled interval,
TechnicalMethod [0.66, 0.93] and Task [0.19, 0.51] still don't overlap here — unlike at n=6 — which
is itself worth reporting as a finding: 5 real repetitions give enough evidence to say
TechnicalMethod outperforms Task with more confidence than the n=6 snapshot alone supported.

### Priority for what to add next (given ~3 weeks total for the whole report, not just Evaluation)

**Reprioritized 2026-07-20, deadline-focused, per direct review.** Three corrections to the
earlier version of this list: (1) the proto2→proto3 synthesis is writing, not an experiment, and
report3's own requirement ("extend the evaluation to cover the whole project, not only the
feature prototype") makes it mandatory — moved into P0. (2) Wilson CI applies to Precision and
Recall only, not F1 (see "Sample size decision" correction above) — fixed below. (3) **Do not
serialize the whole report behind P0/P1.** Introduction, Literature Review, Design, and
Implementation don't depend on unfinished experiment results — draft them now, in parallel,
roughly one chapter per day. Only parts of the Evaluation chapter genuinely have to wait on data.

**P0 (~4-4.5 days) — mandatory, do all 5:**
1. ~~**Run-logging infrastructure + 5 full runs (0.5-1 day).**~~ **Done (2026-07-22).** 5 runs
   logged to `proto3/results/run{1..5}/*.json`. See "Run-logging + variance study" above.
2. ~~**Aggregation + confidence intervals (0.5 day).**~~ **Done (2026-07-22).** Pooled Wilson 95%
   CI on Precision and Recall for all 4 roles, via `proto3/aggregate_runs.py` →
   `proto3/results/aggregate.json`. F1 stays a point estimate only — no CI on F1 (see correction
   above). See "Run-logging + variance study" above.
3. **24-slot manual review (1-1.5 days)** (replaces the old separate "human check" and "evidence
   support/authorship check" — same person reading the same 6 papers once, not three times): per
   (paper, role) — plausibly correct? evidence supports answer? authors' own work, not prior
   work? **Does the quote actually appear in the source text?** (folded in here rather than a
   separate script — the reviewer is already reading the source to judge support/authorship, so
   checking the quote costs nothing extra at this scale; a dedicated automated verbatim-check
   script was considered and dropped as mostly redundant with this pass for only 24 slots. Note
   it's a weaker check than it sounds either way — a verbatim-real quote can still be the *wrong*
   evidence, e.g. a genuine Related Work sentence cited as the paper's own method; that's exactly
   what "evidence supports answer" and "authors' own work" above are for.) Include the
   MapReduce/Task example above as a concrete illustration. Note: this pass has the same
   single-annotator bias as the gold labels themselves — say so once, don't present it as more
   objective.
4. **proto2 → proto3 "fixed / not fixed" synthesis (near-free, folds into figures item's 0.5 day).**
   Map proto2's three named failure modes (output volume, authorship attribution, recall-only
   scoring) onto what items 1-3 actually found — this is what makes the Evaluation chapter cover
   "the whole project," not just proto3. Not an experiment: the skeleton (which failure mode maps
   to which check) can be drafted right now, before items 1-3 even finish, then filled in with
   real numbers once they do.
5. **Submission figures (0.5 day, combined with item 4):** Stage 2c JSON output screenshot, Stage
   3 P/R/F1 table, ideally a proto2-vs-proto3 output comparison (14/0/0/160 sentences vs one
   answer per role, already drafted in `report2/prototype-memo.md` Q12).

**P1 (~1-1.5 days) — one item only, tightly scoped, do not let it re-expand:**
6. **Decomposed-extraction pilot — variant B vs A, nothing more.** 4 independent role-specific
   calls per paper instead of 1 joint call (see "Architecture reconsideration" below), scored with
   the existing `scoring.py` unchanged. Scope limits, explicit: one run each (or B vs the existing
   frozen baseline A), per-role F1 comparison only — **no consolidation pass, and no repeated-run
   variance study for variant B.** Either of those would balloon this back into a multi-day
   project; if there's appetite for them, they belong in Further Work (see "Architecture
   reconsideration"), not here. Promoted ahead of the ablation because it directly targets Task's
   known weakness (F1 0.33, the lowest of the 4 roles) rather than a general robustness check.

**Cut first, in this order, if time runs short (do not attempt out of order):**
1. **Related Work ablation** — a clean controlled experiment, but doesn't improve Task (the
   project's weakest role), so it's the first thing to drop. "Not run, deferred to further work"
   is a legitimate, planned answer for report3.
2. One unscored non-ML-benchmark paper (e.g. HCI) as a qualitative case study of schema fit.
3. A diagnostic (not a shipped metric change) on whether relaxed/stemmed matching would change the
   Task conclusion.
4. A diagnostic (not a shipped schema change) hand-recomputing what EvaluationMetric's P/R/F1
   would be for AlexNet/ResNet if scored as multi-valued (see "Multi-valued roles" below).

**Bottom line: treat "P0 + the decomposed pilot (P1)" as the real completion line for the
experiment/evaluation work.** Effort table for that work only (not the writing):

| Task | Estimate |
|---|---|
| Run-logging implementation + 5 runs | Done |
| Aggregation + CI | Done |
| 24-slot manual review | 1-1.5 days |
| Figures + proto2→proto3 table | 0.5 day |
| Decomposed pilot | 1-1.5 days |
| **Total remaining** | **~3-3.5 days** |

Out of ~21 days total, that leaves ~16-17 days for writing all 6 chapters (~9500 words) plus
citation hunting and revisions — comfortable if drafting starts now in parallel, tight if writing
is left until all experiments finish.

**Explicitly out of scope — defer to the Conclusion's "further work," don't attempt in 3 weeks:**
growing the gold-label corpus for statistical power; a formal inter-annotator-agreement study (no
second human annotator exists on this solo project — an informal AI-based cross-check exists, see
"NotebookLM cross-check" below, but it narrows rather than closes this gap); a full multi-model
comparison (Gemini vs Claude
Haiku vs Llama 3.1 — belongs in the Design chapter's model-choice discussion, not Evaluation);
any variance claim stronger than what the actual run count supports; **the consolidation pass
(variant C) and the full A/B/C three-way comparison** (see "Architecture reconsideration" below)
— designing and debugging a consolidation prompt plus a 5th call per paper is real new scope that
competes directly with the ~16-17 days needed to write all 6 chapters; report3's "work need not be
complete" allowance covers stating this as a planned next step instead; **the full multi-valued
schema implementation** (schema, prompt, gold re-annotation, new scoring function, rerun/rescore —
see "Multi-valued roles" below) — same reasoning, same allowance.

**Risks to state in the report regardless of how much of P1/P2 gets reached:** the substring-match
rule has construct-validity problems independent of pipeline quality (can both under- and
over-credit, see MapReduce example); the frozen baseline JSON is not "ground truth" — it's one
earlier frozen sample, equally subject to non-determinism as any other run, and is already
correctly distinct from `GOLD_LABELS` in the code (keep that distinction equally clear in prose).

**Original n=2 observation — superseded, see "Run-logging + variance study" above for the real
5-run numbers.** (Kept as a one-line historical note: the n=2 anecdote first flagged that Dataset
and EvaluationMetric moved between runs despite unchanged code, `temperature=0`, and `seed=0`; the
5-run study confirmed non-determinism but narrowed it to EvaluationMetric alone — Dataset was
stable across all 5 real runs.)

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
the current joint design was a considered choice. Variant B (decomposed only) is the sole P1 item
above — promoted ahead of the Related Work ablation (now first on the cut list) because it targets
Task's known weakness (F1 0.33) directly. Scope is tightly capped: A vs B, one run each, per-role
F1 only — no consolidation pass, no repeated-run variance study for B. Variant C (consolidation)
and the full 3-way A/B/C comparison are explicitly out of scope for report3 (see the out-of-scope
list above) — real new prompt-design and debugging work, deferred to further work after report3,
not attempted under the current time budget.

If variant B is actually run: reuse `scoring.py` unchanged (each independent call still produces
one `RoleExtraction`, scored the same way as today); the interesting comparison is per-role F1,
A vs B, especially for Task and Dataset (the two roles most likely to benefit from a role-specific
failure-pattern instruction).

---

## Multi-valued roles: which fields need more than one answer (2026-07-20)

Every role currently has exactly one answer (or null). Reconsidered from scratch, using only real
evidence already in this project's own data — not applied uniformly to all 4 roles.

**Per-role evidence:**

- **EvaluationMetric — strongest case, upgrade.** The *current, live* frozen baseline outputs for
  two independent papers already squash two distinct metrics into one string:
  `alexnet.json` and `resnet.json` both answer `"top-1 and top-5 error rates"`. Both papers really
  do report two error rates side by side. `report1/report.md`'s earlier Table 6 also had BERT's
  EvaluationMetric as `"accuracy / F1"`, later refined to `"F1"` alone for scoring tractability —
  not because BERT stopped reporting both.
- **Dataset — real case, upgrade.** BERT's Table 6 gold was `"BooksCorpus / Wikipedia"` (also
  refined away later); BERT genuinely pretrains on both corpora. Transformer's own paper covers two
  WMT language pairs (English-German and English-French) even though the current single-valued
  baseline answer only names one — today's single answer already under-counts what the source
  supports.
- **Task — weak, do NOT upgrade.** The one candidate case (BERT's old "GLUE / SQuAD") was refined
  away and doesn't appear in the current `GOLD_LABELS`. MapReduce's "and"-joined Task answer
  ("automatic parallelization and distribution of large-scale computations") is this memo's own
  already-diagnosed **measurement-instrument artifact** of blunt substring matching (see
  "Evaluation plan" above), not genuine multiplicity. Upgrading Task's schema to patch this would
  conflate two different problems and risks the model padding lists to match a schema that doesn't
  reflect a real property of the role.
- **TechnicalMethod — stays singular.** Zero multi-value evidence across all 6 baselines, and this
  project's own design rationale ("Why proto2's approach fails" above) already deliberately
  reframes the task as "what is THE primary TechnicalMethod" — a considered stance, not an
  oversight to revisit.

**Schema design, if ever implemented:** keep `SingleRoleExtraction` (today's `RoleExtraction`,
renamed) for TechnicalMethod/Task. New `MultiRoleExtraction` for Dataset/EvaluationMetric:
`answers: list[RoleAnswer]` (max 3 items), where `RoleAnswer = {answer: str, evidence: Evidence}`
— **each item carries its own evidence, not one shared quote for the whole list.** A shared quote
can't verbatim-support two different answers (BERT's BooksCorpus/Wikipedia likely appear in
different sentences), and shared evidence would make the P0 "quote-in-source" check ambiguous
about which answer it's meant to justify — every individual answer stays independently falsifiable,
same as today, just applied N times. Give `MultiRoleExtraction` a `primary` property
(`answers[0]` or `None`) so any code that still wants a single scalar doesn't need special-casing.

**Prompt design: ranked list ("primary first"), not a numeric threshold/confidence field.** This
project has already measured real LLM non-determinism (the Dataset/EvaluationMetric F1 drift
between reruns noted above) — a verbalized confidence score would add a second, even less
validated instability axis, with no budgeted calibration study to trust it. Relative ranking is a
better-supported LLM capability than calibrated absolute scoring, and `answers[0]` doubles as "the
primary value" for free. **Enforce the item cap via schema (`max_length`), not prompt wording
alone** — this project already learned that exact lesson once: an earlier prompt-only shape
description was ambiguous and Gemini returned a structurally different (flat-string) evidence
shape than intended; the fix was moving the guarantee into `response_json_schema`, not relying on
prompt text.

**Gold label changes needed, if ever implemented (4 cells only):**

| Paper | Role | Current gold | Proposed gold |
|---|---|---|---|
| bert | Dataset | `"BooksCorpus"` | `["BooksCorpus", "Wikipedia"]` |
| transformer | Dataset | `"WMT"` | `["WMT 2014 English-German", "WMT 2014 English-French"]` |
| alexnet | EvaluationMetric | `"top-5"` | `["top-1 error rate", "top-5 error rate"]` |
| resnet | EvaluationMetric | `"top-1"` | `["top-1 error rate", "top-5 error rate"]` |

Everything else unchanged.

**Scoring approach, if ever implemented:** add a parallel `score_role_multi` (greedy substring
matching, generalizing `score_role`'s tp/fp/fn/tn semantics to N items) rather than rewriting the
existing tested `score_role` — for length ≤1 on both sides it reduces to exactly today's four
cases, so it's an extension, not a replacement, and the existing 13 tests and headline numbers
stay intact. Once Dataset/EvaluationMetric can contribute more than 1 tp/fp/fn per paper, those
two roles' totals are no longer bounded by n=6 the way TechnicalMethod/Task's are — worth a one-
line callout in "Evaluation plan"'s micro/macro discussion if this ever ships.

**Status: write-up only for report3, not implemented.** This is a third scope addition on top of
P0 (~3-3.5 days) and P1 (~2.5-3 days), and full implementation (schema, prompt, gold
re-annotation, new scoring function, rerunning + rescoring 6 papers, redoing the P0 items for the
affected roles since they were computed against the single-valued schema) is not small. ROI is
also weak relative to what's already prioritized: Dataset and EvaluationMetric are already the
second-best-performing roles (F1 0.73 each), while Task — not touched by this change — is the
worst (F1 0.33) and is already the top P1 priority via the decomposed-extraction pilot above.
Complements, does not replace or compete with, the decomposed-extraction pilot or the ablation.

**Optional near-free diagnostic (P2, ~0.25-0.5 day, only if P0+P1 finish with slack):** by hand,
without touching any code, recompute what EvaluationMetric's P/R/F1 would be for just AlexNet and
ResNet if scored as multi-valued using the answers already sitting in the frozen baseline JSON.
Same tier as the existing Task-substring-matching diagnostic already in the P2 list above.

**Full implementation (schema, prompt, gold re-annotation, scoring, rerun) is out of scope for
report3** — add to the out-of-scope list above, alongside variant C (consolidation) and the full
A/B/C comparison: real new scope competing with the ~14-15 days needed to write all 6 chapters,
not needed to prove report3's core claims.

---

## NotebookLM cross-check (2026-07-25)

Each of the 6 papers was run independently through Google NotebookLM, asked for the same
TechnicalMethod/Task/Dataset/EvaluationMetric extraction the proto3 pipeline performs, with
output saved to `notebooks/<paper>.md`. Compared against `proto3/baseline/*.json` (and, for
two cells below, all 5 real runs in `proto3/results/run{1..5}/`).

**Purpose and status:** an informal, single-pass cross-check with one AI tool — no annotation
protocol, no disagreement adjudication, no human second annotator. It narrows but does not
close the "no second annotator" gap noted above and in "Evaluation plan" — do not present it
as a formal inter-annotator-agreement study.

**Findings:**

1. **TechnicalMethod: stable agreement across all 6 papers**, exact or near-exact
   (e.g. "Google", "BERT", "Transformer", "MapReduce" match on both sides). Independent
   corroboration that this is the strongest role.
2. **Multi-valued pattern, independently corroborated.** For BERT, ResNet, and Transformer,
   the single-valued baseline picked one Dataset/EvaluationMetric value where NotebookLM
   (unconstrained) listed several real ones from the same source text — e.g. BERT Dataset:
   baseline `"SQuAD v1.1"` vs NotebookLM's BooksCorpus/Wikipedia (pre-training) plus
   GLUE/SQuAD v1.1+v2.0/SWAG/CoNLL-2003 (evaluation); Transformer Dataset: baseline
   `"WMT 2014 English-German"` vs NotebookLM's addition of WMT 2014 English-French and the WSJ
   Penn Treebank; ResNet Dataset/EvaluationMetric similarly broader (+ CIFAR-10/PASCAL
   VOC/COCO, + mAP). This is a second, independent source pointing at the same gap already
   reasoned about from this project's own data in "Multi-valued roles" above.
3. **MapReduce Dataset — genuine recall miss, not absence.** Gold label is `"TeraSort"`
   (`proto3/aggregate_runs.py` `GOLD_LABELS`). The pipeline answered `null` in the frozen
   baseline **and in all 5 real runs** (`proto3/results/run{1..5}/mapreduce.json`). NotebookLM
   independently found the dataset description in the source text (two ~1TB grep/sort
   benchmark datasets, $10^{10}$ 100-byte records) — confirming the answer is present in the
   paper, so this is a model recall failure, not a case where the source lacks the
   information. Distinct from the already-documented MapReduce **Task** substring-artifact
   above ("answer present but scored wrong by a blunt metric") — this is "answer never
   produced at all."
4. **Pagerank EvaluationMetric — second instance of the "metric is blunt" pattern.** Gold
   label is `"quality"`. The pipeline consistently answered `"precision"` across all 5 real
   runs — not a substring match against `"quality"`, so scored wrong. The paper's own text
   supports both terms ("we need tools that have very high precision..." and "The most
   important measure of a search engine is the quality of its search results"), and
   NotebookLM's independent extraction also names Precision as one of the metrics. This
   suggests the gold label choice, not the model, is the weak point here — a second, parallel
   example to the MapReduce Task case of the same measurement-instrument-artifact pattern.

---

## Research framing

This project uses a long-context LLM as a schema-guided document-level information extractor. The input is a full research paper; the output is a structured JSON profile of the methodology. The output is evaluated against gold labels and validated with supporting evidence quoted from the source text. This framing is more testable and more academically defensible than submitting the paper to an LLM and reporting whatever it returns.

---

## Ablation

**Status: first item on the cut list (2026-07-20) — see "Evaluation plan" above.** Demoted from P1
because it's a clean controlled experiment but doesn't improve Task, the project's weakest role
(F1 0.33) — the decomposed-extraction pilot targets that directly and is P1 instead. Not required
to prove report3's core claims; "not run, deferred to further work" is a legitimate answer.

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
- ~~**Still open: how much of P1/P2 is reachable?**~~ Resolved 2026-07-20: proto2→proto3 synthesis
  is now P0 (mandatory, not optional — it's writing, not an experiment). P1 is just the
  decomposed-extraction pilot, tightly scoped. Everything else (ablation, HCI case study, relaxed-
  matching diagnostic, multi-valued diagnostic) is an explicitly ordered cut list, dropped in that
  order if P0+P1 don't leave enough time to write all 6 chapters — see "Priority for what to add
  next" above.

---

## What happened to Stage 0–4 (NLI + first-person filter)

The earlier proto3 design kept NLI but added a first-person filter, top-N selection, and LLM term extraction as a final step. This is an improvement over proto2 but does not change the fundamental framing — it is still sentence classification. The first-person filter reduces authorship noise but misses passive or impersonal primary claims ("BERT is pre-trained on BooksCorpus..."). The LLM in Stage 4 only sees the top sentences selected by NLI, so it cannot recover anything Stage 1–3 missed.

Document-level LLM extraction removes this dependency chain. The LLM reads the full paper and decides what is the primary method. The authorship problem is handled by the LLM's language understanding, not by heuristic filters.
