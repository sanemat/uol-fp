CSO Classifier v3.0

input
the textual components of a research paper (usually title, abstract, and keywords)
output
a selection of research topics drawn from the CSO.

## 1 Introduction

(i) semantically enhancing the metadata of scientific publications
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
section 7 show how to apply the classifier to other fields of Science
section 8 provide an overview of applications developed by early adopters of the CSO Classifier
section 9 summarise the main contributions and outline future directions of research

## 9 Conclusions

plan to test BERT, SciBERT, and similar modern embeddings, to try and enhance the semantic and post-processing modules.

## 2 Literature review

(i) topic modelling
(ii) supervised machine learning approaches
(iii) approaches based on citation networks
(iv) approaches based on natural language processing

### 2.1 Topic modelling

the latent Dirichlet analysis, LDA

Topic modelling approaches such as LDA can discover latent topics without a strong prior categorisation or training data.
However, the resulting topics often need manual verification by domain experts, because the model produces word distributions rather than meaningful labels. It also introduces noise.

few topics:
less noise, but too broad
many topics:
more detailed, but noisy

### 2.2 Supervised machine learning approaches

It depends on a gold standard.

### 2.3 Approaches based on citation networks

The paper says that citation-based approaches assign each document to only one topic. I should treat this carefully. This is probably true for many hard-clustering citation-network approaches, but it is not an inherent limitation of citation data itself. A citation network could also be used with soft clustering or multi-label scoring.

### 2.4 Approaches based on natural language processing

Many unsupervised topic discovery approaches generate topics from scratch.

My note:
The authors seem to associate unsupervised NLP-based approaches with generating topics from scratch. This is partly true for clustering or topic modelling methods, but it is not inherent to unsupervised learning. An unsupervised method can still use a controlled vocabulary or ontology, for example by matching document representations to predefined topic representations. Therefore, the key issue is whether the method uses domain knowledge, not only whether it is supervised.

## 4 CSO classifier

input the textual components of a research papar (usually title, abstract, and keywords)
output the relevant topics drawn from CSO.

The syntactic module parses the input documents nad identifies CSO concepts that are ex plicitly reffered in the document.

The semantic module uses part-of-speech tagging to identify promising terms and then pxploits word embeddings to infer semantically related topics.

The post-processing module combines the result of these two modules, discards outliers, and enhances the topic set by including relevant super-areas.

### 4.1 Syntactic module

- a syntactic module, which finds explicitly mentioned CSO concepts;

### 4.2 Semantic module

- a semantic module, which uses word embeddings to infer related topics;

### 4.3 Post-processing module

- a post-processing module, which combines and refines the results.


## 7 Employing the CSO Classifier in other domains of Science


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
