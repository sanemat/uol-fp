# Task: Build a Simple System for Methodology Extraction

## Background

Research papers use the word **methodology**, but the meaning is not consistent.

* Some papers use "method" to mean a model (e.g. BERT)
* Some use it to mean research design (e.g. experiment)
* Some parts are clearly written, others are not

Because of this, it is hard to extract methodology automatically.

---

## Key Idea

We do NOT try to find the perfect definition.

Instead, we define a **simple and practical structure** that can be extracted from text.

Methodology = 4 parts:

* **Design** → type of research (experiment, theoretical)
* **Method** → model or algorithm (e.g. BERT)
* **Data** → dataset or source
* **Evaluation** → metrics (accuracy, F1)

These parts are usually **explicitly written** in papers.

---

## Goal

Build a simple pipeline that:

1. reads a research paper text
2. extracts methodology candidates
3. classifies each candidate into a role
4. detects research design
5. outputs a structured result
6. validates consistency

---

## Approach

We do not need a perfect model.

We build a **simple working prototype**.

### Step 1: Candidate Extraction

* Use SciBERT to extract methodology-related phrases
* Targets: model names, algorithm names, dataset names, metric names

---

### Step 2: Role Classification

* Use an LLM to assign each candidate to a role:
  * Method, Data, Evaluation, or Other

---

### Step 3: Design Detection

* Use rules + LLM to classify the research design:
  * experiment, survey, case study, theoretical, algorithm development

---

### Step 4: Build Output

Output format:

```json
{
  "Design": "experiment",
  "Method": ["BERT"],
  "Data": ["MNIST"],
  "Evaluation": ["accuracy"]
}
```

---

### Step 5: Consistency Checking

Apply simple validation rules:

* experimental paper → should have Data and Evaluation
* theoretical paper → may not need a dataset
* Method + Evaluation without Data → may be incomplete

---

## Important Notes

* Focus on **working system**, not perfect accuracy
* Keep implementation simple
* Avoid complex training
* This is a prototype for later improvement

---

## Next Steps

1. Build candidate extraction step (SciBERT or rule-based)
2. Annotate a small gold dataset (10–20 papers, Design / Method / Data / Evaluation labels)
3. Evaluate at three levels:
   * Candidate extraction quality
   * Role classification accuracy
   * Full structure quality
