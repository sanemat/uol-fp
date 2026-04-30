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

1. reads a research paper (text input)
2. extracts key elements (method, data, evaluation)
3. detects research design
4. outputs a structured result

---

## Approach

We do not need a perfect model.

We build a **simple working prototype**.

### Step 1: Sentence Processing

* Split text into sentences

---

### Step 2: Sentence Representation

* Use SciBERT to convert sentences into vectors
* This helps understand sentence meaning
* Run it on google colab, not on local

---

### Step 3: Sentence Grouping

* Use k-means clustering
* Group similar sentences (e.g. training vs evaluation)

---

### Step 4: Entity Extraction (Simple)

* Use rule-based keyword matching
* Extract:

  * Method (BERT, CNN, Adam)
  * Data (MNIST, dataset)
  * Evaluation (accuracy, F1)

(No need for full NER model at this stage)

---

### Step 5: Design Detection

* Use simple rules:

  * if "experiment" or "evaluate" → experiment
  * if "theoretical" → theoretical

---

### Step 6: Build Output

Output format:

```json id="k2m91a"
{
  "Design": "...",
  "Method": [...],
  "Data": [...],
  "Evaluation": [...]
}
```

---

## Important Notes

* Focus on **working system**, not perfect accuracy
* Keep implementation simple
* Avoid complex training
* This is a prototype for later improvement

---

## Future Extension (Optional)

* Replace rules with trained NER model
* Use LLM for classification
* Add consistency checking

---

## Summary

Build a simple pipeline that:

* extracts explicit elements
* groups sentences
* outputs structured methodology

This is the first step toward full methodology understanding.
