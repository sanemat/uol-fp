# Literature Review Memo

Example

Input:

  Attention Is All You Need

Output:

    Discipline:
        - Computer Science

    Field:
        - Natural Language Processing
        - Machine Learning

    Methodology:
        Design or strategy: design and creation + experiment
        Data generation method: Documents
        Technical method: Transformer
        Task: machine translation
        Dataset: WMT machine translation datasets
        EvaluationMetric: BLEU score

Only include used entities in the final MethodologyProfile.


## Outline

Papers: Oates [3], Pilkington & Pretorius [4], SciREX [5], Yin et al. [8]
Total word limit: 2500 words.

Argumentative arc:
Section 2 → Methodology has structure, but no one extracts it automatically.
Section 3 → Extraction systems exist, but need labeled data this project does not have.
Section 4 → Zero-shot NLI removes the labeled data requirement, but adds domain mismatch risk.
Section 5 → No work combines all three. That is the gap.

---

### Section 1: Introduction (~150 words)

Claim: Extracting research methodology from computing papers automatically is useful and currently unsolved.

- State the problem: reading papers to identify method, task, dataset, and metric is slow and manual.
- State the scope: this review covers (a) how methodology is defined, (b) how information is extracted from papers, and (c) how classification can work without training data.
- State the gap you will identify at the end.

---

### Section 2: Defining Research Methodology (~600 words)

Book: Oates [3] (chapters 3, 7–9, 13–16), Paper: Pilkington & Pretorius [4]

Claim: Research methodology in computing has a well-defined structure, but defining it is not the same as extracting it.

- Oates [3] provides the vocabulary: six research strategies (experiment, design and creation, survey, case study, action research, ethnography) and four data generation methods. His book defines what each strategy means for human researchers making methodology choices.
- Pilkington & Pretorius [4] go further: they formalize methodology as a structured ontology (ResearchScheme = PhilosophicalWorldview + ResearchDesign + ResearchMethod) using UML and ontology engineering. Their goal is "providing clear and unambiguous semantics" — a formal structure, not a textbook description.
- The contrast: Oates gives concept names; Pilkington gives formal relationships between those concepts. Together they justify the four-component schema in this project: vocabulary from Oates, formal structure from Pilkington.
- Both works are designed for human use. Neither provides a system to extract methodology components automatically from text.
- Transition: A structured definition exists and can be formalized. The question is whether any system can extract it.

---

### Section 3: Closest Prior Work (~450 words)

Paper: SciREX [5]

Claim: Systems that extract methodology-like entities from papers exist, but all require labeled training data that this project does not have.

- SciREX [5] is the closest prior work: it extracts four entity types — Method, Task, Dataset, Metric — which match the four roles in this project exactly. This shows the problem is real and solvable in principle.
- SciREX operates at the document level. The authors argue that "a significant amount of information can only be gleaned from analyzing the full document" — relations span sections, not just sentences.
- Key limitation: building SciREX required 438 annotated papers and 4 expert PhD-level annotators (Cohen-κ 95%). The corpus comes from Papers with Code, which covers only ML benchmarks.
- This project targets general computing papers (systems, algorithms, HCI) and has no annotated corpus. The SciREX approach cannot be adopted directly.
- Transition: The right entity types are identified, but building a supervised system requires annotation effort that does not exist for this scope. A zero-shot method is needed.

---

### Section 4: Zero-shot Classification (~550 words)

Paper: Yin et al. [8]

Claim: Zero-shot NLI can assign roles to text without task-specific training data, but applying it to scientific papers introduces a domain mismatch risk.

- Yin et al. [8] show that NLI can classify text into any label by turning the label into a natural language hypothesis — "this text is about [label]" — and asking a model whether the text entails it. No labeled examples for the target labels are needed.
- Include Table 4 (reproduced from Yin et al. [8]) to illustrate the hypothesis templates:

| aspect | labels | interpretation | example hypothesis (word) | example hypothesis (wordnet definition) |
|---|---|---|---|---|
| topic | sports etc. | this text is about ? | "?"= sports | "?" = an active diversion requiring physical exertion and competition |
| emotion | anger etc. | this text expresses ? | "?"= anger | "?" = a strong emotion; a feeling that is oriented toward some real or supposed grievance |
| situation | shelter etc. | The people there need ? | "?"= shelter | "?" = a structure that provides privacy and protection from danger |

*Table 4 (reproduced from Yin et al. [8]): example hypotheses for three task types.*

- This directly enables the core step in this project: classifying sentences into TechnicalMethod, Task, Dataset, or EvaluationMetric without a methodology-annotated corpus. This project applies the same entailment approach with four methodology roles:

| role | hypothesis (this project, short label) |
|---|---|
| TechnicalMethod | technical_method |
| Task | task |
| Dataset | dataset |
| EvaluationMetric | evaluation_metric |

*Table X: hypothesis set used in this project (short label format, selected by hypothesis set comparison in proto2/memo.md).*
- Domain mismatch risk: Yin et al. test on Yahoo News articles, emotion tweets, and crisis situation reports. Their NLI model is trained on MNLI (news, fiction, telephone speech). None of these are scientific papers, which use dense technical vocabulary, passive constructions, and section-based structure.
- This project accepts the risk and tests it: the hypothesis set comparison (short vs verbose_v1/v2/v3 in proto2/memo.md) directly investigates how label wording affects classification on scientific text.
- Transition: Zero-shot NLI removes the labeled data requirement. The question is whether any prior work combines this approach with a methodology schema on scientific papers.

---

### Section 5: Synthesis / Gap (~350 words)

Claim: No existing work applies zero-shot NLI with a structured methodology schema to general computing papers. This is the gap this project fills.

- Section 2 (Oates + Pilkington) established the schema: methodology can be defined as four components (TechnicalMethod, Task, Dataset, EvaluationMetric), grounded in formal ontology structure.
- Section 3 (SciREX) showed extraction of the same four types is possible — but required 438 annotated papers, 4 PhD annotators, and a corpus limited to ML benchmarks. This approach cannot generalize to general computing papers without similar annotation effort.
- Section 4 (Yin et al.) showed zero-shot NLI removes the labeled data requirement — but was tested only on news, tweets, and crisis reports, not scientific papers. Domain mismatch is a known risk.
- The gap: no work combines (a) the 4-role methodology schema from Oates/Pilkington, (b) the zero-shot NLI method from Yin et al., and (c) applies it to general computing papers.
- State what this project does: uses zero-shot NLI (Yin et al.'s entailment approach) with the 4-role schema (grounded in Oates and Pilkington) on GROBID-parsed computing papers. Addresses SciREX's annotation bottleneck and Yin et al.'s untested domain in one prototype.

---

## QA

Each question has a type:
- Gap: What does this paper NOT do that your project does?
- Justify: Which decision in your prototype does this paper support?
- Critical: What weakness does this paper point to, in your own work?

Write your answers in the A fields.

---

### Oates [3] — book chapters

**Step 1 — Understand**

Q1a (Chapter 3): Read Chapter 3. List the six research strategies and the four data generation methods Oates defines.
A: The six research designs (Survey, Design and creation, Experiment, Case study, Action research, Ethnography) and the four data generation methods (Interview, Observations, Questionnaire, andDocuments).

Q1b (Chapter 8 + Chapter 9): This project builds a prototype and tests it on real papers.
Read the opening pages of Chapter 8 (design and creation) and Chapter 9 (experiment).
Which of these two strategies fits your project — or does it use both? Write one sentence per strategy explaining why.
A: Design and creation: This project builds a working pipeline that parses papers and classifis sentences into methodology roles.

Q1c (Chapter 17): Chapter 17 covers quantitative data analysis.
proto2/memo.md shows NLI classifier scores (0.85, 0.72, etc.).
Is this the kind of quantitative analysis Oates describes? What does this suggest about how to describe your evaluation?
A: The NLI scores and label counts are a form of quantitative analysis as Oates describes. This means the evaluation should be described in numerical terms.

**Step 2 — Connect to your project**

Q2 (Gap): Oates defines six research strategies for human researchers choosing how to conduct a study.
Your project is an NLP system that reads papers, not a researcher choosing a strategy.
Write one sentence that shows why Oates is still relevant, despite this difference.
A:  The book defines the vocabulary that researchers use to describe their methodology in papers, so the system needs those concept names to identify what to extract.

Q2 (Justify): Oates' six strategies include "experiment", "design and creation", "survey", "case study", "action research", "ethnography."
His four data generation methods include "interviews", "observations", "questionnaires", "documents."
Which of these terms or ideas map to your four roles (TechnicalMethod, Task, Dataset, EvaluationMetric)?
Which do NOT map, and why?
A: "Documents" maps to Dataset, computing papars use existing publications as their data source. "Experiment" maps to how this project tests its pipeline. However, TechincalMethod has no equivalent in Oates, his book defines reasearch strategies, not what algorithm a system uses. Interviews, observations, and questionnaires do not map at all. these are human-subject methods that do not appear in computing papers.

Q3 (Critical): Oates was published in 2006. A reviewer might ask why you cite it for a 2026 NLP project.
Your answer should explain what has NOT changed since 2006 that makes it still useful.
Write two sentences.
A: The six research strategies Oates defines, experiment, design and creation, survey, case study, action reseaerch, and ethnography, still describe how computing researchers condut their work in 2026.
The vocabulary researchres use when writing about their methodology has not changed, so Oates remains the standard reference for identifying what those therms mean.

---

### Pilkington & Pretorius [4]

Sections: Introduction — Ontologies and Ontology Engineering — A Conceptual Model (Section 3) — Concluding Remarks

**Step 1 — Understand**

Q1a (Section 3.2 + Figure 2): Look at Figure 2 in the paper. What are the three boxes in the UML diagram? Write what connects them.
A: The three boxes are ResearchScheme, PhilosophicalWorldview, and ResarchDesign. ResearchScheme belongs to a one PhilosophicalWorldview and has one ore more ResearchDesigns.

Q1b (Section 2): Section 2 explains what an ontology is. How is an ontology different from a textbook chapter? Write one sentence.
A: An ontology defines formal, cpmputable relationships between concepts, while a textbook chapter explainse them in natural language for a fuman reader.

Q1c (Introduction): The paper says it was written to support postgraduate students and supervisors. What specific problem were they trying to solve for students? Write one sentence.
A: Students and supoervisors had no shared, consistent vocabulary for methodology, so they often used the same terms with different meanings.

**Step 2 — Connect to your project**

Q2 (Gap): Pilkington & Pretorius say their goal is "providing clear and unambiguous semantics" for the methodology domain.
They use UML and ontology engineering to build a formal structure.
Does formalizing the structure solve the extraction problem? What is still missing?
A: Formalizing the structure does not solve the extraction problem. Pilkington defines what methodology components are and how they relate, but does not provide a method for finding them automatically in paper text.

Q2 (Justify): The Outline says: "Oates gives concept names; Pilkington gives formal relationships between them."
In your own words: what specific thing does Pilkington add that Oates does NOT give you?
Why do you need BOTH papers to justify your four-component schema?
A: Pilkington adds formal relationships between components with UML that Oates does not define. I need both: Oates names the concept this project uses (experiment, design and creation), and Pilkington shows that theose concepts from a structured schema with defined part.

Q3 (Critical): Their paper was written to support postgraduate students and supervisors in understanding methodology.
Your project reads papers written by researchers, not students.
Is the Pilkington ontology actually the right schema for your input? What might be missing?
A: Pilikington's ontology was designed for planning research, not for reading completed papaers. A philosophical worldview is important, but it rarely appear directly in a paper text.

---

### SciREX [5]

Sections: Introduction — Related Work — Document-Level IE (Section 3) — Model (Section 4) — Evaluation — Conclusion

**Step 1 — Understand**

Q1a (Introduction): SciREX defines four entity types. List them. Write one example for each from a paper you know (e.g. "Attention Is All You Need").
A: Dataset, Metric, Task, Method.
Dataset: WMT machine translation datasets
Metric: BLEU score
Task: machine translation
Method: Transformer

Q1b (Introduction — first paragraph): The paper says sentence-level IE is not enough. Find their reason and write it in your own words. (Key quote: "information ... usually span beyond sentences or even sections.")
A: a lot of information about methodology cannot be extracted from a single sentence, becuase the relationship between method, task, datase, and metric is often spread across multiple sections of the paper..

Q1c (Section 3): Papers with Code is described as "1,170 articles published in ML conferences." What does this tell you about which kind of computing papers SciREX covers? What is NOT covered?
A: SciRex covers only ML benchmark papars, not systems nor algorithm.

**Step 2 — Connect to your project**

Q2 (Gap): SciREX extracts the same four types as your project (Method, Task, Dataset, Metric).
A reviewer might ask: "If SciREX already does this, what is new about your project?"
Write your answer. Focus on what SciREX requires that your project does not have.
A: SciREX uses anotated data. I will use zero-shot text classification.

Q2 (Justify): SciREX required 438 annotated papers, 4 expert PhD annotators, and reached Cohen-κ 95%.
Its corpus is from Papers with Code, which covers only ML benchmark papers.
Your project targets general computing papers (systems, HCI, algorithms).
Write two sentences: (a) why SciREX's annotation scale is a problem for this project, (b) why the ML-only corpus is a further problem.
A: (a) This project has no annotated computing papers. (b) SciREX covers only ML, I will use my system for not only ML, but also system, which use different vocabulary.

Q3 (Critical): SciREX argues that relations span multiple sections — sentence-level IE is not enough.
proto2's pipeline classifies individual sentences. Does this mean proto2 has the same weakness SciREX identifies?
What does proto2/memo.md say about this? (Check: where was Dataset found — sentence or section?)
A: proto2 classifies individual sentences, which has the same weakness SciREX identifies. This is a limit of proto2.

---

### Yin et al. [8]

Sections: Introduction — Related Work — Benchmark the dataset (Section 3) — Benchmark the evaluation (Section 4) — An entailment model for 0SHOT-TC (Section 5) — Experiments (Section 6) — Summary

**Step 1 — Understand**

Q1a (Introduction): Yin et al. define zero-shot text classification as aiming "to associate an appropriate label with a piece of text, irrespective of the text domain and the aspect described by the label." Write this definition in your own words in one sentence.
A: Zero-shot text classification is a method that tries to assign the label without the model being trained in specific area.

Q1b (Section 5): The entailment model converts a label into a hypothesis. The paper uses "this text is about ?" for topic classification. Write the hypothesis your project would use for the label "TechnicalMethod."
A: This text describes a technique, algorithm, system, or architecture used or proposed in the research.

Q1c (Section 3 + Section 6): Three task types are tested. Name them and give one example label for each. (Find them in Section 3 or the experiment tables.)
A:topic detection, emotion detection, and situation detection. sports, anger, shelter.

**Step 2 — Connect to your project**

Q2 (Gap): Yin et al. test on Yahoo News (topics), emotion tweets, and crisis situation reports.
Their NLI model is trained on MNLI (news articles, fiction, telephone speech), GLUE RTE, and FEVER.
None of these are scientific papers.
Name two specific ways scientific paper text differs from these training/test domains.
A: Scentific papars use specialized technical vocabulary. They also use a formal research structure.

Q2 (Justify): Yin et al. propose hypothesis templates like "this text is about [label]."
proto2/memo.md tested short labels vs verbose_v1/v2/v3 hypothesis sentences.
The short labels won (best probe score 3/4, most balanced distribution).
How does this experimental result connect to what Yin et al. say about how labels should be expressed?
A: Yin et al. argue that labels should be expressed as natural-language hypotheses, not specific label indexed. In my experiences, short labels perform better than the more verbose hypothesis templates. However, the result only shows that the short labels worked best among the tested templates, not that they are universally optimal.

Q3 (Critical): proto2/memo.md says "Known Risks: No evaluation against gold labels — precision, recall, and F1 have not been measured."
Yin et al. measure their approach against ground truth on all three task types.
What does the absence of gold labels mean for how strongly you can argue that Yin et al.'s approach transfers to your domain?
A: The absenced of gold labels means that I cannot make a strong quantitative claim that Yin et al.'s approach transfers to scientific papers. My result should therefore be treated as preliminary evidence, not a confirmed evaluation. To make a stronger claim, I need mannually annotated gold labels for my domain.

---

## Cross-paper Synthesis Questions

These questions are for Section 5 (Synthesis).

Q1a: What does Oates contribute to the argument? What does it leave open?
A:

Q1b: What does Pilkington & Pretorius contribute? What does it leave open?
A:

Q1c: What does SciREX contribute? What does it leave open?
A:

Q1d: What does Yin et al. contribute? What does it leave open?
A:

Hint: the Transition sentences in the Outline (end of each section) are good starting points.

Q2: The Outline says the argumentative arc is:
  Section 2 → Methodology has structure, but no one extracts it.
  Section 3 → Extraction exists, but needs labeled data.
  Section 4 → Zero-shot NLI removes that requirement, but domain mismatch is a risk.
  Section 5 → No work combines all three.

Write the Section 5 gap statement as one concrete sentence.
It should name: (a) what schema, (b) what method, (c) what domain.
Example structure: "No existing work applies [method] with [schema] to [domain]."
A:

Q3: SciREX is the closest prior work — same 4 entity types, document-level, published system.
Your project has NO annotated data, targets general computing papers (not just ML), and uses zero-shot NLI.
Name the THREE specific differences between SciREX and your project.
Then write one sentence explaining why these differences matter for the gap argument.
A:

Q4: Yin et al. test on Yahoo News, emotion tweets, and crisis situations.
Your project applies the same NLI approach to scientific paper text (dense vocabulary, passive voice, citation markers).
You have experimental evidence from proto2/memo.md (hypothesis set comparison, section filtering results).
Does your experimental evidence support or contradict the claim that Yin et al.'s approach transfers to scientific text?
Write two sentences: one for "what the evidence shows", one for "what is still uncertain."
A: The experimental evidence gives preliminary support for the claim that Yin et al.'s NLI-based approach transfers to scientific text, since the hypothesis comparison and section filtering produced interpretable and useful results. However, it is still uncertain, we will use gold labels.
