# Why this paper matters
Closest prior work to my component extraction task.
SciBERT BIO tagging extracts Method/Task/Dataset names from AI papers.
Proposes factored labeling to handle large, evolving domain-specific vocabularies.

# What it contributes to my project
Shows F1 ~0.40 on out-of-domain (chronological) evaluation — realistic baseline for my project.
Data-driven factoring (k-means on SciBERT embeddings) outperforms ontology-driven approach.
Introduces DocAIMER document representation (Abstract + Introduction + Methodology + Experiments + Results).
Demonstrates that chronological train/test split reveals true generalization difficulty.

# Which schema fields it supports
Method (TechnicalMethod), Task, Data (Dataset)

# What it does not cover
ResearchDesign (experiment vs. case study etc.) — outside scope of Ghosh.
Evaluation metrics extraction — does not extract metric names or values.

# Useful definitions
Methodology component = named entity for Method, Task, or Dataset extracted from paper text.
Annotation unit = token span labeled with BIO tags (Beginning-Inside-Outside).
DocAIMER = document representation: concatenation of Abstract, Introduction, Methodology, Experiments, Results.
Factored model = variant that assigns category-specific BIO labels rather than shared BIO labels.

# Useful evaluation method
Chronological train-test split: train on papers ≤2017, test on papers >2017.
Simulates deployment scenario where new method names emerge after training.
Compares in-domain (90:10 split within ≤2017) vs. out-of-domain (cross-year) performance.

# Important quotes or sections
- Dataset: PapersWithCode, 34,560 papers, 2,099 method names in knowledge base
- 7 domain categories: General, CV, Seq2Seq, RL, NLP, Audio/Speech, Graph
- Best out-of-domain result: SciBERT-CRF-D Precision 0.5836, Recall 0.3065, F1 0.4019
- Best in-domain result: SciBERT-O Precision 0.9821, Recall 0.9854, F1 0.9854

# Risk of misusing this paper
Do not claim Ghosh 2023a solves full methodology extraction.
It only extracts component names (Method/Task/Dataset) — not ResearchDesign or Evaluation.
In-domain F1 ~0.98 is misleading; realistic out-of-domain F1 ~0.40 is the relevant figure.
