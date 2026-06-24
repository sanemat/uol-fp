---
theme: default
---

# Auto-Extracting Research Methodology from Papers

CM3060 Natural Language Programming — Feature Prototype Demo

---

## The Problem

A research paper has hundreds of sentences.

Which ones tell you:

- **What method** did they use?
- **What task** did they solve?
- **What data** did they train on?
- **How** did they measure success?

Reading manually is slow. Can we automate it?

---

## What We Extract

Four roles from any computing research paper:

| Role | Example |
|---|---|
| **TechnicalMethod** | "Transformer" |
| **Task** | "machine translation" |
| **Dataset** | "WMT 2014 English-German" |
| **EvaluationMetric** | "BLEU score" |

---

## Our Approach — Pipeline

```
PDF  →  GROBID (local)  →  TEI XML
                                ↓
                        Colab pipeline
                                ↓
        Load sections → Clean → Split sentences
                                ↓
                   Classify each sentence by role
                                ↓
                           JSON output
```

---

## Key Technique — Zero-shot NLI

**No labeled training data** was available for this task.

Instead, the model answers a yes/no question per sentence:

> "Does this sentence describe a **[technical method]**?"

- Model: `cross-encoder/nli-deberta-v3-small`
- Runs on free Google Colab (568 MB)
- 4 labels: `technical method` / `task` / `dataset` / `evaluation metric`
- Threshold: score ≥ 0.5 → accepted

---

## Live Demo

Running on the **BERT paper** (Devlin et al., 2019)

→ Switch to Google Colab

---

## Results — Gold Label Evaluation

Does the pipeline find the right answer for each role?
(○ = gold label found in output, ✗ = not found)

| Paper | TechnicalMethod | Task | Dataset | EvaluationMetric |
|---|---|---|---|---|
| Transformer | ○ | ✗ | ✗ | ○ |
| BERT | ○ | ○ | ○ | ○ |
| AlexNet | ○ | ○ | ○ | ○ |

**BERT and AlexNet: all 4 roles correct.**
Transformer: 2/4 — caused by hypothesis wording, not missing information.

---

## Limitations & Next Steps

**Current limitations:**
- Introduction noise — other papers' methods get classified as ours
- Large output volume (e.g. 151 sentences for MapReduce)

**Planned improvements:**
1. Usage NLI filter — keep only "used by the authors", drop "related work"
2. Top-3 selection — rank by NLI score × section weight
3. LLM term extraction — convert sentences to short terms ("Transformer")

---

## Summary

- Zero-shot NLI classifies sentences by methodology role **without any training data**
- Works well on structured ML papers (BERT, AlexNet, ResNet)
- Systems papers (MapReduce) need further work
- Prototype demonstrates feasibility
