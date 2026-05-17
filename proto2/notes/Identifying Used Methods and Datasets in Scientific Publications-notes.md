Identifying UMethods and Datasets in Scientific Publications

This paper supports:
  method and dataset extraction from scientific publications

This paper does not solve:
  full methodology profile extraction
  research design classification
  evaluation metric extraction
  methodology ontology design

Färber et al. focus on identifying methods and datasets that are actually used in scientific publications. Their approach first recognises method and dataset mentions using domain-specific named entity recognition, and then classifies the mentions as used or non-used based on textual context. This is closely related to my project because TechnicalMethod and Dataset are key components of the proposed MethodologyProfile. However, their work does not aim to extract a full methodology structure, such as ResearchDesign, Task, and EvaluationMetric.

## Introduction

mentioned vs used

Färber et al. propose a framework for identifying methods and datasets used in scientific publications. Their approach first performs domain-specific named entity recognition for METHOD and DATASET entities, then classifies each mention as used or non-used based on textual context, and finally aggregates the labels at the document level. This is closely related to my project because TechnicalMethod and Dataset are core components of the proposed MethodologyProfile. However, their work does not aim to construct a full methodology profile, and it does not directly address ResearchDesign, Task, or EvaluationMetric extraction.

1. What is it about?
2. What part of my project does it support?
3. What does it not solve?
4. How will I use it?
5. Useful terms / concepts:
6. One or two key quotes or page references:
