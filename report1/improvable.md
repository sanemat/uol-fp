# Improvable — Score Improvement Priorities

Criteria source: `preliminary-instruction.md` (14 criteria).
Target: `report.md`. Implementation: `proto2/2pipeline.ipynb`.

---

## Current State by Criterion

| # | Criterion | Status | Notes |
|---|---|---|---|
| 1 | Clear, well-formatted, coherent | ✓ | Opening sentence fixed (D done); Figure 1 and 2 now use `<figure>/<figcaption>` (G done) |
| 2 | Knowledge of area | ✓ | 11 references; GROBID [7] and DeBERTa [11] now cited |
| 3 | Critically evaluates prior work | ⚠ | Jain et al. limitations noted, but all sources need sharper "does not transfer because…" critique (→ J, K) |
| 4 | Proper citation and referencing | ✓ | 11 references; all central tools cited |
| 5 | Design clear and high quality | ✓ | Chapter 3 is thorough |
| 6 | Concept justified | ✓ | Good |
| 7 | Workplan in enough detail | ⚠ | Table exists, but task granularity, risks, and evaluation schedule are thin (predicted 3/5) |
| 8 | Workplan feasible | ✓ | OK |
| 9 | Evaluation strategy appropriate | ⚠ | Core: 3 papers, substring match; extended 6-paper results in Appendix B |
| 10 | Feature prototype high quality | ⚠ | Large output (MapReduce 151 sentences) unaddressed |
| 11 | Technically challenging | ✓ | Section 7 documents the challenges well |
| 12 | Demonstration effective and impactful | ✓ | Video recorded |
| 13 | Evaluate prototype and show improvements | ⚠ | GPU batch processing implemented; more improvements still planned |
| 14 | Innovation and excellence | ⚠ | Hypothesis comparison is genuine, but novelty claim needs more careful support (predicted 3.5/5; → M) |

---

## Predicted Marks (external review estimate)

Estimated total: **70–75**. With stronger literature review and clearer evaluation method, could move into high distinction range.

| # | Criterion | Predicted | Weak point |
|---|---|---|---|
| 1 | Clear, formatted, coherent | 4/5 | — |
| 2 | Knowledge of area | 3.5/5 | Literature review short, sources adequate but not deep |
| 3 | Critical evaluation | 3/5 | Criticism exists but "why insufficient" comparisons are shallow |
| 4 | Citation/referencing | 3.5/5 | Format OK; some claims still need stronger citation |
| 5 | Design quality | 4/5 | — |
| 6 | Domain/user justification | 4/5 | — |
| 7 | Workplan detail | 3/5 | Task granularity, risks, evaluation schedule thin |
| 8 | Workplan feasibility | 4/5 | — |
| 9 | Evaluation strategy | 3/5 | Substring match is too recall-oriented; large output makes it easy to pass |
| 10 | Prototype quality | 4/5 | — |
| 11 | Technical challenge | 4/5 | — |
| 12 | Demo effectiveness | n/a | Not reviewed (video not seen) |
| 13 | Prototype evaluation/improvements | 4/5 | — |
| 14 | Innovation/excellence | 3.5/5 | Combination is interesting; novelty claim needs more careful support |

---

## Key Inconsistency (RESOLVED)

Re-run done with short labels. Transformer now shows 62/14/4/3 (balanced). Gold check: Dataset flipped to ✓ (WMT found), but EvaluationMetric flipped to ✗ (BLEU not in any EM sentence — "Our model achieves 28.4 BLEU" was classified as Task). Total remains 10/12. ResNet was re-run correctly (4_resnet); counts 51/6/14/12 confirmed — Table 6 row unchanged.

---

## Priority 1 — Must-do (blocks marks entirely)

### A. Record the video (MP4, 3–5 min) (DONE)

- **Criteria:** 12
- **Why:** Without the video, criterion 12 scores 0. It is a required submission item. No amount of report polish compensates.
- **Effort:** 1–2 hours
- **Content:** Show GROBID converting a PDF, run the notebook on Colab, show the JSON output for 1–2 papers, narrate the design choices briefly.

---

## Priority 2 — High impact, low effort (30–60 min each)

### I. Fix Design / Prototype inconsistency — separate implemented from planned

- **Criteria:** 1, 5, 13
- **Why:** Chapter 3 Section 3 lists usage NLI and top-k as part of the pipeline ("→ usage NLI → top-k sentences per role"). Chapter 4 Section 5 lists the same two as improvements for the next iteration. A marker reading the report sees a contradiction: either they are in or they are not. This is the most visible consistency problem in the report. Fix: in Chapter 3, mark these two steps as planned (e.g. "planned for Iteration 1") or move them out of the pipeline diagram entirely. In Chapter 4, keep them as next-iteration improvements. The pipeline description in Chapter 3 should exactly match what is implemented.
- **Effort:** Edit 1 paragraph in Chapter 3 Section 3; no code change needed.
- **Location:** Chapter 3 Section 3 ("Overall Structure") pipeline sentence; Chapter 4 Section 5 stays unchanged.

### J. Add critical evaluation to Literature Review — not just summaries

- **Criteria:** 3
- **Why:** Criterion 3 is "critically evaluates previous work and/or academic literature." The current Literature Review describes each paper clearly, but the criticism is generic ("his book was published in 2006, but it still provides useful categories"). What is missing: for each source, explain specifically which parts do NOT transfer to this project and why. Examples:
  - Oates [9]: the six strategies are useful for naming design type, but they were written for human researchers to self-classify, not for automatic extraction — no paper explicitly writes "this is an experiment".
  - Pilkington & Pretorius [10]: the formal ontology is useful for schema justification, but philosophical worldview was excluded because it almost never appears as an explicit phrase in paper text — state this as a testable observation, not just a design decision.
  - Jain et al. [5]: the 4-entity schema matches well, but two specific constraints prevent direct reuse: the corpus is Papers with Code (ML benchmark papers only) and annotation required 4 PhD-level experts at Cohen-κ 95% — neither is available here.
  - Yin et al. [11]: the entailment approach transfers, but the training data (MNLI: news, fiction, telephone) has no scientific text — this means the domain mismatch risk is not just theoretical but structurally built into the model weights.
- **Effort:** Add 1–2 sentences of critical evaluation per source (4 sources = ~4–8 sentences total). Revise rather than add paragraphs.
- **Location:** Chapter 2 Sections 1–3; each source's paragraph.

### M. Fix attribution overclaim — Oates/Pilkington justify schema concept, Jain justifies the 4 roles

- **Criteria:** 3, 14
- **Why:** Chapter 3 Section 2 currently says: "Two independent sources agree on the same four types. First, the ontology from Oates [9] and Pilkington & Pretorius [10] suggests a structured vocabulary for research methodology, including TechnicalMethod, Task, Dataset, and EvaluationMetric." This is an overclaim. Oates and Pilkington & Pretorius define methodology structure in general terms (ResearchDesign, ResearchMethod, PhilosophicalWorldview, data generation methods). They do not name TechnicalMethod, Task, Dataset, or EvaluationMetric. The direct support for the four extraction roles comes from Jain et al. [5] (SciREX). The claim that two independent sources agree on the exact four roles is too strong. Fix: separate the two functions clearly:
  - Oates [9] + Pilkington & Pretorius [10] → justify that research methodology has formal, structured components worth extracting
  - Jain et al. [5] → the direct source for the four extraction roles (Dataset, Metric, Task, Method)
  - Yin et al. [11] → justifies zero-shot NLI as the extraction method
  This also strengthens the Literature Review argument, because the chain of reasoning becomes more precise and harder to challenge.
- **Effort:** Revise 2–3 sentences in Chapter 3 Section 2 and 1–2 sentences in Chapter 2 Section 4 (Synthesis). No new sources needed.
- **Location:** Chapter 3 Section 2 ("Design Justification"), first bullet; Chapter 2 Section 4 ("Synthesis"), second paragraph.

### B. Re-run Transformer with short labels → update Tables 5 and 8 (DONE)

- **Criteria:** 9, 13
- **Why:** The Transformer row in Table 5 and Table 8 was generated with `verbose_v1` (not short labels like the other papers). Short labels are the chosen hypothesis set. The inconsistency weakens the evaluation chapter. Re-running and updating the tables fixes this and likely improves the score.
- **Effort:** Run 1 notebook cell, update 2 table rows in the report.
- **Expected result:** If Task and Dataset are found, 10/12 → 12/12.

### C. Implement first-person verb filter in notebook

- **Criteria:** 10, 13
- **Why:** The report mentions this as a planned improvement (Section 6). Implementing it shows actual progress, not just intention. A filter like `"we propose|we use|we introduce|we train|we evaluate|our model|our approach"` reduces MapReduce's 151-sentence TechnicalMethod output to a manageable number before NLI. Report before/after counts.
- **Effort:** 3–4 lines of code; add one sentence to Chapter 4 Section 6.
- **Code location:** `proto2/2pipeline.ipynb`, Step 2 (Classify Sentences cell).

### D. Fix Chapter 2 opening sentence (DONE)

- **Criteria:** 1
- **Why:** `"Attention Is All You Need" is a very famous AI paper.` is too informal for an academic report. It undermines the credibility of the whole chapter.
- **Effort:** Rewrite 1 sentence.
- **Suggested replacement:** Something like: `Extracting research methodology from scientific papers automatically requires identifying what method was used, on what task, with what data, and by what measure — information that is distributed across the paper and not directly signalled by the title.`

---

## Priority 3 — Medium impact, medium effort (1–2 hours)

### K. Add personal judgment traces — show decision process, not just decisions

- **Criteria:** 3, 14
- **Why:** The report reads uniformly as "This project…", "The pipeline…", "This suggests…". This makes every sentence sound the same and removes evidence that a student made real choices. Criterion 14 ("innovation and excellence") and criterion 3 (critical evaluation) reward visible judgment. The goal is not to rewrite the whole report, but to add a few first-person traces in places where a real decision was made under uncertainty.
- **What to add (targeted, not scattered):**
  - Chapter 2 Synthesis: add 1 sentence about why combining these three streams seemed promising but not obvious — e.g. "I could not find a paper that combined Yin et al.'s NLI method with Oates's four-role schema on computing papers, which made the direction uncertain but worth trying."
  - Chapter 3 Section 2 (Design Justification): the hypothesis set comparison was not planned from the start — it was discovered that verbose labels broke the output. Add 1 sentence: "An early run with verbose hypotheses sent almost all BERT sentences to EvaluationMetric, which forced a comparison of four hypothesis sets before settling on short labels."
  - Chapter 4 Section 1.2 (Section Filtering): the switch from keyword-only sections to all body sections was a real decision after a failure. Add 1 sentence: "An earlier version filtered to sections with headings matching 'experiment' or 'result', but the Training Data section of the Transformer paper has neither keyword, and the WMT dataset was missed."
- **Effort:** Add 3 sentences total in targeted locations. Do not rewrite paragraphs.

### L. Strengthen limitations — connect to claim validity, not just observation

- **Criteria:** 13
- **Why:** Chapter 4 Section 4 lists four noise types honestly. But the current writing stops at observation ("substring match is loose", "gold labels were written by the author"). The next step — which shows human judgment — is to say what each limitation means for the reported result (10/12). Examples:
  - Substring match is a recall check, not a precision check. 10/12 means the correct term is present somewhere in the output sentences, not that the output is a clean methodology profile. The result should be stated as "the system retrieves at least one relevant sentence for 10 of 12 role-paper pairs" — not as 83% precision.
  - Gold labels were written by the author without a second annotator. The AlexNet TechnicalMethod label was changed from "AlexNet" to "convolutional" after running the pipeline. This adjustment should be named explicitly: "the gold label was revised after inspection to match what the paper actually uses."
  - These two points together mean: the 10/12 result is an upper bound on recall, not a precision or F1 claim. State this explicitly in the analysis paragraph.
- **Effort:** Add 2–3 sentences to Chapter 4 Section 3.3 (Analysis) and 1 sentence to Section 3.1 (Method).
- **Location:** Chapter 4 Sections 3.1 and 3.3.

### N. Add a precision-oriented check — evaluate top-3 sentences per role for relevance

- **Criteria:** 9, 13
- **Why:** The current evaluation (substring match on any accepted sentence) is recall-oriented. A marker who notices that MapReduce produced 151 TechnicalMethod sentences can reasonably question whether "10/12 gold labels found" is a meaningful result — it may only show that large output lists eventually contain the expected term. Chapter 4 Section 4 acknowledges this honestly, but the evaluation design itself should respond to it. A precision-oriented check addresses this directly. Once Top-N selection (item F) is implemented, the top-3 sentences per role can be manually inspected: does each returned sentence genuinely describe the paper's own methodology in that role? Even a 5-paper × 4-role × top-3 manual check (60 sentences, ~30 min) gives a more convincing evaluation than substring match on 100+ sentences.
- **What to add:** After implementing F (top-N), add a small table in Chapter 4 Section 3: for each role × paper (or a sample of 3 papers), judge whether the top-1 sentence is genuinely relevant (yes/no/partial). Report as "top-1 precision". This does not replace the existing evaluation — it supplements it and directly answers the recall-only weakness.
- **Dependency:** Item F must be implemented first (top-3 selection).
- **Effort:** ~30 min manual annotation; ~10 lines of code to print top-1 per role; add one table and 2 sentences to Chapter 4 Section 3.
- **Location:** Chapter 4 Section 3.2 (Results table) — add a "top-1 relevant?" column or a separate small table.

### E. Add citations for GROBID and DeBERTa (DONE)

- **Criteria:** 2, 4
- **Why:** GROBID and `cross-encoder/nli-deberta-v3-small` are the two most central technologies in the system. Neither is cited. Academic reports are expected to cite the tools they depend on.
- **Effort:** Find 2 papers, add [5] and [6] to the References, add in-text citations in Chapter 3 Section 6.
- **References to add:**
  - DeBERTa: He et al. (2021). DeBERTa: Decoding-enhanced BERT with Disentangled Attention. ICLR 2021.
  - GROBID: Lopez (2009). GROBID: Combining automatic bibliographic data recognition and term extraction for scholarship publications. ECDL 2009.

### F. Implement Top-N selection (top 3 per role by NLI score)

- **Criteria:** 10, 13
- **Why:** MapReduce produces 151 TechnicalMethod sentences. The output is unusable as a methodology profile. Keeping the top 3 by score makes the output useful and concise. This is listed as a planned improvement in Section 6 — implementing it shows it is done, not just planned.
- **Effort:** ~5 lines of code (sort by score, keep top 3); add one before/after count sentence to Chapter 4.
- **Code location:** End of the classify sentences cell in `proto2/2pipeline.ipynb`.

---

## Priority 4 — Lower impact, low effort

### G. Fix Figure 2 markup in Chapter 2 (DONE)

- **Criteria:** 1
- **Why:** Figure 1 uses proper `<figure>` and `<figcaption>` markup. Figure 2 is a raw code block with no figure number or caption. They should be consistent.
- **Effort:** Wrap Figure 2 in `<figure>` markup, add `<figcaption>Figure 2: ...`.

### H. Add post-submission iteration rows to Table 4 (workplan) (DONE)

- **Criteria:** 7
- **Why:** Table 4 ended at "Final submission" with no detail. The backlog improvements (top-N, usage NLI, term extraction) are described in Chapter 4 Section 5 but not in the workplan. Adding 2 rows makes the workplan appear more planned.
- **Effort:** Add 2 rows to Table 4 in Chapter 3 Section 5.

---

## Not Worth the Effort Before 29 June

- **Usage NLI step (second NLI pass):** Complex, adds latency, risk of new bugs; better to keep as a planned improvement in the report.
- **Expanding evaluation to more than 3 papers:** First fix the Transformer row (B); adding more papers without fixing the inconsistency adds noise.
- **Rewriting the Gantt chart:** The screenshots will render on PDF export; the effort is not worth it.
- **LLM term extraction:** Too large a change; the pipeline does not yet have the infrastructure for an LLM call.
