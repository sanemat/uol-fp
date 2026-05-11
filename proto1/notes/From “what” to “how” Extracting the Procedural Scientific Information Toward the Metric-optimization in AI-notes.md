# Why this paper matters
Proposes a richer procedural schema — metric-driven mechanism (Operation, Effect, Direction, Task) — that goes beyond entity extraction to capture *how* a method improves a metric.
Builds MKG_NLP: a knowledge graph of 43K n-ary mechanism relations from NLP papers.
Bridges the gap between named-entity extraction (what Ghosh does) and structured procedural knowledge.

# What it contributes to my project
Shows that extracting "how a method improves a metric" is feasible with BERT + seq2seq pipeline.
Mechanism detection + query-guided extraction + task recognition is a three-stage pipeline — analogous to my candidate extraction + classification stages.
Human evaluation at 81.4% accuracy provides a benchmark for non-standard extraction schemas.
Task extraction F1=89 (precision=93, recall=85) shows that task/method identification is tractable.

# Which schema fields it supports
Method — Operation/Effect/Direction tuple captures how a method works.
Evaluation — metric-driven framing is directly about evaluation metric optimization.
(Partial overlap with my schema; does not map cleanly to Design or Data.)

# What it does not cover
ResearchDesign — not addressed.
Data field (dataset names/sources) — not the focus of this schema.
Computing research beyond AI/NLP — dataset is NLP papers only.

# Useful definitions
Metric-driven mechanism = (Operation, Effect, Direction, Task) n-ary relation describing how an operation affects a metric in a given direction for a given task.
Mechanism detection = binary classification of whether a sentence contains a mechanism relation.
Query-guided seq2seq extraction = BART model prompted with entity-class query to extract relation arguments.
MKG_NLP = NLP Metric-driven Mechanism Knowledge Graph; >43K n-ary relations.
Abs+Sent = training dataset augmented with sentence-level labels in addition to abstract-level labels.

# Useful evaluation method
Human evaluation on extracted relations (81.4% accuracy) — useful when ground truth is hard to define automatically.
Three-frequency split for task extraction: high- / middle- / low-frequency tasks — tests generalization to rare tasks.
Domain adaptation via fine-tuning on SCIERC before target dataset training.

# Important quotes or sections
- Dataset: NLP papers with metric-driven mechanisms; covers single-sentence and multi-sentence cases
- MKG_NLP: >43K n-ary mechanism relations in form (Operation, Effect, Direction, Task)
- Task extraction: F1=89, Precision=93, Recall=85
- Human evaluation: 81.4% accuracy on extracted mechanisms
- Framework: mechanism detection model + query-guided seq2seq extraction + task recognition model

# Risk of misusing this paper
Schema is domain-specific (NLP papers) — do not assume it transfers directly to all computing fields.
"Metric-driven mechanism" is a different unit from my "methodology component" — schemas are not interchangeable.
Human evaluation (81.4%) was on a curated sample; real-world recall may be lower due to multi-sentence mechanisms.
Do not cite this as evidence that full structured methodology extraction is solved; scope is narrower than my project.
