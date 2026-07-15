# prototype-memo.md

This file is a Q&A draft for you to fill in yourself.
Write your answer after each `A:` in your own words.
After you finish, use your answers as material for `prototype.md` (the PDF submission).

This document is about **proto2** (the zero-shot NLI pipeline, already implemented and
evaluated). **proto3** (document-level LLM extraction) is mentioned only briefly, as
work currently in progress — see Q3 and the last question in Section 7.

---

## 1. Template Statement

**Q1:** Which template are you using for this project?

> Reused directly from `report1/report.md` Ch1 §2: Template 12.1 (the NLP module
> template).

A:

---

## 2. Project Overview and Fit

**Q2:** What is the project about? Write one or two sentences.

> Template to fill in:
> "The project extracts [what] from [source] to help [target user] [goal]."
>
> Facts to use (from `report1/report.md` Ch1):
> - Goal: automatically extract research methodology from computing research papers.
> - Four roles: TechnicalMethod, Task, Dataset, EvaluationMetric.
> - Worked example: "Attention Is All You Need" → TechnicalMethod = Transformer,
>   Task = machine translation, Dataset = WMT, EvaluationMetric = BLEU.
> - Target users: computing students doing literature reviews; output should be
>   inspectable (real sentences, not just short terms, at this prototype stage).

A:

**Q3:** How does this prototype fit into the project as a whole?

> Facts to use (from `report1/report.md` Ch3 §5 Work Plan table):
> - This prototype (proto2, zero-shot NLI sentence classification) is the "Feature
>   Prototype" stage — implemented and evaluated before the Preliminary Report
>   submission (29 June).
> - The work plan's next stage ("July, post-submission") is to replace sentence-level
>   classification with document-level extraction using a long-context LLM. This is
>   proto3, and it is **currently in progress**: per `proto3/memo.md`, Stage 0–2
>   (parse XML, extract text, LLM extraction with Gemini `gemini-3.5-flash`) are
>   implemented in `proto3/3pipeline.ipynb`, but the 3-axis evaluation, the Related
>   Work ablation, and batch processing are not yet done.
> - Keep the proto3 mention brief here — one or two sentences framing it as "what
>   comes next," not a full description. The fuller "how you intend to improve it"
>   answer belongs in Section 7.

A:

---

## 3. Features Implemented

**Q4:** What did you implement? Write one sentence.

> Template to fill in:
> "The prototype takes [input] and [what it does] to produce [output]."
>
> Facts to use (from `report1/feature-prototype.md` §1 / `feature-prototype-memo.md`
> Q1):
> - Input: a TEI XML file produced by GROBID from a computing research paper.
> - Action: classifies each sentence by research methodology role using zero-shot NLI.
> - Output: a JSON object with four lists — TechnicalMethod, Task, Dataset,
>   EvaluationMetric.

A:

**Q5:** Why is sentence-level zero-shot NLI classification the most important feature
to prototype?

> Reused from `feature-prototype-memo.md` Q2:
> - Preprocessing (XML parsing, section filtering, sentence splitting) uses standard,
>   already-solved tools (ElementTree, spaCy).
> - Classification is different: it decides which sentences belong to which role.
>   Without it, you just have a list of sentences with no meaning attached — the role
>   assignment IS the output.
> - Zero-shot was the key design choice (no training data available). If it failed,
>   the alternative would need hundreds of annotated papers (Jain et al. [4] used
>   438). Showing zero-shot works is the proof the whole approach is viable.

A:

---

## 4. Algorithms, Techniques and Methods

**Q6:** Describe the pipeline from TEI XML to JSON output. List the main steps in
order.

> Reused from `feature-prototype-memo.md` Q3 (write as a numbered list, each step:
> what goes in, what comes out):
> - Step 1 — Load XML: parse with ElementTree, extract abstract + body `<div>`
>   elements → list of `{heading, text}` dicts.
> - Step 2 — Filter sections: skip References/Acknowledgements (`SKIP_HEADINGS`) and
>   Related Work + its subsections, tracked via the `n` attribute (`SKIP_KEYWORDS`).
> - Step 3 — Split and clean sentences: `pre_clean()` strips citation markers, spaCy
>   splits into sentences, `is_valid()` drops fragments (< 30 chars or no real word).
> - Step 4 — Classify: NLI classifier scores 4 candidate labels per sentence; if the
>   top label scores ≥ 0.5 (`THRESHOLD`), the sentence is added to that role's list in
>   `MethodologyProfile`.

A:

**Q7:** Which model did you use for zero-shot classification, and why?

> Reused from `feature-prototype-memo.md` Q4:
> - Model: `cross-encoder/nli-deberta-v3-small` (Hugging Face). Takes a premise (the
>   sentence) and a hypothesis (a label like "technical method"), scores entailment.
> - Why: DeBERTa is a strong NLI backbone; the `v3-small` variant fits Colab memory
>   (568 MB); the cross-encoder architecture scores premise+hypothesis jointly, more
>   accurately than bi-encoders.
> - Why zero-shot: no annotated dataset exists for this task; supervised training
>   would need hundreds of labeled papers (Jain et al. [4] used 438).

A:

**Q8:** What preprocessing and section filtering does the pipeline apply, and why?

> Reused from `feature-prototype-memo.md` Q5/Q6:
> - `pre_clean()` — strips inline citation markers like `[13]` or `[4, 27]` with a
>   regex, so spaCy does not split sentences at the bracket. Example:
>   `"The model outperforms [4, 27] the baseline."` → `"The model outperforms the
>   baseline."`
> - `is_valid()` — drops sentences shorter than 30 characters, or starting with `†`/
>   `‡` markers, or with no word of 3+ letters — removes bullets, lone numbers,
>   citation stubs.
> - Section filtering — excludes References/Acknowledgements (not methodology
>   content) and Related Work (describes other papers' methods; testing on BERT
>   showed 67→62 TechnicalMethod sentences, -5, after exclusion). All other body
>   sections are kept (not just Experiment/Results), because an earlier keyword-only
>   filter missed the Transformer paper's "Training Data" section entirely.

A:

---

## 5. Code Explanation

**Q9:** Quote and explain the sentence-splitting and cleaning code
(`proto2/2pipeline.ipynb`, "Step 0c — Sentence Splitting with spaCy").

> Actual code from the notebook:
> ```python
> def pre_clean(text: str) -> str:
>     return re.sub(r"\s*\[\d+(?:[,\s]*\d+)*\]\s*", " ", text).strip()
>
> def is_valid(text: str, min_len: int = 30) -> bool:
>     if len(text) < min_len:
>         return False
>     if text.startswith(("†", "‡")):
>         return False
>     return bool(re.search(r"[a-zA-Z]{3,}", text))
> ```
> Explain: what the regex in `pre_clean` matches (citation markers like `[13]` or
> `[4, 27]`), and what each of the three conditions in `is_valid` rejects (too short,
> footnote markers, no real word). Don't just paste the code — say what problem each
> line solves, using the before/after example from Q8.

A:

**Q10:** Quote and explain the classification and threshold logic
(`proto2/2pipeline.ipynb`, "Step 2 — Classify Sentences").

> Actual code from the notebook (trimmed to the decision logic):
> ```python
> LABELS = ["technical method", "dataset", "evaluation metric", "task"]
> THRESHOLD = 0.5
>
> results = classifier(
>     [c.sentence for c in sentences],
>     candidate_labels=LABELS,
>     batch_size=8,
> )
>
> for c, result in zip(sentences, results):
>     top_label = result["labels"][0]
>     top_score = result["scores"][0]
>     accepted = top_score >= THRESHOLD
>     if accepted:
>         if top_label == "technical method":
>             profile.technical_method.append(c.sentence)
>         # ... same pattern for task / dataset / evaluation metric
> ```
> Explain: batched zero-shot classification call, how the top label + score are read
> from the result, and why a fixed 0.5 threshold decides acceptance (and note this is
> a simple, somewhat arbitrary cutoff — a known limitation, see Section 7).

A:

**Q11:** Is the code clear and readable? Is it high quality? Give concrete evidence.

> This question has no direct precedent in `feature-prototype-memo.md` (it is a new
> marking criterion) — answer needs your own reflection, but here is evidence
> available in the repo to cite:
> - Function names document intent directly (`pre_clean`, `is_valid`,
>   `MethodologyProfile`), and `is_valid`/`pre_clean` both have type-annotated
>   signatures (`text: str -> str`, `text: str, min_len: int = 30 -> bool`).
> - `proto2/pyproject.toml` configures `pyright` in `strict` type-checking mode and
>   `ruff` for linting (`select = ["E", "F", "I"]`) and formatting — i.e. the code is
>   checked by a strict type checker and a linter, not just run ad hoc.
> - Honest limitation to mention: this is notebook code (`2pipeline.ipynb`), so it
>   mixes exploratory/print-debugging output with the actual pipeline logic; there
>   are no automated tests for `pre_clean`/`is_valid` even though `pytest` is listed
>   as a dev dependency.

A:

---

## 6. Visual Representation / Demonstration

**Q12:** What does the system output for "Attention Is All You Need"? Describe the
result and note which hypothesis set was used.

> Reused from `feature-prototype-memo.md` Q7 (verbose_v1 run):
> - TechnicalMethod: 14 sentences — contains "Transformer".
> - Task: 0 sentences; Dataset: 0 sentences (verbose_v1's EvaluationMetric hypothesis
>   absorbed almost everything).
> - EvaluationMetric: 160 sentences — contains "BLEU".
> - Key point: hypothesis wording has a large effect on the output distribution; the
>   short-label runs (other papers) are far more balanced.

A:

**Q13:** Summarize the results across all six papers tested. What screenshot(s) or
table(s) will you include?

> Reused from `feature-prototype-memo.md` Q8 (sentence counts per role):
>
> | Paper | TM | Task | Dataset | EM | Hypothesis set |
> |---|---|---|---|---|---|
> | Transformer | 14 | 0 | 0 | 160 | verbose_v1 |
> | BERT | 62 | 23 | 15 | 13 | short |
> | AlexNet | 51 | 6 | 11 | 4 | short |
> | ResNet | 51 | 6 | 14 | 12 | short |
> | MapReduce | 151 | 24 | 3 | 5 | short |
> | Google Search | 69 | 21 | 8 | 29 | short |
>
> This table can be reused directly. For screenshots: `report1/report.md` Appendix A
> already has GitHub Projects roadmap screenshots — decide whether those are still
> relevant here, or whether a fresh screenshot of actual notebook output (e.g. the
> "Step 2 — Results Summary" cell) would better show the prototype "in action." This
> choice is new — no existing screenshot targets this pipeline's own output yet.

A:

---

## 7. Evaluation and Improvement

**Q14:** What evaluation method did you use, and why is it appropriate?

> Reused from `feature-prototype-memo.md` Q9:
> - Method: for each paper, manually identify one gold label per role; run the
>   pipeline; check whether any accepted sentence contains the gold label
>   (case-insensitive substring match); mark ○/✗.
> - Why appropriate: no annotated dataset exists for standard precision/recall/F1;
>   this recall-oriented check only needs the correct answer per paper, and it
>   answers the key prototype-stage question — "does the system find the right
>   information at all?"
> - Link to background: Jain et al. [4] (SciREX) used a similar per-role span-match
>   evaluation.
> - Known limitation: does not measure precision/noise in the output.

A:

**Q15:** What were the results, and what do they show?

> Reused from `feature-prototype-memo.md` Q10/Q11 and `report1/report.md` Appendix B
> (extended 6-paper evaluation):
> - Primary 3-paper table: BERT ○ on all 4 roles; Transformer ✗ Task, ✗ Dataset
>   (caused by verbose_v1 hypothesis bias, not a paper-content problem).
> - Extended 6-paper total: 18/24 (75%) — ML papers 13/16 (81%), systems papers 5/8
>   (63%). Per-paper failures: ResNet ✗ Task, MapReduce ✗ Task + Dataset, Google
>   Search ✗ TechnicalMethod ("PageRank" never appears in the TechnicalMethod output).
> - Role-by-role: TechnicalMethod and Dataset are usually easiest (dedicated
>   sections); Task is hardest (often stated implicitly); EvaluationMetric is found
>   but in low volume.

A:

**Q16:** What are the main limitations / types of noise observed?

> Reused from `feature-prototype-memo.md` Q12 (four noise types, each with a cause):
> 1. Introduction noise — other papers' methods classified as this paper's
>    TechnicalMethod (BERT: "The feature-based approach, such as ELMo..." scored 0.87).
> 2. Quoted/example text read as a real claim (Google Search: a quoted user query
>    classified as Task).
> 3. GROBID artefacts — author-contribution text leaking into the abstract element
>    (Transformer: "Niki designed, implemented..." appeared in TechnicalMethod).
> 4. Large output volume — no cap on accepted sentences (MapReduce: 151
>    TechnicalMethod sentences; Transformer: 160 EvaluationMetric sentences).

A:

**Q17:** How do you intend to improve the prototype? What is the next step, and what
is its current status?

> This is where proto3 belongs (facts from `proto3/memo.md`):
> - Direction: replace sentence-level NLI classification with **document-level
>   extraction using a long-context LLM** (Gemini `gemini-3.5-flash`, via the
>   `google-genai` SDK). The LLM reads the full paper as one document and returns one
>   answer + supporting evidence (section + verbatim quote) per role, instead of
>   accepting every sentence that scores above a threshold.
> - Why: proto2's approach is text classification, not information extraction — it
>   has no mechanism to pick the *one* right answer, no way to distinguish the
>   authors' own method from cited prior work, and its evaluation is recall-only
>   (10/12 means the gold term appeared somewhere in 100+ sentences, not that the
>   output itself was precise).
> - Current status: Stage 0 (parse XML) and Stage 1–2 (text extraction + LLM
>   extraction) are implemented in `proto3/3pipeline.ipynb`. Not yet implemented: the
>   3-axis evaluation (gold label match, human precision check, evidence check),
>   the Related Work ablation, and batch processing across all six papers. Frame this
>   as work in progress, not a finished result.

A:

---

## Reference: Hypothesis Set Comparison

Use these tables when writing the Demonstration and Algorithms answers.

### BERT paper (258 sentences)

| Set | Probe (4 gold correct) | TechnicalMethod | Task | Dataset | EvaluationMetric |
|---|---|---|---|---|---|
| short | **3/4** | 124 | 70 | 33 | 31 |
| verbose_v1 | 2/4 | 11 | 0 | 3 | 244 |
| verbose_v2 | 2/4 | 63 | 11 | 19 | 165 |
| verbose_v3 | 2/4 | 131 | 56 | 60 | 11 |

### Transformer paper (183 sentences)

| Set | Probe (4 gold correct) | TechnicalMethod | Task | Dataset | EvaluationMetric |
|---|---|---|---|---|---|
| short | **3/4** | — | — | — | — |
| verbose_v1 | 2/4 | 14 | 0 | 0 | 160 |

Finding: verbose hypotheses introduce strong label bias; short labels give the best
probe score and the most balanced distribution, across both papers.

## Reference: Gold Labels (6 papers)

| Paper | Gold TM | Gold Task | Gold Dataset | Gold EM |
|---|---|---|---|---|
| Transformer | "Transformer" | "machine translation" | "WMT" | "BLEU" |
| BERT | "BERT" | "GLUE" or "SQuAD" | "BooksCorpus" or "Wikipedia" | "F1" or "accuracy" |
| AlexNet | "convolutional" (paper predates the name "AlexNet") | "object recognition" | "ImageNet" | "top-1" or "top-5" |
| ResNet | "residual" | "image recognition" | "ImageNet" | "top-1" |
| MapReduce | "MapReduce" | "distributed" | "TeraSort" | "seconds" |
| Google Search | "PageRank" | "web search" | "million pages" | "quality" |

## References

[4] Jain, S., van Zuylen, M., Hajishirzi, H., and Beltagy, I. 2020. SciREX: A
Challenge Dataset for Document-Level Information Extraction. In *Proceedings of the
58th Annual Meeting of the Association for Computational Linguistics*, Online, July
2020. Association for Computational Linguistics, 7506–7516.
DOI: https://doi.org/10.18653/v1/2020.acl-main.670

[8] B. J. Oates. 2006. *Researching Information Systems and Computing*. SAGE
Publications, London.

[9] C. Pilkington and L. Pretorius. 2015. A conceptual model of the research
methodology domain. In *Proceedings of the 7th International Joint Conference on
Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K 2015),
Volume 2: KEOD*. SCITEPRESS – Science and Technology Publications, Setúbal, Portugal,
96–107. https://doi.org/10.5220/0005613100960107

[10] Yin, W., Hay, J., and Roth, D. 2019. Benchmarking Zero-shot Text Classification:
Datasets, Evaluation and Entailment Approach. In *Proceedings of the 2019 Conference
on Empirical Methods in Natural Language Processing and the 9th International Joint
Conference on Natural Language Processing (EMNLP-IJCNLP)*, Hong Kong, China, November
2019. Association for Computational Linguistics, 3914–3923.
DOI: https://doi.org/10.18653/v1/D19-1404
