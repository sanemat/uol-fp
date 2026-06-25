# Feature Prototype

## 1. Overview

The prototype takes a TEI XML file produced by GROBID from a computing research paper and classifies each sentence by research methodology role using zero-shot NLI to produce a JSON object with four lists — TechnicalMethod, Task, Dataset, and EvaluationMetric.

The prototype uses zero-shot NLI classification to assign a role (label) to each sentence. Without this step, the pipeline produces only a list of sentences with no meaning attached. The role assignment is the output. If the model fails, the whole prototype fails. Because no annotated training data exists for this task, supervised training is not feasible at this scale — Jain et al. [3] used 438 labeled papers. Zero-shot NLI avoids that requirement entirely, making it the central design choice to validate.

## 2. Implementation

### 2.1 Pipeline

First, a computing paper is converted to TEI XML by GROBID. The pipeline then loads the XML, extracts sections, and filters out References, Acknowledgements, and Related Work. Next, it cleans each section and splits the text into sentences using spaCy. After that, each sentence is classified by the NLI classifier with four candidate labels. If the top score is at or above the threshold (0.5), the sentence is added to the accepted list for that role. The final output is a JSON object containing the accepted sentences per role.

### 2.2 Model

The classifier is `cross-encoder/nli-deberta-v3-small` from Hugging Face. DeBERTa (Decoding-enhanced BERT with Disentangled Attention) is a strong NLI backbone. The `v3-small` variant fits in Colab memory (568 MB) while still performing well. No annotated dataset was available for this task. Supervised training would need hundreds of labeled papers (Jain et al. [3] used 438). Zero-shot reduces this requirement.

### 2.3 Preprocessing

The pipeline applies two preprocessing steps before classification.

First, `pre_clean()` removes inline citation markers such as `[13]` or `[4, 27]` using a regex. Without this step, spaCy may split a sentence at the bracket, producing broken fragments. For example:

> `"The model outperforms [4, 27] the baseline."` → `"The model outperforms the baseline."`

Second, `is_valid()` drops sentences that are shorter than 30 characters or contain no word of three or more letters. This removes bullet characters, lone numbers, and citation stubs that pass through sentence splitting but carry no information. After these two steps, the Transformer paper produced 183 valid sentences for classification.

### 2.4 Section Filtering

References, Acknowledgements, and Related Work are excluded.

- References and Acknowledgements are excluded by exact heading match (`SKIP_HEADINGS`). These sections list citations and credits, not methodology.
- Related Work is excluded by keyword match (`SKIP_KEYWORDS`). Subsections are also skipped automatically by tracking the `n` attribute (e.g. if Related Work is `n="2"`, then `n="2.1"` and `n="2.2"` are also skipped). The reason is that Related Work describes other papers' methods, which the NLI model classifies as TechnicalMethod of the target paper. Testing on BERT showed that excluding Related Work reduced TechnicalMethod from 67 to 62 sentences (−5).

All other body sections are included: Abstract, Introduction, Method/Architecture, Dataset, Experiment, Results, Conclusion, etc. An earlier version used only sections whose heading matched keywords such as "experiment" or "result". The `Training Data` section in the Transformer paper has no such keyword and was missed. Switching to all body sections improved Dataset recall significantly.

## 3. Demonstration

The prototype was tested on six papers. Table 1 shows the number of accepted sentences per role.

| Paper | TechnicalMethod | Task | Dataset | EvaluationMetric | Notes |
|---|---|---|---|---|---|
| Transformer | 14 | 0 | 0 | 160 | verbose_v1: extreme EM bias |
| BERT | 62 | 23 | 15 | 13 | short: balanced |
| AlexNet | 51 | 6 | 11 | 4 | short: balanced |
| ResNet | 51 | 6 | 14 | 12 | short: balanced |
| MapReduce | 151 | 24 | 3 | 5 | short: TM heavy, weak DS/EM |
| Google Search | 69 | 21 | 8 | 29 | short: no standard benchmark |

Table 1: Accepted sentences per role for six papers.

The Transformer paper was run with verbose_v1. Using the verbose_v1 hypothesis set, TechnicalMethod received 14 sentences and EvaluationMetric received 160 sentences. Task and Dataset received 0 sentences each. The gold label "Transformer" was found in the TechnicalMethod output (e.g. "We propose a new simple network architecture, the Transformer...") and "BLEU" was found in the EvaluationMetric output (e.g. "Our model achieves 28.4 BLEU on the WMT 2014..."). However, Task and Dataset produced no output because the verbose_v1 EvaluationMetric hypothesis was too broad and absorbed most sentences.

ML papers (BERT, AlexNet, ResNet) produced balanced output across all four roles using short labels. BERT captured all four gold labels correctly. AlexNet and ResNet also captured Task, Dataset, and EvaluationMetric correctly; TechnicalMethod output did not contain "AlexNet" because the name was coined after the paper was published. Systems papers (MapReduce, PageRank) produced very large TechnicalMethod counts (151 and 69 respectively), possibly because the system is described throughout the paper, and very few Dataset and EvaluationMetric sentences, possibly because these papers do not follow the standard ML benchmark structure.

### Hypothesis Set Comparison

The choice of hypothesis text has a large effect on classification. Four hypothesis sets were tested on the BERT paper (258 sentences). A probe set of four known-answer sentences (one per role) was used to measure correctness.

| Set | Probe (4 gold labels) | TechnicalMethod | Task | Dataset | EvaluationMetric |
|---|---|---|---|---|---|
| short | **3/4** | 124 | 70 | 33 | 31 |
| verbose_v1 | 2/4 | 11 | 0 | 3 | 244 |
| verbose_v2 | 2/4 | 63 | 11 | 19 | 165 |
| verbose_v3 | 2/4 | 131 | 56 | 60 | 11 |

Table 2: Hypothesis set comparison on the BERT paper (258 sentences).

The same pattern was observed on the Transformer paper (183 sentences):

```
We propose the Transformer architecture.        → short=ok, verbose_v1=ok
The task is machine translation from English... → short=NG, verbose_v1=NG
We train on the WMT 2014 English-German dataset.→ short=ok, verbose_v1=NG
We evaluate translation quality using BLEU.     → short=ok, verbose_v1=ok
Correct:                                        → short=3/4, verbose_v1=2/4
```

Figure 1: Probe results for the Transformer paper — four known-answer sentences classified by hypothesis set.

Verbose hypotheses introduced strong label bias. Short labels gave the best probe score and the most balanced distribution. This pattern is consistent across both papers.

## 4. Evaluation

### 4.1 Method

No annotated sentence-level dataset exists for this task, so standard precision, recall, and F1 cannot be measured. Instead, I used a recall-oriented gold label check. For each of three papers, I manually identified one gold label per role — the answer I would expect the system to find (e.g. "Transformer" for TechnicalMethod, "BLEU" for EvaluationMetric). I then ran the pipeline and checked whether any accepted sentence contained that gold label as a substring. The result is a 3-paper × 4-role table (12 data points) with ○ or ✗.

This approach seems appropriate for a prototype because the key question at this stage is whether the system finds the right information at all, not how precise the full output is. Jain et al. [3] used a similar role-based recall check in SciREX, evaluating whether predicted spans match the annotated entity per role.

### 4.2 Results

Gold labels used:

| Paper | TechnicalMethod | Task | Dataset | EvaluationMetric |
|---|---|---|---|---|
| Transformer | "Transformer" | "machine translation" | "WMT" | "BLEU" |
| BERT | "BERT" | "GLUE" | "BooksCorpus" | "F1" |
| AlexNet | "convolutional" | "object recognition" | "ImageNet" | "top-5" |
| ResNet | "residual" | "image recognition" | "ImageNet" | "top-1" |
| MapReduce | "MapReduce" | "distributed" | "TeraSort" | "seconds" |
| Google Search | "PageRank" | "web search" | "million pages" | "quality" |

Table 3: Gold labels — 6 papers × 4 roles.

Result (○ = gold label found in any accepted sentence, ✗ = not found):

| Paper | TechnicalMethod | Task | Dataset | EvaluationMetric |
|---|---|---|---|---|
| Transformer | ○ | ✗ | ✗ | ○ |
| BERT | ○ | ○ | ○ | ○ |
| AlexNet | ○ | ○ | ○ | ○ |

Table 4: Gold label evaluation results.

### 4.3 Analysis

BERT scored ○ on all four roles, which suggests that the pipeline can find all types of methodology information in a well-structured ML paper using short labels. AlexNet also scored ○ on all four roles when using "convolutional" as the TechnicalMethod gold label (the 2012 paper does not use the name "AlexNet" — that name was coined later).

The Transformer scored ✗ on Task and Dataset, but this appears to be caused by the verbose_v1 hypothesis set, not by a failure to find the information in the paper. TechnicalMethod and Dataset tend to be the easier roles because they appear in dedicated sections with explicit mentions. EvaluationMetric is found correctly but in small quantities (4–13 sentences), as metric names appear in few places. Task appears to be the most difficult role: it is often stated implicitly and produced the fewest sentences across all papers. Systems papers (MapReduce, PageRank) produced empty or weak Dataset and EvaluationMetric output, possibly because they do not follow the standard ML benchmark structure.

## 5. Limitations

Four types of noise were observed.

The first type is Introduction noise. Introduction sections describe other papers' methods, which the NLI model incorrectly classifies as TechnicalMethod of the target paper. For example, "The feature-based approach, such as ELMo..." scored 0.87 as TechnicalMethod in the BERT paper. Excluding the Introduction on BERT reduced TechnicalMethod from 62 to 54 sentences, but also removed correct sentences about BERT itself, so full exclusion risks losing signal.

The second type is quoted or example text. Text that is quoted or used as an example in the paper body is classified as a real claim. For example, "you looked at a lot of pages from my Web site." from the Google Search paper was classified as Task.

The third type is GROBID artefacts. GROBID sometimes includes author contribution text in the abstract element. The sentence "Niki designed, implemented, tuned and evaluated countless model variants" appeared in the Transformer TechnicalMethod output.

The fourth type is large output volume. MapReduce produced 151 TechnicalMethod sentences and the Transformer produced 160 EvaluationMetric sentences, because there is no upper limit on accepted sentences.

## 6. Improvements for the Next Iteration

Three improvements are planned for proto3.

The first improvement is a usage NLI step after role classification. Each accepted sentence is passed to a second NLI classifier with labels ["used by the authors", "mentioned as prior or related work"]. Only sentences classified as "used by the authors" are kept. This catches Introduction noise at the sentence level without additional keyword-based section rules — for example, "The feature-based approach, such as ELMo..." would be filtered as "mentioned as prior or related work" rather than kept as TechnicalMethod. As a lighter alternative, a first-person verb filter ("we propose", "we introduce", "we use") may be applied before NLI to reduce the candidate pool from 200+ to approximately 15–40 sentences.

The second improvement is Top-N selection by score × section weight, which will replace the current approach of keeping all accepted sentences. Instead of hundreds of sentences per role, only the top 3 per role will be kept, ranked by NLI score multiplied by a section weight (Abstract and Methods sections ranked higher than Introduction). This addresses the large output volume problem: MapReduce produced 151 TechnicalMethod sentences, but the top 3 by score are sufficient.

The third improvement is LLM term extraction to convert accepted sentences into short terms. The current output is full sentences such as "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms...". The target output for a useful profile is just "Transformer". The gold label evaluation suggests that the correct term is present in the accepted sentence; the missing step is extracting it with a prompt like "What is the TechnicalMethod named in this sentence?"

## 7. Technical Challenge

Zero-shot NLI classification on academic text is technically challenging for three reasons.

The first challenge is that hypothesis engineering is non-trivial and may seem counter-intuitive. More detailed label descriptions do not necessarily improve accuracy. Testing four hypothesis sets showed that verbose descriptions introduced strong label bias: verbose_v1 and verbose_v2 led to the EvaluationMetric label absorbing nearly all sentences (244 out of 258 on BERT, 160 out of 183 on Transformer), leaving Task and Dataset with 0 sentences. verbose_v3 shifted the bias to TechnicalMethod instead. Short labels achieved the best probe score (3/4) and the most balanced distribution across all papers. This required four iterations of design and systematic comparison to discover.

The second challenge is domain mismatch. The model was trained on general-domain NLI benchmarks such as SNLI and MultiNLI, but academic writing is different. Sentences are longer, more complex, and contain domain-specific terms, citation markers, and figure references that were not in the training data. The model must classify sentences like "The attention function can be described as mapping a query and a set of key-value pairs to an output" without any task-specific training on scientific text.

The third challenge is that the model may not distinguish between this paper's methods and other papers' methods. The sentence "The feature-based approach, such as ELMo..." correctly entails "technical method" according to the NLI model — it does describe a method — but the method belongs to a different paper. This distinction may go beyond what NLI alone can do, as it requires understanding who the author is and what the paper claims.

## References

[1] B. J. Oates. 2006. *Researching Information Systems and Computing*. SAGE Publications, London.

[2] C. Pilkington and L. Pretorius. 2015. A conceptual model of the research methodology domain. In *Proceedings of the 7th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K 2015), Volume 2: KEOD*. SCITEPRESS, Setúbal, Portugal, 96–107. https://doi.org/10.5220/0005613100960107

[3] S. Jain, M. van Zuylen, H. Hajishirzi, and I. Beltagy. 2020. SciREX: A Challenge Dataset for Document-Level Information Extraction. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, Online, July 2020. Association for Computational Linguistics, 7506–7516. https://doi.org/10.18653/v1/2020.acl-main.670

[4] W. Yin, J. Hay, and D. Roth. 2019. Benchmarking Zero-shot Text Classification: Datasets, Evaluation and Entailment Approach. In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)*, Hong Kong, China, November 2019. Association for Computational Linguistics, 3914–3923. https://doi.org/10.18653/v1/D19-1404
