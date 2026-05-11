# Structured Methodology Extraction from Computing Research Papers

## 12.1 Identifying research methodologies that are used in research in the computing disciplines.

<!--
Hello. My project is about extracting structured methodology from computing research papers.
-->

---

# Simple Example

A computing paper is not only about its topic.

For "Attention Is All You Need" (Vaswani et al., 2017):

| Question | Answer |
|---|---|
| What kind of research? | new model + experiment |
| What method? | Transformer |
| What task? | machine translation |
| What data? | WMT dataset |
| How evaluated? | BLEU score |

This project extracts this structured profile automatically.

<!--
For example, consider the paper "Attention Is All You Need".
The topic is machine translation.
But there is more.
The authors propose a new method, the Transformer.
They test it on machine translation using a public dataset.
They report BLEU scores.
This project tries to extract all five parts automatically and represent them as a structured profile.
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

Previous work gives two pieces:

| Area | What it gives |
|---|---|
| Methodology theory | labels for research strategies |
| NLP extraction | ways to extract terms from paper text |

But these two pieces are usually separate.

<!--
Oates (2005) defines six research strategies for computing: experiment, survey, case study, action research, ethnography, and design and creation.
Pilkington and Pretorius (2015) separate research design from technical method.
Ghosh et al. (2023) extract method names from AI papers using SciBERT.
SciBERT (Beltagy et al., 2019) is a language model trained on scientific text.
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
| Research Design   | research strategy (hierarchical) | experiment, design_and_creation          |
| Technical Method  | model, algorithm, or technique   | BERT, CNN, k-means                       |
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
Research Design is the overall research strategy, such as experiment or design_and_creation.
Technical Method is the model or algorithm, such as BERT or CNN.
Task is the research problem, such as question answering.
Data and Evaluation are optional details.
This is an operational definition. It is for this project, not a full definition of methodology.
-->

---

# My Approach — Pipeline

1. Extract candidates — SciBERT
2. Classify roles — rules (Technical Method / Task / Data / Evaluation)
3. Detect design — rules
4. Build JSON output
5. Check consistency (e.g. experiment without Task → weak)

<!--
The pipeline has five steps.
First, extract candidate terms using SciBERT.
Second, classify each term into a role: Technical Method, Task, Data, or Evaluation.
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
The main labels are Research Design, Technical Method, and Task.
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
