# Structured Methodology Extraction from Computing Research Papers

<!--
Hello. My project is to automatically extract structured methodology from computing research papers.
-->

---

# Problem

Topic classification is easy with LLMs

But methodology is difficult

- not clearly written
- depends on writing style
- labels are ambiguous

Methodology matters: it helps compare papers and find research trends.

<!--
Today, topic classification is easy with large language models.
But methodology is still difficult.
It is not clearly written in most papers.
It depends on writing style.
And the labels are often ambiguous.
If we can extract methodology automatically, it helps literature review, paper comparison, and trend analysis.
-->

---

# Previous Work — Definitions

Good definitions exist, but no automatic extraction.

- **Oates (2005)** — framework for research methodology in computing
  - five strategies: survey, design and creation, experiment, case study, action research
- **Pilkington & Pretorius (2015)** — conceptual model of the methodology domain
  - includes worldview, design, method, sampling, analysis
- **Osborne & Motta (2015) — Klink-2** — Computer Science Ontology
  - structured, but weak on methodology terms

<!--
Three works define methodology well.
Oates gives five research strategies for computing.
Pilkington and Pretorius give a more detailed conceptual model.
Osborne and Motta build a Computer Science Ontology from web sources.
But none of them extract methodology automatically from paper text.
-->

---

# Previous Work — Extraction

Extraction exists, but results are not structured.

- **Ghosh et al. (2023)** — extracts methodology component names from AI papers
  - factored sequence labelling
  - chronological evaluation: train on old papers, test on newer names
- **SciBERT (Beltagy et al., 2019)** — BERT pretrained on scientific papers
  - better for scientific term extraction than standard BERT
- **Ma et al. (2023)** — metric-driven mechanism schema
  - Operation / Effect / Direction
  - Operation ≈ Method, Effect ≈ Evaluation

<!--
Three works extract methodology-related information from text.
Ghosh et al. extract methodology component names like model names and algorithm names.
SciBERT is a strong base model for scientific text.
Ma et al. propose a schema with Operation, Effect, and Direction.
But none of them build a full structured methodology profile for a paper.
-->

---

# Gap

Methodology definitions exist.
Extraction methods also exist.

But they are still separate.

No previous work builds a **paper-level structured methodology profile**
from research paper text.

<!--
So the gap is clear.
We have good definitions.
We have extraction tools.
But they are still separate.
No previous work builds a paper-level structured methodology profile from text automatically.
-->

---

# My Approach

**Operational definition for this project**

| Part | Example |
|---|---|
| Design | experiment, survey, case study |
| Method | BERT, CNN, k-means |
| Data | MNIST, SQuAD |
| Evaluation | accuracy, F1 |

Pipeline:

1. Extract candidates — SciBERT
2. Classify roles — LLM
3. Detect design — rules + LLM
4. Build JSON output
5. Check consistency

<!--
My approach defines methodology as four parts for this project.
Design, Method, Data, and Evaluation.
This is an operational definition — scoped for this project, not a full methodology model.
The pipeline has five steps.
First, extract candidates using SciBERT.
Second, classify each candidate into a role.
Third, detect the research design.
Fourth, build a JSON output.
Fifth, apply consistency rules.
The final output is a structured profile for each paper.
-->

---

# Next Steps

- Build candidate extraction step
- Annotate a small gold dataset
  - 10–20 abstracts
  - Design / Method / Data / Evaluation labels
- Evaluate at three levels:
  1. Candidate extraction quality
  2. Role classification accuracy
  3. Full structure quality

<!--
The next steps are three.
First, build the candidate extraction step using SciBERT.
Second, annotate a small gold dataset of ten to twenty abstracts with Design, Method, Data, and Evaluation labels.
Third, evaluate the system at three levels: extraction, role classification, and full structure.
-->

---

# References

**Oates, B.J. (2005)** *Researching information systems and computing.* London: SAGE Publications.

**Pilkington, C. and Pretorius, L. (2015)** *A conceptual model of the research methodology domain.* IC3K 2015. doi:10.5220/0005613100960107

**Osborne, F. and Motta, E. (2015)** *Klink-2: integrating multiple web sources to generate semantic topic networks.* ISWC 2015. doi:10.1007/978-3-319-25007-6_24

**Ghosh, S. et al. (2023)** *Enhancing AI research paper analysis: methodology component extraction using factored transformer-based sequence modeling.* arXiv:2311.03401

**Beltagy, I., Lo, K. and Cohan, A. (2019)** *SciBERT: a pretrained language model for scientific text.* EMNLP 2019.

**Ma, Y. et al. (2023)** *From "what" to "how": extracting the procedural scientific knowledge from papers.* Information Processing & Management. doi:10.1016/j.ipm.2023.103282
