CSO Classifier v3.0

input
the textual components of a research paper (usually title, abstract, and keywords)
output
a selection of research topics drawn from the CSO.

## 1 Introduction

(i) enhancing semantically the metadata of scientific publications
(ii) categorising proceedings in digital libraries.
(iii) producing smart analytics
(iv) generating recommendations
(v) detecting research trends

in a top-down fashion:
the advantage of relying on a set of formally defined research topics associated with human readable labels.
it requires such a controlled vocabulary to be available

bottom-up approaches
do not require a predefined vocabulary
to produce noisier and less interpretable results

the Computer Science Ontology (CSO)

three steps.
First, it finds all topics in the ontology that are explicitly mentioned in the input text.
Then, it identifies further semantically related topics by utilising part-of-speech tagging and word embeddings.
Finally, it discards outliers and enriches this set of topics by taking advantage of the CSO taxonomy to include their superareas.

pip install cso-classifier

https://github.com/angelosalatino/cso-classifier
http://w3id.org/cso/cso-classifier

section 2 review the literature
section 3 discuss the Computer Science Ontology
section 4 describe the CSO Classifier and its modules
section 5 evaluate the CSO Classifier against alternative approaches, focusing on the performance of the new method for detecting outliers.
section 6 discuss their new solution for improving the scalability of the CSO Classifier
section 7 how to apply the classifier to other fields of Science
section 8 an overview of applications developed by early adopters of the CSO Classifier
section 9 summarise the main contributions and outline future directions of research

トピックモデリング
教師あり機械学習アプローチ
引用ネットワークに基づくアプローチ
自然言語処理に基づくアプローチ

トピックモデリング
潜在ディリクレ分析

各文書をトピックの混合としてモデル化

教師あり機械学習アプローチ

引用ネットワークに基づくアプローチ
共引用分析によって科学文書をクラスタリングする原理

自然言語処理に基づくアプローチ

generate the topics from scratch
vs
exploit a domain vocabulary or ontology

generate methodology labels from scratch
vs
extract components using a predefined MethodologyProfile schema

A fixed ontology or controlled vocabulary improves interpretability, but it may fail to cover new terms and emerging methods.

For my project, I should not use a fully closed vocabulary. Instead, I can use a controlled schema with open values. The component types are predefined, such as ResearchDesign, TechnicalMethod, Dataset, Task, and EvaluationMetric. However, the actual extracted values can include new models, datasets, tasks, or metrics.

This gives a hybrid approach: ontology-guided structure with open candidate discovery.

1. What is it about?
2. What part of my project does it support?
3. What does it not solve?
4. How will I use it?
5. Useful terms / concepts:
6. One or two key quotes or page references:

- What does CSO represent?
- What is the input of the CSO Classifier?
- What is the output of the CSO Classifier?
- How can CSO help with field or topic mapping?
- Can CSO represent methodology components?
- Can I use CSO as a mapping target, not as the whole classification system?
- What does CSO not solve for my project?
