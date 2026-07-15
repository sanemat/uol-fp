# prototype-memo.md

This file is a Q&A draft for you to fill in yourself.
Write your answer after each `A:` in your own words.
After you finish, use your answers as material for `prototype.md` (the PDF submission).

This document is about **proto3** (document-level LLM extraction) — the main
prototype for this assignment. **proto2** (sentence-level zero-shot NLI) appears only
as background: the previous iteration that motivated proto3 (Q3) and the comparison
baseline for the next improvement (Q17).

---

## 1. Template Statement

**Q1:** Which template are you using for this project?

> Reused directly from `report1/report.md` Ch1 §2: Template 12.1 (the NLP module
> template).

A:

---

## 2. Project Overview and Fit

**Q2:** What is the project about, and what does the current prototype do? Write two
or three sentences.

> Opening sentence to reuse near-verbatim:
> "The current prototype is a document-level methodology extraction pipeline. It was
> developed after an earlier sentence-level zero-shot NLI prototype showed
> limitations in output noise and document-level context."
>
> Facts to add (from `proto3/memo.md` "What proto3 does"):
> - Goal: extract research methodology from a computing research paper — one answer
>   per role (TechnicalMethod, Task, Dataset, EvaluationMetric), each with supporting
>   evidence (section + verbatim quote).
> - Worked example: "Attention Is All You Need" → TechnicalMethod = "Transformer",
>   Task = "machine translation", Dataset = "WMT 2014 English-German",
>   EvaluationMetric = "BLEU".
> - Approach: schema-guided document-level information extraction with a long-context
>   LLM — not "send the paper to an LLM and trust the answer": every answer carries
>   evidence that can be checked against the source text.

A:

**Q3:** Why was this prototype (proto3) developed? What did the previous iteration
(proto2) show that motivated the change?

> Facts to use (from `proto3/memo.md` "Why proto2's approach fails"):
> - proto2 classified every sentence into one of four roles with NLI — text
>   classification, not information extraction.
> - Output volume: MapReduce produced 151 TechnicalMethod sentences. Not usable as an
>   "answer."
> - No mechanism to distinguish the authors' own method from methods cited from prior
>   work (e.g. BERT's Introduction cites ELMo, and NLI scored the ELMo sentence 0.87
>   as TechnicalMethod).
> - Evaluation was recall-only: 10/12 (or 18/24 across 6 papers) meant the gold term
>   appeared somewhere in 100+ sentences, not that the output itself was precise.
> - Threshold 0.5 was arbitrary, with no principled way to cut the output down.
> - Reframe: the real question is "what is the primary TechnicalMethod?" — closer to
>   QA/information extraction than sentence classification. Keep this as background —
>   one paragraph, not a full re-description of proto2 (that belongs to a previous
>   submission, `report1/feature-prototype.md`).

A:

---

## 3. Features Implemented

**Q4:** What did you implement? Write one sentence, then show the concrete output
shape.

> Template to fill in:
> "The prototype takes [input] and [what it does] to produce [output]."
>
> Facts to use (from `proto3/memo.md` "What proto3 does"):
> - Input: TEI XML of one computing research paper (from GROBID).
> - Action: reads the full paper as one document and extracts one answer per role,
>   using a schema-guided prompt to a long-context LLM.
> - Output: one JSON object per paper — for each of the four roles, an `answer` plus
>   an `evidence` object with `section` and `quote`. Example (Transformer paper):
>   ```json
>   {
>     "TechnicalMethod": {
>       "answer": "Transformer",
>       "evidence": {
>         "section": "Model Architecture",
>         "quote": "The Transformer is the first transduction model relying entirely on self-attention..."
>       }
>     }
>   }
>   ```
>   (full 4-role example in the Reference section below).

A:

**Q5:** Why is document-level extraction with evidence the most important feature to
prototype (rather than, say, the preprocessing steps)?

> Facts to use (from `proto3/memo.md` "What proto3 does" / "Why proto2's approach
> fails"):
> - Parsing XML and extracting section text (Stage 0-1) uses the same GROBID-based
>   approach as proto2 — already solved, not the novel part.
> - The novel part is Stage 2: turning a full paper into one structured, evidence-
>   backed answer per role. This is what makes the output usable — a single named
>   answer instead of a list of 14-160 candidate sentences.
> - The evidence field is not decorative: it is what makes the answer checkable
>   (see Q9's evidence-shape story) and what will make the evaluation in Section 7
>   possible.

A:

---

## 4. Algorithms, Techniques and Methods

**Q6:** Describe the pipeline from PDF to structured output. List the stages in
order.

> Reused from `proto3/memo.md` "Pipeline":
> ```
> PDF
>   → GROBID (Stage 0: parse sections, same as proto2)
>   → structured TEI document (Abstract + body sections, References/Acknowledgements skipped)
>   → Stage 1: concatenate section texts in reading order, no sentence-level filtering
>   → Stage 2: LLM extraction with a schema-guided prompt
>   → MethodologyProfile JSON (answer + evidence per role)
> ```
> Key difference from proto2: no sentence splitting, no per-sentence threshold — the
> LLM sees the (mostly) whole document and returns a decision, not a list of
> candidates.

A:

**Q7:** Why document-level extraction, and why feed the LLM the full paper instead of
a filtered excerpt?

> Reused from `proto3/memo.md` "Why document-level and why full paper":
> - Jain et al. (SciREX) [Jain et al. 2020]: "a significant amount of information can only be
>   gleaned from analyzing the full document." Dataset and EvaluationMetric typically
>   appear only in the Experiment section, not Abstract or Method — sending only a
>   subset recreates the recall gap document-level IE is meant to avoid.
> - A typical computing paper in plain text is 4,000-20,000 tokens — within range for
>   modern long-context LLMs without chunking:
>
>   | Model | Context | Cost |
>   |---|---|---|
>   | Gemini Flash | 1M tokens | cheap API |
>   | Claude Haiku | 200k tokens | cheap API |
>   | Llama 3.1 8B Instruct | 128k tokens | free (Colab GPU) |
>
> - Selected: Gemini (`gemini-3.5-flash`, via the `google-genai` SDK) — simplest Colab
>   setup (API key from Colab's built-in secret manager, no separate `.env`/`getpass`
>   flow, no extra API account needed).

A:

**Q8:** How does the prompt distinguish the authors' own method from prior work, and
how is the four-role schema enforced?

> This is the answer to "isn't this just prompting an LLM?" — the design choices are
> concrete, not accidental. Facts to use (from `proto3/memo.md` "Stage 2 — LLM
> extraction"):
> - The prompt names all four roles explicitly and gives a rule: "Use the authors'
>   own method, not methods cited from prior work" — directly targeting proto2's
>   biggest known failure (Q3/Q5).
> - It specifies the exact output shape (nested JSON, one object per role with
>   `answer` and `evidence.section`/`evidence.quote`) and requires the quote to be
>   copied verbatim, not paraphrased — so the answer can be checked against the
>   source text.
> - It tells the model to return `null` for both fields if a role is not present in
>   the paper, rather than guessing.
> - Full prompt text is in the Reference section below — quote the relevant rule
>   lines in your write-up rather than the whole prompt.

A:

---

## 5. Code Explanation

**Q9:** Quote and explain the extraction prompt template
(`proto3/3pipeline.ipynb`, "Stage 2b — Prompt Template").

> Actual prompt (from `proto3/memo.md`, matches the notebook's `PROMPT_TEMPLATE`
> cell):
> ```
> For each of the four roles below, return an object with:
> - "answer": the shortest identifying term (e.g. "Transformer", not "a novel attention-based model")
> - "evidence": an object with "section" (the section heading) and "quote" (one sentence quoted verbatim from the paper that supports the answer)
>
> Rules:
> - Use the authors' own method, not methods cited from prior work.
> - If a field is not present in the paper, return null for both "answer" and "evidence".
> - The "quote" must be copied verbatim from the paper text, not paraphrased.
> ```
> Explain: why `answer` is constrained to "shortest identifying term" (avoids the
> proto2 problem of getting whole sentences back instead of a usable label); why
> `evidence` is a nested object rather than a single string — this was not the
> original design (see Q10's bug story) — and why the verbatim-quote rule matters for
> the evidence check in Section 7.

A:

**Q10:** Quote and explain the Gemini call and response parsing
(`proto3/3pipeline.ipynb`, "Stage 2c — Call Gemini and Parse Response"), including the
evidence-shape bug you found during testing.

> Facts to use (from `proto3/memo.md`, note under the prompt):
> - The call sends `PROMPT_TEMPLATE` (with the paper text substituted in) to
>   `client.models.generate_content` and parses the JSON response with `json.loads`.
> - Bug found during actual testing on "Attention Is All You Need": an earlier prompt
>   version said "evidence" was a single quoted sentence but also said to "return the
>   section heading and one sentence quoted verbatim" — an internally inconsistent
>   instruction. Gemini resolved the ambiguity by returning `evidence` as one flat
>   string with the heading prepended (e.g. `"## Introduction In this work we
>   propose..."`), not the nested `{section, quote}` object the design intended.
> - Fix: the prompt was rewritten to make the nested shape explicit (see Q9), so
>   `evidence.section` and `evidence.quote` are reliably separate fields.
> - This is worth including as evidence of real testing and iteration, not just
>   design on paper — it directly answers "is this technically challenging?"

A:

**Q11:** Is the code clear and readable? Is it high quality? Give concrete evidence.

> No direct precedent for this question (new marking criterion) — needs your own
> reflection, but here is evidence available in the repo:
> - `proto3/pyproject.toml` configures `pyright` in `strict` type-checking mode and
>   `ruff` for linting (`select = ["E", "F", "I"]`) and formatting — the same strict
>   setup as proto2, now applied to the new pipeline.
> - The notebook is organized into named, ordered stages (Setup → Data Models → Stage
>   0 → Stage 1 → Stage 2 → Stage 2b → Stage 2c) as markdown headers, which makes the
>   pipeline structure visible directly in the table of contents.
> - Honest limitation to mention: this is still notebook code mixing exploratory
>   output with pipeline logic; there are no automated tests yet for the JSON-parsing
>   or evidence-validation logic, even though `pytest` is a listed dev dependency.

A:

---

## 6. Visual Representation / Demonstration

**Q12:** What does the output look like for "Attention Is All You Need"? Show the
full JSON and describe what it demonstrates.

> Full example (from `proto3/memo.md` "What proto3 does"; full JSON with all 4 roles
> is in the Reference section below):
> ```json
> {
>   "TechnicalMethod": {"answer": "Transformer", "evidence": {"section": "Model Architecture", "quote": "..."}},
>   "Task": {"answer": "machine translation", "evidence": {"section": "Abstract", "quote": "..."}},
>   "Dataset": {"answer": "WMT 2014 English-German", "evidence": {"section": "Abstract", "quote": "..."}},
>   "EvaluationMetric": {"answer": "BLEU", "evidence": {"section": "Results", "quote": "..."}}
> }
> ```
> Compare against proto2's output for the same paper (14 TechnicalMethod sentences, 0
> Task, 0 Dataset, 160 EvaluationMetric sentences — see Reference section) to make the
> improvement concrete: one checkable answer per role instead of a pile of sentences.

A:

**Q13:** What screenshot(s) or figure(s) will you include?

> Nothing existing targets proto3's own output yet — this is new work. Options to
> consider:
> - A screenshot of the Colab notebook's "Stage 2c" cell output, showing the raw
>   Gemini response and/or the parsed JSON for the Transformer paper.
> - A before/after diagram or table contrasting proto2's sentence-count output with
>   proto3's answer+evidence output (the JSON above vs. the 14/0/0/160 counts).
> - The pipeline diagram from Q6 (PDF → GROBID → LLM → JSON) as a process figure.

A:

---

## 7. Evaluation and Improvement

**Q14:** What evaluation method do you plan to use, and why is it appropriate?

> Reused from `proto3/memo.md` "Evaluation (3 axes)" — same 6 papers and gold labels
> as proto2:
> 1. **Gold label match** — does `answer` contain the gold label as a substring? Same
>    method as proto2, but applied to one answer per role instead of 100+ sentences —
>    much harder to pass than recall over a large candidate list.
> 2. **Human precision check** — is `answer` plausibly correct by human judgment?
>    Catches valid answers that don't match the gold label string, and wrong answers
>    that happen to match it.
> 3. **Evidence check** — does `evidence.quote` appear verbatim in the paper text?
>    Does it support `answer`? Is `evidence.section` consistent with the quote's
>    actual location? Is the evidence about the authors' own work, not prior work?
>    This directly targets the authorship-attribution problem from Q3.

A:

**Q15:** What is the current evaluation status, and what did the initial test show?

> Be honest about what has actually been done (from `proto3/memo.md` "Implementation
> status" and the Q10 bug story):
> - Only an initial, informal test on "Attention Is All You Need" has been run so
>   far — it surfaced the evidence-shape bug (Q10), which was then fixed by making
>   the prompt's output shape explicit.
> - The formal 3-axis evaluation (gold label match / human precision / evidence
>   check) across all six papers has **not** been run yet. Stage 0-2 are implemented
>   in `proto3/3pipeline.ipynb`; the evaluation script, the Related Work ablation, and
>   batch processing across `proto3/previouswork/` are not yet implemented.
> - Frame this as an honest limitation: the pipeline works end-to-end on one paper,
>   but its accuracy across the full paper set is not yet measured.

A:

**Q16:** How do you intend to improve the prototype next?

> Facts to use (from `proto3/memo.md` "Evaluation" and "Ablation"):
> - Run the 3-axis evaluation across all six papers (same set as proto2: Transformer,
>   BERT, AlexNet, ResNet, MapReduce, Google Search/PageRank) using the gold labels in
>   the Reference section below.
> - Compare the result against proto2's 18/24 (75%) recall-only result from
>   `report1/report.md` Appendix B — but note the comparison is not apples-to-apples:
>   proto3's gold-label check is against one answer per role, not against acceptance
>   anywhere in 100+ sentences, so a lower raw score could still represent a stronger
>   result.
> - Run the Related Work ablation (exclude vs. keep Related Work in the input text)
>   to test whether the extra context helps or introduces attribution noise (visible
>   via `evidence.section`).
> - Automate the evidence verbatim check (string search in paper text) as part of the
>   evaluation script, rather than checking by hand.

A:

---

## Reference: Full JSON Output Example (Transformer paper)

From `proto3/memo.md` "What proto3 does":

```json
{
  "TechnicalMethod": {
    "answer": "Transformer",
    "evidence": {
      "section": "Model Architecture",
      "quote": "The Transformer is the first transduction model relying entirely on self-attention to compute representations of its input and output without using sequence-aligned RNNs or convolution."
    }
  },
  "Task": {
    "answer": "machine translation",
    "evidence": {
      "section": "Abstract",
      "quote": "We evaluate on the WMT 2014 English-German and English-French translation tasks."
    }
  },
  "Dataset": {
    "answer": "WMT 2014 English-German",
    "evidence": {
      "section": "Abstract",
      "quote": "We evaluate on the WMT 2014 English-German and English-French translation tasks."
    }
  },
  "EvaluationMetric": {
    "answer": "BLEU",
    "evidence": {
      "section": "Results",
      "quote": "Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task."
    }
  }
}
```

## Reference: Full Extraction Prompt

From `proto3/memo.md` "Stage 2 — LLM extraction":

```
You are extracting research methodology from a computing research paper.

For each of the four roles below, return an object with:
- "answer": the shortest identifying term (e.g. "Transformer", not "a novel attention-based model")
- "evidence": an object with "section" (the section heading) and "quote" (one sentence quoted verbatim from the paper that supports the answer)

Roles:
- TechnicalMethod: the main method, model, algorithm, or system proposed by the authors
- Task: the research task or problem being addressed
- Dataset: the dataset used for training or evaluation
- EvaluationMetric: the metric used to report results

Rules:
- Use the authors' own method, not methods cited from prior work.
- If a field is not present in the paper, return null for both "answer" and "evidence".
- The "quote" must be copied verbatim from the paper text, not paraphrased.
- Return only the JSON object, no explanation, in this exact shape:

{
  "TechnicalMethod": {"answer": "...", "evidence": {"section": "...", "quote": "..."}},
  "Task": {"answer": "...", "evidence": {"section": "...", "quote": "..."}},
  "Dataset": {"answer": "...", "evidence": {"section": "...", "quote": "..."}},
  "EvaluationMetric": {"answer": "...", "evidence": {"section": "...", "quote": "..."}}
}

Paper text:
{paper_text}
```

## Reference: proto2 Background Data (for the "why proto3" and "compare against
proto2" answers)

### proto2 sentence counts (6 papers)

| Paper | TM | Task | Dataset | EM | Hypothesis set |
|---|---|---|---|---|---|
| Transformer | 14 | 0 | 0 | 160 | verbose_v1 |
| BERT | 62 | 23 | 15 | 13 | short |
| AlexNet | 51 | 6 | 11 | 4 | short |
| ResNet | 51 | 6 | 14 | 12 | short |
| MapReduce | 151 | 24 | 3 | 5 | short |
| Google Search | 69 | 21 | 8 | 29 | short |

### proto2 extended evaluation result (from `report1/report.md` Appendix B)

Total: 18/24 (75%) — ML papers 13/16 (81%), systems papers 5/8 (63%). Failures: ResNet
✗ Task, MapReduce ✗ Task + Dataset, Google Search ✗ TechnicalMethod ("PageRank" never
appears in the TechnicalMethod output).

### Gold labels (6 papers) — same set used by proto2 and planned for proto3

| Paper | Gold TM | Gold Task | Gold Dataset | Gold EM |
|---|---|---|---|---|
| Transformer | "Transformer" | "machine translation" | "WMT" | "BLEU" |
| BERT | "BERT" | "GLUE" or "SQuAD" | "BooksCorpus" or "Wikipedia" | "F1" or "accuracy" |
| AlexNet | "convolutional" (paper predates the name "AlexNet") | "object recognition" | "ImageNet" | "top-1" or "top-5" |
| ResNet | "residual" | "image recognition" | "ImageNet" | "top-1" |
| MapReduce | "MapReduce" | "distributed" | "TeraSort" | "seconds" |
| Google Search | "PageRank" | "web search" | "million pages" | "quality" |

## References

[Alyafeai et al. 2025] Zaid Alyafeai, Maged Saeed Al-shaibani, and Bernard Ghanem.
2025. MOLE: Metadata Extraction and Validation in Scientific Papers Using LLMs. In
*Findings of the Association for Computational Linguistics: EMNLP 2025*, Suzhou,
China. Association for Computational Linguistics, 12236–12264.
https://doi.org/10.18653/v1/2025.findings-emnlp.655

[Dagdelen et al. 2024] John Dagdelen, Alexander Dunn, Sanghoon Lee, Nicholas Walker,
Andrew S. Rosen, Gerbrand Ceder, Kristin A. Persson, and Anubhav Jain. 2024.
Structured information extraction from scientific text with large language models.
*Nature Communications* 15 (2024), 1418. DOI: https://doi.org/10.1038/s41467-024-45563-x

[He et al. 2023] Pengcheng He, Jianfeng Gao, and Weizhu Chen. 2023. DeBERTaV3:
Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled
Embedding Sharing. In *The Eleventh International Conference on Learning
Representations (ICLR 2023)*, Kigali, Rwanda.
https://doi.org/10.48550/arXiv.2111.09543

[Jain et al. 2020] Sarthak Jain, Madeleine Van Zuylen, Hannaneh Hajishirzi, and Iz
Beltagy. 2020. SciREX: A Challenge Dataset for Document-Level Information Extraction.
In *Proceedings of the 58th Annual Meeting of the Association for Computational
Linguistics*, Online, July 2020. Association for Computational Linguistics,
7506–7516. DOI: https://doi.org/10.18653/v1/2020.acl-main.670

[Ma et al. 2023] Yubo Ma, Yixin Cao, YongChing Hong, and Aixin Sun. 2023. Large
Language Model Is Not a Good Few-shot Information Extractor, but a Good Reranker for
Hard Samples! In *Findings of the Association for Computational Linguistics: EMNLP
2023*. Association for Computational Linguistics.
DOI: https://doi.org/10.48550/arXiv.2303.08559

[Polak and Morgan 2024] Maciej P. Polak and Dane Morgan. 2024. Extracting accurate
materials data from research papers with conversational language models and prompt
engineering. *Nature Communications* 15 (2024), 1569.
DOI: https://doi.org/10.1038/s41467-024-45914-8

[Sainz et al. 2024] Oscar Sainz, Iker García-Ferrero, Rodrigo Agerri, Oier Lopez de
Lacalle, German Rigau, and Eneko Agirre. 2024. GoLLIE: Annotation Guidelines Improve
Zero-Shot Information-Extraction. In *The Twelfth International Conference on
Learning Representations (ICLR 2024)*.
DOI: https://doi.org/10.48550/arXiv.2310.03668

[Zheng et al. 2024] Hanwen Zheng, Sijia Wang, and Lifu Huang. 2024. A Comprehensive
Survey on Document-Level Information Extraction. In *Proceedings of the Workshop on
the Future of Event Detection (FuturED)*, Miami, Florida, November 2024. Association
for Computational Linguistics, 58–72. DOI: https://doi.org/10.18653/v1/2024.futured-1.6
