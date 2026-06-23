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

A: A student needs to compare papars quickly.

**Q7:** What do those users currently do by hand? What is difficult or time-consuming for them?

> A sentence from your literature review intro is useful here: "When people read papers, they often identify the technical method, task, dataset, and evaluation metric by themselves. This process is slow and manual, especially when they must review many papers."

A: When people read papers, they often identify the technical method, task, dataset, and evaluation metric by themselves. This process is slow and manual, especially when they must review many papers.

---

## 4. Design Justification

**Q8:** Why did you choose zero-shot NLI instead of supervised ML?

> Key fact from your literature review (Jain et al.): a supervised approach required 438 annotated papers and 4 PhD-level annotators. Your project has no annotated corpus. Yin et al. show that NLI can classify without task-specific training. Connect these two facts.

A: Jain et al. a supervised approach required 438 annotated papers and 4 PhD-level annotators. Yin et al. show that NLI can classify without task-specific training. Connect these two facts.

**Q9:** Why did you choose these four roles — TechnicalMethod, Task, Dataset, EvaluationMetric?

> Two independent sources agree on these four types: (1) the ontology from Oates + Pilkington & Pretorius (your literature review section 2), and (2) Jain et al. who independently chose Dataset, Metric, Task, Method. Mention both.

A:

**Q10:** Why is "Design" (research design) out of scope?

> Two reasons from your notes: (1) research design is "harder and more subjective" (proto2/memo.md), and (2) a philosophical worldview "may not appear directly in paper text" (your literature review). Write in your own words.

A: research design is "harder and more subjective" (proto2/memo.md), and (2) a philosophical worldview "may not appear directly in paper text" (your literature review).

**Q11:** Why do you classify at the sentence level?

> From proto2/memo.md: "Hypothesis: sentences in a paper tend to focus on one role at a time. If this holds, sentence-level classification is sufficient." That is your design assumption — state it and say how you tested it.

A:

**Q11b:** Why do you add a second NLI step to classify "used by this paper" vs "mentioned as prior work"?

> Issue #44 (proto2 design): a sentence like "The feature-based approach, such as ELMo..." describes another paper's method, not this paper's. Section-level filtering (skipping Related Work by heading) misses such sentences in the Introduction. A second NLI classifier with labels ["used by the authors", "mentioned as prior or related work"] catches this at the sentence level, without needing keyword-based section rules. Explain why this matters for precision.

A:

---

## 5. Overall Structure

**Q12:** What are the main steps of the pipeline, in order?

> From issue #44 and your notebook: PDF → GROBID (local) → TEI XML → section filtering (skip References, Acknowledgements, Related Work by heading) → sentence splitting + pre-cleaning → (1) role NLI (TechnicalMethod / Task / Dataset / EvaluationMetric / other) → (2) usage NLI (used by this paper / mentioned as prior work) → section_factor weighting → top-k sentences per role → profile output. Write this in your own words.

A:

**Q13:** What is the input to the system? What format?

> A PDF of a computing research paper. After GROBID, the intermediate format is TEI XML. Note what information the XML contains (headings + body text per section).

A:

**Q14:** What is the final output? What does it look like?

> A role-based methodology profile. Write the structure: which 4 fields, what each field contains (sentences or terms), what format (JSON or printed text).

A:

**Q15:** Which parts run locally and which run on Google Colab? Why?

> GROBID runs locally via Docker (it needs a server process). The NLI pipeline (sentence splitting, classification) runs on Colab because it needs a GPU and Python packages. Explain the split briefly.

A:

---

## 6. Key Technologies and Methods

**Q16:** What does GROBID do in this pipeline? Why is it needed?

> GROBID converts a PDF into TEI XML, separating the paper into structured sections (heading + text). Without it, you would have raw PDF text with no section boundaries — making section filtering hard.

A:

**Q17:** Which NLI model does the prototype use? Why is zero-shot classification sufficient here?

primary model is `cross-encoder/nli-deberta-v3-small` (~300 MB, fits free Colab GPU). 
Zero-shot is sufficient because: (1) no methodology-annotated corpus exists for general computing papers, and (2) Yin et al. show NLI generalises across label sets without task-specific training. Mention both the model choice and the reason for zero-shot.

A:

**Q18:** What pre-processing steps do you apply to sentences before classification? Why?

> From proto2/memo.md: (1) `pre_clean()` strips inline citation markers like [13] or [4, 27] before splitting. (2) `is_valid()` drops sentences shorter than 30 characters or without real words. Explain why each step matters.

A:

**Q19:** How did you design the hypothesis labels? What did you learn from the verbose vs short comparison?

> You tested 4 hypothesis sets (short, verbose_v1, verbose_v2, verbose_v3) on BERT paper (258 sentences). Short labels scored best on the 4-sentence probe (3/4 correct) and had the most balanced role distribution. Verbose hypotheses created strong bias (e.g. verbose_v1 assigned 244/258 sentences to EvaluationMetric). The proto2 design (issue #44) uses natural-language sentences as labels: e.g. "This sentence describes a method used in the paper." — and adds a 5th label "This sentence is background or other information." to capture noise without keyword-based section filtering. Summarise what you tried and what you concluded.

A:


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

**Q21:** What is the start week and end week for each task? What is the final submission deadline?

> Write the actual dates. The Preliminary Report submission (#66) is the next hard deadline — find the exact date in the course portal. You will turn Q20 + Q21 into a Gantt chart image for the PDF (does not count toward the word limit).

A:

**Q22:** If the plan falls behind, what will you do? (contingency)

> Two types of contingency:
> (1) Prototype scope: the usage NLI step (used vs mentioned) and section_factor weighting are the most recent additions — they could be simplified or removed if time is short, without breaking the core role classification.

A:

---

## 8. Test and Evaluation

**Q23:** How will you measure whether the system extracts the correct terms?

> Method from proto2/memo.md: for each paper × role, check whether any accepted sentence contains the gold term (substring match). A role is correct if the gold term appears in at least one classified sentence.

A:

**Q24:** What are the gold labels? For each of the 3 papers, write the expected answer for all 4 roles.

> From proto2/memo.md:
> - Transformer paper: TechnicalMethod=Transformer, Task=machine translation, Dataset=WMT, EvaluationMetric=BLEU
> - BERT: TechnicalMethod=BERT, Task=GLUE / SQuAD, Dataset=BooksCorpus / Wikipedia, EvaluationMetric=accuracy / F1
> - AlexNet: TechnicalMethod=AlexNet, Task=image classification, Dataset=ImageNet, EvaluationMetric=top-1 / top-5 error
> Verify these against the actual papers before you write them in the report.

A:

**Q25:** How will you present the results?

> A table: rows = 4 roles, columns = 3 papers, each cell = correct (○) or wrong (×). Total = 12 data points. You might also show the score and the matched sentence.

A:

**Q26:** What counts as "success"?

> Decide your own threshold. Think about what a reasonable baseline is: if the system got 6/12 by chance, what does 10/12 mean? State a number and a reason.

A:

**Q27:** What are the known limitations of this evaluation method?

> From proto2/memo.md and your own experience:
> - Only 3 papers — too small for statistical claims
> - Substring match is loose (a sentence can "contain" the gold term by accident)
> - Output is full sentences, not short terms — so the match is easier than it looks
> - Systems papers (MapReduce, Google Search) do not fit the 4-role structure

A:

**Q28:** If precision or recall is low, what will you do? (contingency)

> Think about: reporting the result honestly, analysing which role or paper type failed and why, treating the hypothesis set comparison as qualitative evidence of iteration even if final numbers are low.

A: see proto3

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
