# Improvable — Score Improvement Priorities

Criteria source: `preliminary-instruction.md` (14 criteria).
Target: `report.md`. Implementation: `proto2/2pipeline.ipynb`.

---

## Current State by Criterion

| # | Criterion | Status | Notes |
|---|---|---|---|
| 1 | Clear, well-formatted, coherent | ✓ | Opening sentence fixed (D done); Figure 1 and 2 now use `<figure>/<figcaption>` (G done) |
| 2 | Knowledge of area | ✓ | 11 references; GROBID [7] and DeBERTa [11] now cited |
| 3 | Critically evaluates prior work | ✓ | Jain et al. limitations well explained |
| 4 | Proper citation and referencing | ✓ | 11 references; all central tools cited |
| 5 | Design clear and high quality | ✓ | Chapter 3 is thorough |
| 6 | Concept justified | ✓ | Good |
| 7 | Workplan in enough detail | ⚠ | Table 3 is sparse; Gantt chart is screenshots |
| 8 | Workplan feasible | ✓ | OK |
| 9 | Evaluation strategy appropriate | ⚠ | Core: 3 papers, substring match; extended 6-paper results in Appendix B |
| 10 | Feature prototype high quality | ⚠ | Large output (MapReduce 151 sentences) unaddressed |
| 11 | Technically challenging | ✓ | Section 7 documents the challenges well |
| 12 | Demonstration effective and impactful | ✓ | Video recorded |
| 13 | Evaluate prototype and show improvements | ⚠ | GPU batch processing implemented; more improvements still planned |
| 14 | Innovation and excellence | ✓ | Hypothesis comparison is a genuine contribution |

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

### H. Add post-submission iteration rows to Table 3 (workplan)

- **Criteria:** 7
- **Why:** Table 3 ends at "Final submission" with no detail. The backlog improvements (top-N, usage NLI, term extraction) are described in Chapter 4 Section 6 but not in the workplan. Adding 2 rows makes the workplan appear more planned.
- **Effort:** Add 2 rows to Table 3 in Chapter 3 Section 7.

---

## Not Worth the Effort Before 29 June

- **Usage NLI step (second NLI pass):** Complex, adds latency, risk of new bugs; better to keep as a planned improvement in the report.
- **Expanding evaluation to more than 3 papers:** First fix the Transformer row (B); adding more papers without fixing the inconsistency adds noise.
- **Rewriting the Gantt chart:** The screenshots will render on PDF export; the effort is not worth it.
- **LLM term extraction:** Too large a change; the pipeline does not yet have the infrastructure for an LLM call.
