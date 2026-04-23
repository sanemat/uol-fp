# Methodology Extraction from Research Papers

---

# Template + Idea

Template:
12 CM3060 Natural Language Programming

12.1 Project Idea 1: Identifying research methodologies that are used
in research in the computing disciplines.

My project:
Automatically extract methodology from papers

<!--
Hello.
I base my project on the template
“Identifying research methodologies in computing research.”
This is from the CM3060 Natural Language Programming course.
My project is to **automatically extract methodology from research papers.**
-->

---

# Problem

Topic classification is easy with LLMs

But methodology is difficult

- not clearly written
- depends on writing style
- labels are ambiguous

<!--
Today, topic classification is easy with large language models.
But methodology is still difficult.
This is because:
- it is not clearly written
- it depends on writing style
- labels are ambiguous
So, methodology is important, but hard to use.
-->

---

# Why + Previous Work

Methodology shows how research is done.

Previous work:
- Models (Oates(2005), Pilkington(2015))
  - define methodology
  - no extraction
- Ontology (ACM Computing Classification System, Computer Science Ontology, Osborne(2015))
  - structured
  - weak for methodology
- LLM / NLP
  - scalable
  - unstable

<!--
Methodology shows how research is done.
There are three types of previous work.
First, models, such as Oates in 2005 and Pilkington in 2015.
They define methodology clearly, but they do not support extraction.
Second, ontology systems, like the ACM Computing Classification System and the Computer Science Ontology.
They give structured classification, but they are weak for methodology.
Third, LLM and NLP approaches.
They are scalable, but the results are often unstable.
-->

---

# Gap

We have:

- definitions (models, ontology)
- extraction tools (LLM)

But:

- no connection
- no structured extraction

<!--
So, there is a clear gap.
We have good definitions from models and ontology.
We also have strong extraction tools like LLMs.
But there is no connection between them.
And there is no structured way to extract methodology.
-->
---

# Idea + Approach

Represent methodology as:

- Design (1)  
- Method (1–2)

Example:
- Design: Experiment  
- Method: dataset evaluation  

LLM extracts from abstract

<!--
My idea is to represent methodology as a simple structure.
It has two parts:
one Design
one or two Methods
For example:
Design can be “Experiment”
Method can be “dataset evaluation”
I use an LLM to extract this structure from a paper abstract.
So the output is structured, not just a label.
-->

---

# Evaluation + Contribution

Evaluation:
- accuracy  
- consistency (important)  
- small human check  

Contribution:
- connect definition and extraction

Goal:
- structure methodology and extract it with LLM

<!--
I evaluate the system in three ways.
First, accuracy, to check correctness.
Second, consistency, to check stability.
Third, a small human check.
Consistency is especially important, because LLM results can change.
The contribution of this project is to connect
definition and extraction.
The goal is to structure methodology and extract it with LLM.
Thank you.
-->
---

# References

**Oates, B. J. (2005)** *Researching information systems and computing.* London: SAGE Publications.

**Pilkington, C. and Pretorius, L. (2015)** *A conceptual model of the research methodology domain*. In: *Proceedings of the International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K 2015)*. Setúbal: SCITEPRESS - Science and Technology Publications, pp. 96–107. doi:10.5220/0005613100960107.

ACM Computing Classification System https://dl.acm.org/ccs

**Osborne, F. and Motta, E., 2015, October.** *Klink-2: integrating multiple web sources to generate semantic topic networks.* In International Semantic Web Conference (pp. 408-424). Cham: Springer International Publishing. https://doi.org/10.1007/978-3-319-25007-6_24
