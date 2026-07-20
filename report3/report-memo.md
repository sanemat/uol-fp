# report-memo.md

This file is a Q&A draft for you to fill in yourself.
Write your answer after each `A:` in your own words.
After you finish, use your answers as material for `report.md` (the draft final
report submission, per `report3-requirement.txt`).

This memo covers the **whole draft report**, not one prototype: it spans the
proto1 → proto2 → proto3 progression. Chapters 2–3 (Literature Review, Design) are
revisions of `report1/report.md`; Chapter 4 (Implementation) follows the same shape
as `report2/prototype-memo.md`'s Features/Algorithms/Code/Visual sections, expanded
to cover implementation to date; Chapter 5 (Evaluation) must extend the preliminary
report's evaluation to the whole project, not just proto3.

**Word budget warning:** the six chapter limits (1000 + 2500 + 2000 + 2000 + 2500 +
1000) sum to 11,000 words, but the strict total max is **9,500**. You will need to
under-run at least one chapter limit — decide where when drafting, don't aim to
max out every section.

---

## Before You Can Answer These

Some answers below need work that is not "keep implementing the pipeline" — it's
data collection, a decision, or a manual check. Do these first, or the Evaluation
and Implementation chapters will be thin:

1. **Run evaluation axis 2** (human plausibility check) over all 6 papers' Stage-2
   outputs — is each `answer` plausibly correct by human judgment? Not yet done
   (`proto3/memo.md` "Implementation status").
2. **Decide and run the axis-3 evidence check** — `proto3/memo.md`'s open question
   leans toward "automatic string search" for the verbatim-quote check, but this
   isn't implemented yet. After running it, manually review any flagged
   quote-mismatch, wrong-section, or prior-work-attribution cases.
3. **Run the Related Work ablation** — exclude Related Work, rerun Stages 0–2,
   recompute Stage 3 metrics, and compare against the main-setting numbers already
   in `proto3/memo.md`. Not run yet.
4. **Clarify "batch processing across `proto3/previouswork/`"** — that directory
   currently holds background/survey PDFs used for the literature review, not
   additional target papers. Decide whether the evaluation set needs more than the
   current 6 papers, or whether this line in `proto3/memo.md` meant something else.
5. **Re-run the pipeline a few more times** to characterize the observed Gemini
   run-to-run variance (2 runs recorded so far: Dataset F1 0.73→0.80→0.91,
   EvaluationMetric F1 0.73→0.67→0.50 with identical code, `temperature=0`,
   `seed=0`). One run is not a stable point estimate — get enough runs to make a
   defensible claim about it in the Evaluation chapter.
6. **Collect screenshots/graphs** for the Implementation and Evaluation chapters'
   required visuals: the Stage 2c JSON output, and the Stage 3 Precision/Recall/F1
   table (word limits exclude figures, so this is free space, not a cost).
7. **Find full bibliographic entries** for any sources named in proto3 material
   but not yet in `report1/report.md`'s reference list — e.g. Dagdelen et al. 2024
   and Polak and Morgan 2024, mentioned in `report2/prototype-memo.md` Q5 without
   full citations.
8. **Re-read any feedback you received on the preliminary report submission** and
   note where it should change the Literature Review or Design chapters — the
   requirement doc explicitly asks you to incorporate it.

---

## 1. Introduction (max 1000 words)

**Q1:** Which project template are you using, and where does the report have to
state it?

> Reused directly: Template 12.1 (NLP module), stated in `report1/report.md` Ch1 §2
> and again in `report2/prototype-memo.md` Q1. The requirement doc says the
> Introduction "must also state which project template you are using" — keep this
> as an explicit sentence, not just implied.

A:

**Q2:** What is the project about, and what motivates it? (Can build on your
proposal — 2-4 sentences.)

> `report1/report.md` Ch1 opening already makes this case: computing researchers
> need to read many papers and identify methodology (technical method, task,
> dataset, evaluation metric) per paper; this is slow and manual; a role-based
> profile supports the first pass of a literature review, not a replacement for
> reading. Decide whether to reuse this near-verbatim or rewrite given the shift
> from proto2 (sentence classification) to proto3 (document-level extraction) —
> the motivation itself hasn't changed, only the approach.

A:

**Q3:** How is this report structured, and what should the reader expect from each
chapter?

> `report1/report.md` Ch1 §4 "Report structure" is the precedent, but it describes
> 4 chapters ending in "Feature Prototype." Report3 has 6 chapters ending in
> "Evaluation" and "Conclusion" — this subsection needs a rewrite, not just a reuse,
> to describe the new Implementation/Evaluation/Conclusion split.

A:

---

## 2. Literature Review (max 2500 words)

**Q4:** What from `report1/report.md` Chapter 2 carries over unchanged?

> The core review (Oates' methodology vocabulary, Pilkington & Pretorius' formal
> ontology, Jain et al./SciREX's four-role schema, Ghosh et al., Färber et al.,
> Yin et al.'s zero-shot NLI) still positions the *problem* — extracting methodology
> from computing papers without an annotated corpus. That framing doesn't change
> just because the extraction method moved from NLI to an LLM.

A:

**Q5:** What needs to change or be added, now that proto3 replaces sentence-level
NLI with document-level LLM extraction?

> `proto3/memo.md` "Why document-level and why full paper" already argues this,
> citing Jain et al./SciREX directly: "a significant amount of information can only
> be gleaned from analyzing the full document." This is a literature-review-level
> claim (document-level IE vs sentence-level classification), not just a design
> note — it belongs here, expanded, not only in Chapter 3. You may also want a new
> subsection on LLM-based structured/schema-guided extraction as a research
> approach (this is where Dagdelen et al. 2024 and Polak and Morgan 2024 — named in
> `report2/prototype-memo.md` Q5 without full citations — would go; see the
> checklist above).

A:

**Q6:** Does anything from `proto2/memo.md`'s findings belong in the literature
review as a negative result to cite against?

> `proto2/memo.md` documented concretely why sentence-level NLI classification
> under-performs: 151 TechnicalMethod sentences for MapReduce, recall-only
> evaluation, no authorship-attribution mechanism (ELMo scored 0.87 as BERT's own
> method). This is your own prior work, and citing it as motivation for the
> document-level approach is legitimate — Chapter 2 of `report1/report.md` already
> gestures at this gap; report3 can make it sharper using the concrete proto2
> numbers.

A:

**Q7:** Does any feedback you received on the preliminary report change this
chapter?

> See checklist item 8. If you have specific feedback comments, list them here with
> how each one is addressed, so the reader (and marker) can see the revision was
> deliberate, not cosmetic.

A:

---

## 3. Design (max 2000 words)

**Q8:** What from `report1/report.md` Chapter 3 (Domain and Users, Design
Justification) still applies?

> Domain (computing research papers: systems, ML, algorithms, HCI) and primary
> users (computing students doing literature reviews) are unchanged by the
> proto2→proto3 shift — the *output* got better, not the target audience. Confirm
> this is still true rather than assuming it.

A:

**Q9:** What is proto3's design justification for schema-guided document-level
extraction, and how does it directly answer proto2's known failures?

> Already drafted in `report2/prototype-memo.md` Q5/Q7/Q8 (Sections 3–4 of that
> memo) — reuse and condense: (a) the core feature is Stage 2, one structured
> evidence-backed answer per role, not a list of 14–160 candidate sentences; (b) the
> authors'-own-work rule in the prompt directly targets proto2's authorship
> problem; (c) the four-role schema is enforced by `response_json_schema`
> (Pydantic-generated JSON Schema), not by prompt wording — a design choice, not an
> accident.

A:

**Q10:** What model was chosen, and what were the alternatives?

> From `proto3/memo.md` "Why document-level and why full paper" — a paper's cleaned
> full text (4,000–20,000 tokens) fits within these context windows without
> chunking:
>
> | Model | Context | Cost |
> |---|---|---|
> | Gemini Flash | 1M tokens | cheap API |
> | Claude Haiku | 200k tokens | cheap API |
> | Llama 3.1 8B Instruct | 128k tokens | free (Colab GPU) |
>
> Selected: Gemini (`gemini-3.5-flash`), chosen for the simplest Colab setup (API
> key via `google.colab.userdata`, no separate account). Note also:
> `gemini-2.5-flash` returned 404 as of July 2026 — Gemini model IDs rotate, worth
> a one-line caveat rather than presenting the model choice as permanent.

A:

**Q11:** Describe the overall pipeline (diagram-worthy — the requirement doc
specifically invites diagrams here).

> ```
> PDF
>   → GROBID (Stage 0: parse sections, same as proto2)
>   → structured TEI document (Abstract + body sections, References/Acknowledgements skipped)
>   → Stage 1: concatenate section texts in reading order, no sentence-level filtering
>   → Stage 2: LLM extraction with a schema-guided prompt
>   → MethodologyProfile JSON (answer + evidence per role)
> ```
> Compare against proto2's pipeline diagram (`report1/report.md` Figure 3) to show
> what changed: no sentence splitting, no per-sentence threshold.

A:

**Q12:** How does the evaluation approach itself need to be (re)designed here,
versus how results are reported in Chapter 5?

> `report1/report.md` Ch3 §6 ("Test and Evaluation") described the *plan* for
> proto2's evaluation (substring gold-label match, ≥10/12 success threshold). This
> chapter's revision should describe the *plan* for the current, extended
> evaluation: the 3-axis design from `proto3/memo.md` ("Evaluation (3 axes)") —
> gold-label match as classification P/R/F1, human precision check, evidence check
> (verbatim/support/section/authorship). Keep the actual *results* for Chapter 5 —
> this section is about what was planned and why it's appropriate, not what was
> found.

A:

**Q13:** What does the updated work plan look like from here to the final report?

> `report1/report.md` Table 5 is the precedent format (Period / Main task /
> Output). Update it: preliminary report and proto2 are "Done"; proto3 Stages 0–2
> and evaluation axis 1 are "Done"; axes 2–3, ablation, and extended-paper batch
> processing are "In progress" or "Post-submission" depending on your timeline
> before the final report deadline.

A:

---

## 4. Implementation (max 2000 words)

Follow the shape of `report2/prototype-memo.md` §§3–6 (Features Implemented →
Algorithms/Techniques → Code Explanation → Visual Representation) — that memo's
answers are largely already written for proto3 and can be condensed into this
chapter rather than rewritten from scratch. Expand to briefly place proto3 in the
proto1 → proto2 → proto3 progression, since this chapter must cover "implementation
to date," not only the current prototype.

**Q14:** In one paragraph, what has been implemented across all three prototype
iterations, and what does proto3 do concretely?

> proto1: AI-drafted reference only, not used directly. proto2: sentence-level
> zero-shot NLI classification (`proto2/memo.md`). proto3: schema-guided
> document-level extraction with a long-context LLM — one answer + evidence
> (section, quote) per role. Concrete output shape: reuse the real
> `proto3/baseline/transformer.json` example already quoted in
> `report2/prototype-memo.md` Q4/Q12.

A:

**Q15:** What are the major algorithms/techniques used, stage by stage?

> Condense `report2/prototype-memo.md` Q6–Q8: GROBID parsing (Stage 0, shared with
> proto2), section concatenation (Stage 1), schema-guided LLM extraction (Stage 2)
> where the four-role shape is enforced by `response_json_schema`
> (`MethodologyProfile.model_json_schema()`) rather than by prompt wording, and the
> null-correlation between `answer`/`evidence` is enforced by a Pydantic
> `model_validator`, not a prompt instruction.

A:

**Q16:** Explain the most important parts of the code.

> Condense `report2/prototype-memo.md` Q9–Q11: the extraction prompt (only states
> what the schema can't express — authorship rule, verbatim-quote rule); the
> Gemini call (`response_json_schema`, `temperature=0`, `seed=0`, direct
> `model_validate_json` parsing, no manual JSON extraction) and the evidence-shape
> bug found during real testing (now structurally prevented by the schema); code
> quality evidence — `pyright --strict`, `ruff`, tests in `proto3/tests/` for
> `scoring.py` and the `model_validator`, `proto3/sync_generated.py` keeping
> notebook cells in sync with `proto3/src/uol_fp/`. Word budget is tight here (2000
> words total for the whole chapter) — pick the 2-3 most technically interesting
> details rather than everything in the precedent memo.

A:

**Q17:** What visual representation(s) of results will you include?

> From the checklist above: a screenshot of the Stage 2c cell output (raw Gemini
> response / parsed JSON), and/or a before/after comparison of proto2's
> sentence-count output vs proto3's answer+evidence output for the same paper (the
> comparison already drafted in `report2/prototype-memo.md` Q12 — 14/0/0/160
> sentences vs one answer per role). Take the actual screenshots before writing
> this section (checklist item 6).

A:

---

## 5. Evaluation (max 2500 words)

Must extend the preliminary report's evaluation to the **whole project**, not just
the current prototype — the requirement doc says this explicitly.

**Q18:** What is the evaluation method, and why is it appropriate?

> Condense `report2/prototype-memo.md` Q14: 3 axes (gold-label match as
> classification P/R/F1, human precision check, evidence check), same 6 papers and
> gold labels as proto2. State explicitly why P/R/F1 is more appropriate here than
> proto2's recall-only substring check: a present-but-wrong answer now costs both
> precision and recall instead of being free.

A:

**Q19:** What are the axis-1 results (gold-label match)?

> From `proto3/memo.md` "Run-to-run variance observed": all 6 papers, comparing
> baseline vs two pipeline runs.
>
> | Role | Baseline F1 | Pipeline run 1 | Pipeline run 2 |
> |---|---|---|---|
> | TechnicalMethod | 0.83 | 0.83 | 0.83 |
> | Task | 0.33 | 0.33 | 0.33 |
> | Dataset | 0.73 | 0.80 | 0.91 |
> | EvaluationMetric | 0.73 | 0.67 | 0.50 |
> | Overall | 0.65 | 0.65 | 0.64 |
>
> TechnicalMethod/Task are stable across runs; Dataset/EvaluationMetric are not,
> despite `temperature=0`/`seed=0`. Report this as one observed run for the
> unstable roles, not a fixed score — and note the stability/instability asymmetry
> across roles as a finding in itself, not just noise to ignore.

A:

**Q20:** What is the status of axes 2 and 3, and the Related Work ablation?

> Be honest, per the checklist: not implemented/run as of this memo. If you
> complete checklist items 1–3 before writing this chapter, report the actual
> results here. If not, state clearly what was planned (Chapter 3 §Q12) versus what
> was actually carried out, and why — this is exactly the kind of gap the
> requirement doc's "we don't expect completed work at this stage" note allows for,
> as long as it's stated honestly rather than glossed over.

A:

**Q21:** What is the critical evaluation — what has this project achieved, and what
still needs improvement?

> Achievements: moved from proto2's recall-only substring check (10/12, then 18/24
> across 6 papers) to proto3's real classification P/R/F1 per role; every answer is
> now evidence-backed and checkable against the source text, addressing proto2's
> authorship-attribution failure. Weaknesses: Task F1 is low (0.33) and needs
> analysis of why; Dataset/EvaluationMetric F1 is unstable run-to-run; axes 2–3
> aren't validated yet, so "the answer is correct" currently rests only on
> substring match, not human or evidence verification; only 6 papers, all
> ML-benchmark-shaped (proto2 already showed systems papers like MapReduce and
> Google Search fit the 4-role schema poorly — check whether this still holds for
> proto3 if you test on them).

A:

**Q22:** How does this evaluation cover the "whole project," not only the current
prototype?

> Consider explicitly narrating the proto2 → proto3 comparison as part of the
> evaluation, not just the design rationale: proto2's known failure modes (output
> volume, authorship attribution, recall-only scoring) each map onto a specific
> proto3 evaluation axis that tests whether it was actually fixed. That mapping
> itself is evidence the evaluation covers the whole project's trajectory.

A:

---

## 6. Conclusion (max 1000 words)

**Q23:** Short summary — what is this project, and what has been built?

> One paragraph: the goal (automatically extract research methodology from
> computing papers using LLMs, per `CLAUDE.md`), the progression (proto1 reference
> → proto2 sentence-NLI → proto3 document-level schema-guided extraction), and
> where it currently stands (Stages 0–2 implemented, axis-1 evaluation done, axes
> 2–3 and ablation pending).

A:

**Q24:** What further work remains?

> From the checklist: axes 2–3, the Related Work ablation, more evaluation runs to
> characterize variance, and possibly testing on non-ML-benchmark papers (systems,
> HCI) to see whether the 4-role schema and document-level extraction generalize
> better than proto2's sentence classification did.

A:

**Q25:** (Optional) Any broader themes worth raising?

> E.g. the tension between structured-output guarantees (syntactic correctness,
> schema conformance) and semantic correctness (is the answer actually right) —
> `proto3/memo.md` makes this distinction explicitly and it's a defensible
> higher-level point about LLM-based extraction generally, not just this project.

A:

---

## Reference

Reuse `report1/report.md`'s References and Dataset Papers lists directly as the
starting point — don't retype them here. Add:
- Any new citations used for the document-level-IE argument (Jain et al./SciREX is
  already cited; add full entries for Dagdelen et al. 2024 and Polak and Morgan
  2024 once found — see checklist item 7).
- Update Appendix-style material (work plan roadmap, extended per-paper evaluation
  tables) following the pattern of `report1/report.md` Appendix A/B, once the
  Related Work ablation and axes 2–3 are run.
