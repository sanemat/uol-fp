# Structured Methodology Extraction from Computing Research Papers

## 12.1 Identifying research methodologies that are used in research in the computing disciplines.

<!--
Hello. My project is about extracting structured methodology from computing research papers.
-->

---

# Problem

LLMs can classify paper topics well.

But methodology is harder.

- not always written clearly
- writing style changes between papers
- labels are not clear

Methodology is useful. It helps us compare papers and find research trends.

<!--
Today, large language models can classify paper topics quite well.
But methodology is harder.
It is not always written clearly.
Writing style changes between papers.
And the labels are often not clear.
If we can extract methodology, it helps literature review, paper comparison, and trend analysis.
-->

---

# Previous Work

Definitions:

- **Oates (2005)** — six research strategies: experiment, survey, case study, ...
- **Osborne & Motta (2015)** — Computer Science Ontology

Extraction:

- **Ghosh et al. (2023)** — extracts method names from AI papers
- **SciBERT (Beltagy et al., 2019)** — BERT trained on scientific text

These give two ideas: methodology has structure, and papers contain extractable terms.

<!--
Some previous work defines methodology well.
Oates gives six research strategies for computing.
Osborne and Motta build a Computer Science Ontology.
Other work extracts information from paper text.
Ghosh et al. extract method names from AI papers.
SciBERT is a useful model for scientific text.
These give us two useful ideas.
First, methodology has structure — it is not just one label.
Second, papers contain terms we can extract automatically.
-->

---

# Gap

Good definitions exist.
Good extraction tools exist.

But they are still separate.

No previous work builds a **paper-level structured methodology profile** from text.

<!--
So the gap is clear.
We have good definitions.
We also have extraction tools.
But they are still separate.
No previous work builds a paper-level structured methodology profile from text automatically.
This is what my project tries to do.
-->

---

# My Approach — Structure

Operational definition for this project:

| Part             | Meaning                          | Example                                  |
| ---------------- | -------------------------------- | ---------------------------------------- |
| ResearchDesign   | research strategy (hierarchical) | experiment, design_and_creation          |
| TechnicalMethod  | model, algorithm, or technique   | BERT, CNN, k-means                       |
| Task             | research task or problem         | question answering, image classification |

Optional: Data (e.g. SQuAD), Evaluation (e.g. F1)

```json
{
  "ResearchDesign": {"primary_type": "design_and_creation", "secondary_types": ["experiment"]},
  "TechnicalMethod": ["Transformer"],
  "Task": ["machine translation"]
}
```

<!--
My approach defines methodology as three main parts.
ResearchDesign is the overall research strategy, such as experiment or design_and_creation.
TechnicalMethod is the model or algorithm, such as BERT or CNN.
Task is the research problem, such as question answering.
Data and Evaluation are optional details.
This is an operational definition. It is for this project, not a full definition of methodology.
-->

---

# My Approach — Pipeline

1. Extract candidates — SciBERT
2. Classify roles — rules (TechnicalMethod / Task / Data / Evaluation)
3. Detect design — rules
4. Build JSON output
5. Check consistency (e.g. experiment without Task → weak)

<!--
The pipeline has five steps.
First, extract candidate terms using SciBERT.
Second, classify each term into a role: TechnicalMethod, Task, Data, or Evaluation.
Third, detect the research design using rules.
Fourth, build a JSON output.
Fifth, apply simple consistency checks.
For example, an experiment paper without a Task is weak.
-->

---

# Next Steps

- Prototype complete — end-to-end test passed
- Run pipeline on 6 dataset papers
- Annotate a small gold dataset (10–20 papers)
- Evaluate: extraction quality / role accuracy / full structure

<!--
The prototype is complete and the end-to-end test has passed.
Next, run the pipeline on all six dataset papers.
Then annotate a small gold dataset of ten to twenty papers.
The main labels are ResearchDesign, TechnicalMethod, and Task.
Data and Evaluation are optional.
Finally, evaluate the system at three levels: extraction quality, role accuracy, and full structure.
-->

---

# References

**Beltagy, I., Lo, K. and Cohan, A. (2019)** 'SciBERT: A pretrained language model for scientific text', in Inui, K., Jiang, J., Ng, V. and Wan, X. (eds.) *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing*. Hong Kong, China: Association for Computational Linguistics, pp. 3615–3620. doi: 10.18653/v1/D19-1371.

**Ghosh, M., Ganguly, D., Basuchowdhuri, P. and Naskar, S.K. (2023)** *Enhancing AI research paper analysis: methodology component extraction using factored transformer-based sequence modeling*. arXiv:2311.03401. Available at: [https://arxiv.org/abs/2311.03401](https://arxiv.org/abs/2311.03401).

**Ma, Y., Liu, J., Lu, W. and Cheng, Q. (2023)** 'From "what" to "how": Extracting the procedural scientific information toward the metric-optimization in AI', *Information Processing & Management*, 60(3), article 103315. doi: 10.1016/j.ipm.2023.103315.

**Oates, B.J. (2005)** *Researching information systems and computing*. London: SAGE Publications.

**Osborne, F. and Motta, E. (2015)** 'Klink-2: integrating multiple web sources to generate semantic topic networks', in Gandon, F., Sabou, M., Sack, H., d'Amato, C., Cudré-Mauroux, P. and Zimmermann, A. (eds.) *The Semantic Web – ISWC 2015*. Cham: Springer International Publishing, pp. 408–424. doi: 10.1007/978-3-319-25007-6_24.

**Pilkington, C. and Pretorius, L. (2015)** 'A conceptual model of the research methodology domain', in *Proceedings of the International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K 2015)*. Setúbal: SCITEPRESS – Science and Technology Publications, pp. 96–107. doi: 10.5220/0005613100960107.
