---
presentationID: 1iG1XWNQtfXCZao_cMtL7VfiTclxLfKWr1cnGdzr3Ysk
title: Structured Methodology Extraction from Computing Research Papers
---
# Structured Methodology Extraction from Computing Research Papers

## 12.1 Identifying research methodologies that are used in research in the computing disciplines.

<!--
Hello. My project is about extracting structured methodology from computing research papers.
-->

---

<!-- {"layout": "Title and two columns"} -->
# Simple Example

A computing paper is not only about its topic.

For "Attention Is All You Need" (Vaswani et al., 2017):

- - -

| Question | Answer |
|---|---|
| What kind of discipline? | Computer Science |
| What field? | NLP + Machine Learning |
| What design or strategy? | new model + experiment |
| What data generation method? | Documents |
| What technical method? | Transformer |
| What task? | machine translation |
| What dataset? | WMT dataset |
| How evaluated? | BLEU score |

This project extracts this structured profile automatically.

<!--
For example, consider the paper "Attention Is All You Need".
The discipline is computer science. But there is more. The fields are Natural Language Processing and Machine Learning. The topic is machine translation. The authors propose a new method, the Transformer. The data generation method is documents. They test it on machine translation using a public dataset. They report BLEU scores.

This project tries to extract all eight parts automatically and represent them as a structured profile.
-->

---
