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

**Q7:** What does the system output for "Attention Is All You Need"? Describe the result (sentence counts and whether gold terms were found). Note which hypothesis set was used and what effect it had.

> Run result (proto2/result/2pipeline-attention.ipynb — used **verbose_v1** hypothesis set):
> - TechnicalMethod: **14 sentences** — ○ contains "Transformer" (e.g. "We propose a new simple network architecture, the Transformer...")
> - Task: **0 sentences** — ✗ (EM bias from verbose_v1 absorbed most sentences)
> - Dataset: **0 sentences** — ✗ (same cause)
> - EvaluationMetric: **160 sentences** — ○ contains "BLEU" (e.g. "Our model achieves 28.4 BLEU on the WMT 2014...")
>
> Key observation: verbose_v1 caused extreme EvaluationMetric bias (160 sentences vs 0 Task/Dataset).
> This matches the hypothesis set comparison result in the Reference table below.
> The short-label run (BERT notebook) gives a much more balanced distribution.

A:

**Q8:** You tested the prototype on six papers. For each, briefly describe what worked and what did not.

> Run results (sentence counts accepted per role):
>
> | Paper | TM (count) | Task (count) | Dataset (count) | EM (count) | Hypothesis set |
> |---|---|---|---|---|---|
> | Transformer | 14 | 0 | 0 | 160 | verbose_v1 |
> | BERT | 62 | 23 | 15 | 13 | short |
> | AlexNet (CNN) | 51 | 6 | 11 | 4 | short |
> | ResNet | 51 | 6 | 14 | 12 | short |
> | MapReduce | 151 | 24 | 3 | 5 | short |
> | PageRank / Google | 69 | 21 | 8 | 29 | short |
>
> Key patterns: Transformer (verbose_v1) shows severe EM bias — Task and Dataset are empty. ML papers (BERT, AlexNet, ResNet) produce balanced results with short labels. Systems papers (MapReduce, PageRank) have large TM counts (the whole system described in every section) and very few Dataset/EM sentences.

A:

| Paper | TechnicalMethod | Task | Dataset | EvaluationMetric | Notes |
|---|---|---|---|---|---|
| Transformer | 14 sentences | 0 sentences | 0 sentences | 160 sentences | verbose_v1: extreme EM bias |
| BERT | 62 sentences | 23 sentences | 15 sentences | 13 sentences | short: balanced |
| AlexNet | 51 sentences | 6 sentences | 11 sentences | 4 sentences | short: balanced |
| ResNet | 51 sentences | 6 sentences | 14 sentences | 12 sentences | short: balanced |
| MapReduce | 151 sentences | 24 sentences | 3 sentences | 5 sentences | short: TM heavy, weak DS/EM |
| Google Search | 69 sentences | 21 sentences | 8 sentences | 29 sentences | short: no standard benchmark |

---

## 4. Evaluation

**Q9:** What evaluation method did you use? Why is it appropriate for an NLP prototype?

> Tip: You have no annotated dataset, so precision/recall/F1 cannot be measured in the traditional way. Instead: for each paper × role, manually define a gold term (e.g. "Transformer", "BLEU"), then check whether any accepted sentence in the output contains that term (substring match). This is a recall-oriented check: it tells you whether the correct information is in the output at all. Reference: Jain et al. [3] used a similar role-based evaluation against annotated spans.

A:

**Q10:** Fill in the gold label evaluation table. For each cell, write ○ (any accepted sentence contains the gold term) or × (not found).

> Gold terms and run results (from proto2/result/):
>
> | Paper | Gold TM | Gold Task | Gold Dataset | Gold EM |
> |---|---|---|---|---|
> | Transformer | "Transformer" | "machine translation" | "WMT" | "BLEU" |
> | BERT | "BERT" | "GLUE" or "SQuAD" | "BooksCorpus" or "Wikipedia" | "F1" or "accuracy" |
> | AlexNet (CNN) | note below | "object recognition" | "ImageNet" | "top-1" or "top-5" |
>
> **AlexNet naming note:** The 2012 paper does not use the name "AlexNet" — that name was coined later.
> Gold term for TM should be "convolutional" (or similar), not "AlexNet".
>
> Run results (○ = gold term found in any accepted sentence, ✗ = not found):

A:

| Paper | TechnicalMethod | Task | Dataset | EvaluationMetric |
|---|---|---|---|---|
| Transformer | ○ | ✗ | ✗ | ○ |
| BERT | ○ | ○ | ○ | ○ |
| AlexNet | ✗ (if gold="AlexNet") | ○ | ○ | ○ |

> Transformer ✗ for Task and Dataset: caused by verbose_v1 EvaluationMetric bias (Task=0 sentences, Dataset=0 sentences).
> AlexNet TM ✗: paper does not use the word "AlexNet". Change gold term to "convolutional" → ○.
> Write in your own words below what these results mean.

**Q11:** What do the evaluation results show? Which roles are easy and which are hard?

> From run results: BERT captured all 4 roles correctly (short labels, balanced distribution). Transformer captured only TM and EM (verbose_v1 caused EM bias, leaving Task and Dataset empty). AlexNet captured Task, Dataset, EM correctly; TM depends on gold label choice.
> Across ML papers (BERT, AlexNet, ResNet): TechnicalMethod and Dataset tend to appear in dedicated architecture/data sections. EvaluationMetric appears in experiment/results sections. Task is most often implicit (only in Abstract or Introduction).

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

## Reference: Hypothesis Set Comparison

Use these tables in the report when discussing technical challenge and iteration.

### BERT paper (258 sentences) — from proto2/memo.md

| Set | Probe (4 gold correct) | TechnicalMethod | Task | Dataset | EvaluationMetric |
|---|---|---|---|---|---|
| short | **3/4** | 124 | 70 | 33 | 31 |
| verbose_v1 | 2/4 | 11 | 0 | 3 | 244 |
| verbose_v2 | 2/4 | 63 | 11 | 19 | 165 |
| verbose_v3 | 2/4 | 131 | 56 | 60 | 11 |

### Transformer paper (183 sentences) — from proto2/result/2pipeline-attention.ipynb

| Set | Probe (4 gold correct) | TechnicalMethod | Task | Dataset | EvaluationMetric |
|---|---|---|---|---|---|
| short | **3/4** | — | — | — | — |
| verbose_v1 | 2/4 | 14 | 0 | 0 | 160 |
| verbose_v2 | 2/4 | — | — | — | — |
| verbose_v3 | 2/4 | — | — | — | — |

> The Transformer notebook ran verbose_v1 only. The EM bias (160 sentences vs 0 Task/Dataset) is visible in the actual run — consistent with BERT findings.

Probe results (Transformer paper):
```
We propose the Transformer architecture.           → short=ok, verbose_v1=ok, v2=ok, v3=ok
The task is machine translation from English...    → short=NG, verbose_v1=NG, v2=NG, v3=ok
We train on the WMT 2014 English-German dataset.   → short=ok, verbose_v1=NG, v2=NG, v3=NG
We evaluate translation quality using BLEU score.  → short=ok, verbose_v1=ok, v2=ok, v3=NG
Correct:                                           → short=3/4, v1=2/4, v2=2/4, v3=2/4
```

Finding: verbose hypotheses introduced strong label bias. Short labels gave the best probe score and most balanced distribution. This pattern is consistent across both BERT (258 sentences) and Transformer (183 sentences).
