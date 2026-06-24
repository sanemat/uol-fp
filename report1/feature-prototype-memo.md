# feature-prototype-memo.md

This file is a Q&A draft for you to fill in yourself.
Write your answer after each `A:` in your own words.
After you finish, use your answers as material for `feature-prototype.md` (the PDF submission).

---

## 1. What Is the Prototype

**Q1:** What did you implement? Write one sentence.

> Tip: Name the input, what the system does, and the output.

A:

**Q2:** Why is sentence-level zero-shot NLI classification the most important feature to prototype?

> Tip: The whole pipeline depends on this step. If NLI classification does not work, the output is meaningless. Other steps (XML parsing, section filtering, sentence splitting) are preprocessing — classification is the core.

A:

---

## 2. Implementation

**Q3:** Describe the pipeline from TEI XML to JSON output. List the main steps in order.

> Tip: The notebook has these steps: (0) load TEI XML and extract sections, (0b) select sections, (0c) split sentences + filter, (2) classify with NLI, output JSON. Write in your own words.

A:

**Q4:** Which model did you use for zero-shot classification, and why?

> Tip: The model is `cross-encoder/nli-deberta-v3-small`. It is a cross-encoder trained on NLI tasks. It accepts a premise (sentence) and a hypothesis (label description) and returns an entailment score. Zero-shot means no task-specific training is needed.

A:

**Q5:** What preprocessing does the pipeline apply before classification?

> Tip: Two functions in Step 0c — `pre_clean()` strips citation markers like `[13]` or `[4, 27]`; `is_valid()` drops sentences shorter than 30 characters or without at least 3 letter-only words.

A:

**Q6:** Which sections of the paper are included, and which are excluded? Why?

> Tip: Excluded via `SKIP_HEADINGS`: References, Acknowledgements. Excluded via `SKIP_KEYWORDS`: Related Work (and its subsections, tracked by the `n` attribute). Reason: these sections describe other papers' work, not this paper's methodology. All other body sections are used. Earlier version used only Experiment/Result sections — switching to full paper improved Dataset recall (e.g., `Training Data` section in Transformer was missed before).

A:

---

## 3. Demonstration

**Q7:** What does the system output for "Attention Is All You Need"? Show the JSON result (all four roles).

> Tip: Run the notebook on the Transformer TEI XML and copy the final JSON output here. The gold answers from proto2/memo.md are: TechnicalMethod = Transformer, Task = machine translation, Dataset = WMT machine translation datasets, EvaluationMetric = BLEU score.

A:

```json
```

**Q8:** You tested the prototype on six papers. For each, briefly describe what worked and what did not.

> Tip: Papers tested — Attention Is All You Need, BERT, AlexNet, ResNet, MapReduce, Google Search. Key observation: the 4-role structure fits ML papers well. Systems papers (MapReduce, Google Search) have no standard benchmark dataset or clear evaluation metric, so those roles are often empty or wrong.

A:

| Paper | TechnicalMethod | Task | Dataset | EvaluationMetric | Notes |
|---|---|---|---|---|---|
| Transformer | | | | | |
| BERT | | | | | |
| AlexNet | | | | | |
| ResNet | | | | | |
| MapReduce | | | | | |
| Google Search | | | | | |

---

## 4. Evaluation

**Q9:** What evaluation method did you use? Why is it appropriate for an NLP prototype?

> Tip: You have no annotated dataset, so precision/recall/F1 cannot be measured in the traditional way. Instead: for each paper × role, manually define a gold term (e.g. "Transformer", "BLEU"), then check whether any accepted sentence in the output contains that term (substring match). This is a recall-oriented check: it tells you whether the correct information is in the output at all. Reference: Jain et al. [3] used a similar role-based evaluation against annotated spans.

A:

**Q10:** Fill in the gold label evaluation table. For each cell, write ○ (any accepted sentence contains the gold term) or × (not found).

> Tip: Gold labels from proto2/memo.md:
> - Transformer: TechnicalMethod=Transformer, Task=machine translation, Dataset=WMT, EvaluationMetric=BLEU
> - BERT: TechnicalMethod=BERT, Task=GLUE/SQuAD, Dataset=BooksCorpus/Wikipedia, EvaluationMetric=accuracy/F1
> - AlexNet: TechnicalMethod=AlexNet, Task=image classification, Dataset=ImageNet, EvaluationMetric=top-1/top-5 error
> Run the notebook on each paper and check the output.

A:

| Paper | TechnicalMethod | Task | Dataset | EvaluationMetric |
|---|---|---|---|---|
| Transformer | | | | |
| BERT | | | | |
| AlexNet | | | | |

**Q11:** What do the evaluation results show? Which roles are easy and which are hard?

> Tip: From testing notes — TechnicalMethod and Dataset tend to appear in dedicated sections (Architecture, Dataset/Data) and score well. Task is often implicit or only in the Abstract, so recall is lower. EvaluationMetric is hardest: often only an introductory sentence like "we measure performance on..." is captured, not the metric name itself.

A:

---

## 5. Weaknesses

**Q12:** What types of noise did you observe in the output? For each type, describe the cause.

> Tip: Four types identified in proto2/memo.md:
> (1) Quoted/example text — e.g. Google Search: `"you looked at a lot of pages..."` classified as Task.
> (2) Author contributions — GROBID includes contribution text in the abstract; classified as TechnicalMethod.
> (3) Introduction noise — other papers' methods described in Introduction score high (e.g. "The feature-based approach, such as ELMo" scored 0.87 as TechnicalMethod on BERT).
> (4) Sentences with numbers or fragments still passing `is_valid()` — a 30-char minimum helps but does not eliminate all cases.

A:

---

## 6. Improvements for Proto3

**Q13:** What three improvements are planned for the next iteration? For each, explain why you expect it to help.

> Tip: From proto2/memo.md Future sections:
> (1) First-person verb filter — "we propose / introduce / use" signals the paper's own work; third-person mentions are usually references to prior work. Applied before or after NLI to reduce Introduction noise.
> (2) Top-N selection by score × section weight — current output keeps all accepted sentences (can be hundreds). Top 3 per role, ranked by score, gives a cleaner result. Section weight: Abstract and Methods rank higher than Introduction.
> (3) LLM term extraction — current output is full sentences; pitch target is short terms like "Transformer" or "BLEU". Pass each accepted sentence to an LLM with prompt: "What is the [role] named in this sentence?" Extract the key noun phrase.

A:

---

## 7. Technical Challenge

**Q14:** Why is zero-shot NLI classification on academic text technically challenging? Give two or three specific reasons.

> Tip from proto2/memo.md Technical challenge section:
> (1) No training data — the model must generalise from NLI training data (general text) to scientific writing without any task-specific examples.
> (2) Hypothesis engineering is non-trivial — you tested 4 hypothesis sets (short, verbose_v1, verbose_v2, verbose_v3). Verbose hypotheses introduced strong label bias: verbose_v1 and verbose_v2 classified most sentences as EvaluationMetric; verbose_v3 as TechnicalMethod. Short labels (3/4 probe correct, most balanced distribution) outperformed all verbose variants. This is counter-intuitive and required systematic experimentation to discover.
> (3) Domain mismatch — NLI models are trained on general-domain text; academic writing has long complex sentences, citation noise, and domain-specific terminology that was not in the training data.

A:

---

## Reference: Hypothesis Set Comparison (BERT paper, 258 sentences)

Use this table in the report when discussing technical challenge and iteration.

| Set | Probe (4 gold sentences correct) | TechnicalMethod | Task | Dataset | EvaluationMetric |
|---|---|---|---|---|---|
| short | **3/4** | 124 | 70 | 33 | 31 |
| verbose_v1 | 2/4 | 11 | 0 | 3 | 244 |
| verbose_v2 | 2/4 | 63 | 11 | 19 | 165 |
| verbose_v3 | 2/4 | 131 | 56 | 60 | 11 |

Finding: verbose hypotheses introduced strong label bias. Short labels gave the best probe score and most balanced distribution.
