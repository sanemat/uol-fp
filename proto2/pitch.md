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
| What discipline? | Computre Science |
| What field? | Natural Language Processing + Machine Learning |
| What kind of research? | new model + experiment |
| What method? | Transformer |
| What task? | machine translation |
| What data? | WMT dataset |
| How evaluated? | BLEU score |

This project extracts this structured profile automatically.

<!--
For example, consider the paper "Attention Is All You Need".
The decipline is computer science. But there is more. The fields are Natural Language Processing and Machine Learning. The topic is machine translation. The authors propose a new method, the Transformer. They test it on machine translation using a public dataset. They report BLEU scores.

This project tries to extract all seven parts automatically and represent them as a structured profile.
-->
