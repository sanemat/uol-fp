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

This is the structure for the literature review.
Total word limit: 2500 words.
Write each section in order.

---

### Section 1: Introduction (~150 words)

State the topic: extracting research methodology from computing papers automatically.
State what you will review: frameworks that define methodology, systems that extract information from papers, and NLP tools that make this possible.
State the gap you expect to find at the end of the review.

---

### Section 2: Defining Research Methodology (~500 words)

Papers: Oates [3], Pilkington & Pretorius [4]

- What is research methodology in computing? How is it structured?
- Oates gives informal, textbook definitions of six research strategies.
- Pilkington & Pretorius give a formal ontology: ResearchScheme = PhilosophicalWorldview + ResearchDesign + ResearchMethod.
- Contrast the two: level of formality, purpose, audience.
- Show how both support the four-component schema used in this project: TechnicalMethod, Task, Dataset, EvaluationMetric.
- End with the gap: neither paper addresses automatic extraction.

---

### Section 3: Extracting Information from Scientific Papers (~600 words)

Papers: SciREX [5], Färber et al. [6], Ghosh et al.

- These papers show existing approaches to entity extraction from research papers.
- SciREX: extracts four entity types (Method, Task, Dataset, Metric) at the document level.
- Färber et al.: extract Method and Dataset; add a used / not-used distinction.
- Ghosh et al.: extract methodology component names using sequence labeling.
- Compare what each covers and what each misses.
- Key shared limitation: all require labeled training data.
- This is the main gap that motivates using zero-shot methods.

---

### Section 4: Classification without Training Data (~500 words)

Papers: Yin et al. [8], CSO Classifier [1]

- This project has no labeled methodology data. What are the options?
- Yin et al.: zero-shot NLI turns a label into a natural language hypothesis. No task-specific training is needed.
- CSO Classifier: uses a fixed ontology and word embeddings to assign research topics without labeled data.
- Contrast the two: CSO uses a closed vocabulary; Yin et al. work with any label.
- CSO is for topics, not methodology components. Its fixed vocabulary is a limitation here.
- Show how Yin et al. directly supports the method used in this project.

---

### Section 5: Scientific NLP Infrastructure (~400 words)

Papers: GROBID [7], SciBERT [2]

- These are tools that support NLP on scientific papers.
- GROBID: converts PDF to structured TEI XML. Enables section-level parsing of papers.
- SciBERT: shows that scientific text is significantly different from general text. The vocabulary overlap between SCIVOCAB and BASEVOCAB is only 42%.
- SciBERT improves results on scientific NLP tasks, but requires labeled data for fine-tuning.
- GROBID is used directly in this project. SciBERT points to a risk: a general NLI model may not work well on scientific text.

---

### Section 6: Synthesis / Gap (~350 words)

- Section 2 provides the structure: what methodology should look like (four components).
- Section 3 shows extraction systems exist but need training data.
- Section 4 shows zero-shot NLI can classify without training data.
- Section 5 provides the NLP infrastructure: GROBID for parsing, SciBERT as a warning about domain mismatch.
- The gap: no existing work combines a methodology schema with zero-shot NLI applied to structured scientific paper sections.
- This is what this project addresses.

---

## QA

Write your answers in the A fields. These questions help you write each section.

---

### Oates [3]

Q1: What are the six research strategies that Oates defines for computing?
A:

Q2: How does Oates define "data generation methods"? Give two examples.
A:

Q3: Which parts of the Oates framework match the four roles in this project (TechnicalMethod, Task, Dataset, EvaluationMetric)?
A:

Q4: What does Oates NOT provide that this project needs?
A:

---

### Pilkington & Pretorius [4]

Q1: What are the three parts of a "research scheme" in their model?
A:

Q2: How is their ontology different from Oates? (Think about format and level of formality.)
A:

Q3: Their model has ResearchDesign and ResearchMethod. How do these map to the four roles in this project?
A:

Q4: What gap does their work leave? Can it be used directly for automatic extraction?
A:

Q5: Together, how do Oates [3] and Pilkington & Pretorius [4] support the design of the MethodologyProfile schema in this project?
A:

---

### SciREX [5]

Q1: What are the four entity types in SciREX? How do they match the four roles in this project?
A:

Q2: Why does SciREX argue that sentence-level information extraction is not enough? Give one reason from the paper.
A:

Q3: What kind of data did SciREX use to train their model? Why is this a problem for this project?
A:

Q4: What does SciREX do well that this project does not do? What does this project do that SciREX does not?
A:

---

### Färber et al. [6]

Q1: What two entity types do Färber et al. extract? How is this different from this project?
A:

Q2: What is the "used vs. not-used" distinction? Why is this useful?
A:

Q3: What does their approach require that this project does not have?
A:

Q4: How does their work support the motivation for this project? What does it prove is possible? What does it leave out?
A:

---

### Ghosh et al.

Q1: What does "factored sequence labeling" mean in simple terms?
A:

Q2: Which role in this project is most similar to what Ghosh et al. extract?
A:

Q3: What is the main technical challenge they address? Does this project face the same challenge?
A:

---

### Yin et al. [8]

Q1: What is zero-shot text classification? Why does it not need training data for the target labels?
A:

Q2: How does the entailment approach work? What does the model compare?
A:

Q3: What are the limits of zero-shot NLI on scientific text? Think about domain mismatch.
A:

Q4: How does this paper directly support the method used in this project?
A:

---

### CSO Classifier [1]

Q1: What is the input and output of the CSO Classifier?
A:

Q2: How does it classify research topics without labeled training data?
A:

Q3: CSO uses a closed vocabulary (a fixed ontology). Why is this a problem for methodology extraction in this project?
A:

Q4: How is the approach in this project different from CSO? What is similar?
A:

---

### GROBID [7]

Q1: What does GROBID do? What is its output format?
A:

Q2: How is GROBID used in this project? At which stage of the pipeline?
A:

Q3: What does GROBID NOT do? What must happen after GROBID runs?
A:

---

### SciBERT [2]

Q1: Why did Beltagy et al. create SciBERT instead of using the original BERT?
A:

Q2: What is the vocabulary overlap between SCIVOCAB and BASEVOCAB? What does this number show?
A:

Q3: To use SciBERT for role classification, what would you need that this project does not have?
A:

Q4: How does SciBERT support the argument that domain-aware NLP matters for scientific text?
A:

---

## Cross-paper Synthesis Questions

These questions are for Section 6. They ask you to connect ideas across papers.

Q1: SciREX [5], Färber et al. [6], and Ghosh et al. all extract entities from research papers. What do they all have in common that this project cannot use?
A:

Q2: Oates [3] and Pilkington & Pretorius [4] define methodology structure. SciREX [5] annotates the same four entity types. Do these two groups connect in the existing literature? What is missing between them?
A:

Q3: This project uses zero-shot NLI (from Yin et al. [8]) on scientific papers (preprocessed by GROBID [7]). What risk does SciBERT [2] point to for using a general NLI model on scientific text?
A:

Q4: What is the one thing that no paper in this review does, which this project tries to do?
A:
