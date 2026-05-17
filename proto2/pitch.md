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
| Proposed method | Transformer |
| Research task | machine translation |
| Evaluation dataset | WMT dataset |
| Evaluation metric | BLEU score |

A paper is not only about its topic.

It also has a method, data, and evaluation.

<!--
I will start with a simple example.

"Attention Is All You Need" introduced the Transformer model.

A topic label may say: this paper is about machine translation.
But I also want to know how the paper works.

Here, the proposed method is Transformer.
The task is machine translation.
The dataset is WMT.
The metric is BLEU.

My project extracts this kind of short profile from computing papers.
-->


---
# Building Role-Based Methodology Profiles from Computing Research Papers

## 12.1 Identifying research methodologies that are used in research in the computing disciplines.

<!--
I am choosing Template 12.1.

The template asks us to identify research methodologies used in computing research.

I focus on four visible parts:
method, task, dataset, and metric.

This is a smaller version of the full idea, but it still answers how the research was done.
-->

---

# Previous Work

| Work | What it does | What is still missing |
|---|---|---|
| Oates | Explains research strategies in computing | Not an NLP system |
| Pilkington & Pretorius | Models methodology as a structure | Does not extract from papers |
| CSO Classifier | Classifies papers by topic | Does not show methodology roles |
| Ghosh et al. | Extracts methodology component names | Does not produce a reader-friendly profile |


<!--
Oates gives the methodology background for computing research.

Pilkington and Pretorius show that methodology can be treated as a structure.

The CSO Classifier classifies papers by topic, but it does not show how the paper works.

Ghosh and colleagues is the closest technical work. They extract methodology component names from AI papers.

The gap is a short, readable profile of the roles inside the paper.
-->

---

# Prototype

Input:

- title
- abstract
- selected paper sections

Output:

**Paper → Role-based MethodologyProfile**

The prototype will extract:

- proposed method
- research task
- evaluation dataset
- evaluation metric

<!--
The prototype takes paper text as input.

The output is a short profile with four roles:
proposed method, task, dataset, and metric.

I will compare the output with a small human-reviewed set of examples.
-->

---

# References

**Angelo Salatino, Francesco Osborne, and Enrico Motta. 2022.** *CSO Classifier 3.0: a scalable unsupervised method for classifying documents in terms of research topics.* International Journal on Digital Libraries 23, 1 (March 2022), 91–110. https://doi.org/10.1007/s00799-021-00305-y

**B. J. Oates. 2006.** *Researching Information Systems and Computing*. SAGE Publications, London.

**C. Pilkington and L. Pretorius. 2015.** *A conceptual model of the research methodology domain.* In *Proceedings of the 7th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K 2015), Volume 2: KEOD*. SCITEPRESS – Science and Technology Publications, Setúbal, Portugal, 96–107. https://doi.org/10.5220/0005613100960107

**Ghosh, M., Ganguly, D., Basuchowdhuri, P. and Naskar, S.K. (2023)** *Enhancing AI research paper analysis: methodology component extraction using factored transformer-based sequence modeling*. arXiv:2311.03401. Available at: [https://arxiv.org/abs/2311.03401](https://arxiv.org/abs/2311.03401).
