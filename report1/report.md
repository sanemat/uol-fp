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

## Chapter 1: Introduction

When computing researchers conduct a literature review, they often need to read many papers and identify the research methodology of each one. Research methodology in computing papers has a recognisable structure: the technical method used, the task being solved, the dataset evaluated on, and the evaluation metric. Identifying these four components for each paper is useful for comparing related work and for understanding how methods in a field have changed over time. When reviewing many papers, however, this process is slow and manual.

Consider "Attention Is All You Need" (Vaswani et al., 2017), one of the most cited papers in machine learning. The title signals the research direction — attention mechanisms — but does not describe how the research was conducted. That information is spread across the paper and requires careful reading to extract. The paper's methodology, once identified, can be summarised as follows:

| Methodology role | Component |
|---|---|
| Technical method | Transformer |
| Research task | machine translation |
| Evaluation dataset | WMT datasets |
| Evaluation metric | BLEU score |

A reader needing this summary would currently have to read through the paper and construct it themselves.

### Topic labels and role profiles

Topic classifiers and search tools help researchers find papers about a subject. But a topic label answers "what is this paper about?", not "how was this research conducted?" Two papers on the same topic can use different methods, train on different datasets, and report different metrics. A role-based profile answers the second question. It does not replace reading; it supports the first pass through a set of papers — before a researcher decides which ones to read in depth.

The distinction matters in practice. A student reviewing papers on text classification needs to know not only which papers address that topic, but also which ones use transformer models versus older approaches, which datasets are most commonly used, and which metrics are reported. Without a structured profile, this comparison requires reading each paper.

### Project goal and approach

This project addresses **Template 12.1**: Identifying research methodologies used in computing research. The goal is to build an automated pipeline that takes a PDF of a computing research paper as input and produces a role-based methodology profile as output. The profile contains four fields:

- **TechnicalMethod** — the method, algorithm, or architecture the authors used (e.g. Transformer)
- **Task** — the problem the research addresses (e.g. machine translation)
- **Dataset** — the data used for training or evaluation (e.g. WMT datasets)
- **EvaluationMetric** — the metric used to assess results (e.g. BLEU score)

The pipeline works in three stages. First, a PDF is converted to TEI XML by GROBID, which identifies sections with headings. Second, sections are filtered (References and Related Work are excluded), and each remaining sentence is cleaned and validated. Third, a zero-shot Natural Language Inference (NLI) model assigns one of the four roles to each sentence without requiring task-specific training data.

Zero-shot classification was chosen because no methodology-annotated corpus exists for general computing papers. Supervised approaches require substantial annotation effort: Jain et al. [3] built a comparable information extraction system using 438 annotated papers and four expert PhD-level annotators. This project targets a broader range of computing papers — including systems, algorithms, and HCI research as well as ML — where no comparable annotated dataset is available. Yin et al. [4] show that NLI-based zero-shot classification can assign arbitrary labels to text without task-specific training examples, making it a practical choice for this setting.

Research design (e.g. experiment vs survey) and philosophical worldview are out of scope. These components can be subjective and may not appear as explicit phrases in the paper text. The four roles listed above appear more directly in the text and are more tractable to classify automatically at the sentence level.

### Target users

The primary users are computing students who need to survey multiple papers for a literature review or research project. They need to find the method, task, dataset, and evaluation metric quickly, before reading a paper in full. The system is intended to support this first pass, not to replace reading.

The output is designed to be inspectable. Each role field contains actual sentences from the paper, allowing the user to judge whether a classified sentence is genuinely relevant to the paper's methodology. At this prototype stage, the output is full sentences rather than short extracted terms. This limitation is discussed in Chapter 4.

### Report structure

Chapter 2 reviews three areas of related work: how research methodology in computing is defined and structured; how methodology-related information can be extracted from scientific papers; and how zero-shot classification can assign labels to text without labeled training data. The chapter identifies a gap that this project addresses.

Chapter 3 describes the system design. It covers the four-role schema and its justification, the full pipeline architecture, the choice of technologies, the evaluation approach, and the work plan.

Chapter 4 presents the feature prototype. It describes the implementation of the zero-shot NLI classification step, demonstrates results on six computing papers, evaluates the prototype against manually identified gold labels, and discusses planned improvements for the next iteration.

---

## Chapter 2: Literature Review

### Introduction

"Attention Is All You Need" is a very famous AI paper. But the title does not tell us how it works.

<pre>
Methodology:
    Design or strategy: design and creation + experiment
    Data generation method: documents
    Technical method: Transformer
    Task: machine translation
    Dataset: WMT machine translation datasets
    EvaluationMetric: BLEU score
</pre>

Figure 1: Research Methodology from "Attention Is All You Need".

Extracting research methodology from computing papers automatically is useful, but it remains challenging. When people read papers, they often identify the technical method, task, dataset, and evaluation metric by themselves. This process is slow and manual, especially when they must review many papers.
This review covers three areas: how methodology is defined, how information is extracted from papers, and how classification can work without training data. At the end, this review will identify a gap: existing methods can extract some information from papers, but reliably extracting full research methodology from computing papers is still difficult.

### Defining Research Methodology

Research methodology in computing papers can be described using a structured vocabulary, but defining it is not the same as extracting it.

Oates [1] provides six research strategies (experiment, design and creation, survey, case study, action research, and ethnography) and four data generation methods (interviews, observations, questionnaires, and documents). His book defines the vocabulary that researchers use to describe their methodology in papers, so my project needs these concept names to identify what to extract. His book was published in 2006, but it still provides useful categories for describing how computing researchers conduct their work.

Pilkington & Pretorius [2] go further: they formalize the structure using UML and ontology engineering, with the goal of "providing clear and unambiguous semantics" [2] — a formal structure, not a textbook description. Key concepts are ResearchScheme, PhilosophicalWorldview, ResearchDesign, and ResearchMethod. ResearchScheme belongs to one PhilosophicalWorldview, has one or more ResearchDesigns, and has one or more ResearchMethods. The paper tries to solve the problem that students and supervisors had no shared, consistent vocabulary for methodology, so they often used the same terms with different meanings.

A philosophical worldview is one of the important parts of Pilkington & Pretorius [2], but it may not appear directly in paper text, so my project skips it.

Oates [1] gives concept names. Pilkington & Pretorius [2] give formal relationships between those concepts. My project uses vocabulary from Oates and formal structure from Pilkington & Pretorius.

Both works are designed for human use. Neither provides a system to extract methodology components automatically from text. These works suggest that methodology can be defined and formalized. The question is whether any system can extract it.


### Closest Prior Work

Systems that extract methodology-like entities from papers exist, but the closest supervised approaches require labeled training data that this project does not have.

Jain et al. [3] extract four entity types: Dataset, Metric, Task, and Method.

Dataset: WMT machine translation datasets
Metric: BLEU score
Task: machine translation
Method: Transformer

Figure 2: Entity types from "Attention Is All You Need".

These four types closely match the four roles in this project. This suggests that the problem is real and may be solvable in principle.

Jain et al. [3] operate at the document level. The authors argue that "a significant amount of information can only be gleaned from analyzing the full document" [3] — relations may span sections, not just sentences.

But Jain et al. [3] required 438 annotated papers and 4 expert PhD-level annotators (Cohen-κ 95%). The corpus comes from Papers with Code, which covers only ML benchmarks. My project targets general computing papers (systems, algorithms, HCI, etc.) and has no annotated corpus. The Jain et al. [3] approach is difficult to adopt directly.

The right entity types are identified, but building a supervised system requires annotation effort that does not exist for this scope. A zero-shot method is therefore a reasonable direction.

### Zero-shot Classification

Zero-shot NLI can assign roles to text without task-specific training data, but applying it to scientific papers introduces a domain mismatch risk.

Yin et al. [4] define zero-shot text classification as assigning a label to text without any task-specific training examples.

Yin et al. [4] show that NLI can classify text into many possible labels by turning the label into a natural language hypothesis — "this text is about [label]" [4] — and asking a model whether the text entails it. No labeled examples for the target labels are needed.

| aspect | labels | interpretation | example hypothesis (word) | example hypothesis (wordnet definition) |
|---|---|---|---|---|
| topic | sports etc. | this text is about ? | "?"= sports | "?" = an active diversion requiring physical exertion and competition |
| emotion | anger etc. | this text expresses ? | "?"= anger | "?" = a strong emotion; a feeling that is oriented toward some real or supposed grievance |
| situation | shelter etc. | The people there need ? | "?"= shelter | "?" = a structure that provides privacy and protection from danger |

*Table 1 (reproduced from Yin et al. [4]): example hypotheses for three task types.*

This provides a possible way to support the core step in this project: classifying sentences into TechnicalMethod, Task, Dataset, or EvaluationMetric without a methodology-annotated corpus. This project applies the same entailment approach with four methodology roles:

| role | hypothesis (this project, short label) |
|---|---|
| TechnicalMethod | technical_method |
| Task | task |
| Dataset | dataset |
| EvaluationMetric | evaluation_metric |

*Table 2: hypothesis set used in this project (short label format, selected by hypothesis set comparison).*

For TechnicalMethod, a longer hypothesis was also tested: "This text describes a technique, algorithm, system, or architecture used or proposed in the research." The hypothesis set comparison investigates whether this verbose form can extract TechnicalMethod more accurately than the short label on scientific text.

However, a domain mismatch risk exists. Yin et al. test on Yahoo News articles, emotion tweets, and crisis situation reports. Their NLI model is trained on MNLI (news, fiction, telephone speech). None of these are scientific papers, which use dense technical vocabulary, passive constructions, and section-based structure.

This project accepts the risk and tests it: the hypothesis set comparison (short vs verbose hypotheses) directly investigates how label wording affects classification on scientific text.

Zero-shot NLI reduces the labeled data requirement. The question is whether any prior work combines this approach with a methodology schema on scientific papers.

### Synthesis

It is difficult to find existing work that applies zero-shot NLI with a structured methodology schema to general computing papers. This is the gap this project addresses.

Section 2 established the schema. Oates [1] and Pilkington & Pretorius [2] together justify a four-component structure — TechnicalMethod, Task, Dataset, and EvaluationMetric — grounded in formal ontology. But both works are designed for human use. Neither provides a system to extract those components from text automatically.

Section 3 showed that extraction of the same four types is possible. Jain et al. [3] built a working system, but it required 438 annotated papers, 4 PhD-level annotators, and a corpus limited to ML benchmarks. This approach cannot generalize to general computing papers without similar annotation effort that this project does not have.

Section 4 showed that zero-shot NLI removes the labeled data requirement. Yin et al. [4] demonstrate that NLI can classify text into any label without task-specific training. But their approach was tested only on news articles, tweets, and crisis reports — not scientific papers. Domain mismatch remains an open risk.

Combining these elements appears to remain underexplored: the 4-role methodology schema from Oates and Pilkington, the zero-shot NLI method from Yin et al., and application to general computing papers. This project addresses that gap. It applies Yin et al.'s entailment approach with the 4-role schema on GROBID-parsed computing papers, without requiring annotated data.

---

## Chapter 3: Design

### 1. Project Overview

The system extracts research methodology from computing papers. An input is a PDF, and an output is a role-based profile (see Figure 1 in Chapter 2 for an example). Without this system, a researcher has to categorize papers by themselves manually. It is very slow.

---

### 2. Domain and Users

The domain is computing research papers. The main targets are systems, ML, algorithm, and HCI.

The primary users are computing students who need to review many papers for a literature review or research project. They need to find the method, task, dataset, and evaluation metric quickly before reading the paper in detail.

Secondary users may include early-stage researchers or supervisors who want a quick overview of a paper. However, the project is designed mainly for students, so the output should be simple, inspectable, and based on sentences from the original paper rather than hidden model decisions.

---

### 3. Design Justification

Jain et al. [3] needed 438 annotated papers and 4 PhD-level annotators for a supervised approach. This project has no annotated corpus. Yin et al. [4] show that NLI can classify text into many possible labels without task-specific training. Zero-shot NLI is a practical choice when training data does not exist.

Two independent sources agree on the same four types. First, the ontology from Oates [1] and Pilkington & Pretorius [2] suggests a structured vocabulary for research methodology, including TechnicalMethod, Task, Dataset, and EvaluationMetric. Second, Jain et al. [3] (SciREX) independently chose the same four categories (Dataset, Metric, Task, Method) for their annotation scheme. The agreement of two independent sources supports the role vocabulary.

Research design (e.g. experiment vs. survey) is subjective — two readers can assign different labels to the same paper. A philosophical worldview may not appear in the paper text at all. The four roles (TechnicalMethod, Task, Dataset, EvaluationMetric) appear as explicit phrases in the text and are easier to match automatically.

The hypothesis is that sentences in a paper tend to describe one role at a time. A sentence about the dataset does not also describe the method. If this holds, sentence-level classification may be sufficient. Tested on 6 papers (Transformer, BERT, AlexNet, ResNet, MapReduce, Google Search). Results appear to support the assumption for ML papers. Systems papers (MapReduce, Google Search) showed weaker fit because they do not follow the standard ML benchmark structure.

A sentence like "The feature-based approach, such as ELMo, applies independently trained context representations" appears in the Introduction of BERT and describes another paper's method, not BERT's. Skipping the Related Work section by heading removes some noise, but not sentences in the Introduction that describe prior work. A second NLI step with labels ["used by the authors", "mentioned as prior or related work"] catches this at the sentence level without needing more keyword rules. This is expected to improve precision: fewer prior-work sentences may be assigned to TechnicalMethod.

These choices fit the user need because the system is not intended to replace expert reading. It is intended to support the first pass of a literature review by showing likely methodology sentences that the user can inspect and verify.

---

### 4. Overall Structure

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

Figure 4: Example output of the system (proto2 prototype).

The current prototype accepts all sentences above a threshold, which can result in a large number of output sentences per role (e.g. 100+ for TechnicalMethod). This is a known prototype limitation.

GROBID runs locally via Docker because it is a Java server process (~1 GB). The NLI pipeline runs on Google Colab because it needs a GPU for fast inference and installs Python packages (transformers, torch, spacy). The TEI XML produced by GROBID is uploaded to Colab manually.

---

### 5. Key Technologies and Methods

GROBID converts a PDF into TEI XML, dividing the paper into sections with headings and body text. Without GROBID, the input would be raw PDF text with no section boundaries, making it difficult to filter by section (e.g. skip References or Related Work).

The prototype uses `cross-encoder/nli-deberta-v3-small` (~300 MB, fits free Colab GPU). Zero-shot is therefore a reasonable approach because: (1) no methodology-annotated corpus exists for general computing papers, so supervised training is not straightforward; (2) Yin et al. show NLI can classify into many possible labels without task-specific training.

Two pre-processing steps clean each sentence before classification. (1) `pre_clean()` strips inline citation markers like [13] or [4, 27] using a regex. Citations break sentence boundaries and cause the splitter to produce short fragments. (2) `is_valid()` drops sentences shorter than 30 characters or without at least one real word. This removes citation stubs (e.g. "[4, 27, 28]"), bullet symbols, and other formatting artefacts that would produce noisy classifications.

Four hypothesis sets (short and three verbose variants) were tested on the BERT paper. Short labels gave the best probe score and the most balanced role distribution. Full results and analysis are in Chapter 4, Section 3.

---

### 6. Work Plan

The work plan is shown visually in Appendix A as a Gantt chart. The main remaining work is Chapter 3, prototype refinement, Chapter 4, and the demonstration video.

| Period | Main task | Output |
|---|---|---|
| Before 29 June | Complete all chapters and working prototype | Preliminary Report |
| After preliminary report | Iterate: improve candidate selection, reduce large outputs, re-evaluate | Improved prototype |
| Final stage | Testing, analysis, video, final writing | Final submission |

Table 3: Work plan summary.

The major tasks are:
- Done: background research, literature notes (Oates, Pilkington, Jain, Yin, GROBID, CSO), pitch
- Done: proto2 prototype — GROBID pipeline, NLI classification, section filtering, pre-processing, hypothesis comparison
- Done: Literature Review (Chapter 2)
- In progress: Chapter 3 — Design; proto2 pipeline refinement
- Backlog: Chapter 4 — Feature Prototype; demonstration video MP4 3–5 min
- Submission: Preliminary Report

The Preliminary Report submission deadline is 29 June. See Appendix A (Figures A1, A2) for the full project roadmap.

If behind schedule: (1) The usage NLI step (used vs. mentioned) and section_factor weighting are the newest additions. They can be simplified or removed without breaking the core role classification. (2) Chapter 4 (Feature Prototype) can be shortened to a brief description of planned improvements. The core pipeline (GROBID → role NLI → profile output) is the minimum deliverable.

---

### 7. Test and Evaluation

For each paper × role, the system checks whether any accepted sentence (score ≥ 0.5) contains the gold term as a substring. A role is correct (○) if at least one classified sentence contains the gold term. Incorrect (×) otherwise.

The gold labels for the three test papers are shown in Table 4.

| Paper | TechnicalMethod | Task | Dataset | EvaluationMetric |
|---|---|---|---|---|
| Transformer | Transformer | machine translation | WMT | BLEU |
| BERT | BERT | GLUE / SQuAD | BooksCorpus / Wikipedia | accuracy / F1 |
| AlexNet | AlexNet | image classification | ImageNet | top-1 / top-5 error |

Table 4: Gold labels — 3 papers × 4 roles.

Results are presented as a table: rows = 4 roles, columns = 3 papers, each cell = ○ (correct) or × (wrong). Total = 12 data points. The matching sentence and score are shown for each ○ cell to make the result inspectable.

Success is defined as ≥ 10 of 12 correct. 10/12 suggests the system finds relevant sentences for most roles across most papers. Lower than 8/12 would indicate a systematic problem worth investigating.

The evaluation is intentionally small but inspectable. Each paper-role pair is judged by whether the system retrieves at least one relevant sentence containing the expected gold term. To avoid hiding errors behind large outputs, the evaluation will also report the number of accepted sentences per role and show the top matching sentence with its score. This makes it possible to see both whether the system finds the correct evidence and whether the output is too broad.

Known constraints of this approach: only 3 papers (too small for statistical claims); substring match is loose; systems papers (MapReduce, Google Search) do not fit the 4-role structure and are excluded; gold labels were written by the author with no formal inter-annotator agreement.

If precision or recall is low, the result will be reported honestly. The analysis will identify which role or paper type failed and explain why (e.g. EvaluationMetric is hardest to capture; systems papers have no standard dataset). The next iteration addresses the two main weaknesses of this evaluation: (1) a first-person verb filter reduces the sentence pool from 200+ to approximately 15–40 candidates before NLI, making substring match less trivially easy; (2) a term extraction step converts the top sentences into short terms (e.g. "Transformer"), allowing a stricter comparison against gold labels. Chapter 4 will describe this plan in detail.

---

### Appendix A — Project Roadmap

<figure>
<img src="Screenshot%202026-06-23%20204411.png" alt="GitHub Projects roadmap — part 1" style="width:100%;max-width:100%;">
<figcaption>Figure A1: Project roadmap (rows 1–24). GitHub Projects roadmap view showing completed iterations (April–June 2026) and current sprint.</figcaption>
</figure>

<figure>
<img src="Screenshot%202026-06-23%20204423.png" alt="GitHub Projects roadmap — part 2" style="width:100%;max-width:100%;">
<figcaption>Figure A2: Project roadmap (rows 26–34). Remaining tasks including chapter writing, video recording, and Preliminary Report submission.</figcaption>
</figure>

---

## Chapter 4: Feature Prototype

### 1. Overview

The prototype takes a TEI XML file produced by GROBID from a computing research paper and classifies each sentence by research methodology role using zero-shot NLI to produce a JSON object with four lists — TechnicalMethod, Task, Dataset, and EvaluationMetric.

The prototype uses zero-shot NLI classification to assign a role (label) to each sentence. Without this step, the pipeline produces only a list of sentences with no meaning attached. The role assignment is the output. If the model fails, the whole prototype fails. Zero-shot NLI avoids the annotation requirement (see Chapter 3, Section 3 for justification), making it the central design choice to validate.

### 2. Implementation

#### 2.1 Pipeline

The pipeline follows the design described in Chapter 3, Section 4. In brief: GROBID converts the PDF to TEI XML; filtered sections are sentence-split with spaCy; each sentence is classified by the NLI model with four candidate labels; sentences scoring ≥ 0.5 are accepted for that role; the final output is a JSON object with one list per role.

#### 2.2 Model

The classifier is `cross-encoder/nli-deberta-v3-small` from Hugging Face. DeBERTa (Decoding-enhanced BERT with Disentangled Attention) is a strong NLI backbone. The `v3-small` variant fits in Colab GPU memory (568 MB) while still performing well. The model choice and zero-shot rationale are described in Chapter 3, Section 5.

#### 2.3 Preprocessing

The pipeline applies two preprocessing steps before classification.

First, `pre_clean()` removes inline citation markers such as `[13]` or `[4, 27]` using a regex. Without this step, spaCy may split a sentence at the bracket, producing broken fragments. For example:

> `"The model outperforms [4, 27] the baseline."` → `"The model outperforms the baseline."`

Second, `is_valid()` drops sentences that are shorter than 30 characters or contain no word of three or more letters. This removes bullet characters, lone numbers, and citation stubs that pass through sentence splitting but carry no information. After these two steps, the Transformer paper produced 183 valid sentences for classification.

#### 2.4 Section Filtering

References, Acknowledgements, and Related Work are excluded.

- References and Acknowledgements are excluded by exact heading match (`SKIP_HEADINGS`). These sections list citations and credits, not methodology.
- Related Work is excluded by keyword match (`SKIP_KEYWORDS`). Subsections are also skipped automatically by tracking the `n` attribute (e.g. if Related Work is `n="2"`, then `n="2.1"` and `n="2.2"` are also skipped). The reason is that Related Work describes other papers' methods, which the NLI model classifies as TechnicalMethod of the target paper. Testing on BERT showed that excluding Related Work reduced TechnicalMethod from 67 to 62 sentences (−5).

All other body sections are included: Abstract, Introduction, Method/Architecture, Dataset, Experiment, Results, Conclusion, etc. An earlier version used only sections whose heading matched keywords such as "experiment" or "result". The `Training Data` section in the Transformer paper has no such keyword and was missed. Switching to all body sections improved Dataset recall significantly.

### 3. Demonstration

The prototype was tested on six papers. Table 5 shows the number of accepted sentences per role.

| Paper | TechnicalMethod | Task | Dataset | EvaluationMetric | Notes |
|---|---|---|---|---|---|
| Transformer | 14 | 0 | 0 | 160 | verbose_v1: extreme EM bias |
| BERT | 62 | 23 | 15 | 13 | short: balanced |
| AlexNet | 51 | 6 | 11 | 4 | short: balanced |
| ResNet | 51 | 6 | 14 | 12 | short: balanced |
| MapReduce | 151 | 24 | 3 | 5 | short: TM heavy, weak DS/EM |
| Google Search | 69 | 21 | 8 | 29 | short: no standard benchmark |

Table 5: Accepted sentences per role for six papers.

Verbose hypotheses caused extreme label bias: verbose_v1 assigned 160 of 183 Transformer sentences to EvaluationMetric, leaving Task and Dataset with 0. ML papers tested (BERT, AlexNet, ResNet) produced balanced output across all four roles with short labels. Systems papers (MapReduce, Google Search) produced very large TechnicalMethod counts and few Dataset or EvaluationMetric sentences, consistent with their lack of standard ML benchmark structure.

#### Hypothesis Set Comparison

The choice of hypothesis text has a large effect on classification. Four hypothesis sets were tested on the BERT paper (258 sentences). A probe set of four known-answer sentences (one per role) was used to measure correctness.

| Set | Probe (4 gold labels) | TechnicalMethod | Task | Dataset | EvaluationMetric |
|---|---|---|---|---|---|
| short | **3/4** | 124 | 70 | 33 | 31 |
| verbose_v1 | 2/4 | 11 | 0 | 3 | 244 |
| verbose_v2 | 2/4 | 63 | 11 | 19 | 165 |
| verbose_v3 | 2/4 | 131 | 56 | 60 | 11 |

Table 6: Hypothesis set comparison on the BERT paper (258 sentences).

Verbose hypotheses introduced strong label bias: verbose_v1 and verbose_v2 sent nearly all sentences to EvaluationMetric, while verbose_v3 shifted the bias to TechnicalMethod. Short labels gave the best probe score (3/4) and the most balanced distribution.

### 4. Evaluation

#### 4.1 Method

No annotated sentence-level dataset exists for this task, so standard precision, recall, and F1 cannot be measured. Instead, I used a recall-oriented gold label check. For each of three papers, I manually identified one gold label per role — the answer I would expect the system to find (e.g. "Transformer" for TechnicalMethod, "BLEU" for EvaluationMetric). I then ran the pipeline and checked whether any accepted sentence contained that gold label as a substring. The result is a 3-paper × 4-role table (12 data points) with ○ or ✗.

This approach seems appropriate for a prototype because the key question at this stage is whether the system finds the right information at all, not how precise the full output is. Jain et al. [3] used a similar role-based recall check in SciREX, evaluating whether predicted spans match the annotated entity per role.

#### 4.2 Results

Gold terms used (based on the planned labels in Chapter 3, Table 4, refined after running the pipeline):

| Paper | TechnicalMethod | Task | Dataset | EvaluationMetric |
|---|---|---|---|---|
| Transformer | "Transformer" | "machine translation" | "WMT" | "BLEU" |
| BERT | "BERT" | "GLUE" | "BooksCorpus" | "F1" |
| AlexNet | "convolutional" | "object recognition" | "ImageNet" | "top-5" |

Table 7: Gold labels as used in evaluation (AlexNet TechnicalMethod refined to "convolutional" since the name "AlexNet" was coined after publication).

Result (○ = gold label found in any accepted sentence, ✗ = not found):

| Paper | TechnicalMethod | Task | Dataset | EvaluationMetric |
|---|---|---|---|---|
| Transformer | ○ | ✗ | ✗ | ○ |
| BERT | ○ | ○ | ○ | ○ |
| AlexNet | ○ | ○ | ○ | ○ |

Table 8: Gold label evaluation results.

#### 4.3 Analysis

BERT scored ○ on all four roles, which suggests that the pipeline can find all types of methodology information in a well-structured ML paper using short labels. AlexNet also scored ○ on all four roles when using "convolutional" as the TechnicalMethod gold label (the 2012 paper does not use the name "AlexNet" — that name was coined later).

The Transformer scored ✗ on Task and Dataset, but this appears to be caused by the verbose_v1 hypothesis set, not by a failure to find the information in the paper. TechnicalMethod and Dataset tend to be the easier roles because they appear in dedicated sections with explicit mentions. EvaluationMetric is found correctly but in small quantities (4–13 sentences), as metric names appear in few places. Task appears to be the most difficult role: it is often stated implicitly and produced the fewest sentences among the papers tested. Systems papers (MapReduce, PageRank) produced empty or weak Dataset and EvaluationMetric output, possibly because they do not follow the standard ML benchmark structure.

### 5. Limitations

Four types of noise were observed.

The first type is Introduction noise. Introduction sections describe other papers' methods, which the NLI model incorrectly classifies as TechnicalMethod of the target paper. For example, "The feature-based approach, such as ELMo..." scored 0.87 as TechnicalMethod in the BERT paper. Excluding the Introduction on BERT reduced TechnicalMethod from 62 to 54 sentences, but also removed correct sentences about BERT itself, so full exclusion risks losing signal.

The second type is quoted or example text. Text that is quoted or used as an example in the paper body is classified as a real claim. For example, "you looked at a lot of pages from my Web site." from the Google Search paper was classified as Task.

The third type is GROBID artefacts. Author contribution text can appear in the GROBID abstract element, producing irrelevant sentences in the TechnicalMethod output.

The fourth type is large output volume. MapReduce produced 151 TechnicalMethod sentences and the Transformer produced 160 EvaluationMetric sentences, because there is no upper limit on accepted sentences.

### 6. Improvements for the Next Iteration

Three improvements are planned.

The first is a usage NLI step after role classification. A second NLI pass with labels ["used by the authors", "mentioned as prior or related work"] keeps only sentences about the paper's own work, catching Introduction noise at the sentence level without additional keyword rules. As a lighter alternative, a first-person verb filter ("we propose", "we introduce", "we use") may reduce the candidate pool from 200+ to approximately 15–40 sentences before NLI.

The second is Top-N selection by score × section weight. Instead of keeping all accepted sentences, only the top 3 per role are kept, ranked by NLI score multiplied by a section weight (Abstract and Method sections ranked higher than Introduction). This addresses the large output volume: MapReduce produced 151 TechnicalMethod sentences, but the top 3 by score may be sufficient for a methodology profile.

The third is LLM term extraction. The current output is full sentences, but the target profile contains short terms (e.g. "Transformer" rather than "We propose a new simple network architecture, the Transformer..."). The gold label evaluation suggests the correct term is present in the output sentence; the next step is extracting it with a prompt such as "What is the TechnicalMethod named in this sentence?"

### 7. Technical Challenge

Zero-shot NLI classification on academic text is technically challenging for three reasons.

The first challenge is that hypothesis engineering is non-trivial. More detailed label descriptions do not necessarily improve accuracy: verbose_v1 and verbose_v2 sent nearly all BERT sentences to EvaluationMetric (244 of 258), while verbose_v3 shifted the bias to TechnicalMethod. Short labels achieved the best probe score and most balanced distribution, but this required four iterations of hypothesis design to discover.

The second challenge is domain mismatch. The NLI model was trained on general-domain benchmarks, but academic writing is structurally different: sentences are longer, more technical, and contain citation markers and figure references that were not in the training data. The model classifies these without any task-specific training on scientific text.

The third challenge is authorship attribution. The sentence "The feature-based approach, such as ELMo..." correctly entails "technical method" according to the NLI model — it does describe a method — but the method belongs to a different paper. Distinguishing a paper's own methods from those it cites may go beyond what NLI alone can do, since it requires understanding who the authors are and what the paper claims.

---

## References

[1] B. J. Oates. 2006. *Researching Information Systems and Computing*. SAGE Publications, London.

[2] C. Pilkington and L. Pretorius. 2015. A conceptual model of the research methodology domain. In *Proceedings of the 7th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K 2015), Volume 2: KEOD*. SCITEPRESS – Science and Technology Publications, Setúbal, Portugal, 96–107. https://doi.org/10.5220/0005613100960107

[3] S. Jain, M. van Zuylen, H. Hajishirzi, and I. Beltagy. 2020. SciREX: A Challenge Dataset for Document-Level Information Extraction. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, Online, July 2020. Association for Computational Linguistics, 7506–7516. https://doi.org/10.18653/v1/2020.acl-main.670

[4] W. Yin, J. Hay, and D. Roth. 2019. Benchmarking Zero-shot Text Classification: Datasets, Evaluation and Entailment Approach. In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)*, Hong Kong, China, November 2019. Association for Computational Linguistics, 3914–3923. https://doi.org/10.18653/v1/D19-1404
