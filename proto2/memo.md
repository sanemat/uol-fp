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

## Observations from Testing

Tested on: Attention Is All You Need, BERT, AlexNet, ResNet, MapReduce, Google Search.

Where information tends to appear:
- TechnicalMethod → Architecture / Model sections
- Dataset → dedicated "Dataset" or "Data" section
- Task → implicit, or in Abstract
- EvaluationMetric / Task results → Experiments / Results sections

Abstract + Experiments alone misses Dataset and TechnicalMethod for many papers.
May need to include more section types, or reconsider the input scope.

### Systems papers (MapReduce, Google Search)

These papers do not follow the ML benchmark structure.
- No standard dataset → Dataset is empty or wrong (e.g., system size described as dataset)
- No clear evaluation metric → EvaluationMetric is empty
- Task is implicit or missing

The 4-role structure fits ML papers better than systems papers.

### Noise

Quoted text or example sentences inside a paper get classified as Task.
Example from Google Search paper: `"you looked at a lot of pages from my Web site."` was classified as Task.
The model has no context to know a sentence is a quote, not a claim.

### EvaluationMetric

Hardest role to capture across all papers.
Often empty, or only an intro sentence is picked up (e.g., "we measure performance on...").
Specific numbers and metric names tend to appear in subsections not captured by keyword filtering.

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

## Future: Better Hypothesis Templates

Currently using short label names as hypotheses (e.g., "technical method").
Better hypotheses may improve NLI accuracy. For example:
- "technical method" → "This sentence describes a method or algorithm used in the research."
- "dataset" → "This sentence describes a dataset or data source used in the research."
- "evaluation metric" → "This sentence describes a metric used to measure performance."
- "task" → "This sentence describes the research task or problem being solved."

Do this after verifying the basic pipeline works.
