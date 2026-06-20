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

Use abstract + experiments section.
- Abstract alone is not enough (dataset and metric are often missing).
- Full paper is too complex.
- Abstract + experiments section is a realistic balance.

## Approach

Classify each sentence by role using an NLI model (zero-shot classification).

Hypothesis to verify:
In real papers, sentences in the abstract and experiments section tend to focus on one role at a time.
If this holds, sentence-level classification is sufficient.

Next step: test on one paper (e.g., "Attention Is All You Need") and check the results manually.

## Section Filtering

GROBID outputs flat `<div>` elements. Subsections are siblings, not children.
The `n` attribute (e.g., `"4"`, `"4.1"`) shows hierarchy, but format is inconsistent across papers (some use trailing dots, some have empty `n`).

So we match by heading text instead: keywords `"experiment"`, `"result"`, `"performance"`.
This covers most papers. Subsections with unrelated names (e.g., "GLUE") are not captured — acceptable for the prototype.

## Future: Better Hypothesis Templates

Currently using short label names as hypotheses (e.g., "technical method").
Better hypotheses may improve NLI accuracy. For example:
- "technical method" → "This sentence describes a method or algorithm used in the research."
- "dataset" → "This sentence describes a dataset or data source used in the research."
- "evaluation metric" → "This sentence describes a metric used to measure performance."
- "task" → "This sentence describes the research task or problem being solved."

Do this after verifying the basic pipeline works.
