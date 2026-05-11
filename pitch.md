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

It is easier to identify a paper's topic than to extract how the research was done.

Methodology is harder because:

- important information is spread across the paper
- writing style changes between papers
- one paper may use more than one research strategy
- labels are not always clear

This matters for literature review, paper comparison, and trend analysis.

<!--
Current systems, including large language models, can often classify a paper's topic.
But extracting methodology is harder.
The important information is spread across the paper.
Different authors write it differently.
One paper may also use more than one research strategy.
This matters for literature review, paper comparison, and trend analysis.
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
Oates, in 2005, defines six research strategies for computing: experiment, survey, case study, action research, ethnography, and design and creation.
Pilkington and Pretorius, in 2015, separate research design from technical method.
Ghosh and colleagues, in 2023, extract method names from AI papers using Scientific BERT, or SciBERT.
SciBERT, from Beltagy and colleagues in 2019, is a language model trained on scientific text.
These give us two useful ideas.
First, methodology has structure, and it is not just one label.
Second, papers contain terms we can extract automatically.
-->

---

# Gap

Good methodology definitions exist.
Good extraction tools exist.

But in the work I reviewed, these two pieces are not yet connected into one paper-level profile.

This project tries to connect them.

<!--
So the gap is clear.
We have good definitions.
We also have good extraction tools.
But in the work I reviewed, these two pieces are not yet connected into one paper-level methodology profile.
This is what my project tries to do.
-->

---

# My Approach — Structure

I define a methodology profile with five parts.

| Part | Meaning | Example |
|---|---|---|
| Research Design | paper-level research strategy | new model + experiment |
| Technical Method | model, algorithm, or technique | Transformer |
| Task | research task or problem | machine translation |
| Data | dataset or data source | WMT |
| Evaluation | metric or benchmark | BLEU |

```json
{
  "ResearchDesign": "design_and_creation + experiment",
  "TechnicalMethod": ["Transformer"],
  "Task": ["machine translation"],
  "Data": ["WMT"],
  "Evaluation": ["BLEU"]
}
```

<!--
My approach defines a methodology profile with five parts.
Research Design is the paper-level research strategy, such as design and creation combined with experiment.
Technical Method is the model or algorithm, such as the Transformer or BERT.
Task is the research problem, such as machine translation.
Data is the dataset or data source, such as WMT.
Evaluation is the metric or benchmark, such as BLEU.
In the prototype, the first three parts are the main focus. Data and Evaluation are defined but secondary.
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

**Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kaiser, Ł. and Polosukhin, I. (2017)** 'Attention is all you need', in *Advances in Neural Information Processing Systems*, 30, pp. 5998–6008. Available at: https://arxiv.org/abs/1706.03762.
