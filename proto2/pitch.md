---
presentationID: 1iG1XWNQtfXCZao_cMtL7VfiTclxLfKWr1cnGdzr3Ysk
title: Building Role-Based Methodology Profiles from Computing Research Papers
---

<!-- {"layout": "Title and two columns"} -->
# Simple Example

"Attention Is All You Need" (Vaswani et al., 2017) is a famous AI paper that introduced the Transformer model.

- - -

| Methodology role | Extracted component |
|---|---|
| Technical method | Transformer |
| Research task | machine translation |
| Evaluation dataset | WMT dataset |
| Evaluation metric | BLEU score |

A paper is not only about its topic.

It also has methodology roles: method, task, data, and evaluation.

<!--
"Attention Is All You Need" is a very famous AI paper. But the title does not tell us how it works.

The table does. Each row assigns a role: the method is Transformer, the task is machine translation, the dataset is WMT, the metric is BLEU. Together, they answer: how does this paper work?

The topic label says what. The role-based profile says how. My project is built on this difference.
-->

---

<!-- {"layout": "Title slide"} -->
# Role-Based Methodology Profiles

## Template 12.1: Identifying research methodologies used in computing research

<!--
Template 12.1 asks us to identify research methodologies in computing research. Roles are my structure for answering that question.
-->

---

# Why This Matters

Topic labels help readers find papers.

Role-based profiles help readers compare papers.

| Topic view | Role view |
|---|---|
| What is this paper about? | How does this paper work? |
| NLP, machine translation | method, task, dataset, metric |

<!--
Two papers on the same topic can use different methods, datasets, and metrics. The topic label does not show this. The role-based profile does.

It is not a replacement for reading. It is a fast way to compare papers before reading deeply.
-->


---

# Previous Work

| Work | What it does | What is still missing |
|---|---|---|
| Oates | Explains research strategies in computing | Not an NLP system |
| Pilkington & Pretorius | Models methodology as a structure | Does not extract from papers |
| CSO Classifier | Classifies papers by topic | Does not show methodology roles |
| Ghosh et al. | Extracts methodology component names | Does not assign methodology roles to extracted names |


<!--
Oates and Pilkington & Pretorius give theoretical background but do not extract from papers automatically. The CSO Classifier classifies by topic — it answers "what", not "how."

Ghosh and colleagues extract methodology component names from AI papers. That is the closest prior work. But a name without a role does not explain how it is used. "BERT" could be a method, a baseline, or a comparison point.

My project assigns roles to extracted names. That turns a list of names into a profile that answers how.
-->

---

<!-- {"layout": "Title and two columns"} -->
# Prototype

Input:

- title
- abstract
- selected paper sections

- - -

Output:

**Paper → Role-based Methodology Profile**

The prototype will extract:

- technical method
- research task
- evaluation dataset
- evaluation metric

<!--
Three steps: extract candidate phrases, classify each by role, combine into a short profile.

Evaluation checks two things: whether the system finds the right terms, and whether it assigns the right roles. A correct term with the wrong role is still wrong.

Research design is not included. It is harder to extract and more subjective. The four roles are the starting point. Design is a possible next step.
-->

---

# References

**Angelo Salatino, Francesco Osborne, and Enrico Motta. 2022.** *CSO Classifier 3.0: a scalable unsupervised method for classifying documents in terms of research topics.* International Journal on Digital Libraries 23, 1 (March 2022), 91–110. https://doi.org/10.1007/s00799-021-00305-y

**B. J. Oates. 2006.** *Researching Information Systems and Computing*. SAGE Publications, London.

**C. Pilkington and L. Pretorius. 2015.** *A conceptual model of the research methodology domain.* In *Proceedings of the 7th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K 2015), Volume 2: KEOD*. SCITEPRESS – Science and Technology Publications, Setúbal, Portugal, 96–107. https://doi.org/10.5220/0005613100960107

**Ghosh, M., Ganguly, D., Basuchowdhuri, P. and Naskar, S.K. (2023)** *Enhancing AI research paper analysis: methodology component extraction using factored transformer-based sequence modeling*. arXiv:2311.03401. Available at: [https://arxiv.org/abs/2311.03401](https://arxiv.org/abs/2311.03401).
