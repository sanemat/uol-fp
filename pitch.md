# Methodology Extraction from Research Papers

---

# Template + Idea

Template:
12 CM3060 Natural Language Programming
12.1 Project Idea 1: Identifying research methodologies that are used
in research in the computing disciplines.

My project:
Automatically extract methodology from papers

---

# Problem

Topic classification is easy with LLMs

But methodology is difficult

- not clearly written
- depends on writing style
- labels are ambiguous

---

# Why + Previous Work

Methodology shows how research is done

Previous work:

Models (Oates(2005), Pilkington(2015))
- define methodology
- no extraction

Ontology (ACM Computing Classification System, Computer Science Ontology, Osborne(2015))
- structured
- weak for methodology

LLM / NLP
- scalable
- unstable

---

# Gap

We have:

- definitions (models, ontology)
- extraction tools (LLM)

But:

- no connection
- no structured extraction

---

# Idea + Approach

Represent methodology as:

Design (1)  
Method (1–2)

Example:
Design: Experiment  
Method: dataset evaluation  

LLM extracts from abstract

---

# Evaluation + Contribution

Evaluation:
- accuracy  
- consistency (important)  
- small human check  

Contribution:
connect definition and extraction

Goal:
structure methodology and extract it with LLM


# References

**Oates, B. J. (2005)** *Researching information systems and computing.* London: SAGE Publications.

**Pilkington, C. and Pretorius, L. (2015)** *A conceptual model of the research methodology domain*. In: *Proceedings of the International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K 2015)*. Setúbal: SCITEPRESS - Science and Technology Publications, pp. 96–107. doi:10.5220/0005613100960107.

ACM Computing Classification System https://dl.acm.org/ccs

**Osborne, F. and Motta, E., 2015, October.** *Klink-2: integrating multiple web sources to generate semantic topic networks.* In International Semantic Web Conference (pp. 408-424). Cham: Springer International Publishing. https://doi.org/10.1007/978-3-319-25007-6_24
