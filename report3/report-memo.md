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

**Don't serialize the whole report behind the checklist below.** Introduction,
Literature Review, Design, and Implementation (Q1–Q17) don't depend on unfinished
experiment results — draft them now, in parallel with the checklist, roughly one
chapter per day. Only parts of the Evaluation chapter (Q19–Q22) genuinely have to
wait on data.

---

## Before You Can Answer These

Some answers below need work that is not "keep implementing the pipeline" — it's
data collection, a decision, or a manual check.

Reprioritized 2026-07-20 per direct review: the proto2→proto3 synthesis moved from
P1 to P0 (it's writing, not an experiment, and report3 requires the Evaluation
chapter to cover "the whole project," not just proto3 — see `proto3/memo.md`
"Priority for what to add next" for the full reasoning). Wilson CI applies to
Precision and Recall only, not F1 (a Wilson interval is for a proportion; F1 is a
harmonic mean, not a proportion — F1 stays a point estimate). Effort for the
items below only (not the writing): ~4-4.5 days for P0, ~1-1.5 days for P1 — treat
"P0 + P1" as the real completion line for experiment work.

**Update 2026-07-22:** P0 items 1 and 2 (run-logging + 5 runs, aggregation + CI)
are done — see below. Remaining P0 work is items 3-5 (~2-2.5 days), plus P1 item 6
(~1-1.5 days).

**P0 — mandatory, all 5:**
1. ~~**Log a real variance study to disk (0.5-1 day).**~~ **Done (2026-07-22).** 5
   full runs logged to `proto3/results/run{1..5}/*.json`, scored and aggregated by
   the new `proto3/aggregate_runs.py` → `proto3/results/aggregate.json`. Per-role
   F1 mean/min/max/range is in `proto3/memo.md` "Run-logging + variance study" —
   use directly for Q20.
2. ~~**Compute confidence intervals (0.5 day).**~~ **Done (2026-07-22).** Wilson
   interval on **Precision and Recall only**, computed on tp/fp/fn pooled across
   the 5 runs (n=30 trials/role), for all 4 roles — see `proto3/memo.md` same
   section. This supersedes the old n=6 baseline-only CI (TechnicalMethod recall
   [0.44, 0.97], Task recall [0.10, 0.70] — these overlapped) with a tighter
   pooled estimate where TechnicalMethod [0.66, 0.93] and Task [0.19, 0.51] no
   longer overlap — report both figures and the caveat that the 30 pooled trials
   are 5 repeats of the same 6 papers, not 30 independent papers. **F1 stays a
   point estimate — no Wilson CI on F1** (it's a harmonic mean, not a proportion;
   a proper F1 interval would need paper-level bootstrap, not worth it given the
   deadline).
3. **Run one consolidated manual review pass (1-1.5 days)** over all 6 papers × 4
   roles (not three separate passes) — plausibly correct? evidence supports
   answer? authors' own work, not prior work? **Does the quote actually appear in
   the source text?** (No separate script for this — a verbatim match only
   proves the LLM followed the "copy verbatim" instruction, not that the
   evidence is good evidence, e.g. a real Related Work sentence could still be
   wrongly cited as the paper's own method — so it's cheaper and just as
   informative to check while already reading the source for support/authorship,
   rather than building standalone tooling for 24 slots.)
4. **Write the proto2 → proto3 "fixed / not fixed" synthesis** (near-free, folds
   into item 5's 0.5 day) — map proto2's three named failure modes (output
   volume, authorship attribution, recall-only scoring) onto what items 1-3
   actually found. Draft the skeleton now, before 1-3 even finish; fill in real
   numbers once they do.
5. **Collect screenshots/graphs (0.5 day, combined with item 4)** for the
   Implementation and Evaluation chapters' required visuals: the Stage 2c JSON
   output, the Stage 3 P/R/F1 table (word limits exclude figures — free space,
   not a cost).

**P1 — one item only, tightly scoped, do not let it re-expand (1-1.5 days):**
6. **Decomposed-extraction pilot — variant B vs A, nothing more.** 4 independent
   role-specific calls instead of 1 joint call, scored with existing `scoring.py`
   unchanged. Scope limits, explicit: one run each (or B vs the existing frozen
   baseline), per-role F1 comparison only — **no consolidation pass, no
   repeated-run variance study for B.** Either would balloon this back into a
   multi-day project.

**Cut first, in this order, if time runs short:**
1. Related Work ablation — doesn't improve Task (the weakest role), so it's first
   to drop. "Not run, deferred to further work" is a legitimate answer.
2. One unscored non-ML-benchmark paper (e.g. HCI) as a qualitative case study.
3. A diagnostic on whether relaxed/stemmed matching would change the Task
   conclusion.
4. A diagnostic hand-recomputing what EvaluationMetric's P/R/F1 would be for
   AlexNet/ResNet if scored as multi-valued.

**Correction, not a to-do:** the earlier note about "batch processing across
`proto3/previouswork/`" was a misunderstanding — that directory holds
background/survey PDFs for the literature review, not additional target papers.
Don't act on it; it's retracted in `proto3/memo.md`.

**Also still needed, regardless of the above:**
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
>
> **Also worth discussing as a forward design consideration (not yet fully
> implemented):** whether extraction should stay joint (current: 1 call → 4
> roles) or move to decomposed extraction (4 independent role-specific calls,
> optionally + a consolidation pass). See `proto3/memo.md` "Architecture
> reconsideration" for the full argument: Khot et al. 2022 (decomposed prompting
> can beat one joint few-shot prompt by letting each subtask's prompt be
> optimized separately) vs. Jain et al./SciREX's document-level argument (joint
> handling can exploit cross-role relationships in one sentence, e.g.
> "Transformer"/"WMT"/"BLEU" together). Frame this as a considered choice, not an
> unexamined default — state clearly that the decomposed-only pilot (no
> consolidation) is a P1 stretch item for this report (results, if run, belong in
> Q22, not here), and the consolidation variant plus full comparison are deferred
> to further work (Q24).
>
> **A second forward design consideration (also not yet implemented):** whether
> every role should stay single-valued, or whether some should allow multiple
> answers. See `proto3/memo.md` "Multi-valued roles" for the evidence-based
> case: Dataset and EvaluationMetric show real multi-value evidence in this
> project's own data (e.g. AlexNet/ResNet's *current* baseline answers already
> squash "top-1 and top-5 error rates" into one string), while Task and
> TechnicalMethod don't (Task's one candidate case was already refined away and
> is better explained as a substring-matching artifact, and TechnicalMethod is
> deliberately singular by design). Discuss the schema shape (per-item evidence,
> not one shared quote for a list — ties back to (c) above) and the choice of a
> ranked "primary first" list over a numeric confidence/threshold field (this
> project's own measured LLM non-determinism argues against trusting a second,
> uncalibrated confidence axis). State clearly this is write-up only for
> report3, not implemented — full implementation is deferred to Q24.

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
> chapter's revision should describe the *plan* from `proto3/memo.md` "Evaluation
> plan" (reprioritized 2026-07-20, deadline-focused): gold-label match as
> classification, with Wilson confidence intervals on P/R (F1 as a point estimate
> only, no CI), a logged variance study, and a consolidated manual review
> pass covering plausibility/support/authorship/quote-in-source in one read, plus
> the proto2→proto3 synthesis (all P0, mandatory); the decomposed-extraction pilot
> (P1, tightly scoped: variant A vs B only, no consolidation); and the Related
> Work ablation (first on the cut list — demoted because it doesn't address
> Task, the weakest role). Keep the actual *results* for Chapter 5 — this section
> is about what was planned and why it's
> appropriate (including why micro/macro averaging, the n=6 sample size, and
> dropping a standalone evidence-verbatim script in favour of folding it into the
> manual review were each decided the way they were), not what was found.
>
> **Addendum (2026-07-22):** now that the 5-run variance study exists, the plan
> section can also justify the pooled-CI design choice made while implementing it
> — pool tp/fp/fn across the 5 runs (n=30 trials/role) rather than compute a
> separate CI per run, because the point was a tighter estimate from real repeated
> measurement, not 5 independent per-run snapshots; and state the trade-off up
> front (non-independent trials, interval narrower than a true 30-paper sample)
> rather than let Chapter 5 discover it. This is still about the *design decision*,
> not the resulting numbers — the numbers themselves belong in Q20.

A:

**Q13:** What does the updated work plan look like from here to the final report?

> `report1/report.md` Table 5 is the precedent format (Period / Main task /
> Output). Update it: preliminary report and proto2 are "Done"; proto3 Stages 0–2
> and the gold-label-match evaluation are "Done"; the 5 P0 items (variance study,
> confidence intervals on P/R, manual review, proto2→proto3 synthesis, figures)
> are "In progress, mandatory"; the P1 decomposed-extraction pilot (tightly
> scoped) is "In progress, one item only"; the Related Work ablation is "Cut
> first if time runs short."

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

> From `proto3/memo.md` "Evaluation plan" (rethought from scratch, not the old
> 3-axis brainstorm): gold-label match as classification P/R/F1 with confidence
> intervals (done), a logged ≥5-run variance study (P0), a consolidated manual
> review pass (P0, one read covering plausibility + evidence-support + authorship
> + quote-in-source in a single pass instead of building separate tooling), and —
> only if time allows — the Related Work ablation (P1). State explicitly why P/R/F1
> is more appropriate than proto2's recall-only substring check: a
> present-but-wrong answer now costs both precision and recall instead of being
> free. Also state why the evaluation was restructured this way: the earlier
> "3 axes" idea bundled a free mechanical check with expensive human-judgment
> checks under one label with no priority; on reflection, even the "free"
> mechanical check (an automated evidence-verbatim script) wasn't worth building
> separately, since it only proves the LLM followed a copy-verbatim instruction,
> not that the evidence is good evidence — and the human reviewer needs to read
> the source anyway to judge support/authorship, so checking the quote there
> costs nothing extra.

A:

**Q19:** What are the gold-label-match results, and how are micro/macro
averaging and sample size handled?

> From `proto3/memo.md` "Evaluation plan":
>
> | Role | P | R | F1 |
> |---|---|---|---|
> | TechnicalMethod | 0.83 | 0.83 | 0.83 |
> | Task | 0.33 | 0.33 | 0.33 |
> | Dataset | 0.80 | 0.67 | 0.73 |
> | EvaluationMetric | 0.80 | 0.67 | 0.73 |
> | Micro | 0.68 | 0.62 | 0.65 |
> | Macro | — | — | 0.655 |
>
> Report macro as the headline "Overall" (the 4 roles are fixed, equally mandatory
> schema fields, not a frequency distribution — a user needs all four), but show
> both and note they're close here (0.65 vs 0.655) only because every role happens
> to have n=6 in this dataset — a coincidence, not a property of the method. On
> sample size: state Wilson 95% CIs on **Precision and Recall** directly rather
> than a vague "small sample" caveat — TechnicalMethod recall 0.83 → CI [0.44,
> 0.97]; Task recall 0.33 → CI [0.10, 0.70]. These substantially overlap: don't
> claim TechnicalMethod is reliably "solved" while Task is reliably "broken."
> **Don't put a Wilson CI on F1** — it's a harmonic mean of P and R, not a
> proportion, so a Wilson interval on it directly isn't statistically meaningful;
> report F1 as a point estimate, with a one-line note that a proper F1 interval
> would need paper-level bootstrap resampling, not worth it at n=6 given the
> deadline. Also explain the decision not to grow the corpus: tightening the P/R
> intervals meaningfully would need ~30-40 gold-labeled papers per role, not the
> 6-10 reachable in 3 weeks with no second annotator — poor ROI, so n=6 stays and
> is reported honestly instead.
>
> **Update 2026-07-22:** the n=6 CIs above are for the single frozen baseline
> sample. A second, tighter CI now exists from the 5 real pipeline runs (pooled
> across runs, n=30 trials/role) — keep that one for Q20, not here, so this
> section stays about the baseline gold-label-match result specifically. Don't
> duplicate the pooled numbers in both places; cross-reference instead.

A:

**Q20:** What did the variance study find, and what does it actually prove?

> **Done (2026-07-22)** — 5 full runs, logged to `proto3/results/run{1..5}/*.json`
> and aggregated by `proto3/aggregate_runs.py` (see `proto3/memo.md` "Run-logging +
> variance study" for the full write-up; numbers also in
> `proto3/results/aggregate.json`). Use the real numbers below, not a placeholder.
>
> **Per-role F1 across 5 runs:**
>
> | Role | F1 mean | F1 min | F1 max | F1 range |
> |---|---|---|---|---|
> | TechnicalMethod | 0.83 | 0.83 | 0.83 | 0.00 |
> | Task | 0.33 | 0.33 | 0.33 | 0.00 |
> | Dataset | 0.91 | 0.91 | 0.91 | 0.00 |
> | EvaluationMetric | 0.57 | 0.33 | 0.67 | 0.33 |
>
> Three of four roles were perfectly stable across 5 real repetitions — stronger
> evidence than the earlier n=2 anecdote, which showed both Dataset and
> EvaluationMetric moving. At n=5, Dataset turned out stable and only
> EvaluationMetric is not (0.33–0.67 across runs, unchanged code/`temperature=0`/
> `seed=0`), narrowing the non-determinism finding rather than just repeating it.
>
> **Pooled Wilson 95% CI on P/R, n=30 trials/role** (tp/fp/fn summed across the 5
> runs):
>
> | Role | P | P 95% CI | R | R 95% CI |
> |---|---|---|---|---|
> | TechnicalMethod | 0.83 | [0.66, 0.93] | 0.83 | [0.66, 0.93] |
> | Task | 0.33 | [0.19, 0.51] | 0.33 | [0.19, 0.51] |
> | Dataset | 1.00 | [0.87, 1.00] | 0.83 | [0.66, 0.93] |
> | EvaluationMetric | 0.57 | [0.39, 0.73] | 0.57 | [0.39, 0.73] |
>
> State the caveat plainly: these 30 trials/role are 5 repeats of the same 6
> papers, not 30 independent papers, so the interval is narrower than a true
> 30-independent-paper sample would give — don't present it as if it were.
> Even so, it's worth reporting as a finding, not just a caveat: TechnicalMethod
> [0.66, 0.93] and Task [0.19, 0.51] no longer overlap, unlike the n=6 baseline
> CIs in Q19 ([0.44, 0.97] vs [0.10, 0.70], which did overlap). Five real
> repetitions give more grounds to say TechnicalMethod reliably outperforms Task
> than the single n=6 snapshot alone supported — while still stopping short of
> calling either "solved" or "broken" outright.
>
> Also worth including regardless of results: MapReduce's Task slot (gold
> `"distributed"`, system answer `"automatic parallelization and distribution of
> large-scale computations"`) fails the substring-match rule despite being
> arguably correct — Task's low F1 (0.33) is partly a measurement-instrument
> artifact, not purely a model failure. This separates "the pipeline is wrong"
> from "the metric is blunt," which is exactly the kind of critical-analysis point
> the grading criteria reward.
>
> **A second instance of the same "metric is blunt" pattern, if the optional P2
> diagnostic was run** (see `proto3/memo.md` "Multi-valued roles"): AlexNet's and
> ResNet's baseline EvaluationMetric answers already say "top-1 and top-5 error
> rates" verbatim — hand-recompute what P/R/F1 would be for these two papers if
> scored as multi-valued instead of against a single gold string, and report the
> difference. If not run, skip this — it's optional, not required.

A:

**Q21:** What did the manual review pass find (including the quote-in-source
check), and what is the status of the Related Work ablation?

> Fill in once the P0 manual review is done. This pass covers plausibility,
> evidence-support, authorship, *and* whether the quote actually appears in the
> source — one read, not separate tooling (see Q18: a standalone verbatim-check
> script was considered and dropped, since it would only prove instruction-
> following, not evidence quality, and the reviewer is reading the source anyway).
> Be precise in the write-up: a quote existing in the source is necessary but not
> sufficient for good evidence — note any case where a real quote was still the
> *wrong* evidence (e.g. attributed to the wrong section or to prior work) as a
> distinct finding from "the quote was fabricated." Note the single-annotator bias
> in this pass applies equally to the gold labels themselves — say so once, don't
> present the manual review as more objective. For the ablation: state its status
> honestly — it's first on the cut list for report3 (demoted from P1 because it
> doesn't address Task, the project's weakest role, the way the decomposed-
> extraction pilot does), not required to prove the core claims, so "not run,
> deferred to further work" is a legitimate, planned answer, not a gap to
> apologize for.

A:

**Q22:** What is the critical evaluation — what has this project achieved, and
what still needs improvement? How does this cover the "whole project," not only
the current prototype?

> Achievements: moved from proto2's recall-only substring check (10/12, then
> 18/24 across 6 papers) to proto3's classification P/R/F1 with confidence
> intervals, now backed by 5 real repeated runs, not a single snapshot (Q20); every
> answer is evidence-backed and (once Q21's manual review is run) verifiably
> checkable against the source text, addressing proto2's authorship-attribution
> failure concretely rather than by design claim alone. Weaknesses: Task F1 is low
> (0.33, stable across all 5 runs, and partly a metric artifact per Q20); only 6
> papers, all ML-benchmark-shaped (proto2 already showed systems papers like
> MapReduce and PageRank fit the 4-role schema worse — note this as an open
> generalization question, not resolved). Write the explicit proto2 → proto3
> "fixed / not fixed" synthesis here: map each of proto2's three named failure
> modes (output volume, authorship attribution, recall-only scoring) onto what
> Q19–Q21 actually found, not just onto the design rationale in Chapter 3 — that
> mapping is what makes this "whole project" evaluation rather than a
> proto3-only one.
>
> **Worth citing from Q20 here specifically:** the pooled 5-run CIs for
> TechnicalMethod [0.66, 0.93] and Task [0.19, 0.51] no longer overlap, unlike the
> single-baseline n=6 CIs in Q19. That's a genuine strengthening of the
> "TechnicalMethod works, Task doesn't" claim over the preliminary report — cite it
> as evidence the evaluation itself matured across the project, not only the
> pipeline.
>
> **If the decomposed-extraction pilot (variant B, see Q9 and `proto3/memo.md`
> "Architecture reconsideration") was run:** report per-role F1, A (joint) vs B
> (decomposed), as the most direct attempt so far at fixing Task's known
> weakness — this is a stronger technical-challenge/critical-evaluation signal
> than the Related Work ablation alone. If not run, say so and point to Q24.

A:

---

## 6. Conclusion (max 1000 words)

**Q23:** Short summary — what is this project, and what has been built?

> One paragraph: the goal (automatically extract research methodology from
> computing papers using LLMs, per `CLAUDE.md`), the progression (proto1 reference
> → proto2 sentence-NLI → proto3 document-level schema-guided extraction), and
> where it currently stands (Stages 0–2 implemented, gold-label-match evaluation
> done with confidence intervals, the evidence-verifiability check/variance
> study/manual review in progress, the Related Work ablation optional/deferred).

A:

**Q24:** What further work remains?

> From `proto3/memo.md`'s explicit out-of-scope list: growing the gold-label
> corpus (shown to be poor ROI at any scale reachable in 3 weeks — say why, using
> the Wilson CI math from Q19, rather than just "no time"), a formal
> inter-annotator-agreement study (no second annotator exists), a full
> multi-model comparison, and the Related Work ablation if it wasn't reached.
> Also worth raising: testing on non-ML-benchmark papers (systems, HCI) to see
> whether the 4-role schema and document-level extraction generalize better than
> proto2's sentence classification did — proto2 already showed systems papers fit
> this schema worse.
>
> **Also explicitly deferred here (see `proto3/memo.md` "Architecture
> reconsideration"):** the consolidation pass (variant C — a 5th call checking
> variant B's 4 role-specific outputs for mutual consistency against their
> evidence) and the full 3-way A/B/C comparison (joint vs decomposed vs
> decomposed+consolidation). State the predicted-outcome hypothesis (per-role
> accuracy: B or C > A; cross-role consistency: C > A > B) as the concrete next
> experiment for after report3, not as a finding — no paper directly shows this
> 4-role methodology-extraction task favors decomposition, so this is a genuine
> open question this project is positioned to test.
>
> **Also deferred here (see `proto3/memo.md` "Multi-valued roles"):** the full
> multi-valued schema implementation for Dataset/EvaluationMetric — new
> `MultiRoleExtraction` type (per-item evidence, ranked list capped at 3 items),
> gold-label re-annotation for 4 cells (bert/transformer Dataset, alexnet/resnet
> EvaluationMetric), a parallel `score_role_multi` scoring function, and
> rerunning + rescoring all 6 papers. State as a concrete next step with the
> evidence already gathered (Q9), not as something still to be investigated from
> scratch.

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
  tables) following the pattern of `report1/report.md` Appendix A/B, once the P0
  evaluation items (variance study, evidence check, confidence intervals, manual
  review) and, if reached, the Related Work ablation are run.
