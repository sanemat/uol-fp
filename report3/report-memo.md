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

A: I use Template 12.1 from the Natural Language Processing (NLP) module:
identifying research methodologies used in computing research papers. The
Introduction states this directly, as the requirement doc asks.

**Q2:** What is the project about, and what motivates it? (Can build on your
proposal — 2-4 sentences.)

> `report1/report.md` Ch1 opening already makes this case: computing researchers
> need to read many papers and identify methodology (technical method, task,
> dataset, evaluation metric) per paper; this is slow and manual; a role-based
> profile supports the first pass of a literature review, not a replacement for
> reading. Decide whether to reuse this near-verbatim or rewrite given the shift
> from proto2 (sentence classification) to proto3 (document-level extraction) —
> the motivation itself hasn't changed, only the approach.

A: When computing researchers do a literature review, they often need to
read many papers and find each paper's method, task, dataset, and
evaluation metric. Reading many papers this way is slow and manual. I treat
these four items as a methodology profile that a reader can extract
automatically, to support the first pass of a literature review, not to
replace reading the paper. This motivation has not changed between proto2
and proto3 — only the extraction approach changed, from sentence-level
zero-shot classification to document-level extraction with a long-context
large language model (LLM).

**Q3:** How is this report structured, and what should the reader expect from each
chapter?

> `report1/report.md` Ch1 §4 "Report structure" is the precedent, but it describes
> 4 chapters ending in "Feature Prototype." Report3 has 6 chapters ending in
> "Evaluation" and "Conclusion" — this subsection needs a rewrite, not just a reuse,
> to describe the new Implementation/Evaluation/Conclusion split.

A: Chapter 2 reviews related work on how research methodology is defined
and structured, how methodology-related information can be extracted from
papers, and how zero-shot classification assigns labels without labeled
training data, then extends this with work on LLM-based structured
extraction. Chapter 3 describes the system design: the four-role schema and
its justification, the pipeline architecture, the model choice, and the
evaluation plan. Chapter 4 covers implementation across all three
prototype iterations, with most detail on proto3's document-level
extraction. Chapter 5 evaluates the whole project so far, not only proto3:
gold-label matching with confidence intervals, a logged variance study, and
a manual review of the extracted evidence. Chapter 6 concludes with a short
summary and further work.

---

## 2. Literature Review (max 2500 words)

**Q4:** What from `report1/report.md` Chapter 2 carries over unchanged?

> The core review (Oates' methodology vocabulary, Pilkington & Pretorius' formal
> ontology, Jain et al./SciREX's four-role schema, Ghosh et al., Färber et al.,
> Yin et al.'s zero-shot NLI) still positions the *problem* — extracting methodology
> from computing papers without an annotated corpus. That framing doesn't change
> just because the extraction method moved from NLI to an LLM.

A: The core review carries over unchanged. Oates [9] and Pilkington &
Pretorius [10] give the vocabulary and formal structure for research
methodology. Jain et al. [5] (SciREX) motivate the four-role schema
(Dataset, Metric, Task, Method) directly — their 438 annotated papers were
drawn from a pool of 1,170 ML-conference articles on Papers with Code, which
quantifies how narrow the ML-benchmark scope of that corpus actually is.
Ghosh et al. [2, 3] and Färber et al. [1] show narrower, supervised
extraction approaches that this project's zero-shot and later LLM-based
approaches respond to. Yin et al. [11] motivate classification without
labeled training data. Even with the short-label hypothesis set that worked
best in proto2, classification errors remained concrete: on the Transformer
paper, "Our model achieves 28.4 BLEU on the WMT 2014 English-to-German
translation task" was classified as Task rather than EvaluationMetric.
Together, this literature positions the problem this project addresses —
extracting methodology from computing papers without an annotated corpus for
this specific four-role schema — and that framing does not change just
because the extraction method moved from sentence-level natural language
inference (NLI) to a document-level large language model (LLM): the
underlying gap is the same for both approaches.

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

A: I expand the review with the document-level information extraction (IE)
argument: Jain et al. [5] argue that "a significant amount of information
can only be gleaned from analyzing the full document." My own data supports
this claim directly — Dataset and EvaluationMetric typically appear only in
the Experiment section of a paper, not the Abstract, so an extraction
method limited to a few sentences would miss them. I add a subsection on
LLM-based structured, schema-guided extraction as a research approach,
citing Dagdelen et al. (2024), who extract structured information from
scientific text with large language models, and Polak and Morgan (2024),
who extract materials data from research papers using conversational
language models and prompt engineering. Structured extraction with LLMs is
not new; I apply it to this project's specific four-role methodology
schema.

**Q6:** Does anything from `proto2/memo.md`'s findings belong in the literature
review as a negative result to cite against?

> `proto2/memo.md` documented concretely why sentence-level NLI classification
> under-performs: 151 TechnicalMethod sentences for MapReduce, recall-only
> evaluation, no authorship-attribution mechanism (ELMo scored 0.87 as BERT's own
> method). This is your own prior work, and citing it as motivation for the
> document-level approach is legitimate — Chapter 2 of `report1/report.md` already
> gestures at this gap; report3 can make it sharper using the concrete proto2
> numbers.

A: proto2's own findings are a legitimate negative result to cite. Sentence-
level NLI classification produced too many candidate sentences to be
usable — 151 TechnicalMethod sentences for the MapReduce paper alone — and
the recall-only substring evaluation (18/24 across six papers) only checked
whether a gold term appeared somewhere in the output, not whether the
output was correct. With 100+ accepted sentences in some roles, a substring
match is nearly certain to succeed somewhere in the list, which inflates the
apparent recall without saying anything about precision. Targeted ablations
show the same output-volume problem concretely: excluding Related Work by
heading cut BERT's TechnicalMethod count from 67 to 62 sentences, and
excluding the whole Introduction cut it further to 54 — but that also
removed sentences that correctly described BERT's own method, so exclusion
traded recall for precision rather than solving the underlying problem.
proto2 also had no mechanism to separate the authors'
own method from a method cited from prior work: a sentence describing ELMo
in BERT's Introduction scored 0.87 as TechnicalMethod, even though ELMo is
prior work, not BERT's own method. Chapter 2 of `report1/report.md` already
gestures at this gap in general terms; I now cite it with these concrete
proto2 numbers as sharper motivation for document-level extraction with an
explicit authorship rule.

**Q7:** Does any feedback you received on the preliminary report change this
chapter?

> See checklist item 8. If you have specific feedback comments, list them here with
> how each one is addressed, so the reader (and marker) can see the revision was
> deliberate, not cosmetic.

A: **FILL IT LATER** — find the actual marker feedback on the preliminary
report (email, Moodle, or elsewhere; not in this repo) and list each
comment with how it's addressed.

---

## 3. Design (max 2000 words)

**Q8:** What from `report1/report.md` Chapter 3 (Domain and Users, Design
Justification) still applies?

> Domain (computing research papers: systems, ML, algorithms, HCI) and primary
> users (computing students doing literature reviews) are unchanged by the
> proto2→proto3 shift — the *output* got better, not the target audience. Confirm
> this is still true rather than assuming it.

A: The domain and users are unchanged. The domain is computing research
papers, mainly systems, machine learning (ML), algorithms, and human-
computer interaction (HCI). The primary users are computing students doing
literature reviews; secondary users are early-stage researchers or
supervisors who want a quick overview of a paper. proto3 changed the output
quality — one checkable answer per role instead of a list of candidate
sentences — not the target domain or audience.

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
>
> **Independent corroboration:** an informal cross-check with Google NotebookLM
> (each paper re-extracted independently, `notebooks/*.md`) found the same
> multi-valued pattern for BERT, ResNet, and Transformer's Dataset/EvaluationMetric
> without being told the schema was single-valued — see `proto3/memo.md`
> "NotebookLM cross-check" for the full comparison. Worth citing as a second,
> independent source alongside this project's own data, with the caveat that it
> is one informal AI-based pass, not a formal inter-annotator study.

A: The core design justification carries over from `report2/prototype-
memo.md`. The core feature is Stage 2: one structured, evidence-backed
answer per role, not a list of 14-160 candidate sentences. The authors'-
own-work rule in the prompt directly targets proto2's authorship-
attribution failure (the ELMo/BERT case from Q6). The four-role JSON shape
is enforced by `response_json_schema`, generated from the Pydantic models,
not by prompt wording — a design choice, not an accident, since it removes
an entire class of parsing and output-shape bugs (see Q16).

Two further design considerations are not yet implemented; I present them
as considered choices for further work, not as defaults I overlooked.
First, whether extraction should stay joint (the current design: one call
returns all four roles) or move to decomposed extraction (four independent
role-specific calls, optionally followed by a consolidation pass). Khot et
al. (2022) show that decomposing a complex task into independently-
optimizable subtasks can beat a single joint few-shot prompt on several
reasoning tasks, while Jain et al./SciREX's document-level argument favours
joint handling, since it can exploit cross-role relationships appearing in
one sentence (e.g. "Transformer"/"WMT"/"BLEU" together). A decomposed-only
pilot (variant B vs the joint baseline, one run each, no consolidation) is
a stretch item for this report; results, if run, belong in Chapter 5
(Q22), and the consolidation variant plus a full comparison are deferred to
further work (Q24).

Second, whether every role should stay single-valued or some should allow
multiple answers. My own data gives an evidence-based case for Dataset and
EvaluationMetric only: the current baseline answers for AlexNet and ResNet
already squash two error rates into one string ("top-1 and top-5 error
rates"), which is real multi-value evidence that Task and TechnicalMethod
do not share (Task's one candidate case is better explained as a
substring-matching artifact, and TechnicalMethod is deliberately singular
by design). BERT's own gold EvaluationMetric label already lists both
"accuracy" and "F1" as acceptable, since the paper genuinely reports both —
a second, independent piece of multi-value evidence from this project's own
earlier work, not just the informal NotebookLM pass below. A multi-valued
design would keep per-item evidence rather than one shared quote for a
whole list, and use a ranked "primary first" list rather than a numeric
confidence field, since this project's own measured non-determinism argues
against trusting a second, uncalibrated confidence axis. An informal
cross-check with Google NotebookLM, run independently on each paper without
being told the schema was single-valued, found the same multi-valued
pattern for BERT, ResNet, and Transformer's Dataset and EvaluationMetric
fields: for BERT, the single-valued baseline names "SQuAD v1.1" as Dataset,
while NotebookLM listed BooksCorpus and Wikipedia for pre-training plus
GLUE, SQuAD v1.1/v2.0, SWAG, and CoNLL-2003 for evaluation, all present in
the same source text; for Transformer, NotebookLM added WMT 2014
English-French and the WSJ Penn Treebank alongside the baseline's WMT 2014
English-German; ResNet's Dataset and EvaluationMetric were similarly broader
(adding CIFAR-10, PASCAL VOC, COCO, and mAP) — a second, independent data
point, though only one informal AI-based pass, not a formal inter-annotator
study. This discussion is write-up only for report3; full implementation is
deferred to Q24.

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

A: A paper's cleaned full text is typically 4,000-20,000 tokens, which fits
within the context window of several modern long-context LLMs without
chunking:

| Model | Context | Cost |
|---|---|---|
| Gemini Flash | 1M tokens | cheap API |
| Claude Haiku | 200k tokens | cheap API |
| Llama 3.1 8B Instruct | 128k tokens | free (Colab GPU) |

I selected Gemini (`gemini-3.5-flash`, via the `google-genai` software
development kit), mainly because it is the simplest to set up from Google
Colab: the API key comes from Colab's built-in secret manager
(`google.colab.userdata`), with no separate account needed beyond the
Google account already used for Colab. One caveat worth stating rather than
hiding: `gemini-2.5-flash` returned a 404 error as of July 2026, since
Google had already retired it for new users. Gemini model IDs rotate, so I
present this as the current working choice, not a permanent one.

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

A: The pipeline runs in five stages:

```
PDF
  → GROBID (Stage 0: parse sections, same as proto2)
  → structured TEI document (Abstract + body sections, References/Acknowledgements skipped)
  → Stage 1: concatenate section texts in reading order, no sentence-level filtering
  → Stage 2: LLM extraction with a schema-guided prompt
  → MethodologyProfile JSON (answer + evidence per role)
```
*Figure: proto3 extraction pipeline, five stages from PDF to structured JSON.*

Compared with proto2's pipeline (`report1/report.md` Figure 3: PDF → GROBID
→ TEI XML → section filtering → sentence splitting and cleaning →
zero-shot NLI role classification → MethodologyProfile JSON), there are two
differences: there is no sentence splitting, and there is no per-sentence
acceptance threshold. The LLM sees the (mostly) whole document and returns
one decision per role directly, instead of a list of candidate sentences
each scored independently.

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

A: This section describes the evaluation *plan*, not results — results
belong in Chapter 5. `report1/report.md` Chapter 3 §6 described proto2's
plan: a substring gold-label match with a 10-out-of-12 success threshold.
For proto3 I redesigned this, because a present-but-wrong answer should
cost something. I score gold-label match as a classification problem (true
positive, false positive, false negative), report Precision, Recall, and F1
per role, and add Wilson 95% confidence intervals on Precision and Recall
only — F1 is a harmonic mean, not a proportion, so a Wilson interval on it
directly is not statistically meaningful; a point-estimate F1 is the honest
choice at this sample size. I report both micro and macro averages,
headlining macro, because the four roles are fixed, equally mandatory
schema fields, not a frequency distribution. I kept the sample at six
papers rather than growing it: tightening the confidence intervals
meaningfully would need roughly 30-40 gold-labeled papers per role, not the
6-10 reachable in three weeks with no second annotator, so growing the
corpus was a poor use of the remaining time. I planned a logged variance
study (repeat the pipeline several times rather than trust one run) and a
single consolidated manual review pass covering plausibility, evidence
support, authorship, and whether the quote appears in the source text,
instead of three separate passes or a standalone verbatim-check script — a
script would only prove the LLM followed the copy-verbatim instruction, not
that the evidence itself is good evidence, and a human reviewer already has
to read the source to judge support and authorship, so checking the quote
there costs nothing extra. The decomposed-extraction pilot is a P1 item,
scoped tightly to variant A vs B with no consolidation pass; the Related
Work ablation is first on the cut list, since it does not address Task, the
weakest role.

Once the five-run variance study existed, I also had to decide how to
compute its confidence interval. I pooled the true/false positive/negative
counts across the five runs (30 trials per role) rather than computing five
separate per-run intervals, because the goal was a tighter estimate from
real repeated measurement, not five independent snapshots. I state the
trade-off directly: these 30 trials are five repeats of the same six
papers, not 30 independent papers, so the interval is narrower than a true
30-paper sample would give. This is a design decision about how the
evaluation was built; the resulting numbers belong in Q20.

**Q13:** What does the updated work plan look like from here to the final report?

> `report1/report.md` Table 5 is the precedent format (Period / Main task /
> Output). Update it: preliminary report and proto2 are "Done"; proto3 Stages 0–2
> and the gold-label-match evaluation are "Done"; the 5 P0 items (variance study,
> confidence intervals on P/R, manual review, proto2→proto3 synthesis, figures)
> are "In progress, mandatory"; the P1 decomposed-extraction pilot (tightly
> scoped) is "In progress, one item only"; the Related Work ablation is "Cut
> first if time runs short."

A:

| Period | Main task | Output | Status |
|---|---|---|---|
| Before 29 June | Literature review, design, proto2 (sentence-level NLI) | Preliminary Report | Done |
| July | proto3 Stages 0-2 (document-level extraction); gold-label-match evaluation with Wilson confidence intervals on Precision/Recall | Baseline P/R/F1 table, 5-run variance study, pooled confidence intervals | Done |
| July-August (P0) | Consolidated manual review pass; proto2→proto3 fixed/not-fixed synthesis; figures for Implementation/Evaluation chapters | Draft Report 3 material | In progress, mandatory |
| August (P1) | Decomposed-extraction pilot, variant A vs B only | Per-role F1 comparison | In progress, one item only |
| August | Related Work ablation | — | Cut first if time runs short |
| August (final stage) | Write Final Report, incorporating whichever P0/P1 items complete in time | Final submission | Not started |

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

A: proto2 was my own sentence-level zero-shot natural language inference
(NLI) classifier: it classified every sentence in a paper into one of the
four roles, producing
a list of candidate sentences per role rather than one answer. proto3
reframes the task as document-level extraction: given a computing paper,
it extracts one answer per role — TechnicalMethod, Task, Dataset,
EvaluationMetric — each with a section heading and a verbatim quote as
evidence, using a schema-guided prompt to a long-context LLM. On "Attention
Is All You Need" [D6], for example: TechnicalMethod = "Transformer", Task =
"machine translation", Dataset = "WMT 2014 English-German", EvaluationMetric
= "BLEU", each backed by its own quote and section.

**Q15:** What are the major algorithms/techniques used, stage by stage?

> Condense `report2/prototype-memo.md` Q6–Q8: GROBID parsing (Stage 0, shared with
> proto2), section concatenation (Stage 1), schema-guided LLM extraction (Stage 2)
> where the four-role shape is enforced by `response_json_schema`
> (`MethodologyProfile.model_json_schema()`) rather than by prompt wording, and the
> null-correlation between `answer`/`evidence` is enforced by a Pydantic
> `model_validator`, not a prompt instruction.

A: The pipeline has five stages. Stage 0 reuses proto2's GROBID-based
parsing to turn a PDF into TEI XML, then keeps the Abstract and body
sections while skipping References and Acknowledgements by heading match.
Stage 1 concatenates the remaining section texts in reading order, with no
sentence splitting and no per-sentence threshold — a direct response to
proto2's output-volume problem. Stage 2 sends the full document to the LLM
with a schema-guided prompt: the four-role JSON shape is enforced by
`response_json_schema`, generated from the `MethodologyProfile` Pydantic
model (`MethodologyProfile.model_json_schema()`), not by describing the
shape in the prompt text; the null-correlation between `answer` and
`evidence` — a role is either both null or both present — is enforced by a
Pydantic `model_validator`, not a prompt instruction. Dataset and
EvaluationMetric often occur only in the Experiment section, not the
Abstract or Method, so I keep the full document rather than an excerpt.

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

A: Four details are the most technically interesting, given the tight word
budget. First, the prompt states only what the JSON schema itself cannot
express: use the authors' own method, not a method cited from prior work;
return null when a role is absent; copy evidence quotes verbatim.
Everything about the output *shape* — the nested `{section, quote}`
evidence object, the four required role fields — lives on the Pydantic
models instead of the prompt text. Second, the Gemini call uses
`response_json_schema` together with `temperature=0` and `seed=0`, and
parses the reply directly with `MethodologyProfile.model_validate_json(...)`,
with no manual JSON-extraction step. An earlier prompt version described
the `evidence` field inconsistently — it asked for "evidence" as a single
quoted sentence, but also said to return the section heading and the quote
together. Testing on "Attention Is All You Need" showed how Gemini resolved
that ambiguity: it returned `evidence` as one flat string with the heading
prepended, e.g. `"## Introduction In this work we propose..."`, instead of
the nested object the design intended; at the time I fixed this by
rewriting the prompt, but today the nested shape is guaranteed by the
schema regardless of prompt wording, so this specific bug class is now
structurally prevented rather than patched. Third, `response_schema` and
`response_json_schema` are not interchangeable:
`response_schema=MethodologyProfile` fails with `400 INVALID_ARGUMENT ...
Unknown name "additional_properties"`, because it converts to Google's own
`Schema` proto, which does not support `additionalProperties`, and
Pydantic's `extra="forbid"` produces exactly that field.
`response_json_schema` accepts a real JSON Schema dict instead, so
`MethodologyProfile.model_json_schema()` is passed there. Fourth, code
quality: `pyright` in strict mode and `ruff` report zero issues, and a
pytest suite in `proto3/tests/` covers `scoring.py`'s evaluation logic and
the `model_validator`'s null-correlation check, with `proto3/sync_generated.py`
keeping notebook cells in sync with the installable `proto3/src/uol_fp/`
modules. `proto3/baseline.ipynb` used to be a byte-identical duplicate of
`3pipeline.ipynb`, kept only because it had produced the six
`proto3/baseline/*.json` files; it has since been deleted, so there is no
second notebook to keep in sync by hand.

**Q17:** What visual representation(s) of results will you include?

> From the checklist above: a screenshot of the Stage 2c cell output (raw Gemini
> response / parsed JSON), and/or a before/after comparison of proto2's
> sentence-count output vs proto3's answer+evidence output for the same paper (the
> comparison already drafted in `report2/prototype-memo.md` Q12 — 14/0/0/160
> sentences vs one answer per role). Take the actual screenshots before writing
> this section (checklist item 6).

A: I include the Stage 2c cell screenshot showing the raw Gemini call and
its parsed JSON output (`report2/Screenshot 2026-07-19 180851.png`),
alongside a screenshot of proto2's sentence-list output on the same paper
(`report2/Screenshot 2026-07-18 195636.png`), so the before/after contrast
is visible directly rather than only described. I also reuse the full
per-paper JSON output tables already drafted in `report2/prototype.md`
(one figure per paper, all six papers) and the sentence-count comparison
table (Transformer: 14 TechnicalMethod / 0 Task / 0 Dataset / 160
EvaluationMetric sentences in proto2, versus one answer per role in proto3)
as the clearest single illustration of what changed between prototypes.

---

## 5. Evaluation (max 2500 words)

Must extend the preliminary report's evaluation to the **whole project**, not just
the current prototype — the requirement doc says this explicitly.

**Addendum (2026-08-09), after review of the assembled `report3/report.md`
draft:** the chapter's thinness isn't from missing analysis — baseline
P/R/F1, Wilson CI, the 5-run variance study, the proto2 → proto3 synthesis,
and the MapReduce/Pagerank error cases are all already there. What's
actually missing is the one axis proto3's own value proposition depends on:
whether the evidence-backed, inspectable output actually holds up — the
thing Chapter 1 promises the reader ("a user can check the quoted evidence
against the source paper"). That's exactly what the manual review (Q21)
measures: does evidence support the answer, is authorship correctly
attributed, does the quote actually appear in the source. Until Q21 is
filled in, this chapter answers "how accurate and stable is this?" but not
"is the thing that makes this different from proto2 — checkable evidence —
actually trustworthy?" **Priority: manual review > decomposed pilot >
Related Work ablation.** The decomposed pilot is a nice-to-have — this
chapter works without it. It does not work without the manual review.

Once the manual review is done, also make the evaluation's own coverage
explicit rather than implicit — a reader currently has to assemble what was
tested themselves. State directly (in Q18 or at the start of Q22) that this
evaluation examined four things: extraction accuracy, stability across
runs, evidence quality, and authorship attribution. A mapping table like
this is useful for both the reader and future-you:

| Question | Evidence in this report |
|---|---|
| Did proto3 fix proto2's output-volume problem? | Yes — one answer per role, by construction |
| Is the extraction itself correct? | P/R/F1 per role, Wilson CI (Q19) |
| Is the output stable across runs? | 5-run variance study (Q20) |
| Is the evidence trustworthy? | Manual review (Q21) |
| Does it avoid misattributing prior work? | Manual review (Q21) |
| Is the schema itself right? | Multi-valued-roles finding (Q9) |
| Does it generalise beyond ML-benchmark papers? | Still weak — open question (Q22) |

This costs no new experiments — it makes the coverage already achieved
legible, which is exactly what "evaluation display good coverage of
appropriate issues" rewards.

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

A: I evaluate gold-label match as a classification problem — Precision,
Recall, and F1 per role, with Wilson 95% confidence intervals on Precision
and Recall — backed by a logged 5-run variance study and a consolidated
manual review pass covering plausibility, evidence support, authorship, and
whether the quote appears in the source text, all in a single read. The
Related Work ablation runs only if time allows.

P/R/F1 is more appropriate than proto2's recall-only substring check,
because a present-but-wrong answer now costs both precision and recall,
instead of being free the way it was when any accepted sentence containing
the gold term counted as a hit, regardless of how many other sentences were
also returned.

I also changed how the evaluation itself is organized. An earlier "three
axes" plan bundled a free mechanical check together with two expensive
human-judgment checks under one label, with no priority between them. On
reflection, even the "free" mechanical check — an automated script
comparing each evidence quote against the source text verbatim — was not
worth building separately: a verbatim match only proves the LLM followed
the copy-verbatim instruction, not that the evidence is good evidence (a
real, verbatim quote from a Related Work sentence could still be the wrong
evidence for a paper's own methodology). The human reviewer already has to
read the source to judge support and authorship, so checking whether the
quote appears there costs nothing extra once folded into that same pass.

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

A: Scoring the frozen baseline against gold labels across all six papers
gives:

| Role | P | R | F1 |
|---|---|---|---|
| TechnicalMethod | 0.83 | 0.83 | 0.83 |
| Task | 0.33 | 0.33 | 0.33 |
| Dataset | 0.80 | 0.67 | 0.73 |
| EvaluationMetric | 0.80 | 0.67 | 0.73 |
| Micro | 0.68 | 0.62 | 0.65 |
| Macro | — | — | 0.655 |

I report macro as the headline "Overall" score, because the four roles are
fixed, equally mandatory schema fields, not a frequency distribution — a
user needs all four, not just whichever role happens to have the most
examples. I show both averages, but note that they are close here (0.65 vs
0.655) only because every role happens to have n=6 in this dataset — a
coincidence of this dataset, not a property of the method.

On sample size, I state Wilson 95% confidence intervals on Precision and
Recall directly, rather than a vague "small sample" caveat:
TechnicalMethod recall 0.83 gives a confidence interval of [0.44, 0.97];
Task recall 0.33 gives [0.10, 0.70]. These substantially overlap, so I do
not claim TechnicalMethod is reliably "solved" while Task is reliably
"broken" at this sample size. I do not put a Wilson interval on F1: it is
the harmonic mean of Precision and Recall, not a proportion, so a Wilson
interval on it directly is not statistically meaningful; I report F1 as a
point estimate, with a note that a proper F1 interval would need
paper-level bootstrap resampling, which is not worth adding at n=6 given
the deadline. I also chose not to grow the corpus: tightening these
intervals meaningfully would need roughly 30-40 gold-labeled papers per
role, not the 6-10 reachable in three weeks with no second annotator, so
n=6 stays, reported honestly rather than hidden behind a vague caveat.

These confidence intervals are for the single frozen baseline sample. A
second, tighter interval exists from five real pipeline runs, pooled across
runs (n=30 trials per role) — I report that one in Q20, not here, so this
section stays about the baseline gold-label-match result specifically.

One gold label also carries a specific evaluator-influence caveat worth
stating plainly: AlexNet's TechnicalMethod gold label was changed from
"AlexNet" to "convolutional" after running the pipeline and inspecting its
output, since the 2012 paper predates the name "AlexNet" and never uses it.
Adjusting a gold label after seeing model output is a real limitation on how
strongly this result generalises, and it is one instance of the broader
single-annotator problem already noted (Q21): I wrote both the gold labels
and, later, the answers being checked against them.

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
> **Two more concrete cases, found via the NotebookLM cross-check** (see
> `proto3/memo.md` "NotebookLM cross-check"): (a) MapReduce's Dataset slot
> (gold `"TeraSort"`) answered `null` in every one of the 5 runs — a genuine
> recall miss, not an absent-data case, since NotebookLM independently found the
> dataset description (two ~1TB grep/sort benchmarks) in the same source text.
> This is a different failure mode from the Task case above: "answer never
> produced" rather than "answer present but scored wrong." (b) Pagerank's
> EvaluationMetric slot (gold `"quality"`) answered `"precision"` in every one
> of the 5 runs — scored wrong by substring match, but the paper's text supports
> both terms, and NotebookLM's independent extraction also names Precision —
> a second instance of the "metric is blunt" pattern, this time pointing at the
> gold label choice rather than the pipeline's answer.
>
> **A second instance of the same "metric is blunt" pattern, if the optional P2
> diagnostic was run** (see `proto3/memo.md` "Multi-valued roles"): AlexNet's and
> ResNet's baseline EvaluationMetric answers already say "top-1 and top-5 error
> rates" verbatim — hand-recompute what P/R/F1 would be for these two papers if
> scored as multi-valued instead of against a single gold string, and report the
> difference. If not run, skip this — it's optional, not required.

A: I logged five full pipeline runs to `proto3/results/run{1..5}/*.json` and
aggregated them with `proto3/aggregate_runs.py`. Per-role F1 across the
five runs:

| Role | F1 mean | F1 min | F1 max | F1 range |
|---|---|---|---|---|
| TechnicalMethod | 0.83 | 0.83 | 0.83 | 0.00 |
| Task | 0.33 | 0.33 | 0.33 | 0.00 |
| Dataset | 0.91 | 0.91 | 0.91 | 0.00 |
| EvaluationMetric | 0.57 | 0.33 | 0.67 | 0.33 |

Three of four roles were perfectly stable across five real repetitions —
stronger evidence than an earlier two-run anecdote, which had shown both
Dataset and EvaluationMetric moving. At n=5, Dataset turned out stable, and
only EvaluationMetric is not (F1 ranged 0.33-0.67 across runs, with
unchanged code, `temperature=0`, and `seed=0`), which narrows the
non-determinism finding rather than just repeating it. The frozen baseline
behind Q19's P/R/F1 table is not a like-for-like sixth run alongside these
five: it was generated before `temperature=0` and `seed=0` were added to the
Gemini call, so only the five logged runs share identical settings.

An informal cross-check with Google NotebookLM, run independently on each
paper, found stable agreement on TechnicalMethod across all six papers —
exact or near-exact matches including "Google", "BERT", "Transformer", and
"MapReduce" — independent corroboration that this is the strongest role.

Pooling true/false positive/negative counts across the five runs gives a
tighter Wilson 95% confidence interval on Precision and Recall (n=30
trials per role):

| Role | P | P 95% CI | R | R 95% CI |
|---|---|---|---|---|
| TechnicalMethod | 0.83 | [0.66, 0.93] | 0.83 | [0.66, 0.93] |
| Task | 0.33 | [0.19, 0.51] | 0.33 | [0.19, 0.51] |
| Dataset | 1.00 | [0.87, 1.00] | 0.83 | [0.66, 0.93] |
| EvaluationMetric | 0.57 | [0.39, 0.73] | 0.57 | [0.39, 0.73] |

I state the caveat plainly: these 30 trials per role are five repeats of
the same six papers, not 30 independent papers, so the interval is
narrower than a true 30-independent-paper sample would give — I do not
present it as if it were. Even so, it is worth reporting as a finding, not
only a caveat: TechnicalMethod [0.66, 0.93] and Task [0.19, 0.51] no longer
overlap, unlike the n=6 baseline intervals in Q19 ([0.44, 0.97] vs [0.10,
0.70], which did overlap). Five real repetitions give more grounds to say
TechnicalMethod reliably outperforms Task than the single n=6 snapshot
alone supported, while I still stop short of calling either role "solved"
or "broken" outright.

One case is worth including regardless of the numbers: MapReduce's Task
slot (gold `"distributed"`, system answer `"automatic parallelization and
distribution of large-scale computations"`) fails the substring-match rule
despite being arguably correct. Task's low F1 (0.33) is partly a
measurement-instrument artifact, not purely a model failure — this
separates "the pipeline is wrong" from "the metric is blunt."

An informal cross-check with Google NotebookLM found two further concrete
cases. MapReduce's Dataset slot (gold `"TeraSort"`) answered `null` in
every one of the five runs — a genuine recall miss, not an absent-data
case, since NotebookLM independently found the dataset description (two
roughly 1 terabyte grep/sort benchmarks) in the same source text. This is a
different failure mode from the Task case above: "answer never produced"
rather than "answer present but scored wrong." Pagerank's EvaluationMetric
slot (gold `"quality"`) answered `"precision"` in every one of the five
runs — scored wrong by substring match, but the paper's text supports both
terms, and NotebookLM's independent extraction also names precision — a
second instance of the "metric is blunt" pattern, this time pointing at the
gold-label choice rather than the pipeline's answer.

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
> present the manual review as more objective. Mention the informal NotebookLM
> cross-check (`proto3/memo.md` "NotebookLM cross-check") as a distinct, non-human
> data point that ran alongside this manual review, not instead of it — it is one
> AI tool's single pass, not a formal inter-annotator study, so it narrows rather
> than replaces the "no second annotator" limitation. For the ablation: state its status
> honestly — it's first on the cut list for report3 (demoted from P1 because it
> doesn't address Task, the project's weakest role, the way the decomposed-
> extraction pilot does), not required to prove the core claims, so "not run,
> deferred to further work" is a legitimate, planned answer, not a gap to
> apologize for.

A: The review template (`proto3/manual_review.md`) is already built, with
each paper's answer, section, and quote staged next to four judgment
columns (plausible? evidence supports? authors' own work? quote in
source?) — it already stages some specific open questions rather than
starting from a blank page: BERT's Task quote cites prior work by name, so
the review needs to decide whether pre-training is BERT's own contribution
or just motivation; ResNet's Task quote cites bracketed prior work for "a
series of breakthroughs," raising the same question of whether the sentence
establishes the paper's own task or credits others'.

**FILL IT LATER** — run the consolidated manual review pass myself
(human judgment, one read per paper × role) to fill in those four judgment
columns for all 24 slots, including the two questions above: plausibly
correct? evidence supports the answer? authors' own work, not prior work?
does the quote appear verbatim in the source? Note any case where a real,
verbatim quote is still the *wrong* evidence (e.g. wrong section, or prior
work) as a distinct finding from a fabricated quote. State the
single-annotator bias applies equally to the gold labels (I wrote both).
Cite the informal NotebookLM cross-check (Q20) alongside this, not instead
of it.

The Related Work ablation is first on the cut list for report3, demoted
from P1 because it does not address Task, the project's weakest role, the
way the decomposed-extraction pilot does. It is not required to prove the
core claims, so "not run, deferred to further work" is the honest, planned
answer here, not a gap to apologize for.

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
> generalization question, not resolved). Also name MapReduce's Dataset slot
> (stable `null` across all 5 runs, gold `"TeraSort"`) as a concrete weakness,
> externally corroborated by the NotebookLM cross-check (Q20, `proto3/memo.md`
> "NotebookLM cross-check") — the dataset description is confirmed present in the
> source text, so this is a genuine model recall failure, distinct from the
> gold-label-artifact cases. Write the explicit proto2 → proto3
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

A: Mapping proto2's three named failure modes onto what proto3 actually
measured, across the whole project rather than proto3 alone:

| proto2 failure mode | proto3 status | Evidence |
|---|---|---|
| Output volume (151 TechnicalMethod sentences for MapReduce) | Fixed by design | One answer per role, every paper, by construction of Stage 2's schema-guided extraction |
| No authorship-attribution mechanism (ELMo scored 0.87 as BERT's TechnicalMethod) | Fixed by design, not yet independently verified | The authors'-own-work rule targets this directly; verifiable checking is pending the manual review (Q21) |
| Recall-only evaluation (10/12, then 18/24 substring match) | Fixed | Precision/Recall/F1 per role, Wilson confidence intervals on Precision/Recall, a 5-run variance study (Q19-Q20) |

Achievements: I moved from proto2's recall-only substring check to proto3's
classification-based Precision/Recall/F1 with confidence intervals, now
backed by five real repeated runs rather than a single snapshot (Q20).
Every answer is evidence-backed, and the pooled five-run confidence
intervals show TechnicalMethod [0.66, 0.93] and Task [0.19, 0.51] no longer
overlapping, unlike the single-baseline n=6 intervals in Q19 — a genuine
strengthening of the "TechnicalMethod works, Task doesn't" claim over the
preliminary report, evidence that the evaluation itself matured across the
project, not only the pipeline.

Weaknesses: Task's F1 is low (0.33, stable across all five runs, and partly
a metric artifact per Q20's MapReduce case). The dataset is only six
papers, all ML-benchmark-shaped — proto2 already showed systems papers like
MapReduce and Google Search fit the four-role schema worse, and I treat
this as an open generalization question, not a resolved one. A concrete
weakness worth naming directly: MapReduce's Dataset slot answered `null`
across all five runs (gold `"TeraSort"`), externally corroborated by the
NotebookLM cross-check, which confirms the dataset description is present
in the source text — a genuine model recall failure, distinct from the
gold-label-artifact cases elsewhere in the results.

**FILL IT LATER** (only if I run the decomposed-extraction pilot, variant B,
before the deadline) — report per-role F1, A (joint) vs B (decomposed); the
most direct attempt so far at fixing Task's known weakness, and a stronger
technical-challenge signal than the Related Work ablation alone. If not
run, keep the pointer to Q24 as-is.

---

## 6. Conclusion (max 1000 words)

**Addendum (2026-08-09), after review of the assembled `report3/report.md`
draft:** this chapter isn't short on remaining work to describe — it's short
on landing what the project actually found. The current Summary/Further
Work/Broader Theme structure reports what was built and what's next, but
Q23's opening ("This project automatically extracts research
methodology...") is a summary of what was done, not of what was learned.
Once the manual review (Q21) lands, restructure this chapter's opening
around three questions instead:

1. **Did it work?** The honest answer is "partially": TechnicalMethod
   extraction and output usability improved clearly over proto2; Task
   accuracy and schema generality to non-ML-benchmark papers remain
   unresolved.
2. **What did the project actually teach us?** The hardest problem was not
   producing structured JSON — schema conformance is solved by
   `response_json_schema` (Q16, Q25) — but deciding what the four roles mean
   consistently across different kinds of computing papers. MapReduce and
   Google Search struggle not only because of LLM limitations but because
   Task/Dataset/EvaluationMetric, as a schema, comes from ML-benchmark
   structure and doesn't map cleanly onto systems research.
3. **Did it meet the original user need?** Return to Chapter 1's goal —
   support the first pass of a literature review. proto2's output was too
   voluminous to serve that purpose; proto3's one-answer-per-role-plus-
   evidence format is a clear improvement, but Task's low accuracy and the
   still-unimplemented multi-valued roles (Q9) mean a user still needs to
   verify results by hand, not trust them outright.

This ties Introduction → Design → Evaluation → Conclusion into one argument,
and needs no new experiments — only the manual review results from Chapter 5
to fill in points 1 and 3 concretely.

**Q23:** Short summary — what is this project, and what has been built?

> One paragraph: the goal (automatically extract research methodology from
> computing papers using LLMs, per `CLAUDE.md`), the progression (proto1 reference
> → proto2 sentence-NLI → proto3 document-level schema-guided extraction), and
> where it currently stands (Stages 0–2 implemented, gold-label-match evaluation
> done with confidence intervals, the evidence-verifiability check/variance
> study/manual review in progress, the Related Work ablation optional/deferred).

A: This project automatically extracts research methodology — technical
method, task, dataset, and evaluation metric — from computing research
papers using large language models. I built two implemented iterations:
proto2, my own sentence-level zero-shot NLI classifier, which worked but
produced too much unusable output and could not separate authors' own methods from cited
prior work; and proto3, the current document-level, schema-guided
extraction pipeline, which returns one evidence-backed answer per role per
paper. As of this draft, Stages 0-2 are implemented, the gold-label-match
evaluation is done with confidence intervals and a 5-run variance study,
the consolidated manual review is in progress, and the Related Work
ablation is optional and deferred.

**Q24:** What further work remains?

> From `proto3/memo.md`'s explicit out-of-scope list: growing the gold-label
> corpus (shown to be poor ROI at any scale reachable in 3 weeks — say why, using
> the Wilson CI math from Q19, rather than just "no time"), a formal
> inter-annotator-agreement study with a human annotator (none exists on this
> solo project — the informal NotebookLM cross-check in Q20/Q21 narrows this gap
> but does not close it, since it's one AI tool's single pass with no annotation
> protocol, not a substitute for a human second annotator), a full
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

A: Several items are deliberately left for further work rather than
attempted in the time available. Growing the gold-label corpus is a poor
use of remaining time at any scale reachable in three weeks: the Wilson
confidence-interval math in Q19 shows that meaningfully tightening the
intervals needs roughly 30-40 gold-labeled papers per role, not the 6-10 I
could realistically add. A formal inter-annotator-agreement study with a
second human annotator does not exist on this solo project; the informal
NotebookLM cross-check in Q20/Q21 narrows this gap but does not close it,
since it is one AI tool's single pass with no annotation protocol, not a
substitute for a human second annotator. A full multi-model comparison
(Gemini vs Claude Haiku vs Llama 3.1) and the Related Work ablation, if not
reached, are also left for later. Testing on non-ML-benchmark papers —
systems, human-computer interaction (HCI) — would show whether the
four-role schema and document-level extraction generalize better than
proto2's sentence classification did, since proto2 already showed systems
papers fit this schema worse.

Two design considerations from Chapter 3 are concrete next steps rather
than open-ended ideas. First, the consolidation pass (variant C: a fifth
call checking the decomposed pilot's four role-specific outputs for mutual
consistency against their evidence) and the full three-way comparison of
joint (A), decomposed (B), and decomposed-plus-consolidation (C)
extraction. My hypothesis is that per-role accuracy follows B or C > A, and
cross-role consistency follows C > A > B, but I state this as the next
experiment to run after report3, not as a finding — no paper directly shows
that this four-role methodology-extraction task favours decomposition, so
it is a genuine open question this project is positioned to test. Second,
the full multi-valued schema implementation for Dataset and
EvaluationMetric: a new `MultiRoleExtraction` type with per-item evidence
and a ranked list capped at three items, gold-label re-annotation for the
four cells already identified (BERT/Transformer Dataset, AlexNet/ResNet
EvaluationMetric), a parallel `score_role_multi` scoring function, and
rerunning and rescoring all six papers. I already gathered the supporting
evidence for this in Q9; what remains is implementation.

**Q25:** (Optional) Any broader themes worth raising?

> E.g. the tension between structured-output guarantees (syntactic correctness,
> schema conformance) and semantic correctness (is the answer actually right) —
> `proto3/memo.md` makes this distinction explicitly and it's a defensible
> higher-level point about LLM-based extraction generally, not just this project.

A: One broader theme worth raising is the tension between structured-output
guarantees and semantic correctness. `response_json_schema` guarantees
that Gemini's reply is syntactically valid and has the right shape — the
schema-conformance problem is solved. It does not guarantee the *content*
is correct: an answer can be syntactically well-formed and still wrong, as
the "metric is blunt" cases in Q20 and the planned manual review (Q21)
show. This distinction between schema conformance and semantic correctness
is not specific to this project; it applies to LLM-based structured
extraction generally, and I think it is worth stating explicitly rather
than letting the schema's guarantees imply more than they actually prove.

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

**Fill status:**
- Checklist item 7 is already done. `report2/prototype.md`'s References
  section already has full, DOI-bearing entries for both:
  - Dagdelen, J., Dunn, A., Lee, S., Walker, N., Rosen, A. S., Ceder, G.,
    Persson, K. A., and Jain, A. 2024. Structured information extraction
    from scientific text with large language models. *Nature
    Communications* 15 (2024), 1418.
    https://doi.org/10.1038/s41467-024-45563-x
  - Polak, M. P., and Morgan, D. 2024. Extracting accurate materials data
    from research papers with conversational language models and prompt
    engineering. *Nature Communications* 15 (2024), 1569.
    https://doi.org/10.1038/s41467-024-45914-8
  These can be copied directly into report3's References list.
- `report1/report.md`'s References ([1]-[11]) and Dataset Papers ([D1]-[D6])
  lists are complete and ready to reuse verbatim as report3's starting
  point — confirmed by reading the file directly.
- **FILL IT LATER** — update the Appendix-style material (work plan
  roadmap, extended per-paper evaluation tables) once the manual review
  (Q21) and, if reached, the Related Work ablation are run.
