# feature-prototype-memo.md

This file is a Q&A draft for you to fill in yourself.
Write your answer after each `A:` in your own words.
After you finish, use your answers as material for `feature-prototype.md` (the PDF submission).

---

## 1. What Is the Prototype

**Q1:** What did you implement? Write one sentence.

> Template to fill in:
> "The prototype takes [input] and [what it does] to produce [output]."
>
> Facts to use:
> - Input: a TEI XML file produced by GROBID from a computing research paper
> - Action: classifies each sentence by research methodology role using zero-shot NLI
> - Output: a JSON object with four lists — TechnicalMethod, Task, Dataset, EvaluationMetric

A: The prototype takes a TEI XML file produced by GROBID from a computing research paper and classifies each sentence by research methodology role using zero-shot NLI to produce a JSON object with four lists — TechnicalMethod, Task, Dataset, and EvaluationMetric.

**Q2:** Why is sentence-level zero-shot NLI classification the most important feature to prototype?

> Think about the pipeline in two parts: preprocessing (Steps 0–0c) and classification (Step 2).
>
> Preprocessing (XML parsing, section filtering, sentence splitting) uses standard tools — ElementTree, spaCy. These are solved problems. You could replace them with other tools and the output would be similar.
>
> Classification is different. It decides which sentences belong to which role. Without it, you have a list of 183 sentences (Transformer) or 258 sentences (BERT) with no meaning attached. The role assignment IS the output. If the model fails, the whole prototype fails.
>
> Also: zero-shot classification was the key design choice (no training data). If zero-shot NLI does not work, you would need a supervised model — which would require 438 annotated papers (Jain et al. [3]). So showing that zero-shot works is the proof that the approach is viable.

A: The prototype uses zero-shot NLI classification to assign a role (label) to each sentence.

---

## 2. Implementation

**Q3:** Describe the pipeline from TEI XML to JSON output. List the main steps in order.

> Write as a numbered list. Each step: what goes in, what comes out.
>
> Step 1 — Load XML: Input = TEI XML file. Parse with ElementTree. Extract the abstract and all body `<div>` elements. Output = list of `{heading, text}` dicts.
>
> Step 2 — Filter sections: Skip sections whose heading is in SKIP_HEADINGS (References, Acknowledgements) or SKIP_KEYWORDS (Related Work). Also skip subsections of Related Work by tracking the `n` attribute (e.g. if Related Work is `n="2"`, skip `n="2.1"`, `n="2.2"` etc.). Output = filtered list of sections.
>
> Step 3 — Split and clean sentences: For each section, run `pre_clean()` to strip citation markers like `[13]`, then split with spaCy into sentences, then `is_valid()` to drop fragments (< 30 chars or no real words). Output = list of `CandidateWithContext` objects (sentence + section name).
>
> Step 4 — Classify: For each sentence, call the NLI classifier with 4 candidate labels. If the top label scores ≥ 0.5, add the sentence to the corresponding role list in `MethodologyProfile`. Output = JSON dict with 4 keys (TechnicalMethod, Task, Dataset, EvaluationMetric), each a list of accepted sentences.

A: First, a computing paper is converted to TEI XML by GROBID. The pipeline then loads the XML, extracts sections, and filters out References, Acknowledgements, and Related Work. Next, it cleans each section and splits the text into sentences using spaCy. After that, each sentence is classified by the NLI classifier with 4 candidate labels. If the top score is at or above the threshold (0.5), the sentence is added to the accepted list for that role. The final output is a JSON object containing the accepted sentences per role.

**Q4:** Which model did you use for zero-shot classification, and why?

> Model: `cross-encoder/nli-deberta-v3-small` from Hugging Face.
>
> What it does: it takes two inputs — a **premise** (the paper sentence) and a **hypothesis** (a label description like `"technical method"`) — and predicts whether the premise entails the hypothesis. The score for "entailment" is used as the classification score.
>
> Why this model:
> - It is trained on NLI data (general text), so it generalises to new labels without task-specific training → zero-shot.
> - DeBERTa (Decoding-enhanced BERT with Disentangled Attention) is a strong NLI backbone. The `v3-small` variant fits in Colab memory (568 MB) while still performing well.
> - The cross-encoder architecture scores premise + hypothesis jointly, which gives more accurate entailment judgements than bi-encoders.
>
> Why zero-shot matters: no annotated dataset exists for this task. Supervised training would need hundreds of labeled papers (Jain et al. [3] used 438). Zero-shot avoids this requirement entirely.

A: DeBERTa (Decoding-enhanced BERT with Disentangled Attention) is a strong NLI backbone. The `v3-small` variant fits in Colab memory (568 MB) while still performing well. No annotated dataset was available for this task. Supervised training would need hundreds of labeled papers (Jain et al. [3] used 438). Zero-shot reduces this requirement.

**Q5:** What preprocessing does the pipeline apply before classification?

> Two steps in Step 0c. For each, explain what the problem is, what the function does, and give a concrete before/after example.
>
> **pre_clean()** — Problem: citation markers like `[13]` or `[4, 27]` appear inside sentences after GROBID extraction. If not removed, spaCy may split on them or the NLI model sees noise. The function strips them with a regex. Example: `"The model outperforms [4, 27] the baseline."` → `"The model outperforms the baseline."`
>
> **is_valid()** — Problem: after splitting, some "sentences" are fragments — a bullet character `"•"`, a lone number, or a citation stub like `"[4, 27, 28] ."`. These pass through sentence splitting but carry no information. The function drops any sentence shorter than 30 characters or without at least one word of 3+ letters.
>
> Effect: the actual run produced 183 sentences on the Transformer paper after pre-cleaning; without these filters, fragments and stubs would appear in the classification input.

A: The pipeline applies two preprocessing steps before classification. First, `pre_clean()` removes inline citation markers such as `[13]` or `[4, 27]` using a regex. Without this step, spaCy may split a sentence at the bracket, producing broken fragments. For example, `"The model outperforms [4, 27] the baseline."` becomes `"The model outperforms the baseline."` Second, `is_valid()` drops sentences that are shorter than 30 characters or contain no word of 3 or more letters. This removes bullet characters, lone numbers, and citation stubs that pass through sentence splitting but carry no information. After these two steps, the Transformer paper produced 183 valid sentences for classification.

**Q6:** Which sections of the paper are included, and which are excluded? Why?

> Describe three things: (1) what is excluded and why, (2) what is included, (3) why you chose "all body sections" rather than only experiment sections.
>
> **Excluded:**
> - References, Acknowledgements — via exact heading match (`SKIP_HEADINGS`). These sections list citations and credits, not methodology.
> - Related Work — via keyword match (`SKIP_KEYWORDS`). Also skips subsections automatically by tracking the `n` attribute. Reason: Related Work describes other papers' methods, which the NLI model incorrectly classifies as TechnicalMethod of this paper. Testing on BERT showed 67 → 62 TechnicalMethod sentences (-5) after excluding Related Work.
>
> **Included:** all other body sections — Abstract, Introduction, Method/Architecture, Dataset, Experiment, Results, Conclusion, etc.
>
> **Why all sections, not just Experiment/Results:**
> Earlier version used only sections whose heading matched keywords like "experiment" or "result". The `Training Data` section in the Transformer paper has no such keyword — it was missed. Dataset role recall improved significantly after switching to all body sections. The trade-off is more noise from Introduction (other papers' methods), but recall is more important at this prototype stage.

A: I exclude References, Acknowledgements, and Related Work.

---

## 3. Demonstration

**Q7:** What does the system output for "Attention Is All You Need"? Describe the result (sentence counts and whether gold labels were found). Note which hypothesis set was used and what effect it had.

> Run result (proto2/result/2pipeline-attention.ipynb — used **verbose_v1** hypothesis set):
> - TechnicalMethod: **14 sentences** — ○ contains "Transformer" (e.g. "We propose a new simple network architecture, the Transformer...")
> - Task: **0 sentences** — ✗ (EM bias from verbose_v1 absorbed most sentences)
> - Dataset: **0 sentences** — ✗ (same cause)
> - EvaluationMetric: **160 sentences** — ○ contains "BLEU" (e.g. "Our model achieves 28.4 BLEU on the WMT 2014...")
>
> Key observation: verbose_v1 caused extreme EvaluationMetric bias (160 sentences vs 0 Task/Dataset).
> This matches the hypothesis set comparison result in the Reference table below.
> The short-label run (BERT notebook) gives a much more balanced distribution.

A: The system classified 183 sentences from the Transformer paper. Using the verbose_v1 hypothesis set, TechnicalMethod received 14 sentences and EvaluationMetric received 160 sentences. Task and Dataset received 0 sentences each. The gold label "Transformer" was found in the TechnicalMethod output (e.g. "We propose a new simple network architecture, the Transformer...") and "BLEU" was found in the EvaluationMetric output (e.g. "Our model achieves 28.4 BLEU on the WMT 2014..."). However, Task and Dataset produced no output because the verbose_v1 EvaluationMetric hypothesis was too broad and absorbed most sentences. This suggests that hypothesis choice can have a large effect on the output distribution.

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

A: The prototype was tested on six papers. ML papers (BERT, AlexNet, ResNet) produced balanced output across all four roles using short labels. BERT captured all four gold labels correctly. AlexNet and ResNet also captured Task, Dataset, and EvaluationMetric correctly; TechnicalMethod output did not contain "AlexNet" because the name was coined after the paper was published. The Transformer paper was run with verbose_v1 and showed extreme EvaluationMetric bias, leaving Task and Dataset empty. Systems papers (MapReduce, PageRank) produced very large TechnicalMethod counts (151 and 69 respectively), possibly because the system is described throughout the paper, and very few Dataset and EvaluationMetric sentences, possibly because these papers do not follow the standard ML benchmark structure.

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

> **What the method is (step by step):**
> 1. For each paper, manually identify the correct answer for each role. Example for Transformer: TechnicalMethod = "Transformer", Task = "machine translation", Dataset = "WMT", EvaluationMetric = "BLEU".
> 2. Run the pipeline on that paper. Collect all accepted sentences per role.
> 3. For each role: check whether any accepted sentence contains the gold label (case-insensitive substring match). Mark ○ if found, ✗ if not.
> 4. Result: a 3-paper × 4-role table (12 data points).
>
> **Why this is appropriate:**
> - No annotated dataset exists for this task. Standard precision/recall/F1 requires a gold-standard annotation for every sentence — you have none.
> - This method only requires knowing the correct answer per paper (easy to verify manually from the paper itself).
> - It is a **recall-oriented** check: it tells you whether the correct information appears anywhere in the output. For a prototype, the key question is "does the system find the right information at all?" — not "is every output sentence correct?"
> - Limitation: it does not measure precision (how much noise is in the output). That is a known limitation to discuss.
>
> **Link to background work:** Jain et al. [3] (SciREX) evaluated role extraction by checking whether predicted spans match annotated spans per role — a similar "is the right entity found?" approach.

A: No annotated sentence-level dataset exists for this task, so standard precision, recall, and F1 cannot be measured. Instead, I used a recall-oriented gold label check. For each of three papers, I manually identified one gold label per role — the answer I would expect the system to find (e.g. "Transformer" for TechnicalMethod, "BLEU" for EvaluationMetric). I then ran the pipeline and checked whether any accepted sentence contained that gold label as a substring. The result is a 3-paper × 4-role table (12 data points) with ○ or ✗. This approach seems appropriate for a prototype because the key question at this stage is whether the system finds the right information at all, not how precise the full output is. Jain et al. [3] used a similar role-based recall check in SciREX, evaluating whether predicted spans match the annotated entity per role. Success is defined as ≥ 10 of 12 correct (consistent with design.md section 8).

**Q10:** Fill in the gold label evaluation table. For each cell, write ○ (any accepted sentence contains the gold label) or × (not found).

> Gold terms and run results (from proto2/result/):
>
> | Paper | Gold TM | Gold Task | Gold Dataset | Gold EM |
> |---|---|---|---|---|
> | Transformer | "Transformer" | "machine translation" | "WMT" | "BLEU" |
> | BERT | "BERT" | "GLUE" or "SQuAD" | "BooksCorpus" or "Wikipedia" | "F1" or "accuracy" |
> | AlexNet (CNN) | note below | "object recognition" | "ImageNet" | "top-1" or "top-5" |
> | ResNet | "residual" | "image recognition" | "ImageNet" | "top-1" |
> | MapReduce | "MapReduce" | "distributed" | "TeraSort" | "seconds" |
> | Google Search | "PageRank" | "web search" | "million pages" | "quality" |
>
> **AlexNet naming note:** The 2012 paper does not use the name "AlexNet" — that name was coined later.
> Gold term for TM should be "convolutional" (or similar), not "AlexNet".
>
> Run results (○ = gold label found in any accepted sentence, ✗ = not found):

A:

| Paper | TechnicalMethod | Task | Dataset | EvaluationMetric |
|---|---|---|---|---|
| Transformer | ○ | ✗ | ✗ | ○ |
| BERT | ○ | ○ | ○ | ○ |
| AlexNet | ✗ (if gold="AlexNet") | ○ | ○ | ○ |

> Transformer ✗ for Task and Dataset: caused by verbose_v1 EvaluationMetric bias (Task=0 sentences, Dataset=0 sentences).
> AlexNet TM ✗: paper does not use the word "AlexNet". Change gold label to "convolutional" → ○.
> Write in your own words below what these results mean.

**Q11:** What do the evaluation results show? Which roles are easy and which are hard?

> Answer in two parts: (a) what the table shows overall, (b) role-by-role analysis.
>
> **(a) Overall:**
> BERT scored ○ on all 4 roles. This shows the pipeline can find all four types of methodology information in a well-structured ML paper using short labels.
> Transformer scored ✗ on Task and Dataset — but the cause is the hypothesis set (verbose_v1), not the paper. This shows that hypothesis choice has a large effect on output.
>
> **(b) Role-by-role — what tends to work and what does not:**
>
> - **TechnicalMethod** — usually ○. The method is named explicitly in dedicated sections (Abstract, Architecture). Many sentences describe it. 62 TM sentences in BERT, 51 in AlexNet, 51 in ResNet.
>
> - **Dataset** — usually ○ for ML papers. Papers have a dedicated "Dataset" or "Data" section. 15 sentences in BERT (BooksCorpus found), 11 in AlexNet (ImageNet found), 14 in ResNet. Weak for systems papers (MapReduce: 3 sentences, no standard benchmark).
>
> - **EvaluationMetric** — mixed. BERT ○ (F1 found in 13 sentences). AlexNet ○ (top-5 found in 4 sentences). But quantity is low — often only 4–13 sentences. Metric names appear in a small number of places (Experiment/Results tables).
>
> - **Task** — hardest role. BERT ○ (GLUE found, 23 sentences). AlexNet ○ (object recognition found, 6 sentences). For Transformer with verbose_v1: 0 sentences (all absorbed by EM). Task is often stated implicitly ("we solve X") rather than labelled, making it harder to classify.

A: BERT scored ○ on all four roles, which suggests that the pipeline can find all types of methodology information in a well-structured ML paper using short labels. AlexNet and ResNet also scored well. The Transformer scored ✗ on Task and Dataset, but this appears to be caused by the verbose_v1 hypothesis set, not by a failure to find the information in the paper. TechnicalMethod and Dataset tend to be the easier roles because they appear in dedicated sections (Architecture, Dataset) with explicit mentions. EvaluationMetric is found correctly but in small quantities (4–13 sentences), as metric names appear in few places. Task appears to be the most difficult role: it is often stated implicitly and produced the fewest sentences across all papers. Systems papers (MapReduce, PageRank) produced empty or weak Dataset and EvaluationMetric output, possibly because they do not follow the standard ML benchmark structure.

---

## 5. Weaknesses

**Q12:** What types of noise did you observe in the output? For each type, describe the cause.

> Write as a numbered list. For each: name the type, give the specific example from the runs, explain why the model classifies it incorrectly.
>
> **(1) Introduction noise — other papers' methods:**
> Example from BERT: the sentence `"The feature-based approach, such as ELMo..."` scored 0.87 as TechnicalMethod.
> Cause: The Introduction describes prior work to motivate BERT. The NLI model sees "feature-based approach" and correctly judges it as a technical method — but it is another paper's method, not BERT's.
> Effect from testing: excluding Introduction on BERT reduced TechnicalMethod from 62 → 54 (-8) and Task from 23 → 17 (-6). But Introduction also contains signal about BERT itself, so excluding it entirely loses correct information.
>
> **(2) Quoted / example text:**
> Example from Google Search paper: `"you looked at a lot of pages from my Web site."` was classified as Task.
> Cause: This is a quoted user query used as an example in the paper. The NLI model reads it as a description of a task. The model has no way to distinguish quoted strings from factual claims.
>
> **(3) Author contributions (GROBID artefact):**
> GROBID sometimes includes author contribution text in the abstract element. Example: a sentence like "Niki designed, implemented, tuned and evaluated countless model variants" (Transformer paper, found in TechnicalMethod output) describes what a person did, not the technical method.
> Cause: GROBID extraction artefact — this text is in the XML abstract but is not part of the scientific content.
>
> **(4) Large output volume — hundreds of sentences per role:**
> MapReduce: 151 TechnicalMethod sentences. Transformer: 160 EvaluationMetric sentences.
> Cause: no upper limit on accepted sentences. Every sentence scoring ≥ 0.5 is included. For a long paper or a biased hypothesis set, this produces hundreds of sentences that are hard to use.

A: Four types of noise were observed. First, Introduction sections describe other papers' methods, which the NLI model incorrectly classifies as TechnicalMethod of the target paper. For example, "The feature-based approach, such as ELMo..." scored 0.87 as TechnicalMethod in the BERT paper. Excluding the Introduction on BERT reduced TechnicalMethod from 62 to 54 sentences, but also removed correct sentences about BERT itself, so full exclusion risks losing signal. Second, quoted or example text in the paper body is classified as a real claim. For example, "you looked at a lot of pages from my Web site." from the Google Search paper was classified as Task. Third, GROBID sometimes includes author contribution text in the abstract element. The sentence "Niki designed, implemented, tuned and evaluated countless model variants" appeared in the Transformer TechnicalMethod output. Fourth, the output volume can be very large. MapReduce produced 151 TechnicalMethod sentences and the Transformer produced 160 EvaluationMetric sentences, because there is no upper limit on accepted sentences.

---

## 6. Improvements for Proto3

**Q13:** What three improvements are planned for the next iteration? For each, explain why you expect it to help.

> Write as a numbered list. For each: (a) what you will add/change, (b) what problem it solves, (c) what evidence from proto2 makes you think it will help.
>
> **(1) First-person verb filter:**
> What: before or after NLI, check whether the sentence contains a first-person active verb — "we propose", "we introduce", "we present", "we use", "we train". Keep only sentences with such verbs as strong candidates. Third-person or passive sentences ("X has been used in prior work") are more likely to describe other papers.
> Problem it solves: Introduction noise (type 1 in Q12). The sentence "The feature-based approach, such as ELMo..." does not contain "we propose" — it would be filtered.
> Evidence: testing on BERT showed Introduction noise as the biggest remaining noise source after Related Work exclusion.
>
> **(2) Top-N selection by score × section weight:**
> What: instead of keeping all sentences with score ≥ 0.5, keep only the top N (e.g. N=3) per role, ranked by score multiplied by a section weight. Abstract and Methods sections get a higher weight than Introduction.
> Problem it solves: large output volume (Q12 type 4). MapReduce had 151 TM sentences. Top-3 would give 3 sentences — usable output.
> Evidence: current output for Transformer has 160 EvaluationMetric sentences. The first one already contains "BLEU". Keeping all 160 adds no value.
>
> **(3) LLM term extraction:**
> What: take each accepted sentence and pass it to an LLM (e.g. Claude) with a prompt: "What is the [TechnicalMethod / Task / Dataset / EvaluationMetric] named in this sentence? Reply with a short noun phrase only."
> Problem it solves: the gap between sentence-level output and the pitch target. Current output: `"We propose a new simple network architecture, the Transformer, based solely on attention mechanisms..."`. Target output: `"Transformer"`.
> Evidence: the gold label evaluation (Q10) checks for substring match — it shows the correct information IS in the sentence. The missing step is extracting just the key term from that sentence.

A: Three improvements are planned for proto3. First, a usage NLI step will be added after role classification. Each accepted sentence is passed to a second NLI classifier with labels ["used by the authors", "mentioned as prior or related work"]. Only sentences classified as "used by the authors" are kept. This catches Introduction noise at the sentence level without additional keyword-based section rules — for example, "The feature-based approach, such as ELMo..." would be filtered as "mentioned as prior or related work" rather than kept as TechnicalMethod. As a lighter alternative, a first-person verb filter ("we propose", "we introduce", "we use") may be applied before NLI to reduce the candidate pool from 200+ to approximately 15–40 sentences. Second, Top-N selection by score × section weight will replace the current approach of keeping all accepted sentences. Instead of hundreds of sentences per role, only the top 3 per role will be kept, ranked by NLI score multiplied by a section weight (Abstract and Methods sections ranked higher than Introduction). This addresses the large output volume problem: MapReduce produced 151 TechnicalMethod sentences, but the top 3 by score are sufficient. Third, LLM term extraction will convert accepted sentences into short terms. The current output is full sentences such as "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms...". The target output for a useful profile is just "Transformer". The gold label evaluation suggests that the correct term is present in the accepted sentence; the missing step is extracting it with a prompt like "What is the TechnicalMethod named in this sentence?"

---

## 7. Technical Challenge

**Q14:** Why is zero-shot NLI classification on academic text technically challenging? Give two or three specific reasons.

> Write each reason as a paragraph. Use specific numbers and examples from the results.
>
> **(1) Hypothesis engineering is non-trivial and counter-intuitive:**
> You cannot just describe the label in plain English and expect better results. The experiment tested 4 hypothesis sets. Intuition says: more detailed descriptions → better accuracy. The result was the opposite. verbose_v1 (long description of TechnicalMethod, Dataset, EvaluationMetric, Task) caused EM to absorb nearly all sentences — 244/258 on BERT, 160/183 on Transformer. Task became 0. verbose_v3 shifted the bias to TechnicalMethod instead. Short labels (just `"technical method"`, `"dataset"`, etc.) achieved the best probe score (3/4) and the most balanced distribution across all runs. This required 4 iterations of design and systematic comparison to discover.
>
> **(2) Domain mismatch between NLI training data and scientific writing:**
> The model (`cross-encoder/nli-deberta-v3-small`) was trained on general-domain NLI benchmarks (e.g. SNLI, MultiNLI). Academic text is different: sentences are longer, more complex, and contain domain-specific terms, citation markers, and structure (e.g. section headings, figure references) that were not in the training data. Example: the sentence "The attention function can be described as mapping a query and a set of key-value pairs to an output" (Transformer) is grammatically complex and domain-specific. The model must judge whether this sentence entails "technical method" without ever having seen similar text during training.
>
> **(3) Noise is hard to separate from signal without task-specific knowledge:**
> The sentence "The feature-based approach, such as ELMo, uses the pre-trained representations as additional features" (BERT Introduction) describes ELMo, not BERT. But to the NLI model, it entails "technical method" with high confidence (0.87) — because it does describe a technical method. Distinguishing "this paper's method" from "another paper's method" requires understanding of who is the author and what the paper claims, which goes beyond what NLI can do. This is why BERT had 62 TechnicalMethod sentences when only a few describe BERT itself.

A: Zero-shot NLI classification on academic text is technically challenging for three reasons. First, hypothesis engineering is non-trivial and may seem counter-intuitive. More detailed label descriptions do not necessarily improve accuracy. Testing four hypothesis sets showed that verbose descriptions introduced strong label bias: verbose_v1 and verbose_v2 led to the EvaluationMetric label absorbing nearly all sentences (244 out of 258 on BERT, 160 out of 183 on Transformer), leaving Task and Dataset with 0 sentences. verbose_v3 shifted the bias to TechnicalMethod instead. Short labels achieved the best probe score (3/4) and the most balanced distribution across all papers. This required four iterations of design and systematic comparison to discover. Second, the model was trained on general-domain NLI benchmarks such as SNLI and MultiNLI, but academic writing is different. Sentences are longer, more complex, and contain domain-specific terms, citation markers, and figure references that were not in the training data. The model must classify sentences like "The attention function can be described as mapping a query and a set of key-value pairs to an output" without any task-specific training on scientific text. Third, the model may not be able to distinguish between this paper's methods and other papers' methods. The sentence "The feature-based approach, such as ELMo..." correctly entails "technical method" according to the NLI model — it does describe a method — but the method belongs to a different paper. This distinction may go beyond what NLI alone can do, as it requires understanding who the author is and what the paper claims.

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

## References

[1] B. J. Oates. 2006. *Researching Information Systems and Computing*. SAGE Publications, London.

[2] C. Pilkington and L. Pretorius. 2015. A conceptual model of the research methodology domain. In *Proceedings of the 7th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K 2015), Volume 2: KEOD*. SCITEPRESS – Science and Technology Publications, Setúbal, Portugal, 96–107. https://doi.org/10.5220/0005613100960107

[3] Jain, S., van Zuylen, M., Hajishirzi, H., and Beltagy, I. 2020. SciREX: A Challenge Dataset for Document-Level Information Extraction. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, Online, July 2020. Association for Computational Linguistics, 7506–7516. DOI: https://doi.org/10.18653/v1/2020.acl-main.670

[4] Yin, W., Hay, J., and Roth, D. 2019. Benchmarking Zero-shot Text Classification: Datasets, Evaluation and Entailment Approach. In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)*, Hong Kong, China, November 2019. Association for Computational Linguistics, 3914–3923. DOI: https://doi.org/10.18653/v1/D19-1404
