<style>
@page {
  size: A4;
  margin: 2.5cm;
}

html, body {
  font-size: 12.5pt;
  line-height: 1.5;
}

p, li, td, th, blockquote, figcaption, caption {
  font-size: 12.5pt;
  line-height: 1.5;
}

pre, code {
  font-size: 12pt;
  line-height: 1.4;
}

pre {
  white-space: pre-wrap;
  word-break: break-word;
}

table {
  width: 100%;
  border-collapse: collapse;
}

table, figure, img {
  max-width: 100%;
}

h1 {
  font-size: 18pt;
  line-height: 1.3;
}

h2 {
  font-size: 15pt;
  line-height: 1.35;
}

h3 {
  font-size: 13.5pt;
  line-height: 1.4;
}

* {
  box-sizing: border-box;
}
</style>

# Design

## 1. Project Overview (39 words)

The system extracts research methodology from computing papers. An input is a PDF, and an output is a role-based profile.

Without this system, a researcher has to categorize them by themselves manually. It is very slow.

<pre>
Methodology:
    Technical method: Transformer
    Task: machine translation
    Dataset: WMT machine translation datasets
    EvaluationMetric: BLEU score
</pre>

Figure 1: Research Methodology from "Attention Is All You Need".

---

## 2. Template (19 words)

Template 12.1: Identifying research methodologies used in computing research. I extract research methodologies based on 4 roles.

---

## 3. Domain and Users (130 words)

The domain is computing research papers. The main targets are systems, ML, algorithm, and HCI.

The primary users are computing students who need to review many papers for a literature review or research project. They need to find the method, task, dataset, and evaluation metric quickly before reading the paper in detail.

Secondary users may include early-stage researchers or supervisors who want a quick overview of a paper. However, the project is designed mainly for students, so the output should be simple, inspectable, and based on sentences from the original paper rather than hidden model decisions.

When people read papers, they often identify the technical method, task, dataset, and evaluation metric by themselves. This process is slow and manual, especially when they must review many papers.

---

## 4. Design Justification (367 words)

Jain et al. [3] needed 438 annotated papers and 4 PhD-level annotators for a supervised approach. This project has no annotated corpus. Yin et al. [4] show that NLI can classify text into many possible labels without task-specific training. Zero-shot NLI is a practical choice when training data does not exist.

Two independent sources agree on the same four types. First, the ontology from Oates [1] and Pilkington & Pretorius [2] suggests a structured vocabulary for research methodology, including TechnicalMethod, Task, Dataset, and EvaluationMetric. Second, Jain et al. [3] (SciREX) independently chose the same four categories (Dataset, Metric, Task, Method) for their annotation scheme. The agreement of two independent sources supports the role vocabulary.

Research design (e.g. experiment vs. survey) is subjective — two readers can assign different labels to the same paper. A philosophical worldview may not appear in the paper text at all. The four roles (TechnicalMethod, Task, Dataset, EvaluationMetric) appear as explicit phrases in the text and are easier to match automatically.

The hypothesis is that sentences in a paper tend to describe one role at a time. A sentence about the dataset does not also describe the method. If this holds, sentence-level classification may be sufficient. Tested on 6 papers (Transformer, BERT, AlexNet, ResNet, MapReduce, Google Search). Results appear to support the assumption for ML papers. Systems papers (MapReduce, Google Search) showed weaker fit because they do not follow the standard ML benchmark structure.

A sentence like "The feature-based approach, such as ELMo, applies independently trained context representations" appears in the Introduction of BERT and describes another paper's method, not BERT's. Skipping the Related Work section by heading removes some noise, but not sentences in the Introduction that describe prior work. A second NLI step with labels ["used by the authors", "mentioned as prior or related work"] catches this at the sentence level without needing more keyword rules. This is expected to improve precision: fewer prior-work sentences may be assigned to TechnicalMethod.

These choices fit the user need because the system is not intended to replace expert reading. It is intended to support the first pass of a literature review by showing likely methodology sentences that the user can inspect and verify.

---

## 5. Overall Structure (218 words)

The pipeline runs as follows: PDF → GROBID (runs locally via Docker) → TEI XML → section filtering (skip References, Acknowledgements, Related Work by heading) → sentence splitting with spaCy + pre_clean() + is_valid() → role NLI (TechnicalMethod / Task / Dataset / EvaluationMetric) with threshold 0.5 → usage NLI (used by this paper / mentioned as prior work) → top-k sentences per role → MethodologyProfile output as JSON.

The input is a PDF of a computing research paper. After GROBID, the intermediate format is TEI XML. Each section has a heading attribute and body text. The abstract is separate from the body sections.

The output is a MethodologyProfile with four fields: TechnicalMethod, Task, Dataset, EvaluationMetric. Each field is a list of sentences from the paper. Final output is a Python dict printed as JSON. Example:

```json
{
  "TechnicalMethod": ["We propose the Transformer..."],
  "Task": ["applied to machine translation..."],
  "Dataset": ["on the WMT 2014 English-German..."],
  "EvaluationMetric": ["achieving 28.4 BLEU on the WMT 2014..."]
}
```

Figure 2: Example output of the system (proto2 prototype).

The current prototype accepts all sentences above a threshold, which can result in a large number of output sentences per role (e.g. 100+ for TechnicalMethod). This is a known prototype limitation.

GROBID runs locally via Docker because it is a Java server process (~1 GB). The NLI pipeline runs on Google Colab because it needs a GPU for fast inference and installs Python packages (transformers, torch, spacy). The TEI XML produced by GROBID is uploaded to Colab manually.

---

## 6. Key Technologies and Methods (248 words)

GROBID converts a PDF into TEI XML, dividing the paper into sections with headings and body text. Without GROBID, the input would be raw PDF text with no section boundaries, making it difficult to filter by section (e.g. skip References or Related Work).

The prototype uses `cross-encoder/nli-deberta-v3-small` (~300 MB, fits free Colab GPU). Zero-shot is therefore a reasonable approach because: (1) no methodology-annotated corpus exists for general computing papers, so supervised training is not straightforward; (2) Yin et al. show NLI can classify into many possible labels without task-specific training.

Two pre-processing steps clean each sentence before classification. (1) `pre_clean()` strips inline citation markers like [13] or [4, 27] before sentence splitting. Citations break sentence boundaries and cause the splitter to produce short fragments. (2) `is_valid()` drops sentences shorter than 30 characters or without at least one real word. This removes citation stubs (e.g. "[4, 27, 28]"), bullet symbols, and other formatting artefacts that would produce noisy classifications.

Four hypothesis sets were tested on the BERT paper (258 sentences). Short labels (e.g. "technical method") scored best on the 4-sentence probe (3 of 4 correct) and had the most balanced distribution across roles. Verbose labels created strong role bias: verbose_v1 assigned 244 of 258 sentences to EvaluationMetric because the hypothesis was too broad. verbose_v3 was too narrow for EvaluationMetric and missed a sentence with "BLEU score." Conclusion: in this test, short labels appear to work better for this model.

---

## 7. Work Plan (183 words)

The work plan is shown visually in Appendix A as a Gantt chart. The main remaining work is Chapter 3, prototype refinement, Chapter 4, and the demonstration video.

| Period | Main task | Output |
|---|---|---|
| Before 29 June | Complete all chapters and working prototype | Preliminary Report |
| After preliminary report | Iterate: improve candidate selection, reduce large outputs, re-evaluate | Improved prototype |
| Final stage | Testing, analysis, video, final writing | Final submission |

Table 1: Work plan summary.

The major tasks are:
- Done: background research, literature notes (Oates, Pilkington, Jain, Yin, GROBID, CSO), pitch
- Done: proto2 prototype — GROBID pipeline, NLI classification, section filtering, pre-processing, hypothesis comparison
- Done: Literature Review (Chapter 2)
- In progress: Chapter 3 — Design (#68); proto2 pipeline refinement (#44)
- Backlog: Chapter 1 — Introduction (#70); Chapter 4 — Feature Prototype (#72); demonstration video MP4 3–5 min (#71)
- Submission: Preliminary Report (#66)

The Preliminary Report submission deadline is 29 June. See Appendix A (Figures A1, A2) for the full project roadmap.

If behind schedule: (1) The usage NLI step (used vs. mentioned) and section_factor weighting are the newest additions. They can be simplified or removed without breaking the core role classification. (2) Chapter 4 (Feature Prototype) can be shortened to a brief description of planned improvements. The core pipeline (GROBID → role NLI → profile output) is the minimum deliverable.

---

## 8. Test and Evaluation (352 words)

For each paper × role, the system checks whether any accepted sentence (score ≥ 0.5) contains the gold term as a substring. A role is correct (○) if at least one classified sentence contains the gold term. Incorrect (×) otherwise.

The gold labels for the three test papers are shown in Table 2.

| Paper | TechnicalMethod | Task | Dataset | EvaluationMetric |
|---|---|---|---|---|
| Transformer | Transformer | machine translation | WMT | BLEU |
| BERT | BERT | GLUE / SQuAD | BooksCorpus / Wikipedia | accuracy / F1 |
| AlexNet | AlexNet | image classification | ImageNet | top-1 / top-5 error |

Table 2: Gold labels — 3 papers × 4 roles.

Results are presented as a table: rows = 4 roles, columns = 3 papers, each cell = ○ (correct) or × (wrong). Total = 12 data points. The matching sentence and score are shown for each ○ cell to make the result inspectable.

Success is defined as ≥ 10 of 12 correct. 10/12 suggests the system finds relevant sentences for most roles across most papers. Lower than 8/12 would indicate a systematic problem worth investigating.

The evaluation is intentionally small but inspectable. Each paper-role pair is judged by whether the system retrieves at least one relevant sentence containing the expected gold term. To avoid hiding errors behind large outputs, the evaluation will also report the number of accepted sentences per role and show the top matching sentence with its score. This makes it possible to see both whether the system finds the correct evidence and whether the output is too broad.

Known constraints of this approach: only 3 papers (too small for statistical claims); substring match is loose; systems papers (MapReduce, Google Search) do not fit the 4-role structure and are excluded; gold labels were written by the author with no formal inter-annotator agreement.

If precision or recall is low, the result will be reported honestly. The analysis will identify which role or paper type failed and explain why (e.g. EvaluationMetric is hardest to capture; systems papers have no standard dataset). The next iteration addresses the two main weaknesses of this evaluation: (1) a first-person verb filter reduces the sentence pool from 200+ to approximately 15–40 candidates before NLI, making substring match less trivially easy; (2) a term extraction step converts the top sentences into short terms (e.g. "Transformer"), allowing a stricter comparison against gold labels. Chapter 4 will describe this plan in detail.

---

## References

[1] B. J. Oates. 2006. *Researching Information Systems and Computing*. SAGE Publications, London.

[2] C. Pilkington and L. Pretorius. 2015. A conceptual model of the research methodology domain. In *Proceedings of the 7th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K 2015), Volume 2: KEOD*. SCITEPRESS – Science and Technology Publications, Setúbal, Portugal, 96–107. https://doi.org/10.5220/0005613100960107

[3] Jain, S., van Zuylen, M., Hajishirzi, H., and Beltagy, I. 2020. SciREX: A Challenge Dataset for Document-Level Information Extraction. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, Online, July 2020. Association for Computational Linguistics, 7506–7516. DOI: https://doi.org/10.18653/v1/2020.acl-main.670

[4] Yin, W., Hay, J., and Roth, D. 2019. Benchmarking Zero-shot Text Classification: Datasets, Evaluation and Entailment Approach. In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)*, Hong Kong, China, November 2019. Association for Computational Linguistics, 3914–3923. DOI: https://doi.org/10.18653/v1/D19-1404

---

## Appendix A — Project Roadmap

<figure>
<img src="Screenshot%202026-06-23%20204411.png" alt="GitHub Projects roadmap — part 1" style="width:100%;max-width:100%;">
<figcaption>Figure A1: Project roadmap (rows 1–24). GitHub Projects roadmap view showing completed iterations (April–June 2026) and current sprint.</figcaption>
</figure>

<figure>
<img src="Screenshot%202026-06-23%20204423.png" alt="GitHub Projects roadmap — part 2" style="width:100%;max-width:100%;">
<figcaption>Figure A2: Project roadmap (rows 26–34). Remaining tasks including chapter writing, video recording, and Preliminary Report submission.</figcaption>
</figure>
