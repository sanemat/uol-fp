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

A topic label may say that this paper is about machine translation.
But this table shows something different: how the paper works.

It shows the method, the task, the dataset, and the metric.

My project tries to extract this kind of short profile from computing papers.
-->

---

<!-- {"layout": "Title slide"} -->
# Role-Based Methodology Profiles

## Template 12.1: Identifying research methodologies used in computing research

<!--
I am using Template 12.1.

The template asks us to identify research methodologies used in computing research.

The full template is broad, so I focus on four parts that are usually visible in papers:
method, task, dataset, and metric.
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
The motivation is simple.

But when readers compare papers, they need more detail.

Two papers may have the same topic, but use different methods, datasets, or metrics.

So the profile is not meant to replace reading.
It is a quick guide before reading deeply.
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

The CSO Classifier classifies papers by topic.

Ghosh and colleagues extract methodology component names from AI papers.

My project sits between these ideas.
It uses the idea of structured methodology, but the output is small and reader-friendly.
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

- proposed method
- research task
- evaluation dataset
- evaluation metric

<!--
The prototype takes paper text as input.

It has three steps.

First, extract candidate phrases.
Second, classify their roles.
Third, combine the results into one short profile.

For evaluation, I will use a small human-reviewed set.

I will check two things:
whether the system finds the right terms,
and whether it assigns the right roles.

A correct term with the wrong role is still not useful.

I do not try to extract the full research design in this prototype.  
That would be harder and more subjective.  
I treat it as a possible extension after the four visible roles.
-->

---

# References

**Angelo Salatino, Francesco Osborne, and Enrico Motta. 2022.** *CSO Classifier 3.0: a scalable unsupervised method for classifying documents in terms of research topics.* International Journal on Digital Libraries 23, 1 (March 2022), 91–110. https://doi.org/10.1007/s00799-021-00305-y

**B. J. Oates. 2006.** *Researching Information Systems and Computing*. SAGE Publications, London.

**C. Pilkington and L. Pretorius. 2015.** *A conceptual model of the research methodology domain.* In *Proceedings of the 7th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K 2015), Volume 2: KEOD*. SCITEPRESS – Science and Technology Publications, Setúbal, Portugal, 96–107. https://doi.org/10.5220/0005613100960107

**Ghosh, M., Ganguly, D., Basuchowdhuri, P. and Naskar, S.K. (2023)** *Enhancing AI research paper analysis: methodology component extraction using factored transformer-based sequence modeling*. arXiv:2311.03401. Available at: [https://arxiv.org/abs/2311.03401](https://arxiv.org/abs/2311.03401).
