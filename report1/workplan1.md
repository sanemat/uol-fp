# Work Plan

This feedback looks difficult at first, but the problems are clear. The feedback does not only say that the work is weak. It also tells me what I need to improve.

The most important issue is the evaluation.

## 1. Rebuild the evaluation

The current evaluation checks whether at least one accepted sentence contains the gold label.

There is another problem. Some gold labels were changed after seeing the model results. For example, the AlexNet TechnicalMethod label was changed from `AlexNet` to `convolutional`.

The feedback asks for:

* fixed gold labels
* more papers
* precision and recall

The next evaluation should use this process:

1. Create all gold labels before checking the model results.
2. Allow more than one correct answer for each role.
   Example: `Dataset = {BooksCorpus, English Wikipedia}`.
3. Calculate TP, FP, and FN.
4. Calculate precision, recall, and F1.
5. Show results for each paper and each role.
6. Calculate macro averages.
7. Do not change the gold labels after the evaluation starts.

Before running the next model, the gold dataset should also be checked carefully. Some current gold labels may be incomplete or incorrect. For example, BERT has several datasets and evaluation metrics, and some labels for MapReduce and ResNet may need to be checked.

---

## 2. Justify the threshold

The current NLI system uses a threshold of `0.5`.

The report also says that success means at least `10 out of 12` correct results.

These values need a clear reason.

The next evaluation should compare several thresholds, for example:

* 0.3
* 0.4
* 0.5
* 0.6
* 0.7

For each threshold, I should measure precision and recall.

If I need to choose one threshold, I should:

1. choose the threshold using development papers;
2. keep the test papers separate;
3. use the fixed threshold on the test papers.

This will give a clear reason for the final threshold.

---

## 3. Test the sentence-level assumption

The current report says:

> The hypothesis is that sentences in a paper tend to describe one role at a time.

It then says that the results seem to support this assumption for ML papers.

However, this may be circular. The system uses single-label classification, so the results naturally show one label for each sentence.

The next gold annotation should allow multiple labels for one sentence:

* TechnicalMethod
* Task
* Dataset
* EvaluationMetric
* Other

Then I can measure how many sentences actually contain more than one role.

For example:

> “We evaluate BERT on the GLUE benchmark and achieve 80.5% accuracy.”

This sentence may contain more than one role.

If many sentences have several roles, this will show a limitation of single-label sentence classification. This is still a useful research result.

---

## 4. Improve the literature review by comparing studies

The literature review already has relevant sources, but the same sources are used many times.

The next version should separate the literature into different purposes.

### Research problem literature

* research methodology representation
* scientific information extraction

### Technical literature

* GROBID
* NLI and zero-shot classification
* scientific document processing
* evaluation methods
* annotation methods

The review should also compare studies more directly.

Instead of writing:

> A does X.
> B does Y.
> C does Z.

I should write something like:

> A solves X, but it needs labelled data.
> B reduces the problem to only one role.
> C can separate used methods from mentioned methods, but it only supports two entity types.
> Therefore, none of these systems solves both the broad extraction problem and the lack of labelled training data.

The current synthesis section already starts to do this. The next version should remove repeated descriptions and make this comparison the main structure.

---

## 5. Fix the citations

This is mainly a formatting task.

The current numbered citations do not start from `[1]` in the order they first appear in the report.

The next version should:

1. start with `[1]` for the first source used in the text;
2. increase the number in the order that sources first appear;
3. use one citation style consistently.

The report should also avoid mixing different citation styles unless the required style allows it.

---

## 6. Improve the user and domain analysis

The current user analysis is too short.

The report mainly says that the users are computing students, early-stage researchers, and supervisors.

The next version should connect user needs to system requirements and evaluation.

| User need                             | System requirement          | Evaluation           |
| ------------------------------------- | --------------------------- | -------------------- |
| Quickly understand a paper            | Show the four roles clearly | Output size          |
| Check the original paper              | Show evidence sentences     | Evidence correctness |
| Avoid missing important information   | High recall                 | Recall               |
| Avoid too much irrelevant information | Reduce noisy output         | Precision            |

This will improve both the user analysis and the evaluation strategy.

---

## 7. Create a proper system diagram

The current diagram is only a simple flow:

`PDF → GROBID → TEI → filtering → sentence splitting → NLI → JSON`

The next diagram should show more detail.

It should include:

* input
* PDF parsing
* validation
* extraction
* post-processing
* output

It should also show possible problems:

* PDF parsing failure
* empty or invalid sections
* low-confidence prediction
* no result for a role
* multiple candidates
* evidence sentences
* user-facing results

A proper diagram should make the full system easier to understand.

---

## 8. Improve the work plan

The current work plan mainly uses large periods such as July and August.

The next work plan should divide the work into smaller tasks:

`Gold annotation → evaluation framework → model runs → error analysis → ablation study → final writing`

For each task, the plan should include:

* duration
* dependencies
* risks
* contingency time

This will make the plan easier to evaluate.

---

## 9. Increase the technical challenge

The Technical Challenge score is only `2/8`.

The current report explains several difficult problems:

* hypothesis engineering
* domain mismatch
* authorship attribution

However, the implementation can still look like a simple combination of existing tools:

`GROBID + spaCy + pretrained NLI model`

The next prototype should compare several approaches using the same fixed gold dataset.

For example:

* NLI baseline
* document-level LLM
* improved extraction method

The evaluation framework should include:

* extraction quality
* evidence grounding
* structured output
* multiple values for one role
* precision
* recall
* F1
* failure analysis

This will make the technical work deeper and easier to evaluate.

---

# Priority

## A. Fix the research problems first

1. Rebuild and freeze the gold dataset.
2. Use precision, recall, and F1.
3. Test the threshold and the sentence-level assumption.

## B. Improve the argument

4. Rewrite the literature review around comparisons.
5. Connect users, requirements, and evaluation.
6. Make the next prototype technically stronger.

## C. Fix clear report problems

7. Fix citations.
8. Create a proper system diagram.
9. Create a more detailed work plan.

The first task should be the gold dataset. It should be completed before the next model evaluation. The gold labels must be independent from the model results.
