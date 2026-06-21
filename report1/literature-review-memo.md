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

---

### Section 1: Introduction (~150 words)

State the topic: extracting research methodology from computing papers automatically.
State what you will review: frameworks that define methodology structure, and systems that extract it from papers.
State the gap you expect to find at the end of the review.

---

### Section 2: Defining Research Methodology (~650 words)

Book: Oates [3] (chapters 3, 7–9, 13–16), Paper: Pilkington & Pretorius [4]

- What is research methodology in computing? How is it structured?
- Oates gives informal, textbook definitions of six research strategies and four data generation methods.
- Pilkington & Pretorius give a formal ontology: ResearchScheme = PhilosophicalWorldview + ResearchDesign + ResearchMethod.
- Contrast the two: level of formality, purpose, audience.
- Show how both support the four-component schema used in this project: TechnicalMethod, Task, Dataset, EvaluationMetric.
- End with the gap: neither paper addresses automatic extraction.

---

### Section 3: Extracting Information from Scientific Papers (~600 words)

Paper: SciREX [5]

- SciREX extracts four entity types (Method, Task, Dataset, Metric) at the document level from scientific papers.
- The four entity types match the four roles in this project directly.
- Key limitation: requires labeled training data (human annotation).
- Explain why this is a problem for this project.

---

### Section 4: Zero-shot Classification (~550 words)

Paper: Yin et al. [8]

- This project has no labeled methodology data. Zero-shot NLI is the solution.
- Yin et al.: zero-shot NLI turns a label into a natural language hypothesis. No task-specific training is needed.
- Explain the entailment approach in simple terms.
- Discuss the limit: NLI models are trained on general text, not scientific text. There may be a domain mismatch.
- Show how this paper directly supports the method used in this project.

---

### Section 5: Synthesis / Gap (~350 words)

- Section 2 provides the structure: what methodology should look like (four components).
- Section 3 shows an extraction system exists but needs labeled training data.
- Section 4 shows zero-shot NLI can classify without training data.
- The gap: no existing work combines a methodology schema with zero-shot NLI on scientific papers.
- This is what this project addresses.

---

## QA

Write your answers in the A fields. These questions help you write each section.

---

### Oates [3] — book chapters

Q1: What are the six research strategies that Oates defines for computing? (Chapter 3)
A:

Q2: What are the four data generation methods? Give two examples and explain one briefly. (Chapters 13–16)
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

## Cross-paper Synthesis Questions

These questions are for Section 5 (Synthesis). They ask you to connect ideas across papers.

Q1: Oates [3] and Pilkington & Pretorius [4] define methodology structure. SciREX [5] annotates the same four entity types. Do these two groups connect in the existing literature? What is missing between them?
A:

Q2: SciREX [5] and Yin et al. [8] both work with the same four categories (Method, Task, Dataset, Metric). What is the key difference in what they require to run?
A:

Q3: Yin et al. [8] test zero-shot NLI on general text (news, emotions). This project applies it to scientific papers. What is the risk, and why does this project accept that risk?
A:

Q4: What is the one thing that no paper in this review does, which this project tries to do?
A:
