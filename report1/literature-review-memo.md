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

- Oates [3] provides the theoretical vocabulary: six research strategies and four data generation methods. This supports the four-component schema (TechnicalMethod, Task, Dataset, EvaluationMetric) used in this project.
- Pilkington & Pretorius [4] go further: they formalize methodology as a structured ontology (ResearchScheme = PhilosophicalWorldview + ResearchDesign + ResearchMethod). This shows that methodology is a structured profile, not a single label.
- Both agree: methodology has components. Neither provides a system to extract them automatically from text.
- Transition: A structured definition exists. The question is whether any system can extract it.

---

### Section 3: Closest Prior Work (~450 words)

Paper: SciREX [5]

Claim: Systems that extract methodology-like entities from papers exist, but all require labeled training data that this project does not have.

- SciREX [5] extracts four entity types — Method, Task, Dataset, Metric — which match the four roles in this project exactly. This confirms the problem is real and the four-role structure is well-motivated.
- SciREX operates at the document level, not the sentence level. This is a stronger model of how information is spread across a paper.
- Key limitation: SciREX was trained on human-annotated data. Such annotations do not exist for general computing papers.
- Transition: The right entity types are identified, but the approach cannot be adopted without labeled data. A zero-shot method is needed.

---

### Section 4: Zero-shot Classification (~550 words)

Paper: Yin et al. [8]

Claim: Zero-shot NLI can assign roles to text without task-specific training data, but applying it to scientific papers introduces a domain mismatch risk.

- Yin et al. [8] show that NLI can classify text into any label by turning the label into a natural language hypothesis. No labeled examples for the target labels are needed.
- This directly enables the core step in this project: classifying sentences into TechnicalMethod, Task, Dataset, or EvaluationMetric without a methodology-annotated corpus.
- Risk: Yin et al. test on general text (news, emotions, situations). Scientific papers differ in vocabulary and structure. Transfer may be imperfect.
- This project accepts the risk and tests it: the hypothesis set comparison (short vs verbose_v1/v2/v3 in proto2/memo.md) directly investigates label expression.
- Transition: Zero-shot NLI fills the training data gap. The question is whether any prior work combines this approach with a methodology schema applied to scientific papers.

---

### Section 5: Synthesis / Gap (~350 words)

Claim: No existing work combines a structured methodology schema with zero-shot NLI on scientific papers. This is the gap this project fills.

- Section 2 establishes the schema: what methodology should look like (four components).
- Section 3 shows extraction is possible but requires labeled data.
- Section 4 shows zero-shot NLI removes the labeled data requirement.
- The gap: no work connects Section 2's schema with Section 4's method and applies it to Section 3's domain (scientific papers).
- State what this project does: applies zero-shot NLI with the 4-role schema from Oates/Pilkington to GROBID-parsed scientific papers.

---

## QA

Each question has a type:
- Gap: What does this paper NOT do that your project does?
- Justify: Which decision in your prototype does this paper support?
- Critical: What weakness does this paper point to, in your own work?

Write your answers in the A fields.

---

### Oates [3] — book chapters

Q1 (Gap): pitch.md says "Oates: Explains research strategies in computing | Not an NLP system."
Write one sentence that explains this gap without dismissing the book.
A:

Q2 (Justify): Your project extracts TechnicalMethod, Task, Dataset, EvaluationMetric.
Which part of Oates' framework gives the vocabulary for these four roles?
A:

Q3 (Critical): A reviewer might ask: "Why cite a 2006 textbook for an NLP project in 2024?"
What is your answer in two sentences?
A:

---

### Pilkington & Pretorius [4]

Q1 (Gap): Their model is a conceptual ontology. Your project is an NLP system.
What has to happen to go from a conceptual model to automatic extraction? Does their paper address this?
A:

Q2 (Justify): gap.md asks "which work gives the role vocabulary?"
Is the answer Pilkington & Pretorius, Oates, or both? How do you decide what to write?
A:

Q3 (Critical): pitch.md says "Models methodology as a structure | Does not extract from papers."
Is this a fair criticism of a conceptual modelling paper? How do you phrase it as a gap, not an attack?
A:

---

### SciREX [5]

Q1 (Gap): SciREX annotates the same 4 entity types as your project.
Does this strengthen or weaken your argument for building something new?
A:

Q2 (Justify): SciREX uses a trained model on human-annotated data.
Your project uses zero-shot NLI. What is the specific reason your project cannot follow SciREX's approach?
A:

Q3 (Critical): SciREX argues sentence-level IE is not enough — document-level is needed.
Does proto2's pipeline agree with this? What did you observe in your own experiments?
A:

---

### Yin et al. [8]

Q1 (Gap): Yin et al. test zero-shot NLI on general text (news, emotions, situations).
Your project applies it to scientific papers. What is the domain mismatch risk?
A:

Q2 (Justify): proto2/memo.md tested 4 hypothesis sets (short, verbose_v1/v2/v3).
Which finding from those experiments connects to Yin et al.'s argument about how labels should be expressed?
A:

Q3 (Critical): proto2/memo.md says "Known Risks: No evaluation against gold labels."
How does this limit how strongly you can claim that Yin et al.'s approach works for your domain?
A:

---

## Cross-paper Synthesis Questions

These questions are for Section 5 (Synthesis).

Q1: gap.md asks "which work gives the role vocabulary? which work shows extraction is possible?"
Answer this with the 4 papers you are using. One sentence per paper.
A:

Q2: pitch.md's Previous Work table originally included Ghosh et al. You removed Ghosh.
Which paper in your current 4 takes Ghosh's role in the argument?
A:

Q3: In one sentence for Section 5: what is the single gap that all 4 papers together reveal,
which your project addresses?
A:
