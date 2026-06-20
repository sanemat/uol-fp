Example

Input:

  Attention Is All You Need

Output:

    Discipline:
        - Computer Science

    Field:
        - Natural Language Processing
        - Machine Learning

    Methodology:
        Design or strategy: design and creation + experiment
        Data generation method: Documents
        Technical method: Transformer
        Task: machine translation
        Dataset: WMT machine translation datasets
        EvaluationMetric: BLEU score

Only include used entities in the final MethodologyProfile.

---

## Scope Decision

Focus on 4 roles only:
- TechnicalMethod
- Task
- Dataset
- EvaluationMetric

Do not extract: Discipline, Field, Design, Data generation method.
These are harder and more subjective. They are out of scope for the prototype.

## Input Decision

Use all body sections.
- Abstract + Experiments alone missed Dataset and TechnicalMethod for many papers.
- Full paper adds noise (Introduction, Related Work describe other work), but recall improves.
- References and Acknowledgements are skipped via `SKIP_HEADINGS`.

## Approach

Classify each sentence by role using an NLI model (zero-shot classification).

Hypothesis: sentences in a paper tend to focus on one role at a time.
If this holds, sentence-level classification is sufficient.

## Section Filtering

GROBID outputs flat `<div>` elements. Subsections are siblings, not children.
The `n` attribute (e.g., `"4"`, `"4.1"`) shows hierarchy, but format is inconsistent across papers.

Earlier approach: keyword match on heading text (`"experiment"`, `"result"`, `"performance"`).
Intermediate approach: use all sections, skip only References and Acknowledgements.
Current approach: use all sections, skip References, Acknowledgements, and Related Work.

Switching to all sections improved Dataset recall significantly.
Example: `Training Data` section in Transformer paper was missed before; now captured with 0.85–0.92 score.

### Related Work exclusion

Added `SKIP_KEYWORDS = {"related work", "related works"}` with substring + case-insensitive match.
Also tracks the `n` attribute (e.g. `"2"`) to skip subsections (e.g. `"2.1"`, `"2.2"`) automatically.
This removes noise from BERT (3 subsections under Related Work), ResNet, MapReduce, and Google Search.

## Observations from Testing

Tested on: Attention Is All You Need, BERT, AlexNet, ResNet, MapReduce, Google Search.

Where information tends to appear:
- TechnicalMethod → Architecture / Model sections
- Dataset → dedicated "Dataset" or "Data" section
- Task → implicit, or in Abstract
- EvaluationMetric / Task results → Experiments / Results sections

Switched to all body sections. Dataset recall improved.
New noise sources appeared (see below).

### Systems papers (MapReduce, Google Search)

These papers do not follow the ML benchmark structure.
- No standard dataset → Dataset is empty or wrong (e.g., system size described as dataset)
- No clear evaluation metric → EvaluationMetric is empty
- Task is implicit or missing

The 4-role structure fits ML papers better than systems papers.

### Noise

Several noise types observed:

- **Quoted / example text** — e.g. Google Search: `"you looked at a lot of pages from my Web site."` classified as Task.
- **Short fragments** — `"•"`, `"The"`, `"[4, 27, 28, 22] ."`, citation stubs pass the threshold.
- **Author contributions** — GROBID includes author contribution text in the abstract. These get classified as TechnicalMethod.
- **Introduction / Related Work** — other papers' methods are classified as TechnicalMethod of this paper.

A minimum sentence length filter (e.g., 30 chars) would remove most short fragments.
Introduction noise is harder to fix without section-level filtering.
Related Work is now excluded via `SKIP_KEYWORDS` (see Section Filtering).

### EvaluationMetric

Hardest role to capture across all papers.
Often empty, or only an intro sentence is picked up (e.g., "we measure performance on...").
Better hypothesis templates may help.

## Better Output for Iteration

Current output (dict of sentence lists) is hard to use for tuning.

Better: show all sentences with label and score, including rejected ones.
Example format:
```
[Abstract] The dominant sequence transduction...  technical_method  0.72 ✓
[Abstract] Listing order is random.               dataset           0.48 ✗
```

This helps answer:
- Is the label correct?
- Is the threshold right?
- What is being missed?

## Sentence Splitting + Noise Filter (done)

Added to Step 0c:
- `pre_clean()` — strips inline citation markers (`[13]`, `[4, 27]` etc.) before splitting.
- `is_valid()` — drops sentences shorter than 30 chars or without real words.

Compared `en_core_web_sm` vs `pySBD` — counts nearly identical (e.g. 185 vs 181 on Transformer).
Kept `en_core_web_sm`; splitter choice doesn't matter after pre-cleaning.

Tried SciSpacy (`en_core_sci_sm`) — dropped: causes numpy binary incompatibility in Colab.

## Future: Better Hypothesis Templates

Currently using short label names as hypotheses (e.g., "technical method").
Better hypotheses may improve NLI accuracy. For example:
- "technical method" → "This sentence describes a method or algorithm used in the research."
- "dataset" → "This sentence describes a dataset or data source used in the research."
- "evaluation metric" → "This sentence describes a metric used to measure performance."
- "task" → "This sentence describes the research task or problem being solved."

Do this after verifying the basic pipeline works.
