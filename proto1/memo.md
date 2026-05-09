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

Methodology = 3 main parts + optional details:

* **ResearchDesign** → hierarchical research design grounded in Oates (2006) and Pilkington & Pretorius. Fields: `family` (empirical / non_empirical / mixed), `primary_type` (survey / experiment / case_study / action_research / ethnography / design_and_creation / model_or_theory_building), `subtype` (algorithm_development / system_development / model_building / theory_building), `secondary_types`
* **TechnicalMethod** → model, algorithm, or technique (e.g. BERT, CNN). Separated from Oates/Pilkington "Research Method" (interviews, observations, questionnaires).
* **Task** → research task or problem (e.g. question answering, image classification)

Optional:

* **Data** → dataset or source (e.g. MNIST, SQuAD)
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

We build a **simple working prototype**, then improve based on error analysis.

### Step 1: Candidate Extraction

* Use SciBERT to extract methodology-related phrases (sentence-by-sentence, max_length=128)
* Targets: model names, algorithm names, dataset names, metric names
* Save each candidate with its context: `{candidate, sentence, section, source_paper}`

The `section` field is best-effort (heuristic heading detection). Falls back to `"unknown"`.

---

### Step 2: Role Classification

* Rule-based for baseline: hard-coded term lists + context regex
* Input: candidate string only (for now)
* Log: full `{candidate, sentence, section, role}` saved for error analysis

---

### Step 3: Design Detection

* Rule-based: regex pattern matching on abstract or first ~2000 chars

---

### Step 4: Build Output

Output format:

```json
{
  "ResearchDesign": {
    "family": "mixed",
    "primary_type": "design_and_creation",
    "subtype": "algorithm_development",
    "secondary_types": ["experiment"]
  },
  "TechnicalMethod": ["Transformer", "self-attention"],
  "Task": ["machine translation"],
  "Optional": {
    "Data": ["WMT 2014 English-German"],
    "Evaluation": ["BLEU"]
  }
}
```

---

### Step 5: Consistency Checking

Apply simple validation rules:

* Experiment or DesignAndCreation without Task → weak
* Experiment or DesignAndCreation without TechnicalMethod → weak
* TechnicalMethod without Task → incomplete

---

## Pipeline Architecture (revised)

PDF parsing is preprocessing, not part of the research pipeline.

```
Local:
  PDF → GROBID (Docker) → TEI XML

Colab:
  upload TEI XML
  → parse sections (abstract, body divs, skip references)
  → sentence splitting
  → candidate extraction
  → role classification
  → design detection
  → output JSON
```

GROBID provides section structure for free:
- abstract
- section heading + body text
- references separated (not included in body)

TEI XML is kept as-is (not converted to JSON). Colab reads the XML directly using ElementTree.

---

## TEI XML Format (GROBID output)

GROBID version: **0.8.1** (`lfoppiano/grobid:0.8.1` Docker image)

Namespace: `http://www.tei-c.org/ns/1.0` (always needed for ElementTree queries)

Key paths used for parsing:

| Content | XPath |
|---------|-------|
| Title | `.//tei:titleStmt/tei:title` |
| Abstract | `.//tei:abstract` (use `itertext()` to get full text) |
| Body sections | `.//tei:body//tei:div` |
| Section heading | `div/tei:head` |
| Section paragraphs | `div/tei:p` (use `itertext()` — `p.text` misses inline elements like `<ref>`, `<formula>`) |

`itertext()` pattern (required — `element.text` alone is wrong):

```python
NS = {"tei": "http://www.tei-c.org/ns/1.0"}

def _text(element) -> str:
    return " ".join(element.itertext()).strip()
```

GROBID automatically:
- Separates references into `<listBibl>` (not in body)
- Assigns section headings from paper structure
- Handles multi-column layouts

---

## Input Length Constraints

Both BERT-based models and LLMs have input length limits.
Full paper text cannot be processed at once.

Solution: sentence-level splitting within each section.

* SciBERT processes each sentence with `max_length=128` (or 256 — compare in experiments)
* LLM receives only the candidate list (or candidate + sentence + section), not the full paper

Role of each model:

| Step | Model | Input |
|------|-------|-------|
| Candidate extraction | SciBERT + regex | sentence (max 128 tokens) |
| Role classification | rule-based → LLM later | candidate (+ sentence + section when needed) |
| Design detection | regex → LLM later | abstract text |
| Integration | rules | classified candidates |

---

## Error Analysis Strategy

Run the prototype first. Check the log output. Classify failures into 3 types:

1. **Missing candidate** — term is in the paper but not extracted
2. **Noisy candidate** — extracted but not methodology-related
3. **Wrong role** — extracted with correct role potential, but classified wrong

Then decide improvements:

| Failure type | Next action |
|--------------|-------------|
| Missing | Fix regex, NER, max_length, or section range |
| Noisy | Add stoplist, section filter, or candidate scoring |
| Wrong role | Pass `sentence` + `section` to LLM (no restructuring needed) |

In the report:

> The first prototype uses sentence-level candidate extraction and passes only the candidate
> list to the classifier. This simple design is used as a baseline. If role classification
> is inaccurate, an error analysis will determine whether additional context (source sentence,
> section name) is needed.

---

## Internal Data Structure

From the beginning, each candidate is stored as:

```json
{
  "candidate": "BERT",
  "sentence": "We fine-tune BERT on the SST-2 dataset.",
  "section": "Method",
  "source_paper": "paper_id_001"
}
```

The LLM receives only `candidate` at first. `sentence` and `section` are added later if
error analysis shows role classification is wrong.

---

## Theoretical Basis

This project is based on two main sources: Oates (2006) and Pilkington and Pretorius (2015). Both works discuss research methodology in computing and information systems. They are useful because this project also focuses on computing research papers.

### Oates' Research Strategies

Oates (2006) explains several research strategies used in information systems and computing research. These include survey, experiment, case study, action research, ethnography, and design and creation.

In this project, Oates is used as the main basis for the **Research Design** labels. For example, a paper may use an experiment, a case study, or design and creation. In computing research, design and creation is especially important because many papers propose a new artefact, such as an algorithm, model, architecture, system, or framework.

For example, a paper that proposes a new neural network architecture can be treated as a form of **design and creation**. If the paper also evaluates the architecture on benchmark datasets, it may also include an **experimental** element.

### Pilkington and Pretorius' Research Methodology Domain Model

Pilkington and Pretorius (2015) propose a conceptual model of the research methodology domain for computing fields. Their model is useful because it separates different parts of research methodology, such as research design and research methods.

This distinction is important for this project. In many methodology extraction tasks, words such as "method", "model", "algorithm", and "evaluation" can easily be mixed together. Pilkington and Pretorius help clarify that research design is different from the concrete methods or procedures used inside a study.

Therefore, this project uses their work as a structural basis. The system does not only extract a flat list of terms. Instead, it tries to organize extracted information into different roles.

### Operational Schema Used in This Project

This project adapts the ideas from Oates and Pilkington and Pretorius into a simplified schema for automatic extraction.

The schema is:

```json
{
  "ResearchDesign": {
    "family": "empirical | non_empirical | mixed | unknown",
    "primary_type": "survey | experiment | case_study | action_research | ethnography | design_and_creation | model_or_theory_building | unknown",
    "subtype": "algorithm_development | system_development | model_building | theory_building | none",
    "secondary_types": []
  },
  "TechnicalMethod": [],
  "Data": [],
  "Evaluation": [],
  "Task": []
}
```

### ResearchDesign

`ResearchDesign` describes the overall design or strategy of the paper. This part is mainly based on Oates' research strategies, with support from Pilkington and Pretorius' distinction between research design and research methods.

Examples include:

```text
survey
experiment
case_study
action_research
ethnography
design_and_creation
model_or_theory_building
```

For computing papers, `design_and_creation` is especially important. It can include the development of algorithms, models, systems, architectures, or frameworks.

### TechnicalMethod

`TechnicalMethod` is used for computational methods and technical components.

Examples include:

```text
BERT
Transformer
self-attention
multi-head attention
CNN
SVM
Adam
dropout
```

This label is intentionally called `TechnicalMethod`, not simply `Method`. This is because in Oates and Pilkington and Pretorius, "research method" often refers to data collection or analysis methods, such as interviews, observations, questionnaires, measurements, or argumentation. In this project, the target is different: it is the extraction of technical methods from computing papers.

### Data

`Data` refers to datasets, corpora, benchmarks, or other data sources used in the paper.

Examples include:

```text
SST-2
MNIST
ImageNet
WMT 2014 English-German
Penn Treebank
Papers with Code metadata
```

### Evaluation

`Evaluation` refers to evaluation metrics, benchmarks, or evaluation procedures.

Examples include:

```text
accuracy
F1 score
BLEU
perplexity
precision
recall
human evaluation
cross-validation
```

### Task

`Task` refers to the research task or application area.

Examples include:

```text
machine translation
sentiment classification
named entity recognition
question answering
constituency parsing
image classification
```

This category is useful because task names are often confused with data or evaluation terms. For example, "machine translation" is a task, while "WMT 2014 English-German" is data and "BLEU" is an evaluation metric.

### Example

For the paper *Attention Is All You Need*, the structured output may look like this:

```json
{
  "ResearchDesign": {
    "family": "mixed",
    "primary_type": "design_and_creation",
    "subtype": "algorithm_development",
    "secondary_types": ["experiment"]
  },
  "TechnicalMethod": [
    "Transformer",
    "self-attention",
    "multi-head attention",
    "positional encoding",
    "feed-forward network",
    "residual connection",
    "layer normalization",
    "dropout",
    "label smoothing",
    "Adam"
  ],
  "Data": [
    "WMT 2014 English-German",
    "WMT 2014 English-French",
    "Wall Street Journal Penn Treebank"
  ],
  "Evaluation": [
    "BLEU",
    "perplexity",
    "F1"
  ],
  "Task": [
    "machine translation",
    "constituency parsing"
  ]
}
```

### Summary

Oates (2006) provides the main basis for classifying research design, especially through research strategies such as experiment, case study, survey, and design and creation.

Pilkington and Pretorius (2015) provide a useful structural distinction between research design and research methods. This helps the project avoid mixing the overall research design with specific technical components.

Based on these two works, this project defines a practical extraction schema with five parts:

```text
ResearchDesign
TechnicalMethod
Data
Evaluation
Task
```

This schema is not a direct copy of either framework. It is an operational schema for automatic methodology extraction from computing research papers.

---

## Important Notes

* Focus on **working system**, not perfect accuracy
* Keep implementation simple
* Avoid complex training
* This is a prototype for later improvement

See `todo.md` for task tracking.
