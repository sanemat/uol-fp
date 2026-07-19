# prototype-memo.md

This file is a Q&A draft for you to fill in yourself.
Write your answer after each `A:` in your own words.
After you finish, use your answers as material for `prototype.md` (the PDF submission).

This document is about **proto3** (document-level LLM extraction) — the main
prototype for this assignment. **proto2** (sentence-level zero-shot NLI) appears only
as background: the previous iteration that motivated proto3 (Q3) and the comparison
baseline for the next improvement (Q16).

---

## 1. Template Statement

**Q1:** Which template are you using for this project?

> Reused directly from `report1/report.md` Ch1 §2: Template 12.1 (the NLP module
> template).

A: This project addresses **Template 12.1** from the Natural Language Processing (NLP) module: Identifying research methodologies used in computing research.

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
> - How this fits into the project as a whole: the overall goal (per `CLAUDE.md`) is
>   automatically extracting research methodology from computing research papers using
>   LLMs. proto3 is the current iteration toward that goal — proto1 is an AI-drafted
>   reference only (not used in submissions), proto2 was the sentence-level NLI
>   attempt, proto3 reframes the task as document-level extraction.

A: The current prototype is a document-level methodology extraction. It was developed after an earlier sentence-level zero-shot NLI prototype showed limitations in output noise and document-level context. At least one answer per role (TechnicalMethod, Task, Dataset, and EvaluationMetric) with supporting evidence. This is a schema-guided document-level information extraction approach using a long-context LLM — every answer carries evidence that can be checked against the source text, not "send the paper to an LLM and trust the answer." For example, on "Attention Is All You Need," the prototype extracts TechnicalMethod = "Transformer", Task = "machine translation", Dataset = "WMT 2014 English-German", EvaluationMetric = "BLEU". This fits into the overall project goal (automatically extracting research methodology from computing research papers using LLMs) as the current iteration: proto1 is an AI-drafted reference only, proto2 was the sentence-level NLI attempt, and proto3 reframes the task as document-level extraction.

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

A: The previous prototype clasified MapReduce as TechnicalMethod correctly. But it clasified 151 sentences to TechnicalMethod. the real question is "what is the primary TechnicalMethod?" — closer to QA/information extraction than sentence classification. proto2 classified every sentence into one of four roles using zero-shot NLI — this is text classification, not information extraction. It also had no way to separate the authors' own method from methods cited from prior work: for example, BERT's Introduction cites ELMo, and NLI scored the ELMo sentence 0.87 as TechnicalMethod. Its evaluation was recall-only (10/12, or 18/24 across 6 papers) — the gold term only had to appear somewhere in 100+ sentences, not be the output itself — and the 0.5 threshold used to cut sentences was arbitrary, with no principled way to reduce the list.

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
>   an `evidence` object with `section` and `quote`. Example (Transformer paper, real
>   output from `proto3/baseline/transformer.json`, not a mockup):
>   ```json
>   {
>     "TechnicalMethod": {
>       "answer": "Transformer",
>       "evidence": {
>         "section": "Abstract",
>         "quote": "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely."
>       }
>     }
>   }
>   ```
>   (full 4-role example is the first entry in the Appendix below).

A: TEI XML of one computing research paper (from GROBID) and reads the full paper as one document and extracts one answer per role using a prompt to LLM to produce one JSON object per paper. Concrete output shape (Transformer paper, real output from `proto3/baseline/transformer.json`, not a mockup):
```json
{
  "TechnicalMethod": {
    "answer": "Transformer",
    "evidence": {
      "section": "Abstract",
      "quote": "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely."
    }
  }
}
```
(full 4-role example is the first entry in the Appendix below.)

**Q5:** Why is document-level extraction with evidence the most important feature to
prototype (rather than, say, the preprocessing steps)?

> Facts to use (from `proto3/memo.md` "What proto3 does" / "Why proto2's approach
> fails"):
> - Parsing XML and extracting section text (Stage 0-1) uses the same GROBID-based
>   approach as proto2 — already solved, not the core feature.
> - The core feature being prototyped is Stage 2: turning a full paper into one
>   structured, evidence-backed answer per role. This is what makes the output
>   usable — a single named answer instead of a list of 14-160 candidate sentences.
>   (Structured extraction with LLMs is not itself new — see [Dagdelen et al. 2024],
>   [Polak and Morgan 2024] — the prototype applies it to this project's specific
>   4-role methodology schema.)
> - The evidence field is not decorative: it is what makes the answer checkable
>   (see Q9's evidence-shape story) and what will make the evaluation in Section 7
>   possible.

A: Parsing XML using GROBID-based approach is not the core feature. The core is evidence-based structured answer per role. This shows one output instead of a list of one hundred of candidate sentences. Structured extraction with LLMs is not itself new (see [Dagdelen et al. 2024], [Polak and Morgan 2024]) — the prototype applies it to this project's specific 4-role methodology schema. The evidence field is not decorative: it is what makes the answer checkable (see Q9) and what makes the evaluation in Section 7 possible.

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
>
> The requirement text encourages diagrams for this section specifically — this
> five-stage pipeline is a natural candidate to draw here, not only as a figure in
> Section 6 (see Q13).

A:
```
PDF
  → GROBID (Stage 0: parse sections, same as proto2)
  → structured TEI document (Abstract + body sections, References/Acknowledgements skipped)
  → Stage 1: concatenate section texts in reading order, no sentence-level filtering
  → Stage 2: LLM extraction with a schema-guided prompt
  → MethodologyProfile JSON (answer + evidence per role)
```
Stage 0 skips References/Acknowledgements by heading (`proto3/3pipeline.ipynb`, "Stage 0 — Parse XML"):
```python
SKIP_HEADINGS = {"references", "acknowledgements", "acknowledgments"}
...
for div in root.findall(".//tei:body//tei:div", NS):
    heading = div.findtext("tei:head", namespaces=NS) or ""
    if heading.lower().strip() in SKIP_HEADINGS:
        continue
    ...
```
Stage 1 just joins section texts in order, no filtering:
```python
document_text = ""
for s in sections:
    document_text += f"## {s['heading']}\n\n{s['text']}\n\n"
```
The key difference from proto2 is that there is no sentence splitting and no per-sentence threshold — the LLM sees the (mostly) whole document and returns one decision per role, not a list of candidate sentences.

**Q7:** Why document-level extraction, and why feed the LLM the full paper instead of
a filtered excerpt?

> Reused from `proto3/memo.md` "Why document-level and why full paper":
> - Jain et al. (SciREX) [Jain et al. 2020]: "a significant amount of information can only be
>   gleaned from analyzing the full document." Dataset and EvaluationMetric typically
>   appear only in the Experiment section, not Abstract or Method — sending only a
>   subset recreates the recall gap document-level IE is meant to avoid.
> - The papers used in this prototype fit within the model's context window, so the
>   first version sends the full structured paper instead of introducing chunking or
>   retrieval. Model used: Gemini (`gemini-3.5-flash`, via the `google-genai` SDK).
> - Keep this short — "why full document" is the point being made here, not a
>   comparison against other LLMs or context-window sizes.

A: Document-level extraction is used because a significant amount of information can only be found by analyzing the full document [Jain et al. 2020] — Dataset and EvaluationMetric typically appear only in the Experiment section, not the Abstract or Method, so sending only a filtered excerpt would recreate the same recall gap document-level extraction is meant to avoid. The papers used in this prototype fit within the model's context window, so the full structured paper (`document_text` from Q6) is sent directly instead of introducing chunking or retrieval. Model setup (`proto3/3pipeline.ipynb`, "Stage 2 — LLM Extraction"):
```python
client = genai.Client(api_key=userdata.get("GEMINI_API_KEY"))
MODEL_NAME = "gemini-3.5-flash"
```

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

A: The prompt names all four roles explicitly and states one rule: use the authors' own method, not methods cited from prior work. This targets proto2's biggest known failure — e.g. BERT's Introduction citing ELMo, which proto2's NLI scored 0.87 as TechnicalMethod. The four-role schema is enforced by giving the exact output shape in the prompt: one JSON object per role with an `answer` and a nested `evidence` object (`section` and `quote`), and by requiring the quote to be copied verbatim rather than paraphrased, so each answer can be checked against the source text. If a role is not present in the paper, the model is told to return `null` for both fields instead of guessing.

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

A: Quote (from `proto3/3pipeline.ipynb`, "Stage 2b — Prompt Template"):
```
For each of the four roles below, return an object with:
- "answer": the shortest identifying term (e.g. "Transformer", not "a novel attention-based model")
- "evidence": an object with "section" (the section heading) and "quote" (one sentence quoted verbatim from the paper that supports the answer)

Rules:
- Use the authors' own method, not methods cited from prior work.
- If a field is not present in the paper, return null for both "answer" and "evidence".
- The "quote" must be copied verbatim from the paper text, not paraphrased.
```
`answer` is constrained to the shortest identifying term so the model returns a usable label ("Transformer") instead of a full sentence — this was proto2's core problem, where the "answer" was really 151 candidate sentences. `evidence` is a nested object rather than a single string so `section` and `quote` stay separate fields; this was not the first design (see Q10) — an earlier version asked for a single string and Gemini merged the heading and quote together, which is not checkable. The verbatim-quote rule matters because Section 7's evidence check needs to confirm the quote appears in the paper text word-for-word, not paraphrased text that cannot be searched for.

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
> - Reproducibility: the call now passes `config=types.GenerateContentConfig(temperature=0, seed=0)`.
>   Rationale: this is schema-guided extraction, not creative generation — the same
>   paper should yield the same answer, so sampling diversity (the point of a
>   non-zero temperature) is not wanted here. `seed` is an added determinism lever
>   alongside `temperature=0`.
> - Honest limitation: `temperature=0` and a fixed `seed` reduce but do not fully
>   guarantee identical output on every run — some LLM serving backends, including
>   Gemini's, can still vary slightly at temperature 0 (e.g. batching effects), so
>   exact reproducibility is not fully guaranteed.

A: Quote (from `proto3/3pipeline.ipynb`, "Stage 2c — Call Gemini and Parse Response"):
```python
response = client.models.generate_content(
    model=MODEL_NAME,
    contents=prompt,
    config=types.GenerateContentConfig(temperature=0, seed=0),
)

raw_text = response.text.strip()
if raw_text.startswith("```"):
    raw_text = raw_text.strip("`")
    raw_text = raw_text.removeprefix("json").strip()

profile = json.loads(raw_text)
```
This sends the full prompt (with the paper text substituted in) to `client.models.generate_content` and parses the response with `json.loads` after stripping any Markdown code fence Gemini adds around the JSON. `config=types.GenerateContentConfig(temperature=0, seed=0)` was added after testing — this is schema-guided extraction, not creative generation, so sampling diversity is not wanted, and a fixed seed is a second determinism lever alongside temperature 0. Even with both set, some LLM serving backends, including Gemini's, can still vary slightly at temperature 0 (e.g. batching effects), so exact reproducibility is not fully guaranteed. During testing on "Attention Is All You Need," an earlier prompt version asked for "evidence" as a single quoted sentence but also said to return the section heading and the quote together — an internally inconsistent instruction. Gemini resolved the ambiguity by returning `evidence` as one flat string with the heading prepended (e.g. `"## Introduction In this work we propose..."`), not the nested `{section, quote}` object the design intended. The fix was to rewrite the prompt to make the nested shape explicit (Q9), after which `evidence.section` and `evidence.quote` came back as reliably separate fields.

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
> - Second honest limitation: `proto3/baseline.ipynb` is a byte-identical duplicate of
>   `proto3/3pipeline.ipynb` (confirmed with `diff` — no differences), used to run the
>   pipeline once per paper via manual file upload to produce the six
>   `proto3/baseline/*.json` outputs. Its own Colab-badge cell still links to
>   `.../proto3/3pipeline.ipynb`, not its own filename — a small but concrete
>   inconsistency to weigh against the strict typing/linting setup above.

A: I use `pyright` in `strict` type-checking mode and `ruff` for linting (`select = ["E", "F", "I"]`) and formatting — the same strict setup as proto2, now applied to this new pipeline. The notebook is organized into named, ordered stages (Setup → Data Models → Stage 0 → Stage 1 → Stage 2 → Stage 2b → Stage 2c) as markdown headers, so the pipeline structure is visible directly in the table of contents. Two honest limitations: this is still notebook code mixing exploratory output with pipeline logic, and there are no automated tests yet for the JSON-parsing or evidence-validation logic, even though `pytest` is a listed dev dependency. Also, `proto3/baseline.ipynb` is a byte-identical duplicate of `proto3/3pipeline.ipynb`, used to run the pipeline once per paper via manual file upload to produce the six `proto3/baseline/*.json` outputs — its own Colab-badge cell still links to `.../proto3/3pipeline.ipynb`, not its own filename, a small but concrete inconsistency to weigh against the strict typing/linting setup above.

---

## 6. Visual Representation / Demonstration

**Q12:** What does the output look like for "Attention Is All You Need"? Show the
full JSON and describe what it demonstrates.

> Full example — use the real output, the first JSON block in the Appendix below
> (`proto3/baseline/transformer.json`), not a mockup:
> ```json
> {
>   "TechnicalMethod": {"answer": "Transformer", "evidence": {"section": "Abstract", "quote": "..."}},
>   "Task": {"answer": "machine translation", "evidence": {"section": "Abstract", "quote": "..."}},
>   "Dataset": {"answer": "WMT 2014 English-German", "evidence": {"section": "Training Data and Batching", "quote": "..."}},
>   "EvaluationMetric": {"answer": "BLEU", "evidence": {"section": "Machine Translation", "quote": "..."}}
> }
> ```
> Compare against proto2's output for the same paper (14 TechnicalMethod sentences, 0
> Task, 0 Dataset, 160 EvaluationMetric sentences — see Reference section) to make the
> improvement concrete: one checkable answer per role instead of a pile of sentences.

A: Full JSON (from `proto3/baseline/transformer.json`, real output, not a mockup):
```json
{
  "TechnicalMethod": {
    "answer": "Transformer",
    "evidence": {
      "section": "Abstract",
      "quote": "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely."
    }
  },
  "Task": {
    "answer": "machine translation",
    "evidence": {
      "section": "Abstract",
      "quote": "Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train."
    }
  },
  "Dataset": {
    "answer": "WMT 2014 English-German",
    "evidence": {
      "section": "Training Data and Batching",
      "quote": "We trained on the standard WMT 2014 English-German dataset consisting of about 4.5 million sentence pairs."
    }
  },
  "EvaluationMetric": {
    "answer": "BLEU",
    "evidence": {
      "section": "Machine Translation",
      "quote": "On the WMT 2014 English-to-German translation task, the big transformer model (Transformer (big) in Table 2) outperforms the best previously reported models (including ensembles) by more than 2.0 BLEU, establishing a new state-of-the-art BLEU score of 28.4."
    }
  }
}
```
This is the real output for "Attention Is All You Need," not a mockup — same file as `proto3/baseline/transformer.json`. Each of the four roles has one named answer plus a checkable evidence quote and its section. Compared to proto2's output for the same paper (14 TechnicalMethod sentences, 0 Task, 0 Dataset, 160 EvaluationMetric sentences), this is one answer per role instead of a pile of candidate sentences, each with a specific place in the paper to verify it against.

**Q13:** What screenshot(s) or figure(s) will you include?

> Nothing existing targets proto3's own output yet — this is new work. Options to
> consider:
> - A screenshot of the Colab notebook's "Stage 2c" cell output, showing the raw
>   Gemini response and/or the parsed JSON for the Transformer paper.
> - A before/after diagram or table contrasting proto2's sentence-count output with
>   proto3's answer+evidence output (the JSON above vs. the 14/0/0/160 counts).
> - The pipeline diagram from Q6 (PDF → GROBID → LLM → JSON) as a process figure.

A: A before/after screenshot pair contrasting proto2's sentence-count output with proto3's answer+evidence output, to make the improvement in Q12 concrete.

![proto3 output](<./Screenshot 2026-07-18 195120.png>)
![proto2 output](<./Screenshot 2026-07-18 195636.png>)

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
> 3. **Evidence check** — in priority order (1-2 are the research-relevant checks;
>    3-4 are grounding/implementation checks):
>    1. Does `evidence.quote` support `answer`?
>    2. Is the evidence about the target paper's own work, not prior work? This
>       directly targets the authorship-attribution problem from Q3.
>    3. Does `evidence.quote` appear verbatim in the input paper text?
>    4. Is `evidence.section` the correct section for that quote?

A: The evaluation uses the same 6 papers and gold labels as proto2, checked on three axes. First, gold label match: does `answer` contain the gold label as a substring — the same method as proto2, but now applied to one answer per role instead of over 100 candidate sentences, which is much harder to pass. Second, a human precision check: is `answer` plausibly correct by human judgment — this catches valid answers that do not match the gold string, and wrong answers that happen to match it. Third, an evidence check, in priority order: does `evidence.quote` support `answer`; is the evidence about the target paper's own work and not prior work (the authorship problem from Q3); does `evidence.quote` appear verbatim in the paper text; and is `evidence.section` the correct section for that quote. This method is appropriate because it checks precision, not just recall — proto2's recall-only score only showed the gold term appeared somewhere in the output, not that the output itself was a usable answer.

**Q15:** What is the current evaluation status, and what did the initial test show?

> Be honest about what has actually been done (from `proto3/memo.md` "Implementation
> status", the Q10 bug story, and `proto3/baseline/*.json`):
> - Initial, informal testing on "Attention Is All You Need" surfaced the
>   evidence-shape bug (Q10), fixed by making the prompt's output shape explicit.
> - Since then, Stage 0-2 has been run on all six papers in the set (same set as
>   proto2: Transformer, BERT, AlexNet, ResNet, MapReduce, PageRank) — the raw
>   answer+evidence JSON for each is saved in `proto3/baseline/*.json` (matches the
>   six examples in the Reference/Appendix section below).
> - The formal 3-axis evaluation (gold label match / human precision / evidence
>   check) against these six outputs has **not** been run yet — there is no scoring
>   script and no pass/fail count. The Related Work ablation and batch processing
>   across `proto3/previouswork/` are also not yet implemented.
> - Frame this as an honest limitation: extraction now runs end-to-end across the
>   whole six-paper set and produces output for every paper, but its accuracy has
>   not yet been measured against the gold labels.
> - Informal, quick check only (axis 1, gold-label substring match, done by hand
>   against `proto3/baseline/*.json` and the gold-label table in the Reference
>   section below — not the formal evaluation script, and no human-precision or
>   evidence-verification pass has been done):
>
>   | Paper | TM | Task | Dataset | EM | Score |
>   |---|---|---|---|---|---|
>   | Transformer | match | match | match | match | 4/4 |
>   | BERT | match | no | no | match | 2/4 |
>   | AlexNet | match | match | match | match | 4/4 |
>   | ResNet | match | no | match | match | 3/4 |
>   | MapReduce | match | no | no (null) | no | 1/4 |
>   | PageRank | no | no | match | no (null) | 1/4 |
>
>   Total: 15/24 (62.5%). Caveats worth stating: strict substring matching
>   penalizes near-misses (e.g. ResNet's answer "image classification" vs. gold
>   "image recognition" — arguably close but scored as a miss here); MapReduce and
>   PageRank both have one `null` field, which always scores as a miss under this
>   method. Treat this as a rough indicator to write from, not a result to cite as
>   final — the formal evaluation (Q16) is what would confirm or correct it.
> - Timing caveat: the six `proto3/baseline/*.json` files were generated before
>   `temperature=0`/`seed=0` were added to the Gemini call (see Q10). They were run
>   at the SDK's default sampling settings, not the now-deterministic config. If the
>   formal evaluation (Q16) is run against fresh output instead of these existing
>   files, scores could shift slightly from the 15/24 above.

A: Initial, informal testing on "Attention Is All You Need" surfaced the evidence-shape bug (Q10), fixed by making the prompt's output shape explicit. Since then, Stage 0–2 has been run on all six papers in the same set as proto2 (Transformer, BERT, AlexNet, ResNet, MapReduce, PageRank); the raw answer+evidence JSON for each is saved in `proto3/baseline/*.json`. The formal 3-axis evaluation from Q14 has not been run yet — there is no scoring script and no pass/fail count, and the Related Work ablation and batch processing across `proto3/previouswork/` are not yet implemented either.

As an informal, quick check only (gold-label substring match by hand, not the formal evaluation script, and no human-precision or evidence-verification pass):

| Paper | TM | Task | Dataset | EM | Score |
|---|---|---|---|---|---|
| Transformer | match | match | match | match | 4/4 |
| BERT | match | no | no | match | 2/4 |
| AlexNet | match | match | match | match | 4/4 |
| ResNet | match | no | match | match | 3/4 |
| MapReduce | match | no | no (null) | no | 1/4 |
| PageRank | no | no | match | no (null) | 1/4 |

Total: 15/24 (62.5%). Strict substring matching penalizes near misses — ResNet's answer "image classification" versus gold "image recognition" is arguably close but scored as a miss here — and MapReduce and PageRank each have one `null` field, which always scores as a miss under this method. This is a rough indicator, not a final result; the formal evaluation in Q16 would confirm or correct it. The six `proto3/baseline/*.json` files were also generated before `temperature=0`/`seed=0` were added to the Gemini call, so scores could shift slightly if the formal evaluation runs against fresh output instead of these existing files.

**Q16:** How do you intend to improve the prototype next?

> Facts to use (from `proto3/memo.md` "Evaluation" and "Ablation"):
> - Score the six outputs already in `proto3/baseline/*.json` against the gold labels
>   in the Reference section below, using the 3-axis method from Q14 — the raw
>   extraction is done (Q15); scoring it is the next step, not a re-run.
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

A: The next step is to score the six outputs already in `proto3/baseline/*.json` against the gold labels using the 3-axis method from Q14 — the extraction itself is done (Q15); scoring it is what remains. The result can then be compared against proto2's 18/24 (75%) recall-only result, though the comparison is not apples-to-apples: proto3's check is against one answer per role, not acceptance anywhere in 100+ sentences, so a lower raw score could still represent a stronger result. I also plan to run the Related Work ablation (exclude vs. keep Related Work in the input text) to test whether the extra context helps or introduces attribution noise, visible through `evidence.section`, and to automate the evidence verbatim check (string search in the paper text) as part of the evaluation script instead of checking by hand.

---

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

## Appendix

Real pipeline output, one block per paper, same order as the gold-label table above
(Transformer, AlexNet, BERT, MapReduce, Google Search/PageRank, ResNet) — matches
`proto3/baseline/*.json` exactly. This is the actual Stage 0-2 output referenced by
Q4, Q12, and Q15's informal score table, not a design mockup.

```json
{
  "TechnicalMethod": {
    "answer": "Transformer",
    "evidence": {
      "section": "Abstract",
      "quote": "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely."
    }
  },
  "Task": {
    "answer": "machine translation",
    "evidence": {
      "section": "Abstract",
      "quote": "Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train."
    }
  },
  "Dataset": {
    "answer": "WMT 2014 English-German",
    "evidence": {
      "section": "Training Data and Batching",
      "quote": "We trained on the standard WMT 2014 English-German dataset consisting of about 4.5 million sentence pairs."
    }
  },
  "EvaluationMetric": {
    "answer": "BLEU",
    "evidence": {
      "section": "Machine Translation",
      "quote": "On the WMT 2014 English-to-German translation task, the big transformer model (Transformer (big) in Table 2) outperforms the best previously reported models (including ensembles) by more than 2.0 BLEU, establishing a new state-of-the-art BLEU score of 28.4."
    }
  }
}
```

```json
{
  "TechnicalMethod": {
    "answer": "deep convolutional neural network",
    "evidence": {
      "section": "Abstract",
      "quote": "We trained a large, deep convolutional neural network to classify the 1.2 million high-resolution images in the ImageNet LSVRC-2010 contest into the 1000 different classes."
    }
  },
  "Task": {
    "answer": "object recognition",
    "evidence": {
      "section": "Introduction",
      "quote": "Current approaches to object recognition make essential use of machine learning methods."
    }
  },
  "Dataset": {
    "answer": "ImageNet",
    "evidence": {
      "section": "The Dataset",
      "quote": "ImageNet is a dataset of over 15 million labeled high-resolution images belonging to roughly 22,000 categories."
    }
  },
  "EvaluationMetric": {
    "answer": "top-1 and top-5 error rates",
    "evidence": {
      "section": "The Dataset",
      "quote": "On ImageNet, it is customary to report two error rates: top-1 and top-5, where the top-5 error rate is the fraction of test images for which the correct label is not among the five labels considered most probable by the model."
    }
  }
}
```

```json
{
  "TechnicalMethod": {
    "answer": "BERT",
    "evidence": {
      "section": "Abstract",
      "quote": "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers."
    }
  },
  "Task": {
    "answer": "Language model pre-training",
    "evidence": {
      "section": "Introduction",
      "quote": "Language model pre-training has been shown to be effective for improving many natural language processing tasks (Dai and  Le, 2015; Peters et al., 2018a; Radford et al., 2018; Howard and Ruder, 2018) ."
    }
  },
  "Dataset": {
    "answer": "SQuAD v1.1",
    "evidence": {
      "section": "SQuAD v1.1",
      "quote": "The Stanford Question Answering Dataset (SQuAD v1.1) is a collection of 100k crowdsourced question/answer pairs  (Rajpurkar et al., 2016) ."
    }
  },
  "EvaluationMetric": {
    "answer": "F1 score",
    "evidence": {
      "section": "SQuAD v1.1",
      "quote": "Our single BERT model outperforms the top ensemble system in terms of F1 score."
    }
  }
}
```

```json
{
  "TechnicalMethod": {
    "answer": "MapReduce",
    "evidence": {
      "section": "Abstract",
      "quote": "MapReduce is a programming model and an associated implementation for processing and generating large data sets."
    }
  },
  "Task": {
    "answer": "automatic parallelization and distribution of large-scale computations",
    "evidence": {
      "section": "Introduction",
      "quote": "The major contributions of this work are a simple and powerful interface that enables automatic parallelization and distribution of large-scale computations, combined with an implementation of this interface that achieves high performance on large clusters of commodity PCs."
    }
  },
  "Dataset": {
    "answer": null,
    "evidence": null
  },
  "EvaluationMetric": {
    "answer": "elapsed time",
    "evidence": {
      "section": "Effect of Backup Tasks",
      "quote": "The entire computation takes 1283 seconds, an increase of 44% in elapsed time."
    }
  }
}
```

```json
{
  "TechnicalMethod": {
    "answer": "Google",
    "evidence": {
      "section": "Abstract",
      "quote": "In this paper, we present Google, a prototype of a large-scale search engine which makes heavy use of the structure present in hypertext."
    }
  },
  "Task": {
    "answer": "information retrieval",
    "evidence": {
      "section": "Introduction",
      "quote": "The Web creates new challenges for information retrieval."
    }
  },
  "Dataset": {
    "answer": "24 million pages",
    "evidence": {
      "section": "Anchor-test",
      "quote": "In our current crawl of 24 million pages. we had over 259 million anchors which we indexed."
    }
  },
  "EvaluationMetric": {
    "answer": null,
    "evidence": null
  }
}
```

```json
{
  "TechnicalMethod": {
    "answer": "deep residual learning framework",
    "evidence": {
      "section": "Introduction",
      "quote": "In this paper, we address the degradation problem by introducing a deep residual learning framework."
    }
  },
  "Task": {
    "answer": "image classification",
    "evidence": {
      "section": "Introduction",
      "quote": "Deep convolutional neural networks [22, 21] have led to a series of breakthroughs for image classification [21, 49, 39]."
    }
  },
  "Dataset": {
    "answer": "ImageNet 2012 classification dataset",
    "evidence": {
      "section": "ImageNet Classification",
      "quote": "We evaluate our method on the ImageNet 2012 classification dataset [35] that consists of 1000 classes."
    }
  },
  "EvaluationMetric": {
    "answer": "top-1 and top-5 error rates",
    "evidence": {
      "section": "ImageNet Classification",
      "quote": "We evaluate both top-1 and top-5 error rates."
    }
  }
}
```
