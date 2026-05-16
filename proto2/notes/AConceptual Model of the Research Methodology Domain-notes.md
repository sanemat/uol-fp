ResearchScheme
  has PhilosophicalWorldview
  has ResearchDesign
  has ResearchMethod

## Section 1: Abstract, introduction

an ontology of research methodology domain

"A research scheme that is made up of a philosophical world view, a research design, and research methods ..."

A research scheme consists of:

- Philosophical worldview
- Research design
- Research methods

The research question:
What are the main concepts and relations that make up a research methodology that will guide and support students in their undestanding of the domain?

"What are the main concepts and relations that make up a research methodology ... ?"

section 2
A review of the field of ontologies and ontology engineering.
section 3
The research methodology domain and its conceptualisation will then be described.
section 4
conclusions will be drawn and pointer s to future work outlined.

## Section 2: Ontologies and ontology engineering

1. "Semantic" refers to the meaning of the data that is explicitly represented, and this meaning is transferred along with the data.
2. The individual facts or peces of data are linked in a network of information.

Ontologies in Education

the way to resource disocovery, a primary purpose of the Dublin Core standard.

An ontology provides structure to data by providing a shared, formal, and explicit conceptual model of a domain and allows a common understanding of data by providing a controlled and limited vocabulary that defines the concepts of a particular domain rigorously as we ll as defining the relationships among them.

"An ontology provides structure to data by providing a shared, formal, and explicit cenceptual model of a domain ..."

An Ontology Enginnering Approach

### Specification

The purpose of the ontology is to be a content- and communication-oriented ontology that decribes the research methodology field/domain

### Cenceptualisation
### Implementation

Figure 1: An ontology development process map
Ontology development process
- Specification
  - Identify stakeholders
  - Define purpse, goals, and requirements
  - Outline knowledge sources
  - Delimit scope and granularity
  - Plan quality assurance
  - Propse competence test
- Conceptualisation
  - Generate vocabulary
  - Formulate concepts
  - Define properties, relations, axioms
- Impelmentation

Research methodology / research scheme

Sage Research Methods Online (SRMO) http://srmo.sagepub.com

概念モデルのモデリング文法としてUMLを使用する

「研究方法論」という用語と「研究計画」という用語の意味

研究をより大きな科学的探求の体型の中に位置づけ、特定の研究デザインを研究に適用すべき理由、方法、理由を説明し、適切な方法を採用することを決定し記述するという観点から、研究を実施する全体的な正当性、こんきょ、論理を意味するものと解釈される

研究計画
研究方法論に含まれる概念を記述する構造であり、提案された全体的な方法論のニーズを満たすための特定のアプローチや方法(方法論とは対照的に)の選択を網羅するもの
したがって、研究計画は研究の基盤となる哲学的世界観、研究の構造を提供する研究設計、及び設計で使用される研究方法から構成されます。

"A research scheme ... is a structure that describes the concepts that are included in a research methodology ..."

単一の哲学的世界観
一つ以上の研究デザイン
研究方法

Paper
  has Discipline
  has Field
  has MethodologyProfile

MethodologyProfile
  has ResearchDesign
  has DataGenerationMethod
  has TechnicalMethod
  has Task
  has Data
  has Evaluation

---
Input:
  Attention Is All You Need

Output:
  Discipline:
    - Computer Science

  Field:
    - Natural Language Processing
    - Machine Learning

  MethodologyProfile:
    has ResearchDesign:
      - design and creation
      - experiment

    has DataGenerationMethod:
      - documents

    has TechnicalMethod:
      - Transformer

    has Task:
      - machine translation

    has Data:
      - WMT 2014 English-German dataset
      - WMT 2014 English-French dataset

    has Evaluation:
      - BLEU score

1. What is it about?
2. What part of my project does it support?
3. What does it not solve?
4. How will I use it?
5. Useful terms / concepts:
6. One or two key quotes or page references:

- How do Pilkington and Pretorius model the research methodology domain?
- What parts are included in their research scheme?
- How do they explain research design?
- How do they explain research methods?
- Does this support treating methodology as a structure, not one label?
- Can their model be used directly for NLP extraction?
- What does their work not solve for my project?
