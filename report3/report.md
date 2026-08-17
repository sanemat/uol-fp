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

# Report (6138 words, excluding tables, figures, references, and appendices)

## Chapter 1: Introduction (471 words)

When computing researchers do a literature review, they often need to read many papers and find each paper's method, task, dataset, and evaluation metric. Reading many papers this way is slow and manual. I treat these four items as a methodology profile that a reader can extract automatically, to support the first pass of a literature review, not to replace reading the paper.

Consider "Attention Is All You Need" [D6]:

| Methodology role | Component |
|---|---|
| Technical method | Transformer |
| Task | machine translation |
| Dataset | WMT 2014 English-German |
| Evaluation metric | BLEU |

Table 1: Role-based methodology profile for "Attention Is All You Need" [D6].

A reader needing this summary currently has to read the paper and construct it themselves. A topic label answers "what is this paper about?"; a role-based profile answers "how was this research conducted?" Two papers on the same topic can use different methods, train on different datasets, and report different metrics, so a topic label alone does not answer that second question.

I use Template 12.1 from the Natural Language Processing (NLP) module: identifying research methodologies used in computing research papers.

This motivation has not changed since the preliminary report. What changed is the extraction approach. proto2, my first working prototype, classified every sentence in a paper into one of the four roles using zero-shot natural language inference (NLI), producing a list of candidate sentences per role rather than one answer. proto3, the current prototype, reframes the task as document-level extraction: given a paper, a long-context large language model (LLM) returns one answer per role, each backed by a section heading and a verbatim quote as evidence.

The primary users are computing students doing literature reviews. Secondary users are early-stage researchers or supervisors who want a quick overview of a paper. The output is designed to be inspectable: a user can check the quoted evidence against the source paper.

### Report structure

Chapter 2 reviews related work on how research methodology is defined and structured, how methodology-related information can be extracted from scientific papers, and how zero-shot classification assigns labels without labeled training data, then extends this with work on LLM-based structured extraction, and with proto2's own findings as motivation for document-level extraction.

Chapter 3 describes the system design: the four-role schema and its justification, the pipeline architecture, the model choice, and the evaluation plan, including two design considerations (decomposed extraction, multi-valued roles) written up as considered further work rather than implemented defaults.

Chapter 4 covers implementation across all three prototype iterations, with most detail on proto3's document-level extraction: the pipeline stages, the schema-guided prompt, the Gemini call, and a visual before/after comparison against proto2.

Chapter 5 evaluates the whole project so far: gold-label matching scored as a classification problem with confidence intervals, a logged 5-run variance study, and a critical evaluation mapping proto2's named failure modes onto what proto3 actually measured.

Chapter 6 concludes with a short summary of the whole project and further work, including one broader theme about structured-output guarantees versus semantic correctness in LLM-based extraction.

---

## Chapter 2: Literature Review (1505 words)

Chapter 1 showed a four-role profile for "Attention Is All You Need" [D6]. Figure 1 shows a fuller view of the same paper, including the design strategy and data generation method defined by Oates [1].

<figure>
<pre>
Methodology:
    Design or strategy: design and creation + experiment
    Data generation method: documents
    Technical method: Transformer
    Task: machine translation
    Dataset: WMT machine translation datasets
    EvaluationMetric: BLEU score
</pre>
<figcaption>Figure 1: Research Methodology from "Attention Is All You Need" [D6].</figcaption>
</figure>

This review covers four areas: how methodology is defined, how information is extracted from papers, how classification can work without labeled training data, and how large language models (LLMs) extract structured information directly from scientific text. It ends with a synthesis positioning this project, and a note on feedback received on the preliminary report.

### 1. Defining Research Methodology

Research methodology in computing papers can be described using a structured vocabulary, but defining it is not the same as extracting it.

Oates [1] provides six research strategies (experiment, design and creation, survey, case study, action research, and ethnography) and four data generation methods (interviews, observations, questionnaires, and documents). His book defines the vocabulary that researchers use to describe their methodology in papers, so my project needs these concept names to identify what to extract. However, the six strategies were designed for human researchers to self-classify their own work — papers rarely contain the explicit phrase "this is an experiment". The vocabulary can be used to name what to look for, but it may not transfer directly to automatic extraction from text.

Pilkington & Pretorius [2] go further: they formalize the structure using UML (Unified Modeling Language) and ontology engineering, with the goal of "providing clear and unambiguous semantics" [2]. Key concepts are ResearchScheme, PhilosophicalWorldview, ResearchDesign, and ResearchMethod: a ResearchScheme belongs to one PhilosophicalWorldview, has one or more ResearchDesigns, and has one or more ResearchMethods.

A philosophical worldview is one of the key components in Pilkington & Pretorius [2], but it tends not to appear as an explicit phrase in completed research papers, so I exclude it from extraction. Research design (e.g. experiment vs. survey) [3] is similarly out of scope: it can be subjective, two readers can assign different labels to the same paper, and it is not the focus of this project's four roles.

Oates [1] gives concept names. Pilkington & Pretorius [2] give formal relationships between those concepts. My project uses vocabulary from Oates and formal structure from Pilkington & Pretorius. Both works are designed for human use; neither provides a system to extract methodology components automatically from text. The four roles used in this project (TechnicalMethod, Task, Dataset, and EvaluationMetric) draw more directly on Jain et al. [4], reviewed next.

### 2. Extracting Methodology from Papers

Systems that extract methodology-like entities from papers exist [4, 5, 6], but the closest approaches are supervised and need labeled training data that I do not have.

Jain et al. [4] (SciREX) extract four entity types — Dataset, Metric, Task, and Method — that closely match the four roles in this project. They operate at the document level, arguing that "a significant amount of information can only be gleaned from analyzing the full document" [4] — relations may span sections, not just sentences. However, Jain et al. required 438 annotated papers and four expert PhD-level annotators (Cohen's κ 95%), drawn from a pool of 1,170 ML-conference articles on Papers with Code, which covers only ML benchmarks. My project targets general computing papers (systems, algorithms, human-computer interaction (HCI), and ML research) where no comparable annotated dataset is available, so neither the corpus scope nor the annotation effort behind SciREX transfers directly.

Ma et al. [7] propose a metric-driven mechanism schema that extracts three components (mechanism, task, and metric) from NLP papers using a query-guided sequence-to-sequence model, but their work is limited to the NLP domain and does not extend to general computing research.

Ghosh et al. [5, 6] use supervised transformer-based sequence labeling to extract methodology component names from AI research papers. They argue that methodology names are difficult to extract because they are large, fast-evolving, domain-specific, and context-dependent. Unlike Jain et al. [4], who extract four entity types at the document level, Ghosh et al. focus narrowly on TechnicalMethod. Their approach covers only TechnicalMethod, leaving Task, Dataset, and EvaluationMetric unaddressed, and their training data does not cover general computing research such as systems, algorithms, or HCI.

Färber et al. [8] extract methods and datasets from scientific publications using domain-specific named entity recognition (NER) followed by usage classification, which distinguishes whether each mention is used by the authors or only cited as prior work. This "used vs mentioned" distinction is directly relevant to a noise problem this project also has: a sentence describing a prior method (for example, ELMo, cited in BERT's Introduction) can be misread as the paper's own method. However, Färber et al. cover only Method and Dataset, not Task or EvaluationMetric, and their NER model requires labeled entity mentions that are not available for this project.

These supervised methods all depend on domain-specific annotated corpora that this project does not have. A zero-shot approach removes this requirement, at the cost of domain adaptation, reviewed next.

### 3. Zero-shot Classification

Yin et al. [9] define zero-shot text classification as assigning a label to text without any task-specific training examples. They show that natural language inference (NLI) can classify text into many possible labels by turning the label into a hypothesis (for example, "this text is about sports") and asking a model whether the text entails it. I applied this approach directly in proto2, my first prototype: four methodology-role hypotheses, one per role, classified independently against each sentence in a paper, using a DeBERTa-v3-based zero-shot classification model [10].

| aspect | labels | interpretation | example hypothesis (word) |
|---|---|---|---|
| topic | sports etc. | this text is about ? | "?" = sports |
| emotion | anger etc. | this text expresses ? | "?" = anger |
| situation | shelter etc. | The people there need ? | "?" = shelter |

*Table 2 (adapted from Yin et al. [9]): example hypotheses for three general-domain task types.*

A domain mismatch risk exists: Yin et al. test on Yahoo News articles, emotion tweets, and crisis situation reports, and their NLI model is trained on MNLI (Multi-Genre Natural Language Inference; covers news, fiction, and telephone speech) — none of these are scientific papers, which tend to use dense technical vocabulary, passive constructions, and section-based structure. proto2 tested this risk directly by comparing hypothesis wordings on scientific text: a verbose TechnicalMethod hypothesis sent 244 of 258 BERT sentences to EvaluationMetric, a single poorly chosen hypothesis collapsing the label distribution, while short labels gave the best probe score and the most balanced distribution across four roles. Even with short labels, classification errors remained: on the Transformer paper, "Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task" was classified as Task rather than EvaluationMetric. This showed that hypothesis design is a real cost in zero-shot systems, but it did not fix the design-level problem in proto2's own results, covered next.

### 4. proto2's Own Findings as a Negative Result

Sentence-level NLI classification produced too many candidate sentences to be usable — 151 TechnicalMethod sentences for the MapReduce paper alone — and its recall-only substring evaluation (18/24 across six papers) only checked whether a gold term appeared somewhere in the output, not whether the output itself was correct. With 100+ accepted sentences in some roles, a substring match is nearly certain to succeed somewhere in the list, which inflates the apparent recall without saying anything about precision. Excluding Related Work by heading, which describes other papers rather than the target paper's own methodology, cut BERT's TechnicalMethod count from 67 to 62 sentences; excluding the whole Introduction cut it further to 54, but also removed sentences that correctly described BERT's own method, so full exclusion traded recall for precision rather than solving the underlying problem. proto2 also had no mechanism to separate a paper's own method from one it cites: a sentence describing ELMo in BERT's Introduction scored 0.87 as TechnicalMethod, even though ELMo is prior work, not BERT's own method. This sharpens Färber et al.'s [8] "used vs mentioned" gap (Section 2 above) with a concrete instance from my own data, and motivates proto3's document-level extraction with an explicit authorship rule (Chapter 3).

### 5. Document-Level and LLM-Based Structured Extraction

Jain et al. [4] argue that "a significant amount of information can only be gleaned from analyzing the full document" — a document-level information extraction (IE) claim. My own data supports this directly: Dataset and EvaluationMetric typically appear only in a paper's Experiment section, not the Abstract, so an extraction method effectively limited to a small set of sentences, as proto2's Introduction-heavy output tended to be, would miss them.

Structured extraction with LLMs is an established research approach. Dagdelen et al. [11] extract structured information from scientific text with LLMs. Polak and Morgan [12] extract materials data from research papers using conversational LLMs and prompt engineering. Both apply an LLM to pull structured fields out of scientific documents, similar in spirit to how proto3 pulls a four-role methodology profile from a computing paper. I apply this general approach to this project's specific four-role schema, combined with the authorship rule (Section 4 above) and a document-level context window (Chapter 3).

### 6. Synthesis

I could not find prior work combining the structured methodology vocabulary from Oates [1] and Pilkington & Pretorius [2], the four-role schema from Jain et al. [4], zero-shot or LLM-based extraction without an annotated corpus, and general computing papers rather than only ML benchmarks, which motivated testing the combination directly across two prototype iterations.

| Source | Contribution | Strength | Limitation | Relevance to this project |
|---|---|---|---|---|
| Oates [1] | Methodology vocabulary | Clear concept names for methodology components | Designed for human use; not extraction-oriented | Motivates structured extraction |
| Pilkington & Pretorius [2] | Formal methodology ontology | Formal relationships between concepts | No extraction system or corpus | Supports treating methodology as a structured domain |
| Jain et al. [4] | Document-level extraction of Dataset, Metric, Task, and Method | All four roles; working system; document-level argument | 438 annotated ML papers; four PhD annotators | Confirms four roles; motivates document-level extraction and both proto2 and proto3's approaches |
| Ghosh et al. [5, 6] | TechnicalMethod extraction from AI papers | Methodology-specific sequence labeling | One role only; AI papers; supervised | Shows difficulty of extracting method names |
| Färber et al. [8] | Used vs mentioned methods and datasets | Handles authorship attribution | Method and Dataset only; labeled mentions required | Motivates proto3's authors'-own-work rule |
| Yin et al. [9] | Zero-shot NLI text classification | No task-specific training data needed | Tested on general-domain text only; sentence-level | Basis for proto2; superseded by document-level extraction in proto3 |
| Dagdelen et al. [11]; Polak and Morgan [12] | LLM-based structured extraction from scientific text | Document-level, schema-guided, no annotated corpus needed | Applied to different domains (materials science) | Basis for proto3's schema-guided LLM extraction |

Table 3: Key sources for this project.

### Feedback on the Preliminary Report

The preliminary report received marker feedback. This revision addresses each written comment directly:

| Marker comment | How this revision addresses it |
|---|---|
| Relies heavily on the same small group of sources; a literature review can be built around the methods and tools used, without needing similar projects; avoid casual first-person narration such as "I test", use academic language | This chapter adds two sources on LLM-based structured extraction (Dagdelen et al. [11]; Polak and Morgan [12]), the method proto3 itself uses, and Khot et al. [13] on decomposed prompting for Chapter 3's architecture discussion; the whole report also moves to a formal academic register |
| In-text citation numbering started from `[7]`, not `[1]`; author names were mixed with numbered citations | References are renumbered by order of first appearance, starting at `[1]`; every reference-list entry is cited at least once in the body text |
| Project concept needs a thorough analysis of the target domain and users | Chapter 3 §1 adds a user-need / system-requirement / evaluation table connecting each user need to a concrete requirement and how it is measured |
| No proper diagram of data flow, component interaction, failure handling, and the user interface; key technologies section needed more detail | Figure 2 is replaced with a box/failure-path diagram showing parse failure, empty-section handling, the no-supported-answer case, and the user-facing output step |
| Workplan should show task durations, dependencies, risks, and contingency time, with a fuller task breakdown | Table 7 breaks the remaining work into duration, dependencies, risk, and contingency |
| Prototype evaluation used only a small number of papers and counted one matching word as a correct result | Chapter 5 scores gold-label match as classification (Precision/Recall/F1) with Wilson confidence intervals, backed by a 5-run variance study and a consolidated manual review |
| The literature review repeats points and needs a more critical comparison between studies; the design is easy to follow, but diagrams, threshold choice, and the sentence-level classification assumption need justification; the next evaluation should use fixed gold labels, more papers, precision and recall | Section 6's synthesis table and the study-vs-study comparisons above address the first point; Chapter 3 §4 now states directly that proto3 has no per-sentence threshold to justify and that the sentence-level circularity concern does not apply once extraction is document-level; of the evaluation redesign, fixed gold labels and Precision/Recall are addressed directly (Chapter 5 §1-2), but growing the paper count beyond six is a scope decision this revision does not implement — Chapter 5 §2 states the reason (the Wilson-interval math shows meaningfully tightening the CIs would need 30-40 gold-labeled papers per role) rather than claiming the point is resolved |

---

## Chapter 3: Design (1144 words)

The system extracts research methodology from computing papers. An input is a PDF, and an output is a role-based profile (Table 1, Chapter 1).

### 1. Domain and Users

The domain and users are unchanged from the preliminary report. The domain is computing research papers, mainly systems, machine learning (ML), algorithms, and human-computer interaction (HCI). The primary users are computing students doing literature reviews; secondary users are early-stage researchers or supervisors who want a quick overview of a paper. proto3 changed the output quality — one checkable answer per role instead of a list of candidate sentences — not the target domain or audience.

Table 4 connects each user need to a system requirement and the metric that evaluates it, addressing the preliminary report's feedback that the domain and user analysis needed a fuller, more evidenced connection between users and requirements, not just a list of who the users are.

| User need | System requirement | Evaluation |
|---|---|---|
| Quickly understand a paper | Show the four roles clearly | Output size (one answer per role, Chapter 4) |
| Check the original paper | Show evidence sentences | Evidence correctness (manual review, Chapter 5 §4) |
| Avoid missing important information | High recall | Recall (Chapter 5 §2-3) |
| Avoid too much irrelevant information | Reduce noisy output | Precision (Chapter 5 §2-3) |

Table 4: User needs mapped to system requirements and evaluation.

### 2. Design Justification

The core feature is Stage 2: one structured, evidence-backed answer per role, not a list of 14-160 candidate sentences (Chapter 2, Section 4). The authors'-own-work rule in the prompt directly targets proto2's authorship-attribution failure (the ELMo/BERT case, Chapter 2, Section 4). The four-role JSON shape is enforced by `response_json_schema`, generated from Pydantic models rather than described in the prompt text, which removes an entire class of parsing and output-shape bugs (Chapter 4).

Two further design considerations are not yet implemented.

First, whether extraction should stay joint (the current design: one call returns all four roles) or move to decomposed extraction (four independent role-specific calls, optionally followed by a consolidation pass). Khot et al. [13] show that decomposing a complex task into independently-optimizable subtasks can beat a single joint few-shot prompt on several reasoning tasks, while Jain et al.'s [4] document-level argument (Chapter 2) favours joint handling, since it can exploit cross-role relationships appearing in one sentence (e.g. "Transformer"/"WMT"/"BLEU" together). A decomposed-only pilot (variant B vs the joint baseline, one run each, no consolidation) is a stretch item for this report; results, if run, belong in Chapter 5, and the consolidation variant plus a full comparison are deferred to further work (Chapter 6).

Second, whether every role should stay single-valued, or whether some should allow multiple answers. The baseline already shows that Dataset and EvaluationMetric can be naturally multi-valued: AlexNet and ResNet both report top-1 and top-5 error rates squashed into one string, and BERT's own gold EvaluationMetric label lists both "accuracy" and "F1" as acceptable (Appendix B, Table B1), since the paper genuinely reports both. An informal NotebookLM cross-check, run independently on each paper without being told the schema was single-valued, produced similarly multi-valued outputs for BERT, ResNet, and Transformer — for example, BERT's single-valued Dataset answer is "SQuAD v1.1," while NotebookLM listed BooksCorpus, Wikipedia, GLUE, and SQuAD v1.1/v2.0 from the same source text. Task and TechnicalMethod show no such pattern. Forcing Dataset and EvaluationMetric into one string loses information; a multi-valued design would need per-item evidence rather than one shared quote per list, and a ranked "primary first" order rather than a numeric confidence field, since this project's own measured non-determinism (Chapter 5) argues against a second, uncalibrated confidence axis. This discussion is write-up only for this report; full implementation is deferred to Chapter 6.

### 3. Model Choice

A paper's cleaned full text is typically 4,000-20,000 tokens, which fits within the context window of several modern long-context LLMs without chunking:

| Model | Context | Cost |
|---|---|---|
| Gemini Flash | 1M tokens | cheap API |

Table 5: Long-context model.

I selected Gemini (`gemini-3.5-flash`, via the `google-genai` software development kit), mainly because it is the simplest to set up from Google Colab: the API key comes from Colab's built-in secret manager (`google.colab.userdata`), with no separate account needed beyond the Google account already used for Colab.

### 4. Overall Pipeline

The pipeline runs in five stages. The preliminary report's feedback asked for a diagram that shows data flow, component interaction, failure handling, and where results reach the user, not only a linear arrow list, so Figure 2 below adds each stage's failure path and the final user-facing step:

<figure>
<pre>
PDF input
  │
  ▼
GROBID parse (Stage 0) ──fail──▶ parse error surfaced to user
  │ ok
  ▼
TEI validation ──empty/invalid section──▶ section skipped, logged
  │ ok
  ▼
Stage 1: concatenate sections (reading order)
  │
  ▼
Stage 2: schema-guided LLM extraction ──no supported answer in text──▶ role = null (not fabricated)
  │ ok
  ▼
MethodologyProfile JSON (answer + evidence per role)
  │
  ▼
User-facing output: role table + quoted evidence (Table 1 / Figure 6)
</pre>
<figcaption>Figure 2: proto3 extraction pipeline with failure paths and the user-facing output step.</figcaption>
</figure>

Compared with proto2's pipeline (PDF → GROBID [14] → TEI XML → section filtering → sentence splitting and cleaning → zero-shot NLI role classification → MethodologyProfile JSON), there are two differences: there is no sentence splitting, and there is no per-sentence acceptance threshold. The LLM sees the (mostly) whole document and returns one decision per role directly, instead of a list of candidate sentences each scored independently.

These two differences directly resolve two items from the preliminary report's feedback. First, the feedback asked for a clear reason behind proto2's NLI acceptance threshold of `0.5`. proto3 has no such value to justify, because extraction is no longer a per-sentence accept/reject decision. Second, the feedback questioned proto2's sentence-level assumption that a sentence describes one role at a time, since single-label sentence classification could only ever produce single-label results, whatever the underlying text actually contained. That circularity does not apply to proto3 either, since extraction is document-level rather than per-sentence; the related but distinct question of whether a *role* (not a sentence) should allow more than one answer is addressed separately in Section 2 above.

### 5. Evaluation Plan

proto2's plan treated a substring gold-label match with a 10-out-of-12 success threshold as sufficient, but a present-but-wrong answer cost nothing there. For proto3 I redesigned this: I score gold-label match as a classification problem (true positive, false positive, false negative), report Precision, Recall, and F1 per role, and add Wilson 95% confidence intervals on Precision and Recall only — F1 is a harmonic mean, not a proportion, so a Wilson interval on it directly is not statistically meaningful; a point-estimate F1 is appropriate at this sample size. I report both micro and macro averages, headlining macro, because the four roles are fixed, equally mandatory schema fields, not a frequency distribution.

I kept the sample at six papers rather than growing it: tightening the confidence intervals meaningfully would need roughly 30-40 gold-labeled papers per role, not the 6-10 reachable in three weeks with no second annotator, so I kept the corpus at six papers given the remaining time and annotation constraints; this limits generalisability and remains a limitation of the evaluation. I planned a logged variance study (repeat the pipeline several times rather than trust one run) and a single consolidated manual review pass covering plausibility, evidence support, authorship, and whether the quote appears in the source text.

Once the five-run variance study existed, I also had to decide how to report it. I chose not to pool the five runs' true/false positive/negative counts into a single Wilson interval (n=30 trials per role): the 30 trials are five repeats of the same six papers, not 30 independent observations, so treating them as independent Bernoulli trials would overstate precision. Instead, I keep the two measures separate: the n=6 baseline Wilson interval (Section 2 above) for paper-level uncertainty, and the five-run F1 mean, minimum, maximum, and range (Chapter 5) for run-to-run non-determinism. Each answers a different question, and neither substitutes for the other.

### 6. Work Plan

| Period | Main task | Output | Status |
|---|---|---|---|
| Before 29 June | Literature review, design, proto2 (sentence-level NLI) | Preliminary Report | Done |
| July | proto3 Stages 0-2 (document-level extraction); gold-label-match evaluation with Wilson confidence intervals on Precision/Recall | Baseline P/R/F1 table, 5-run F1 variance table (mean/min/max/range) | Done |
| July-August | Consolidated manual review pass; proto2 → proto3 fixed/not-fixed synthesis; figures for Implementation/Evaluation chapters | Draft Report 3 material | Done |
| August | Decomposed-extraction pilot, variant A vs B only | — | Cut, not run |
| August | Related Work ablation | — | Cut, not run |
| August (final stage) | Write Final Report, incorporating whichever items complete in time | Final submission | Not started |

Table 6: Work plan summary.

The preliminary report's feedback asked the workplan to show durations, dependencies, risks, and contingency time explicitly, not just broad monthly periods. Table 7 breaks the remaining work down to that level of detail:

| Task | Duration | Depends on | Risk | Contingency |
|---|---|---|---|---|
| Report3 feedback pass (this revision) | 1-1.5 days | Marker feedback on report1 (received) | Scope creep into re-running experiments instead of writing | Fixed time box; defer any experiment-shaped idea to Chapter 6 further work |
| Report3 final assembly and word-budget trim | 0.5 day | All chapter drafts complete | Total exceeds the 9,500-word cap | Cut from Introduction/Conclusion first, since Literature Review and Evaluation carry the marked criteria |
| Final Report write-up | Remaining time to deadline | Report3 marker feedback | Underestimating how much the final-report feedback changes | Reserve the last few days as unallocated contingency, not scheduled to any task |

Table 7: Remaining work broken into duration, dependencies, risk, and contingency.

---

## Chapter 4: Implementation (735 words)

proto1 was an AI-drafted reference implementation only, not used directly, per this module's constraint on AI assistance for CM3060 submissions. proto2 was my own sentence-level zero-shot natural language inference (NLI) classifier: it classified every sentence in a paper into one of the four roles, producing a list of candidate sentences per role rather than one answer. proto3 reframes the task as document-level extraction: given a computing paper, it extracts one answer per role — TechnicalMethod, Task, Dataset, EvaluationMetric — each with a section heading and a verbatim quote as evidence, using a schema-guided prompt to a long-context LLM. On "Attention Is All You Need" [D6], for example: TechnicalMethod = "Transformer", Task = "machine translation", Dataset = "WMT 2014 English-German", EvaluationMetric = "BLEU", each backed by its own quote and section.

### 1. Features Implemented

The prototype takes GROBID TEI XML and produces one JSON object containing an answer and evidence for each of the four roles (full example below). Parsing the XML and extracting section text reuses proto2's GROBID-based approach; the core new feature is extracting one structured answer and its evidence per role, using a schema-guided prompt to a long-context LLM rather than classifying each sentence independently.

### 2. Algorithms and Techniques

The pipeline has five stages. Stage 0 reuses proto2's GROBID-based parsing to turn a PDF into TEI XML, then keeps the Abstract and body sections while skipping References and Acknowledgements by heading match. Stage 1 concatenates the remaining section texts in reading order, with no sentence splitting and no per-sentence threshold — a direct response to proto2's output-volume problem (Chapter 2). Stage 2 sends the full document to the LLM with a schema-guided prompt: the four-role JSON shape is enforced by `response_json_schema`, generated from the `MethodologyProfile` Pydantic model, not by describing the shape in the prompt text; the null-correlation between `answer` and `evidence` — a role is either both null or both present — is enforced by a Pydantic `model_validator`, not a prompt instruction. Dataset and EvaluationMetric often occur only in the Experiment section, not the Abstract or Method, so I keep the full document rather than an excerpt.

<figure>

```python
class Evidence(BaseModel):
    section: str = Field(description="Exact section heading containing the quote.")
    quote: str = Field(
        description="One sentence quoted verbatim from the paper, supporting answer."
    )


class RoleExtraction(BaseModel):
    answer: str | None
    evidence: Evidence | None

    @model_validator(mode="after")
    def answer_and_evidence_must_match(self) -> Self:
        if (self.answer is None) != (self.evidence is None):
            raise ValueError(
                "answer and evidence must either both be null or both be present"
            )
        return self
```

<figcaption>Figure 3: Evidence/RoleExtraction Pydantic models with the null-correlation validator (`proto3/3pipeline.ipynb`, "Data Models").</figcaption>
</figure>

### 3. Code Explanation

Four details are the most technically interesting, given the tight word budget for this chapter. First, the prompt states only what the JSON schema itself cannot express:

<figure>
<pre>
Rules:
- Use the authors' own method, not methods cited from prior work.
- Return null when a role is not present in the paper.
- Evidence quotes must be copied verbatim from the paper, not paraphrased.
</pre>
<figcaption>Figure 4: Prompt rules excerpt from `proto3/3pipeline.ipynb`, "Stage 2b — Prompt Template".</figcaption>
</figure>

Everything about the output *shape* — the nested `{section, quote}` evidence object, the four required role fields — lives on the Pydantic models (Figure 3) instead of the prompt text.

Second, the Gemini call uses `response_json_schema` together with `temperature=0` and `seed=0`, and parses the reply directly with `MethodologyProfile.model_validate_json(...)`, with no manual JSON-extraction step:

<figure>

```python
response = client.models.generate_content(
    model=MODEL_NAME,
    contents=prompt,
    config=types.GenerateContentConfig(
        temperature=0,
        seed=0,
        response_mime_type="application/json",
        response_json_schema=MethodologyProfile.model_json_schema(),
    ),
)

profile = MethodologyProfile.model_validate_json(response.text)
```

<figcaption>Figure 5: Gemini call and response parsing (`proto3/3pipeline.ipynb`, "Stage 2c — Call Gemini and Parse Response").</figcaption>
</figure>

An earlier prompt version described the `evidence` field inconsistently — it asked for "evidence" as a single quoted sentence, but also said to return the section heading and the quote together. Testing on "Attention Is All You Need" showed how Gemini resolved that ambiguity: it returned `evidence` as one flat string with the heading prepended, e.g. `"## Introduction In this work we propose..."`, instead of the nested `{section, quote}` object the design intended. At the time I fixed this by rewriting the prompt to make the nested shape explicit; today the nested shape is guaranteed by the schema regardless of prompt wording, so this specific bug class is now structurally prevented rather than patched.

Third, `response_schema` and `response_json_schema` are not interchangeable. `response_schema=MethodologyProfile` fails with `400 INVALID_ARGUMENT ... Unknown name "additional_properties"`, because it converts to Google's own `Schema` proto, which does not support `additionalProperties`, and Pydantic's `extra="forbid"` produces exactly that field. `response_json_schema` accepts a real JSON Schema dict instead, so `MethodologyProfile.model_json_schema()` is passed there.

Fourth, code quality: `pyright` in strict mode and `ruff` report zero issues, and a pytest suite in `proto3/tests/` covers `scoring.py`'s evaluation logic and the `model_validator`'s null-correlation check, with `proto3/sync_generated.py` keeping notebook cells in sync with the installable `proto3/src/uol_fp/` modules. `proto3/baseline.ipynb` used to be a byte-identical duplicate of `3pipeline.ipynb`, kept only because it had produced the six `proto3/baseline/*.json` files; it has since been deleted, so there is no second notebook to keep in sync by hand.

### 4. Visual Representation

For "Attention Is All You Need" [D6], the full extraction output is:

<figure>

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

<figcaption>Figure 6: Full extraction output for "Attention Is All You Need" [D6] (`proto3/baseline/transformer.json`).</figcaption>
</figure>

I include the Stage 2c cell screenshot showing the raw Gemini call and its parsed JSON output, so the extraction is visible running directly rather than only described. Table 8 already shows the proto2/proto3 before/after contrast numerically, so it is not repeated here as a screenshot.

<figure>
<img src="Screenshot%202026-08-17%20093143.png" alt="proto3 Stage 2c cell and output" style="width:100%;max-width:100%;">
<figcaption>Figure 7: proto3 Stage 2c cell and output (screenshot).</figcaption>
</figure>

Table 8 shows the same contrast numerically for the Transformer paper: proto2's accepted-sentence counts per role versus proto3's one answer per role.

| Paper | proto2 TechnicalMethod | proto2 Task | proto2 Dataset | proto2 EvaluationMetric | proto3 |
|---|---|---|---|---|---|
| Transformer [D6] | 14 sentences | 0 sentences | 0 sentences | 160 sentences | 1 answer + evidence per role |

Table 8: proto2 sentence-count output vs proto3 answer-and-evidence output, Transformer paper.

---

## Chapter 5: Evaluation (1654 words)

### 1. Evaluation Method

I evaluate gold-label match as a classification problem — Precision, Recall, and F1 per role, with Wilson 95% confidence intervals on Precision and Recall — backed by a logged 5-run variance study and a consolidated manual review pass covering plausibility, evidence support, authorship, and whether the quote appears in the source text, all in a single read. The Related Work ablation runs only if time allows.

Precision/Recall/F1 (P/R/F1) is more appropriate than proto2's recall-only substring check, because a present-but-wrong answer now costs both precision and recall, instead of being free the way it was when any accepted sentence containing the gold term counted as a hit, regardless of how many other sentences were also returned.

The manual review folds the evidence-verbatim check into the same pass as support and authorship, rather than a separate automated script: a verbatim match only proves the LLM followed the copy-verbatim instruction, not that the evidence is good evidence (a real, verbatim quote from a Related Work sentence could still be the wrong evidence for a paper's own methodology), and the reviewer already has to read the source to judge support and authorship.

### 2. Gold-Label-Match Results

Scoring the frozen baseline (`proto3/baseline/*.json`) against gold labels across all six papers gives:

| Role | P | R | F1 |
|---|---|---|---|
| TechnicalMethod | 0.83 | 0.83 | 0.83 |
| Task | 0.33 | 0.33 | 0.33 |
| Dataset | 0.80 | 0.67 | 0.73 |
| EvaluationMetric | 0.80 | 0.67 | 0.73 |
| Micro | 0.68 | 0.62 | 0.65 |
| Macro | — | — | 0.655 |

Table 9: Baseline gold-label-match results, all six papers.

I report macro as the headline "Overall" score, because the four roles are fixed, equally mandatory schema fields, not a frequency distribution — a user needs all four, not just whichever role happens to have the most examples. I show both averages, but note that they are close here (0.65 vs 0.655) only because every role happens to have n=6 in this dataset — a coincidence of this dataset, not a property of the method.

On sample size, Wilson 95% confidence intervals give a clearer picture than a vague "small sample" caveat: TechnicalMethod recall 0.83 gives a confidence interval of [0.44, 0.97]; Task recall 0.33 gives [0.10, 0.70]. These substantially overlap, so I do not claim TechnicalMethod is reliably "solved" while Task is reliably "broken" at this sample size. I do not put a Wilson interval on F1: it is the harmonic mean of Precision and Recall, not a proportion, so a Wilson interval on it directly is not statistically meaningful; I report F1 as a point estimate instead. I kept the corpus at n=6 for the reasons given in Chapter 3. One gold label also carries a specific evaluator-influence caveat worth stating plainly: AlexNet's TechnicalMethod gold label was changed from "AlexNet" to "convolutional" after running the pipeline and inspecting its output, since the 2012 paper predates the name "AlexNet" and never uses it. Adjusting a gold label after seeing model output is a real limitation on how strongly this result generalises, and it is one instance of a broader single-annotator problem: I wrote both the gold labels and, later, the answers being checked against them (Section 4 below).

These next two figures show the scoring running directly in the notebook, rather than only as transcribed numbers: Figure 8 gives the aggregate baseline result behind Table 9, and Figure 9 gives a representative single-paper breakdown (Transformer), baseline versus pipeline.

<figure>
<img src="Screenshot%202026-08-17%20093240.png" alt="Baseline P/R/F1 scoring output" style="width:100%;max-width:100%;">
<figcaption>Figure 8: Baseline P/R/F1 scoring output (`proto3/3pipeline.ipynb`, Stage 3).</figcaption>
</figure>

<figure>
<img src="Screenshot%202026-08-17%20093305.png" alt="Per-paper gold-label scoring, baseline vs pipeline, Transformer" style="width:100%;max-width:100%;">
<figcaption>Figure 9: Per-paper gold-label scoring for the Transformer paper, baseline vs. pipeline (`proto3/3pipeline.ipynb`, Stage 3).</figcaption>
</figure>

### 3. Variance Study

I logged five full pipeline runs to `proto3/results/run{1..5}/*.json` and aggregated them with `proto3/aggregate_runs.py`. Per-role F1 across the five runs:

| Role | F1 mean | F1 min | F1 max | F1 range |
|---|---|---|---|---|
| TechnicalMethod | 0.83 | 0.83 | 0.83 | 0.00 |
| Task | 0.33 | 0.33 | 0.33 | 0.00 |
| Dataset | 0.91 | 0.91 | 0.91 | 0.00 |
| EvaluationMetric | 0.57 | 0.33 | 0.67 | 0.33 |

Table 10: Per-role F1 across 5 real pipeline runs (`proto3/results/aggregate.json`).

Three of four roles were perfectly stable across five real repetitions — stronger evidence than an earlier two-run anecdote, which had shown both Dataset and EvaluationMetric moving. At n=5, Dataset turned out stable, and only EvaluationMetric is not (F1 ranged 0.33-0.67 across runs, with unchanged code, `temperature=0`, and `seed=0`), which narrows the non-determinism finding rather than just repeating it. The frozen baseline behind Table 9 in Section 2 is not a like-for-like sixth run alongside these five: it was generated before `temperature=0` and `seed=0` were added to the Gemini call, so only the five logged runs share identical settings.

An informal cross-check with Google NotebookLM, run independently on each paper, found stable agreement on TechnicalMethod across all six papers — exact or near-exact matches including "Google", "BERT", "Transformer", and "MapReduce" — independent corroboration that this is the strongest role.

I did not pool the five runs' true/false positive/negative counts into a Wilson interval (n=30 trials per role): the 30 trials are five repeats of the same six papers, not 30 independent observations, so an ordinary Wilson interval on them would overstate precision. Paper-level uncertainty (how results might vary across a different sample of papers) is already covered by the n=6 baseline Wilson interval in Section 2 above; the five-run study instead answers a different question — run-to-run non-determinism, how the same six papers' results vary when the pipeline is simply run again — and Table 10's mean/min/max/range already answers that question without a confidence interval on top of it. On that basis, TechnicalMethod's F1 (0.83) exceeded Task's F1 (0.33) in every one of the five runs, a consistent gap that needs no interval to state.

MapReduce's Task slot (gold `"distributed"`, system answer `"automatic parallelization and distribution of large-scale computations"`) fails the substring-match rule despite being arguably correct — Task's low F1 is partly a measurement-instrument artifact, not purely a model failure.

MapReduce's Dataset slot (gold `"TeraSort"`) answered `null` in every one of the five runs — a genuine recall miss, since NotebookLM independently found the dataset description (two roughly 1 terabyte grep/sort benchmarks) in the same source text. Pagerank's EvaluationMetric slot (gold `"quality"`) answered `"precision"` in every one of the five runs — scored wrong by substring match, but the paper's text supports both terms, and NotebookLM's independent extraction also names precision.

### 4. Manual Review and the Related Work Ablation

The review template is already built, with each paper's answer, section, and quote staged next to four judgment columns (plausible? evidence supports? authors' own work? quote in source?) — it stages some specific open questions rather than starting from a blank page: BERT's Task quote cites prior work by name, so the review needs to decide whether pre-training is BERT's own contribution or just motivation; ResNet's Task quote cites bracketed prior work for "a series of breakthroughs," raising the same question of whether the sentence establishes the paper's own task or credits others'.

All 24 slots are scored. Two are null (Pagerank/EvaluationMetric, MapReduce/Dataset), judged separately below; across the other 22 scored slots:

| Check | Failures (of 22) | Slots |
|---|---|---|
| Plausible? | 2 | Pagerank/TechnicalMethod, Pagerank/Task |
| Evidence supports? | 5 | Pagerank/TechnicalMethod, Pagerank/Task, AlexNet/Task, BERT/Task, BERT/Dataset |
| Authors' own work? | 6 | Pagerank/Task, AlexNet/Task, BERT/Task, BERT/Dataset, BERT/EvaluationMetric, ResNet/Task |
| Quote in source? | 1 | ResNet/Task |

Table 11: Manual review failure counts by check type, 22 scored slots.

Six slots pass the quote-in-source check but still fail on evidence-support or authorship — a real, verbatim quote that is still the *wrong* evidence, distinct from a fabricated quote: Pagerank/TechnicalMethod ("Google is the proposed system, not the technical method"), Pagerank/Task ("information retrieval is the broader problem domain, not the task performed by the proposed system"), AlexNet/Task ("the quote does not directly prove that this is AlexNet's own task"), BERT/Task (the quoted sentence "describes prior work rather than BERT's own contribution"), BERT/Dataset ("valid dataset, but one of several"), and BERT/EvaluationMetric ("F1 is one of several evaluation metrics used across BERT's downstream tasks"). ResNet's Task answers this chapter's own open question from Section 2: the quote "cites bracketed prior work `[21, 49, 39]` for the breakthroughs," crediting prior work rather than establishing the paper's own task — the one slot where quote-in-source and authorship fail together, rather than the "verbatim but wrong" pattern above.

On the two null slots: MapReduce's Dataset is a real miss, not a genuine absence — the paper "uses large benchmark datasets for grep and sort experiments (about 1 TB each)," which NotebookLM independently found in the source text (Section 3 above). Pagerank's EvaluationMetric is more ambiguous and leans toward the gold label being the problem: precision "is discussed as an important search-quality criterion, but it is not actually measured or reported as an experimental metric" — gold `"quality"` is likely too vague or mislabeled.

BERT's Dataset and EvaluationMetric failures also confirm the multi-valued-roles finding from Chapter 3 directly: choosing only one of several correct answers can be technically correct but still gives an incomplete picture. Some gold answers may also be too simple or use the wrong category, so evaluating against gold labels alone can give a misleading result.

This pass has the same single-annotator bias as the gold labels it checks against — the same problem already noted in Section 2: I wrote both the gold labels and, later, the answers being checked against them. I do not present this review as more objective than the gold labels themselves.

The Related Work ablation is first on the cut list for this report, demoted from a higher priority because it does not address Task, the project's weakest role, the way the decomposed-extraction pilot does. It is not required to prove the core claims, so it stays deferred to further work.

### 5. Critical Evaluation

Mapping proto2's three named failure modes onto what proto3 actually measured, across the whole project rather than proto3 alone:

| proto2 failure mode | proto3 status | Evidence |
|---|---|---|
| Output volume (151 TechnicalMethod sentences for MapReduce) | Fixed by design | One answer per role, every paper, by construction of Stage 2's schema-guided extraction |
| No authorship-attribution mechanism (ELMo scored 0.87 as BERT's TechnicalMethod) | Addressed by design, but not reliably solved | The authors'-own-work rule targets this directly; the manual review above found 6 of 22 scored slots still fail authorship, concentrated in Task (4 of 6 papers) |
| Recall-only evaluation (10/12, then 18/24 substring match) | Fixed | Precision/Recall/F1 per role, Wilson confidence intervals on Precision/Recall, a 5-run variance study |

Table 12: proto2 → proto3 synthesis.

Achievements: I moved from proto2's recall-only substring check to proto3's classification-based Precision/Recall/F1 with confidence intervals, now backed by five real repeated runs rather than a single snapshot. Every answer is evidence-backed, and the five-run study shows TechnicalMethod's F1 consistently exceeding Task's F1 in every run, strengthening the "TechnicalMethod works, Task doesn't" claim from the single-baseline n=6 evaluation in Section 2, without needing a pooled confidence interval to make the point.

Weaknesses: Task's F1 is low (0.33, stable across all five runs, and partly a metric artifact per Section 3). The four-role schema itself is ML-benchmark-shaped, inherited from SciREX's ML-conference corpus (Chapter 2, Section 2); of the six papers, two are systems papers (MapReduce, Google Search), and proto2 already showed these fit the schema worse than the four ML papers, an open generalization question. MapReduce's Dataset slot answered `null` across all five runs (gold `"TeraSort"`), externally corroborated by the NotebookLM cross-check, which confirms the dataset description is present in the source text — a genuine model recall failure, distinct from the gold-label-artifact cases elsewhere in the results.

The decomposed-extraction pilot (variant B) was not run — cut, along with the Related Work ablation, and both stay deferred to further work (Chapter 6).

---

## Chapter 6: Conclusion (629 words)

### Summary

This project automatically extracts research methodology — technical method, task, dataset, and evaluation metric — from computing research papers using large language models. I built two implemented iterations: proto2, my own sentence-level zero-shot NLI classifier, which worked but produced too much unusable output and could not separate authors' own methods from cited prior work; and proto3, the current document-level, schema-guided extraction pipeline, which returns one evidence-backed answer per role per paper.

**Did it work?** Partially: TechnicalMethod extraction and output usability improved clearly over proto2; Task accuracy and schema generality to non-ML-benchmark papers remain unresolved.

**What did the project actually teach us?** The hardest problem was not producing structured JSON — schema conformance is solved by `response_json_schema` (Chapter 4) — but deciding what the four roles mean consistently across different kinds of computing papers. MapReduce and Google Search struggle not only because of LLM limitations but because Task/Dataset/EvaluationMetric, as a schema, comes from ML-benchmark structure and doesn't map cleanly onto systems research.

**Did it meet the original user need?** Returning to Chapter 1's goal — support the first pass of a literature review — proto2's output was too voluminous to serve that purpose; proto3's one-answer-per-role-plus-evidence format is a clear improvement, but Task's low accuracy and the still-unimplemented multi-valued roles (Chapter 3) mean a user still needs to verify results by hand, not trust them outright.

As of this draft, Stages 0-2 are implemented, the gold-label-match evaluation is done with confidence intervals and a 5-run variance study, the consolidated manual review is done, and the decomposed-extraction pilot and the Related Work ablation were both cut, not run.

### Further Work

Several items remain for further work. Given the remaining time and annotation constraints, the corpus was kept at six papers rather than grown; this limits generalisability and remains a limitation of the evaluation (Chapter 3). A formal inter-annotator-agreement study with a second human annotator does not exist on this solo project; the informal NotebookLM cross-check in Chapter 5 narrows this gap but does not close it, since it is one AI tool's single pass with no annotation protocol. A full multi-model comparison (Gemini vs Claude Haiku vs Llama 3.1) and the Related Work ablation, if not reached, are also left for later. Testing on non-ML-benchmark papers — systems, human-computer interaction (HCI) — would show whether the four-role schema and document-level extraction generalize better than proto2's sentence classification did, since proto2 already showed systems papers fit this schema worse.

The consolidation pass from Chapter 3 (variant C: a fifth call checking the decomposed pilot's four role-specific outputs for mutual consistency against their evidence) and the full three-way comparison of joint (A), decomposed (B), and decomposed-plus-consolidation (C) extraction are the next experiment to run. My hypothesis is that per-role accuracy follows B or C > A, and cross-role consistency follows C > A > B, but no paper directly shows that this four-role methodology-extraction task favours decomposition, so it remains untested. The multi-valued schema for Dataset and EvaluationMetric also remains to be implemented: a new `MultiRoleExtraction` type with per-item evidence and a ranked list capped at three items, gold-label re-annotation for the four cells already identified (BERT/Transformer Dataset, AlexNet/ResNet EvaluationMetric), a parallel `score_role_multi` scoring function, and rerunning and rescoring all six papers.

### Broader Theme

One broader theme worth raising is the tension between structured-output guarantees and semantic correctness. `response_json_schema` guarantees that Gemini's reply is syntactically valid and has the right shape — the schema-conformance problem is solved. It does not guarantee the *content* is correct: an answer can be syntactically well-formed and still wrong, as the "metric is blunt" cases and the manual review in Chapter 5 show. This distinction between schema conformance and semantic correctness is not specific to this project — it applies to LLM-based structured extraction generally.

---

## References

[1] Briony J. Oates. 2006. *Researching Information Systems and Computing*. SAGE Publications, London.

[2] Colin Pilkington and Laurette Pretorius. 2015. A conceptual model of the research methodology domain. In *Proceedings of the 7th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K 2015), Volume 2: KEOD*. SCITEPRESS – Science and Technology Publications, Setúbal, Portugal, 96–107. https://doi.org/10.5220/0005613100960107

[3] Zsolt T. Kosztyán, Tünde Király, Tibor Csizmadia, Attila Imre Katona, and Ágnes Vathy-Fogarassy. 2025. Automated research methodology classification using machine learning. *Engineering Applications of Artificial Intelligence*, article 111039. https://doi.org/10.1016/j.engappai.2025.111039

[4] Sarthak Jain, Madeleine Van Zuylen, Hannaneh Hajishirzi, and Iz Beltagy. 2020. SciREX: A Challenge Dataset for Document-Level Information Extraction. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, Online, July 2020. Association for Computational Linguistics, 7506–7516. https://doi.org/10.18653/v1/2020.acl-main.670

[5] Madhusudan Ghosh, Debasis Ganguly, Partha Basuchowdhuri, and Sudip Kumar Naskar. 2023a. Enhancing AI research paper analysis: methodology component extraction using factored transformer-based sequence modeling. arXiv:2311.03401. https://doi.org/10.48550/arXiv.2311.03401

[6] Madhusudan Ghosh, Debasis Ganguly, Partha Basuchowdhuri, and Sudip Kumar Naskar. 2023b. Extracting methodology components from AI research papers: a data-driven factored sequence labeling approach. In *Proceedings of the 32nd ACM International Conference on Information and Knowledge Management (CIKM 2023)*. https://doi.org/10.1145/3583780.3615258

[7] Yongqiang Ma, Jiawei Liu, Wei Lu, and Qikai Cheng. 2023. From "what" to "how": Extracting the procedural scientific information toward the metric-optimization in AI. *Information Processing & Management*, 60(3), article 103315. https://doi.org/10.1016/j.ipm.2023.103315

[8] Michael Färber, Alexander Albers, and Felix Schüber. 2021. Identifying Used Methods and Datasets in Scientific Publications. In *Proceedings of the Second Workshop on Scholarly Document Understanding (SDU@AAAI 2021)*. https://ceur-ws.org/Vol-2831/paper19.pdf

[9] Wenpeng Yin, Jamaal Hay, and Dan Roth. 2019. Benchmarking Zero-shot Text Classification: Datasets, Evaluation and Entailment Approach. In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)*, Hong Kong, China, November 2019. Association for Computational Linguistics, 3914–3923. https://doi.org/10.18653/v1/D19-1404

[10] Pengcheng He, Jianfeng Gao, and Weizhu Chen. 2021. DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing. arXiv:2111.09543. https://doi.org/10.48550/arXiv.2111.09543

[11] John Dagdelen, Alexander Dunn, Sanghoon Lee, Nicholas Walker, Andrew S. Rosen, Gerbrand Ceder, Kristin A. Persson, and Anubhav Jain. 2024. Structured information extraction from scientific text with large language models. *Nature Communications* 15 (2024), 1418. https://doi.org/10.1038/s41467-024-45563-x

[12] Maciej P. Polak and Dane Morgan. 2024. Extracting accurate materials data from research papers with conversational language models and prompt engineering. *Nature Communications* 15 (2024), 1569. https://doi.org/10.1038/s41467-024-45914-8

[13] Tushar Khot, Harsh Trivedi, Matthew Finlayson, Yao Fu, Kyle Richardson, Peter Clark, and Ashish Sabharwal. 2022. Decomposed Prompting: A Modular Approach for Solving Complex Tasks. arXiv:2210.02406. https://doi.org/10.48550/arXiv.2210.02406

[14] Patrice Lopez. 2009. GROBID: Combining Automatic Bibliographic Data Recognition and Term Extraction for Scholarship Publications. In *Research and Advanced Technology for Digital Libraries: Proceedings of ECDL 2009*. Springer Berlin Heidelberg, Berlin, Heidelberg, 473–474. https://doi.org/10.1007/978-3-642-04346-8_62

---

## Dataset Papers

[D1] Sergey Brin and Lawrence Page. 1998. The anatomy of a large-scale hypertextual web search engine. *Computer Networks and ISDN Systems*, 30(1–7), 107–117. https://doi.org/10.1016/S0169-7552(98)00110-X

[D2] Jeffrey Dean and Sanjay Ghemawat. 2004. MapReduce: Simplified data processing on large clusters. In *Proceedings of the 6th Symposium on Operating Systems Design and Implementation (OSDI '04)*. USENIX Association, 137–150. https://www.usenix.org/conference/osdi-04/mapreduce-simplified-data-processing-large-clusters

[D3] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2019. BERT: Pre-training of deep bidirectional transformers for language understanding. In *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT 2019)*, Volume 1. Minneapolis, Minnesota: Association for Computational Linguistics, 4171–4186. https://doi.org/10.18653/v1/N19-1423

[D4] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. 2016. Deep residual learning for image recognition. In *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2016)*, 770–778. https://doi.org/10.1109/CVPR.2016.90

[D5] Alex Krizhevsky, Ilya Sutskever, and Geoffrey E. Hinton. 2012. ImageNet classification with deep convolutional neural networks. In *Advances in Neural Information Processing Systems*, 25, 1097–1105. https://proceedings.neurips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html

[D6] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. Attention is all you need. In *Advances in Neural Information Processing Systems*, 30, 5998–6008. https://proceedings.neurips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html

---

## Appendix A — Project Roadmap

<figure>
<img src="Screenshot%202026-08-17%20091753.png" alt="GitHub Projects roadmap — part 1" style="width:100%;max-width:100%;">
<figcaption>Figure A1: Project roadmap (rows 1–17). March–April 2026: Concept Pitch, template decision, background research, the Research Plan item, and early literature-note rewrites (Oates, Pilkington, CSO classifier, GROBID, identifying users).</figcaption>
</figure>

<figure>
<img src="Screenshot%202026-08-17%20091846.png" alt="GitHub Projects roadmap — part 2" style="width:100%;max-width:100%;">
<figcaption>Figure A2: Project roadmap (rows 18–33). May–June 2026: SciBERT/SciREX/Yin et al. literature acquisition, proto2 build, Preliminary Report submission, Chapters 1–4 write-up, video recording, and the start of proto3 (LLM decision, Stage 0–1 parsing, Stage 2 schema-guided extraction).</figcaption>
</figure>

<figure>
<img src="Screenshot%202026-08-17%20091926.png" alt="GitHub Projects roadmap — part 3" style="width:100%;max-width:100%;">
<figcaption>Figure A3: Project roadmap (rows 34–51). June–July 2026: proto3 write-up, gold-label P/R/F1 testing, Stage-2 run logging and Wilson CI aggregation, report3 figure and citation collection, the consolidated manual review, the proto2→proto3 synthesis, the roadmap update itself, and Final Report submission. The red line marks the current iteration (17 August).</figcaption>
</figure>

---

## Appendix B — Extended proto3 Output and Background Data (All 6 Papers)

Chapter 4 shows the full extraction output for the Transformer paper (Figure 6). This appendix gives the same output for the remaining five papers, all from `proto3/baseline/*.json`, plus the gold labels and proto2 background counts used throughout Chapters 4–5.

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
*Figure B1: Full extraction output for AlexNet [D5].*

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
*Figure B2: Full extraction output for BERT [D3].*

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
*Figure B3: Full extraction output for MapReduce [D2].*

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
*Figure B4: Full extraction output for Google Search (PageRank) [D1].*

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
*Figure B5: Full extraction output for ResNet [D4].*

### Gold labels (six papers)

| Paper | Gold TechnicalMethod | Gold Task | Gold Dataset | Gold EvaluationMetric |
|---|---|---|---|---|
| Transformer [D6] | "Transformer" | "machine translation" | "WMT" | "BLEU" |
| BERT [D3] | "BERT" | "GLUE" or "SQuAD" | "BooksCorpus" or "Wikipedia" | "F1" or "accuracy" |
| AlexNet [D5] | "convolutional" (paper predates the name "AlexNet") | "object recognition" | "ImageNet" | "top-1" or "top-5" |
| ResNet [D4] | "residual" | "image recognition" | "ImageNet" | "top-1" |
| MapReduce [D2] | "MapReduce" | "distributed" | "TeraSort" | "seconds" |
| Google Search [D1] | "PageRank" | "web search" | "million pages" | "quality" |

Table B1: Gold labels used for evaluation (six papers).

### proto2 background data

| Paper | TM | Task | Dataset | EM | Hypothesis set |
|---|---|---|---|---|---|
| Transformer [D6] | 14 | 0 | 0 | 160 | verbose_v1 |
| BERT [D3] | 62 | 23 | 15 | 13 | short |
| AlexNet [D5] | 51 | 6 | 11 | 4 | short |
| ResNet [D4] | 51 | 6 | 14 | 12 | short |
| MapReduce [D2] | 151 | 24 | 3 | 5 | short |
| Google Search [D1] | 69 | 21 | 8 | 29 | short |

Table B2: proto2 sentence-count output per role (six papers). proto2's extended evaluation result (`report1/report.md` Appendix B) was 18/24 (75%): ML papers 13/16 (81%), systems papers 5/8 (63%). Failures: ResNet ✗ Task, MapReduce ✗ Task + Dataset, Google Search ✗ TechnicalMethod ("PageRank" never appears in the TechnicalMethod output).

The manual review (Chapter 5, Section 4) is now done — see Table 11 there for the per-check breakdown. The decomposed-extraction pilot and the Related Work ablation were both cut, not run — no per-paper P/R/F1 breakdown or additional figures to add here.
