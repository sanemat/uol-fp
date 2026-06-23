# design-memo.md

This file is a Q&A draft for you to fill in yourself.
Write your answer after each `A:` in your own words.
After you finish, use your answers as material for `design.md` (the PDF submission).

---

## 1. Project Overview

**Q1:** What does this system do? Write one or two sentences.

A: The system extracts research methodology from computing papers. A input is a PDF, a out put is a role-based profile.

**Q2:** Without this system, what does a researcher have to do manually? What is the problem?

A: A researcher have to categorize them by themselves manually. It's very slow.

**Q3:** What is the output of the system? Write a concrete example using "Attention Is All You Need".

A:

<pre>
Methodology:
    Technical method: Transformer
    Task: machine translation
    Dataset: WMT machine translation datasets
    EvaluationMetric: BLEU score
</pre>

Figure 1: Research Methodology from "Attention Is All You Need".


---

## 2. Template

**Q4:** Which template did you choose? (name and number) How does it match what your project does?

A: Template 12.1: Identifying research methodologies used in computing research. I extract research methodologies based on 4 roles.

---

## 3. Domain and Users

**Q5:** What is the domain of this project?

> Computing research + NLP. What kind of documents? What kind of problem? Be specific — not just "AI" but what activity the system supports.

A: Computing papers. The main targets are systems, ML, algorithm, HCI.

**Q6:** Who are the intended users? Describe their role, what they want to do, and how they would use this system.

> Think about: a researcher doing a literature survey, a student who needs to compare papers quickly, a reviewer who wants to see methodology at a glance. Pick the most realistic one and be specific.

A: A student who needs to compare many papers quickly. They read each paper to find the method, task, dataset, and metric. This takes time when reviewing many papers.

**Q7:** What do those users currently do by hand? What is difficult or time-consuming for them?

> A sentence from your literature review intro is useful here: "When people read papers, they often identify the technical method, task, dataset, and evaluation metric by themselves. This process is slow and manual, especially when they must review many papers."

A: When people read papers, they often identify the technical method, task, dataset, and evaluation metric by themselves. This process is slow and manual, especially when they must review many papers.

---

## 4. Design Justification

**Q8:** Why did you choose zero-shot NLI instead of supervised ML?

> Key fact from your literature review (Jain et al.): a supervised approach required 438 annotated papers and 4 PhD-level annotators. Your project has no annotated corpus. Yin et al. show that NLI can classify without task-specific training. Connect these two facts.

A: Jain et al. needed 438 annotated papers and 4 PhD-level annotators for a supervised approach. This project has no annotated corpus. Yin et al. show that NLI can classify text into many possible labels without task-specific training. Zero-shot NLI is a practical choice when training data does not exist.

**Q9:** Why did you choose these four roles — TechnicalMethod, Task, Dataset, EvaluationMetric?

> Two independent sources agree on these four types: (1) the ontology from Oates + Pilkington & Pretorius (your literature review section 2), and (2) Jain et al. who independently chose Dataset, Metric, Task, Method. Mention both.

A: Two independent sources agree on the same four types. First, the ontology from Oates and Pilkington & Pretorius suggests a structured vocabulary for research methodology, including TechnicalMethod, Task, Dataset, and EvaluationMetric. Second, Jain et al. (SciREX) independently chose the same four categories (Dataset, Metric, Task, Method) for their annotation scheme. The agreement of two independent sources supports the role vocabulary.

**Q10:** Why is "Design" (research design) out of scope?

> Two reasons from your notes: (1) research design is "harder and more subjective" (proto2/memo.md), and (2) a philosophical worldview "may not appear directly in paper text" (your literature review). Write in your own words.

A: Research design (e.g. experiment vs. survey) is subjective — two readers can assign different labels to the same paper. A philosophical worldview may not appear in the paper text at all. The four roles (TechnicalMethod, Task, Dataset, EvaluationMetric) appear as explicit phrases in the text and are easier to match automatically.

**Q11:** Why do you classify at the sentence level?

> From proto2/memo.md: "Hypothesis: sentences in a paper tend to focus on one role at a time. If this holds, sentence-level classification is sufficient." That is your design assumption — state it and say how you tested it.

A: The hypothesis is that sentences in a paper tend to describe one role at a time. A sentence about the dataset does not also describe the method. If this holds, sentence-level classification may be sufficient. Tested on 6 papers (Transformer, BERT, AlexNet, ResNet, MapReduce, Google Search). Results appear to support the assumption for ML papers. Systems papers (MapReduce, Google Search) showed weaker fit because they do not follow the standard ML benchmark structure.

**Q11b:** Why do you add a second NLI step to classify "used by this paper" vs "mentioned as prior work"?

> Issue #44 (proto2 design): a sentence like "The feature-based approach, such as ELMo..." describes another paper's method, not this paper's. Section-level filtering (skipping Related Work by heading) misses such sentences in the Introduction. A second NLI classifier with labels ["used by the authors", "mentioned as prior or related work"] catches this at the sentence level, without needing keyword-based section rules. Explain why this matters for precision.

A: A sentence like "The feature-based approach, such as ELMo, applies independently trained context representations" appears in the Introduction of BERT and describes another paper's method, not BERT's. Skipping the Related Work section by heading removes some noise, but not sentences in the Introduction that describe prior work. A second NLI step with labels ["used by the authors", "mentioned as prior or related work"] catches this at the sentence level without needing more keyword rules. This is expected to improve precision: fewer prior-work sentences may be assigned to TechnicalMethod.

---

## 5. Overall Structure

**Q12:** What are the main steps of the pipeline, in order?

> From issue #44 and your notebook: PDF → GROBID (local) → TEI XML → section filtering (skip References, Acknowledgements, Related Work by heading) → sentence splitting + pre-cleaning → (1) role NLI (TechnicalMethod / Task / Dataset / EvaluationMetric / other) → (2) usage NLI (used by this paper / mentioned as prior work) → section_factor weighting → top-k sentences per role → profile output. Write this in your own words.

A: PDF → GROBID (runs locally via Docker) → TEI XML → section filtering (skip References, Acknowledgements, Related Work by heading) → sentence splitting with spaCy + pre_clean() + is_valid() → role NLI (TechnicalMethod / Task / Dataset / EvaluationMetric) with threshold 0.5 → usage NLI (used by this paper / mentioned as prior work) → top-k sentences per role → MethodologyProfile output as JSON.

**Q13:** What is the input to the system? What format?

> A PDF of a computing research paper. After GROBID, the intermediate format is TEI XML. Note what information the XML contains (headings + body text per section).

A: A PDF of a computing research paper. After GROBID, the intermediate format is TEI XML. Each section has a heading attribute and body text. The abstract is separate from the body sections.

**Q14:** What is the final output? What does it look like?

> A role-based methodology profile. Write the structure: which 4 fields, what each field contains (sentences or terms), what format (JSON or printed text).

A: A MethodologyProfile with four fields: TechnicalMethod, Task, Dataset, EvaluationMetric. Each field is a list of sentences from the paper. Final output is a Python dict printed as JSON. Example:

```json
{
  "TechnicalMethod": ["We propose the Transformer..."],
  "Task": ["applied to machine translation..."],
  "Dataset": ["on the WMT 2014 English-German..."],
  "EvaluationMetric": ["achieving 28.4 BLEU on the WMT 2014..."]
}
```

The current prototype accepts all sentences above a threshold, which can result in a large number of output sentences per role (e.g. 100+ for TechnicalMethod). This is a known prototype limitation.

**Q15:** Which parts run locally and which run on Google Colab? Why?

> GROBID runs locally via Docker (it needs a server process). The NLI pipeline (sentence splitting, classification) runs on Colab because it needs a GPU and Python packages. Explain the split briefly.

A: GROBID runs locally via Docker because it is a Java server process (~1 GB). The NLI pipeline runs on Google Colab because it needs a GPU for fast inference and installs Python packages (transformers, torch, spacy). The TEI XML produced by GROBID is uploaded to Colab manually.

---

## 6. Key Technologies and Methods

**Q16:** What does GROBID do in this pipeline? Why is it needed?

> GROBID converts a PDF into TEI XML, separating the paper into structured sections (heading + text). Without it, you would have raw PDF text with no section boundaries — making section filtering hard.

A: GROBID converts a PDF into TEI XML, dividing the paper into sections with headings and body text. Without GROBID, the input would be raw PDF text with no section boundaries, making it difficult to filter by section (e.g. skip References or Related Work).

**Q17:** Which NLI model does the prototype use? Why is zero-shot classification sufficient here?

primary model is `cross-encoder/nli-deberta-v3-small` (~300 MB, fits free Colab GPU). 
Zero-shot is sufficient because: (1) no methodology-annotated corpus exists for general computing papers, and (2) Yin et al. show NLI generalises across label sets without task-specific training. Mention both the model choice and the reason for zero-shot.

A: The prototype uses `cross-encoder/nli-deberta-v3-small` (~300 MB, fits free Colab GPU). Zero-shot is therefore a reasonable approach because: (1) no methodology-annotated corpus exists for general computing papers, so supervised training is not straightforward; (2) Yin et al. show NLI can classify into many possible labels without task-specific training.

**Q18:** What pre-processing steps do you apply to sentences before classification? Why?

> From proto2/memo.md: (1) `pre_clean()` strips inline citation markers like [13] or [4, 27] before splitting. (2) `is_valid()` drops sentences shorter than 30 characters or without real words. Explain why each step matters.

A: (1) `pre_clean()` strips inline citation markers like [13] or [4, 27] before sentence splitting. Citations break sentence boundaries and cause the splitter to produce short fragments. (2) `is_valid()` drops sentences shorter than 30 characters or without at least one real word. This removes citation stubs (e.g. "[4, 27, 28]"), bullet symbols, and other formatting artefacts that would produce noisy classifications.

**Q19:** How did you design the hypothesis labels? What did you learn from the verbose vs short comparison?

> You tested 4 hypothesis sets (short, verbose_v1, verbose_v2, verbose_v3) on BERT paper (258 sentences). Short labels scored best on the 4-sentence probe (3/4 correct) and had the most balanced role distribution. Verbose hypotheses created strong bias (e.g. verbose_v1 assigned 244/258 sentences to EvaluationMetric). The proto2 design (issue #44) uses natural-language sentences as labels: e.g. "This sentence describes a method used in the paper." — and adds a 5th label "This sentence is background or other information." to capture noise without keyword-based section filtering. Summarise what you tried and what you concluded.

A: Tested 4 hypothesis sets on the BERT paper (258 sentences). Short labels (e.g. "technical method") scored best on the 4-sentence probe (3 of 4 correct) and had the most balanced distribution across roles. Verbose labels created strong role bias: verbose_v1 assigned 244 of 258 sentences to EvaluationMetric because the hypothesis was too broad. verbose_v3 was too narrow for EvaluationMetric and missed a sentence with "BLEU score." Conclusion: in this test, short labels appear to work better for this model.


---

## 7. Work Plan

**Q20:** List the major tasks.

> From your project board (github.com/users/sanemat/projects/3), grouped:
> - **Done:** background research, literature notes (Oates, Pilkington, Jain et al., Yin et al.), pitch, proto2 prototype (GROBID + NLI pipeline, section filtering, pre-processing, hypothesis comparison)
> - **Done:** Literature Review (Chapter 2)
> - **Ready / In progress:** Write Chapter 3 — Design (#68), own the code — proto2 pipeline (#44)
> - **Backlog:** Write Chapter 1 — Introduction (#70), Write Chapter 4 — Feature Prototype (#72), Record video MP4 3–5 min (#71)
> - **Submission:** Preliminary Report (#66, max 6000 words: Intro 1000 + Lit Review 2500 + Design 2000 + Feature Prototype 1500)
>
> Use this list to write your own task plan. Add actual dates.

A:
- Done: background research, literature notes (Oates, Pilkington, Jain, Yin, GROBID, CSO), pitch
- Done: proto2 prototype — GROBID pipeline, NLI classification, section filtering, pre-processing, hypothesis comparison
- Done: Literature Review (Chapter 2)
- In progress: Chapter 3 — Design (#68); proto2 pipeline refinement (#44)
- Backlog: Chapter 1 — Introduction (#70); Chapter 4 — Feature Prototype (#72); demonstration video MP4 3–5 min (#71)
- Submission: Preliminary Report (#66, max 6000 words: Intro 1000 + Lit Review 2500 + Design 2000 + Feature Prototype 1500)

**Q21:** What is the start week and end week for each task? What is the final submission deadline?

> Write the actual dates. The Preliminary Report submission (#66) is the next hard deadline — find the exact date in the course portal. You will turn Q20 + Q21 into a Gantt chart image for the PDF (does not count toward the word limit).

A: [Add actual dates from the course portal. Today is 2026-06-23. Suggested Gantt chart range: June–August 2026. Add a Gantt chart image for the PDF — it does not count toward the word limit.]

**Q22:** If the plan falls behind, what will you do? (contingency)

> Two types of contingency:
> (1) Prototype scope: the usage NLI step (used vs mentioned) and section_factor weighting are the most recent additions — they could be simplified or removed if time is short, without breaking the core role classification.

A: If behind schedule: (1) The usage NLI step (used vs. mentioned) and section_factor weighting are the newest additions. They can be simplified or removed without breaking the core role classification. (2) Chapter 4 (Feature Prototype) can be shortened to a brief description of planned improvements. The core pipeline (GROBID → role NLI → profile output) is the minimum deliverable.

---

## 8. Test and Evaluation

**Q23:** How will you measure whether the system extracts the correct terms?

> Method from proto2/memo.md: for each paper × role, check whether any accepted sentence contains the gold term (substring match). A role is correct if the gold term appears in at least one classified sentence.

A: For each paper × role, check whether any accepted sentence (score ≥ 0.5) contains the gold term as a substring. A role is correct (○) if at least one classified sentence contains the gold term. Incorrect (×) otherwise.

**Q24:** What are the gold labels? For each of the 3 papers, write the expected answer for all 4 roles.

> From proto2/memo.md:
> - Transformer paper: TechnicalMethod=Transformer, Task=machine translation, Dataset=WMT, EvaluationMetric=BLEU
> - BERT: TechnicalMethod=BERT, Task=GLUE / SQuAD, Dataset=BooksCorpus / Wikipedia, EvaluationMetric=accuracy / F1
> - AlexNet: TechnicalMethod=AlexNet, Task=image classification, Dataset=ImageNet, EvaluationMetric=top-1 / top-5 error
> Verify these against the actual papers before you write them in the report.

A: [Verify BERT and AlexNet gold labels against the actual papers before submitting.]

| Paper | TechnicalMethod | Task | Dataset | EvaluationMetric |
|---|---|---|---|---|
| Transformer | Transformer | machine translation | WMT | BLEU |
| BERT | BERT | GLUE / SQuAD | BooksCorpus / Wikipedia | accuracy / F1 |
| AlexNet | AlexNet | image classification | ImageNet | top-1 / top-5 error |

**Q25:** How will you present the results?

> A table: rows = 4 roles, columns = 3 papers, each cell = correct (○) or wrong (×). Total = 12 data points. You might also show the score and the matched sentence.

A: A table: rows = 4 roles, columns = 3 papers, each cell = ○ (correct) or × (wrong). Total = 12 data points. Also show the matching sentence and score for each ○ cell to make the result inspectable.

**Q26:** What counts as "success"?

> Decide your own threshold. Think about what a reasonable baseline is: if the system got 6/12 by chance, what does 10/12 mean? State a number and a reason.

A: Success = ≥ 10 of 12 correct. 10/12 suggests the system finds relevant sentences for most roles across most papers. Lower than 8/12 would indicate a systematic problem worth investigating.

**Q27:** What are the known limitations of this evaluation method?

> From proto2/memo.md and your own experience:
> - Only 3 papers — too small for statistical claims
> - Substring match is loose (a sentence can "contain" the gold term by accident)
> - Output is full sentences, not short terms — so the match is easier than it looks
> - Systems papers (MapReduce, Google Search) do not fit the 4-role structure

A:
- Only 3 papers — too small for statistical claims
- Substring match is loose — a sentence can "contain" the gold term without being about it
- Output is full sentences, not short terms — matching is easier than it appears
- The number of accepted sentences per role can be 100+; with that many sentences, substring match is nearly certain to succeed, which inflates the apparent accuracy
- Systems papers (MapReduce, Google Search) do not fit the 4-role structure; excluded from evaluation
- Gold labels were written manually by the author (no formal inter-annotator agreement)

**Q28:** If precision or recall is low, what will you do? (contingency)

> Think about: reporting the result honestly, analysing which role or paper type failed and why, treating the hypothesis set comparison as qualitative evidence of iteration even if final numbers are low.

A: Report the result honestly. Analyse which role or paper type failed and explain why (e.g. EvaluationMetric is hardest to capture; systems papers have no standard dataset). The hypothesis set comparison experiment (verbose vs short) is qualitative evidence of iteration and analysis, even if final numbers are low. The next prototype will address the large-output problem by applying document-level information extraction before role classification, reducing the number of candidates before NLI. Chapter 4 will describe this improvement plan in detail.

---

## Checklist (review before submission)

Requirements from design-requirement.txt:

- [ ] Project overview → Q1, Q2, Q3
- [ ] Template → Q4
- [ ] Domain and users → Q5, Q6, Q7
- [ ] Design justification → Q8, Q9, Q10, Q11, Q11b
- [ ] Overall structure → Q12, Q13, Q14, Q15
- [ ] Key technologies and methods → Q16, Q17, Q18, Q19, Q19b
- [ ] Work plan (Gantt) → Q20, Q21, Q22 (add chart as image in PDF)
- [ ] Test and evaluation → Q23, Q24, Q25, Q26, Q27, Q28

Marking criteria:
- [ ] Design is clear and high quality
- [ ] Concept is justified based on domain and users
- [ ] Workplan explained in enough detail
- [ ] Workplan is feasible
- [ ] Contingency plans exist → Q22, Q28
- [ ] Evaluation is sufficiently comprehensive
- [ ] Evaluation strategy is appropriate to the aims

## References

[1] B. J. Oates. 2006. *Researching Information Systems and Computing*. SAGE Publications, London.

[2] C. Pilkington and L. Pretorius. 2015. A conceptual model of the research methodology domain. In *Proceedings of the 7th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K 2015), Volume 2: KEOD*. SCITEPRESS – Science and Technology Publications, Setúbal, Portugal, 96–107. https://doi.org/10.5220/0005613100960107

[3] Jain, S., van Zuylen, M., Hajishirzi, H., and Beltagy, I. 2020. SciREX: A Challenge Dataset for Document-Level Information Extraction. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, Online, July 2020. Association for Computational Linguistics, 7506–7516. DOI: https://doi.org/10.18653/v1/2020.acl-main.670

[4] Yin, W., Hay, J., and Roth, D. 2019. Benchmarking Zero-shot Text Classification: Datasets, Evaluation and Entailment Approach. In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)*, Hong Kong, China, November 2019. Association for Computational Linguistics, 3914–3923. DOI: https://doi.org/10.18653/v1/D19-1404
