# Structured Methodology Extraction from Computing Research Papers

## 12.1 Identifying research methodologies that are used in research in the computing disciplines.

<!--
Hello. My project is about extracting structured methodology from computing research papers.
-->

---

# Problem

LLMs can classify paper topics quite well.

But methodology is harder.

* it is often not written clearly
* it depends on writing style
* labels can be unclear

Methodology is important. It helps us compare papers and find research trends.

<!--
Today, large language models can classify paper topics quite well.
But methodology is harder.
It is often not written clearly.
It depends on the writing style of each paper.
Also, the labels can be unclear.
If we can extract methodology automatically, it can help literature review, paper comparison, and trend analysis.
-->

---

# Previous Work — Definitions

Good definitions exist, but they do not extract methodology automatically.

* **Oates (2005)** — framework for research methodology in computing

  * five strategies: survey, design and creation, experiment, case study, action research
* **Pilkington & Pretorius (2015)** — conceptual model of the methodology domain

  * includes worldview, design, method, sampling, and analysis
* **Osborne & Motta (2015) — Klink-2** — Computer Science Ontology

  * structured, but weak for methodology terms

<!--
Some previous work defines methodology well.
Oates gives five research strategies for computing.
Pilkington and Pretorius give a more detailed conceptual model.
Osborne and Motta build a Computer Science Ontology from web sources.
However, these works do not extract methodology automatically from paper text.
-->

---

# Previous Work — Extraction

Extraction exists, but the results are not structured as methodology.

* **Ghosh et al. (2023)** — extracts methodology component names from AI papers

  * factored sequence labelling
  * chronological evaluation: train on old papers, test on newer names
* **SciBERT (Beltagy et al., 2019)** — BERT pretrained on scientific papers

  * useful for scientific term extraction
* **Ma et al. (2023)** — procedural scientific information

  * Operation / Effect / Direction
  * useful for understanding how a method changes results

<!--
Other previous work extracts methodology-related information from text.
Ghosh et al. extract methodology component names, such as model names and algorithm names.
SciBERT is a useful base model for scientific text.
Ma et al. propose a schema with Operation, Effect, and Direction.
However, these works do not build one paper-level methodology structure with design, method, and task together.
-->

---

# From Labels to Structure

Previous work gives two useful ideas.

1. Methodology is not one simple label.

   * it includes research design and research methods
2. Scientific papers contain extractable entities.

   * method, task, dataset, metric

So this project represents methodology as a small structure.

<!--
Previous work does not give exactly my structure.
But it gives two useful ideas.
First, methodology is not just one label. It has structure, such as design and methods.
Second, scientific information extraction already studies entities such as methods, tasks, datasets, and metrics.
My project combines these ideas into one practical structure for computing papers.
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
We also have extraction tools.
But they are still separate.
No previous work builds a paper-level structured methodology profile from text automatically.
-->

---

# My Approach — Structure

Operational definition for this project:

| Part   | Meaning                        | Example                                  |
| ------ | ------------------------------ | ---------------------------------------- |
| Design | overall research design        | experiment, survey, case study           |
| Method | model, algorithm, or technique | BERT, CNN, k-means                       |
| Task   | research task or problem       | question answering, image classification |

Optional details:

* Data: MNIST, SQuAD
* Evaluation: accuracy, F1

<!--
My approach defines methodology as three main parts for the first version.
They are Design, Method, and Task.
This is an operational definition. It is for this project, not a full definition of methodology.
Data and Evaluation are also useful, but I treat them as optional details at this stage.
This keeps the project smaller and closer to previous work.
-->

---

# Example Output

```json
{
  "Design": "experiment",
  "Method": ["BERT"],
  "Task": ["question answering"],
  "Optional": {
    "Data": ["SQuAD"],
    "Evaluation": ["F1"]
  }
}
```

<!--
This is an example of the final output.
The main methodology profile has Design, Method, and Task.
Data and Evaluation can be added when the information is available.
This is more structured than a flat list of extracted terms.
-->

---

# My Approach — Pipeline

1. Extract candidates — SciBERT
2. Classify roles — LLM
3. Detect design — rules + LLM
4. Build JSON output
5. Check consistency

<!--
The pipeline has five steps.
First, extract candidates using SciBERT.
Second, classify each candidate into a role.
Third, detect the research design.
Fourth, build a JSON output.
Fifth, apply consistency rules.
The final output is a structured profile for each paper.
-->

---

# Consistency Checks

Simple rules can find weak or inconsistent structures.

* Experiment without Task → weak
* Experiment without Method → weak
* Method without Task → incomplete
* Theoretical design with benchmark-style Evaluation → possible mismatch

<!--
After building the structure, I can check simple consistency rules.
For example, an experiment usually needs a task and a method.
A method without a task may be incomplete.
A theoretical paper with benchmark-style evaluation may need checking.
These rules do not prove that the output is correct.
But they help find weak outputs and useful error cases.
-->

---

# Next Steps

* Build the candidate extraction step
* Annotate a small gold dataset

  * 10–20 papers
  * Design / Method / Task labels
  * optional Data / Evaluation labels
* Evaluate at three levels:

  1. Candidate extraction quality
  2. Role classification accuracy
  3. Full structure quality

<!--
The next steps are three.
First, build the candidate extraction step using SciBERT.
Second, annotate a small gold dataset of ten to twenty papers with Design, Method, and Task labels.
Data and Evaluation can be annotated as optional details.
Third, evaluate the system at three levels: extraction, role classification, and full structure.
-->

---

# References

**Beltagy, I., Lo, K. and Cohan, A. (2019)** ‘SciBERT: A pretrained language model for scientific text’, in Inui, K., Jiang, J., Ng, V. and Wan, X. (eds.) *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing*. Hong Kong, China: Association for Computational Linguistics, pp. 3615–3620. doi: 10.18653/v1/D19-1371.

**Ghosh, M., Ganguly, D., Basuchowdhuri, P. and Naskar, S.K. (2023)** *Enhancing AI research paper analysis: methodology component extraction using factored transformer-based sequence modeling*. arXiv:2311.03401. Available at: [https://arxiv.org/abs/2311.03401](https://arxiv.org/abs/2311.03401).

**Ma, Y., Liu, J., Lu, W. and Cheng, Q. (2023)** ‘From “what” to “how”: Extracting the procedural scientific information toward the metric-optimization in AI’, *Information Processing & Management*, 60(3), article 103315. doi: 10.1016/j.ipm.2023.103315.

**Oates, B.J. (2005)** *Researching information systems and computing*. London: SAGE Publications.

**Osborne, F. and Motta, E. (2015)** ‘Klink-2: integrating multiple web sources to generate semantic topic networks’, in Gandon, F., Sabou, M., Sack, H., d’Amato, C., Cudré-Mauroux, P. and Zimmermann, A. (eds.) *The Semantic Web – ISWC 2015*. Cham: Springer International Publishing, pp. 408–424. doi: 10.1007/978-3-319-25007-6_24.

**Pilkington, C. and Pretorius, L. (2015)** ‘A conceptual model of the research methodology domain’, in *Proceedings of the International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K 2015)*. Setúbal: SCITEPRESS – Science and Technology Publications, pp. 96–107. doi: 10.5220/0005613100960107.
