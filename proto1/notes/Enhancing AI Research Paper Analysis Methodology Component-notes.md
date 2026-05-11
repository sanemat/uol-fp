# Why this paper matters
Extension of Ghosh 2023a with transformer-based factored models and a chronological retraining mechanism.
Introduces the LFGB (Label-based Factored Granular Binary) variant, the best performer on chronological evaluation.
Provides honest post-hoc manual benchmark showing realistic precision ~0.62.

# What it contributes to my project
Shows F1 ~0.34 on chronological out-of-domain evaluation — confirms 2023a result.
Retraining with silver-standard data (model predictions fed back as training data) improves handling of emerging method names.
Zero-shot analysis: for SEQ and RL categories, >75% of test entities were unseen in training — motivates LLM-based approach.
Chronological evaluation framework is the right way to measure methodology extraction quality.

# Which schema fields it supports
Method (TechnicalMethod) only

# What it does not cover
ResearchDesign — still outside scope.
Evaluation metrics extraction — not addressed.

# Useful definitions
Chronological evaluation framework = incremental evaluation where model trained on year ≤t is tested on year t+1, t+2, etc.
Silver-standard retraining = model predictions on year t+1 are used as training labels to produce an updated model for year t+2.
LFGB = Label-based Factored Granular Binary: binary partitioning of label space; best chronological performer.
Partitioned input space = training data split into domain-specific subsets, each training a separate labeler.
Partitioned label space = BIO label set split into per-domain variants.

# Useful evaluation method
Incremental chronological evaluation: train on ≤2017, test on 2018, 2019, 2020 separately.
Post-hoc manual benchmark on 285 post-2017 sentences for precision/recall ground truth.
Zero-shot / few-shot split: count test entities unseen vs. seen in training.

# Important quotes or sections
- Best out-of-domain F1: SciBERT CRF-LFGB = 0.3433
- Post-hoc manual evaluation: Precision 0.623, Recall 0.2099, F1 0.314
- Zero-shot SEQ/RL categories: >75% test entities unseen in training
- Same dataset as 2023a: 34,560 PapersWithCode papers, train ≤2017 / test >2017

# Risk of misusing this paper
In-domain F1 ~0.98 (same as 2023a) is misleading; cite out-of-domain ~0.34 as the realistic figure.
Silver-standard retraining reduces label quality — treat it as an approximation, not ground truth.
Do not equate "factored model" improvements with solving the full methodology extraction problem.
