# report-memo.md

This file is a Q&A draft for you to fill in yourself.
Write your answer after each `A:` in your own words.
After you finish, use your answers as material for `report.md` (the final report
submission, per `report4-requirement.txt`).

This memo covers the **whole final report**, revising `report3/report.md` (the
completed draft, 6122/9500 words, all 6 chapters) into the final submission. It
mirrors report3's chapter structure and question numbers (Q1–Q25) exactly, so each
question below points back to the report3 answer as its starting draft rather than
restating it — the work here is revision and expansion, not a rewrite from scratch.

**Word budget:** report4's per-chapter limits (1000 + 2500 + 2000 + 2500 + 2500 +
1000 = 10,500) match the strict total max exactly this time — unlike report3, there
is no forced under-run. Implementation's cap rose from 2000 to 2500 words, and the
brief now asks for "the entire implementation" and Evaluation to "critique the
project as a whole," not just extend it — both signal real expansion is expected,
not padding. report3 used only 6122 words total, so there is roughly 4,400 words of
genuine room across the report, weighted toward Chapters 4 and 5.

**New format requirements (report4-requirement.txt, not in report3):**
- Every chapter title must state its own word count, e.g. `1. Introduction (783/1000
  words)` — report3's headings already show a word count; just add the `/max` part.
- The Introduction must state "the project number in the way it has been listed in
  the template," not just name the template — stricter than report3's wording. See
  the checklist below.
- The report must include a link to a **publicly viewable code repository**, which
  must stay public until results are received.
- A **3–5 minute video** is a separate required submission alongside the report: your
  own spoken voice explaining and demonstrating the working project, no AI-generated
  voice, not sped up.

---

## Before You Can Answer These

**1. Report3 feedback — blocking, not yet available.** report4-requirement.txt asks
you to incorporate "the feedback you have obtained from your submissions" (plural —
report1's is already folded in via Chapter 2's Q7 table; report3's is a separate,
later round). No report3 feedback file exists in this repo yet. Once you receive it,
add a feedback-response table the same way Q7 already does for report1 — wherever
the marker's comments land (Literature Review, Design, Implementation, or
Evaluation), not necessarily all in one chapter. Don't guess at report3 feedback
content in the meantime; leave a placeholder and revisit.

**2. Re-verify report1/feedback.txt is still honoured — a check, not new work.**
report3's Q7 table already mapped every report1 rubric comment to a fix: citation
numbering restarts at `[1]`, no mixing of author names with numbered citations,
academic register with no "I test" narration, a pipeline diagram showing failure
paths, a workplan table with duration/dependency/risk/contingency columns, and
Precision/Recall/F1 evaluation with confidence intervals. As you expand chapters for
report4, especially Literature Review and Implementation, re-check each of these
still holds — a new citation added out of order, or a slip back into casual "I test
X and see Y" narration while drafting new material, would undo a point already won.

**3. Confirm the project-number format against the actual module template
document.** report3 states "Template 12.1" consistently (`report1/report.md`,
`design.md`, `design-memo.md`). report4 asks for the project number "in the way it
has been listed in the template" — check this phrasing against the original module
template-listing document (not present in this repo) before assuming "Template
12.1" alone satisfies it; the module handbook may list a distinct project number.

**4. Public code repository link.** Not required in report3, required in report4.
Confirm the repository is public (or make it public) and decide where the link goes
in the report — Chapter 1 (Introduction) is the natural place, alongside the
template statement.

**5. Video — script, recording, and voiceover, all still to do.**
`report1/demo-script.md` plus `report1/video/*.mp4` is the precedent pattern from an
earlier deliverable — reuse the *approach* (a written script before recording), not
the content, since the project has moved from proto1's prototype to proto3's
pipeline. Requirements to hold to while planning it: 3–5 minutes, your own spoken
explanation (no AI-generated voice), not sped up, must show the project actually
working. See "Video & Repository" at the end of this memo for a shape to plan
against.

**6. Decided: promote the decomposed-extraction pilot (Variant B), consolidation
(Variant C) as a conditional stretch.** Of report3's cut/deferred list (Related Work
ablation, decomposed-extraction pilot, multi-valued-schema implementation,
non-ML-benchmark case study, corpus growth, formal inter-annotator study), Variant B
is committed as this round's technical centerpiece — it targets Task, the project's
weakest role (F1 0.33, stable across all 5 report3 runs), directly, and reuses
existing code (`RoleExtraction`, `score_role`/`score_profile`) with low implementation
risk. Variant C runs only if B's results justify it. Everything else on the list
stays deferred to genuine further work — see "3-Week Workplan (Variant B/C)" below
for the full schedule and decision gate.

**7. Word-count-in-title formatting.** Low-effort, easy to forget: once each
chapter's final word count is known, add it to the heading exactly as
`N. Chapter Name (used/max words)`.

---

## 3-Week Workplan (Variant B/C)

report3 feedback (the marker's score on the draft) is confirmed **not** to arrive
within this 3-week window, so no time below is reserved for responding to it — only
the report1/feedback.txt re-verification (checklist item 2) is ongoing work, not a
new fix. This schedule is the source material for Chapter 3's Q14 (Work Plan) `A:`
answer, the same relationship report3's own checklist had to its Q13.

**Why Variant B, not a new proto4:** `proto3/memo.md` "Architecture reconsideration"
(lines 413–467) already designed decomposed extraction in full — four independent
role-specific Gemini calls instead of one joint call — citing Khot et al. (2022) on
decomposed prompting. It was cut from report3 purely for time, not because it was a
bad idea. It directly targets Task, the weakest role, is cheap to implement
(`RoleExtraction` and `score_role`/`score_profile` need no changes — see
`proto3/src/uol_fp/models.py` and `scoring.py`), and is a better "technically
challenging"/"originality" lever than starting a new prototype line from scratch,
which would also have to redo GROBID parsing, section extraction, and evaluation
under report4's tighter remaining time plus its new requirements (repo link, video).

### Iteration 1 (Week 1, ~Aug 24–30): Implement and score Variant B

- Write 4 role-specific prompts, one per role, each stating that role's specific
  failure pattern per `proto3/memo.md` lines 435–443 (TechnicalMethod: primary vs
  component vs prior work; Task: what problem is actually solved; Dataset: actually
  used, not just mentioned; EvaluationMetric: actually used to report results). Keep
  the existing authors'-own-work and verbatim-quote rules in each prompt.
- Add a new pipeline stage in `proto3/3pipeline.ipynb` (new cells, following the
  existing Stage 2 pattern, IDs kept stable) making 4 independent Gemini calls per
  paper with `response_json_schema=RoleExtraction.model_json_schema()`,
  `temperature=0`, `seed=0`. Assemble the 4 results into the `{role: answer}` shape
  `score_profile` already expects. Run `make sync-generated` after any
  `src/uol_fp` change.
- Run once across all 6 papers (scope capped per `proto3/memo.md` line 458 — one run
  each, no repeated-run variance study for B). Log to a new `proto3/results_b/`,
  mirroring `proto3/results/run{N}/*.json`'s shape.
- Score with the existing `score_role`/`score_profile` — produce a per-role F1 table,
  A (joint baseline) vs B. Key question: does Task's F1 move?
- In parallel, no dependency on B's results: checklist items 3–5 and 7 (template
  number check, repo public/link, video script draft, word-count-in-title format),
  and the report1/feedback.txt re-verification pass as Chapters 1–3 get copied from
  report3 into `report4/report.md`.
- `make lint` and `make test` in `proto3/` stay clean (ruff + pytest) after the new
  stage is added.

### Iteration 2 (Week 2, ~Aug 31–Sep 6): Decision gate, then Chapter 4/5 writing

- **Decision gate on B's results:**
  - If B improves Task (or other roles) without regressing the rest: proceed to
    **Variant C** — a 5th call per paper (`proto3/memo.md` lines 430–433) passing B's
    4 outputs plus their evidence, asking only whether they are mutually consistent
    with the evidence, correcting contradictions/role confusion, introducing no new
    values. Needs one new Pydantic model (the only new schema work in this plan).
    Score C the same way as A/B; test the hypothesis already stated in
    `proto3/memo.md` line 450: per-role accuracy B or C > A, cross-role consistency
    C > A > B.
  - If B does not help Task: stop here and report it as a finding, not a gap —
    report3 already treated "not run, deferred" and "the metric is blunt" as
    legitimate, honestly reported results. Reallocate the freed time to the next item
    on `proto3/memo.md`'s cut list — one non-ML-benchmark paper (e.g. HCI) as a
    qualitative case study — rather than the multi-valued-schema stretch, which
    `proto3/memo.md` lines 544–548 already argues has weak ROI (Dataset and
    EvaluationMetric are already the second-best roles at F1 0.73; Task, untouched by
    that change, is the actual weak point).
  - **Result (2026-08-28):** Variant B run for all 6 papers, one run each, scored
    against `results/run1` (Variant A, also one run) via
    `proto3/aggregate_variant_b.py`:

    | Role | A F1 | B F1 | ΔF1 |
    |---|---|---|---|
    | TechnicalMethod | 0.83 | 0.83 | +0.00 |
    | Task | 0.33 | 0.33 | +0.00 |
    | Dataset | 0.91 | 1.00 | +0.09 |
    | EvaluationMetric | 0.67 | 0.67 | +0.00 |

    Task's F1 did not move — the role-specific failure-pattern prompt made no
    measurable difference on the one role it targeted. Dataset improved (+0.09),
    an incidental effect, not the hypothesis under test (its prompt was not
    written against a known Dataset failure). Per the gate above: **stop here,
    do not proceed to Variant C.** This is the "B does not help Task" branch —
    report it as a finding, not a gap.
- Manual-review spot-check only the changed slots (e.g. Task across all 6 papers
  under B, and under C if run) against `proto3/manual_review.md`'s existing
  four-column format — not a full 24-slot redo.
- Writing: Q10 (Design) moves from "considered, not implemented" to "implemented,
  results in Chapter 5"; Q16/Q17 (Implementation) get real new material using the
  raised 2500-word cap genuinely; Q20–23 (Evaluation) get the new A vs B (vs C) table
  and an updated proto2→proto3→(B/C) synthesis. Continue the report1/feedback.txt
  re-verification pass as these chapters are rewritten.
- Start recording video footage once the new stage's output is stable — a live run
  producing the decomposed (and consolidated, if applicable) output, to script
  against in Iteration 3.

### Iteration 3 (Week 3, ~Sep 7–13): Freeze, assemble, polish, submit

- **Freeze all experiments this week** — no new technical work past the start of
  Iteration 3, mirroring report3's own cut-list discipline.
- Assemble `report4/report.md` from `report3/report.md` as the base, applying every
  answer in this memo. Adapt `report3/count_words.py` into `report4/count_words.py`
  (same exclusion rules, pointed at `report4/report.md`) and check every chapter
  against report4's caps (1000 / 2500 / 2000 / 2500 / 2500 / 1000, strict total
  10,500) — Chapters 4 and 5 are where the new word budget should actually land.
- Final reference-list pass: renumber citations from `[1]` in order of first
  appearance, no author-name/number mixing — the report1-feedback item most likely to
  regress after heavy rewriting, so check it last, not just early.
- Finish and record the video narration in your own voice (no AI-generated voice, not
  sped up), 3–5 minutes, showing the Variant B/C pipeline actually running.
- Confirm the repository is still public and its link is correctly embedded in
  Chapter 1.
- Final proofread for academic register — no "I test X and see Y" narration slipping
  back into newly written material.
- Reserve at least 1–2 unallocated buffer days at the end. With report3 feedback
  confirmed not landing in this window, this slack goes entirely to polish rather
  than being split with a feedback-response task.

---

## 1. Introduction (max 1000 words)

**Q1:** Which project template are you using, and where does the report have to
state it?

> report3 base: `report3/report-memo.md` Q1. Reuse the content, but check item 3
> above first — report4 asks specifically for "the project number... in the way it
> has been listed in the template," which is stricter than report3's "must also
> state which project template you are using." Confirm the exact wording/number
> before finalizing this answer.

A:

**Q2:** What is the project about, and what motivates it?

> report3 base: `report3/report-memo.md` Q2. The motivation hasn't changed since
> report3 (this was already true moving proto2→proto3); confirm it's still true
> moving into the final report, and note if anything from report3/report1 feedback
> changes how this should be framed.

A:

**Q3:** How is this report structured, and what should the reader expect from each
chapter?

> report3 base: `report3/report-memo.md` Q3. The chapter list and order are
> unchanged from report3 (same 6 chapters); only the per-chapter emphasis
> description may need small updates if Chapter 4/5's scope genuinely expands (item
> 6 above).

A:

**Q4 (new for report4):** Where does the report state the public code repository
link, and is the repository actually public right now?

> Not part of report3 — see checklist item 4. Confirm current visibility (`gh repo
> view --json visibility` or the GitHub UI) before writing this, don't assume.

A:

---

## 2. Literature Review (max 2500 words)

**Q5:** What from `report1/report.md` Chapter 2 carries over unchanged?

> report3 base: `report3/report-memo.md` Q4 (lines 186–212). Unless new sources are
> added for report4, this should carry over from report3's version essentially as-is
> — re-verify against checklist item 2 (citation numbering/order) if anything else
> in the chapter shifts.

A:

**Q6:** What changed or was added for document-level LLM extraction (proto3), and
does it still need anything further for report4?

> report3 base: `report3/report-memo.md` Q5 (lines 214–239). Check whether any newly
> promoted report3-deferred item (checklist item 6 — e.g. the decomposed-extraction
> pilot) pulls in further literature (Khot et al. is already cited for this in
> Chapter 3/Q9; confirm whether it needs a literature-review-level mention too if
> variant B is actually run this round).

A:

**Q7:** Does anything from `proto2/memo.md`'s findings belong here as a negative
result?

> report3 base: `report3/report-memo.md` Q6 (lines 241–271). Unchanged unless new
> evidence surfaces.

A:

**Q8:** Does feedback you received change this chapter?

> report3 base: `report3/report-memo.md` Q7 (lines 273–292) — the full report1
> feedback-response table already lives here. For report4: (a) re-verify each row
> still holds (checklist item 2), and (b) once report3 feedback arrives (checklist
> item 1), add a second table in the same format for whatever it flags in this
> chapter specifically.

A:

---

## 3. Design (max 2000 words)

**Q9:** What from Chapter 3 (Domain and Users, Design Justification) still applies?

> report3 base: `report3/report-memo.md` Q8 (lines 298–329), including the user-need
> / system-requirement / evaluation table. Unchanged unless the user base or domain
> genuinely shifted — confirm rather than assume.

A:

**Q10:** What is the design justification for schema-guided document-level
extraction, and how does it answer proto2's known failures?

> report3 base: `report3/report-memo.md` Q9 (lines 331–430) — includes the two
> forward-looking design considerations (joint vs decomposed extraction;
> single-valued vs multi-valued roles) that report3 explicitly left as "write-up
> only, not implemented." Per checklist item 6, Variant B is committed for report4 —
> this section needs to move from *considered choice* to *implemented design* for the
> joint-vs-decomposed question specifically (multi-valued roles likely stays
> write-up-only, see the workplan's Iteration 2 decision gate) — and the corresponding
> Q20–23 results updated to match, not left saying "deferred." See "3-Week Workplan
> (Variant B/C)" above for the schedule this depends on.

A:

**Q11:** What model was chosen, and what were the alternatives?

> report3 base: `report3/report-memo.md` Q10 (lines 432–466). Re-check the model-ID
> caveat (`gemini-2.5-flash` 404'd; IDs rotate) is still accurate at time of writing
> report4 — Gemini model availability may have changed again.

A:

**Q12:** Describe the overall pipeline.

> report3 base: `report3/report-memo.md` Q11 (lines 468–530), including the
> failure-path diagram added in response to report1 feedback (checklist item 2 — a
> proper diagram showing data flow, component interaction, failure handling, and the
> user-facing output). Reuse the diagram; update only if the pipeline itself changed
> (e.g. a promoted decomposed-extraction pilot adds a stage).

A:

**Q13:** How was the evaluation approach itself designed, versus how results are
reported in Chapter 5?

> report3 base: `report3/report-memo.md` Q12 (lines 532–600). If checklist item 6
> promotes new experiments, this section should state the *plan* for them (why
> run, what's compared, what's out of scope) — keep actual *results* in Chapter 5,
> same separation report3 already used.

A:

**Q14:** What does the updated work plan look like from here to the final
submission?

> report3 base: `report3/report-memo.md` Q13 (lines 602–637), including the
> duration/dependency/risk/contingency table added for report1 feedback (checklist
> item 2). This table needs a full new pass for report4: report3's remaining rows
> ("Report3 feedback pass," "Report3 final assembly," "Final Report write-up") are
> now either done or need replacing with the actual remaining tasks — report3
> feedback response, any promoted experiments (item 6), video production (item 5),
> and final word-budget trim.

A:

---

## 4. Implementation (max 2500 words)

report4-requirement.txt asks this chapter to cover "the entire implementation,"
"greatly expanded" — stronger language than report3's "to date." With the cap raised
from 2000 to 2500 words and report3 only using 735 of its 2000, there is real room
(and an explicit instruction) to go deeper here, not just carry report3's chapter
forward unchanged.

**Q15:** In one paragraph, what has been implemented across all three prototype
iterations, and what does proto3 do concretely?

> report3 base: `report3/report-memo.md` Q14 (lines 649–669). Still accurate as a
> one-paragraph summary; the expansion for report4 belongs in Q16/Q17 below, not
> here.

A:

**Q16:** What are the major algorithms/techniques used, stage by stage?

> report3 base: `report3/report-memo.md` Q15 (lines 671–693). report3 condensed
> `report2/prototype-memo.md` Q6–Q8 heavily due to the 2000-word chapter cap. With
> report4's cap at 2500 and "entire implementation" as the instruction, revisit
> what was condensed and consider restoring more of the original stage-by-stage
> detail (GROBID parsing specifics, section-concatenation logic, schema-enforcement
> mechanics) rather than reusing the condensed version unchanged. Also add the
> Variant B decomposed-extraction stage (and Variant C's consolidation call, if run)
> as a new stage in this walkthrough — see "3-Week Workplan (Variant B/C)," Iteration
> 1–2, above.

A:

**Q17:** Explain the most important parts of the code.

> report3 base: `report3/report-memo.md` Q16 (lines 695–741) — already covers four
> technically interesting details (prompt design, `response_json_schema` +
> `temperature=0`/`seed=0`, the `response_schema` vs `response_json_schema`
> distinction, code-quality tooling). report3 explicitly picked "the 2-3 most
> interesting details" because of the tight 2000-word budget (line 707); with 2500
> words and "entire implementation" as the brief, this is the section most likely to
> need genuinely new material — consider what was left out of report3 for space
> (e.g. more on `scoring.py`'s evaluation logic, the `model_validator` mechanics, or
> details of any newly promoted experiment from checklist item 6). The Variant B
> role-specific prompts (and Variant C's consolidation prompt, if run) are a strong
> candidate for one of this section's "most interesting details" slots — see the
> workplan above.

A:

**Q18:** What visual representation(s) of results will you include?

> report3 base: `report3/report-memo.md` Q17 (lines 743–766). Add any new
> screenshots/figures needed for whatever gets promoted under checklist item 6
> (e.g. a decomposed-pilot output comparison), and take them before drafting this
> section, same as report3's approach.

A:

---

## 5. Evaluation (max 2500 words)

report4-requirement.txt asks this chapter to "give a critique of the project as a
whole — highlighting successes, failures, limitations, and possible extensions,"
sharper language than report3's "extend to the whole project." report3's own
addendum (its memo, lines 775–810) already restructured this chapter around whether
the evidence-backed output is trustworthy, not just accurate — that framing carries
forward directly into report4's "critique... successes, failures, limitations."

**Q19:** What is the evaluation method, and why is it appropriate?

> report3 base: `report3/report-memo.md` Q18 (lines 812–854). Add one sentence on the
> A-vs-B(-vs-C) evaluation axis per checklist item 6 — see "3-Week Workplan
> (Variant B/C)" above for what's committed.

A:

**Q20:** What are the gold-label-match results, and how are micro/macro averaging
and sample size handled?

> report3 base: `report3/report-memo.md` Q19 (lines 856–941), including the Wilson
> CI reasoning (Precision/Recall only, not F1) and the explicit decision to keep
> n=6. The n=6 corpus stays as-is for report4 (checklist item 6 keeps corpus growth
> deferred) — report3's own reasoning (~30–40 papers needed to meaningfully tighten
> the interval) still holds. This section itself should be about Variant A alone,
> same as report3; the A-vs-B(-vs-C) comparison belongs in Q23 instead.

A:

**Q21:** What did the variance study find, and what does it actually prove?

> report3 base: `report3/report-memo.md` Q20 (lines 943–1071) — the 5-run F1 table,
> the pooled-CI reasoning and caveat, and the MapReduce/Pagerank NotebookLM
> cross-check cases. Unchanged unless a new run (e.g. from a promoted decomposed
> pilot) adds comparable data.

A:

**Q22:** What did the manual review pass find, and what is the status of the
Related Work ablation?

> report3 base: `report3/report-memo.md` Q21 (lines 1073–1170) — all 24 slots
> already scored in `proto3/manual_review.md`, with the six-slots-pass-quote-but-fail
> evidence/authorship breakdown. If the Related Work ablation gets promoted under
> checklist item 6, update its status here from "cut, deferred" to actual results;
> otherwise report3's "not required to prove the core claims" framing still applies
> and can carry forward.

A:

**Q23:** What is the critical evaluation — what has this project achieved, and what
still needs improvement, across the whole project?

> report3 base: `report3/report-memo.md` Q22 (lines 1172–1243), including the
> proto2→proto3 "fixed / not fixed" synthesis table. This is the section report4's
> "critique... successes, failures, limitations, and possible extensions" language
> maps onto most directly — check the table and prose already answer "possible
> extensions" explicitly (report3's Q24/Chapter 6 "Further Work" covers this; make
> sure Chapter 5 itself, not only Chapter 6, names limitations plainly, since the
> brief asks this chapter specifically to do so). If checklist item 6 promotes new
> experiments, add their results to this synthesis rather than leaving them only in
> Q21/Q22 in isolation.

A:

---

## 6. Conclusion (max 1000 words)

**Q24:** Short summary — what is this project, and what has been built?

> report3 base: `report3/report-memo.md` Q23 (lines 1280–1299), already restructured
> around the three questions (did it work / what did the project teach us / did it
> meet the user need) per report3's own addendum. Update the "as of this draft"
> status line for whatever changed under checklist item 6, and reflect that this is
> now the final submission, not a draft.

A:

**Q25:** What further work remains?

> report3 base: `report3/report-memo.md` Q24 (lines 1301–1369). Remove the
> decomposed-extraction item, since Variant B is committed for report4 (checklist
> item 6, "3-Week Workplan" above) rather than deferred; keep Variant C here if
> Iteration 2's decision gate skips it. Everything else (corpus growth, formal
> inter-annotator study, multi-model comparison, multi-valued schema, remaining
> non-ML-benchmark testing) likely still belongs here as genuine further work beyond
> even the final report.

A:

**Q26 (optional):** Any broader themes worth raising?

> report3 base: `report3/report-memo.md` Q25 (lines 1371–1387) — the
> structured-output-guarantees-vs-semantic-correctness theme. Still applicable;
> extend only if a newly promoted experiment (checklist item 6) adds a genuinely new
> broader point, rather than restating the same theme with different numbers.

A:

---

## Video & Repository

Not part of report3; both are report4-only submission requirements (see checklist
items 4–5). Plan these deliberately rather than leaving them to the end:

**Video — checklist:**
- 3–5 minutes total.
- Your own spoken voice throughout, explaining and justifying approach choices, not
  just narrating what's on screen — no AI-generated voice.
- Not sped up.
- Must show the project actually working (a real pipeline run, not only slides) —
  videos that don't show a working project score lower per the brief.
- Draft a short script first (`report1/demo-script.md` is the precedent format from
  an earlier deliverable — same idea, new content: proto3's pipeline, not the
  earlier prototype).

**Repository — checklist:**
- Confirm current visibility and make public if needed.
- Link must stay live until results are received, not just at submission time.
- Add the link into the report itself (Chapter 1 — see Q4 above).

## Reference

Reuse `report3/report.md`'s References and Dataset Papers lists directly as the
starting point. Add any new citations pulled in by a promoted checklist-item-6
experiment (e.g. if the decomposed-extraction pilot is actually run and needs
further citation beyond Khot et al., already in report3's Chapter 3).
