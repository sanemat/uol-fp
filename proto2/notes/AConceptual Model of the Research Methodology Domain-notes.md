ResearchScheme
  has PhilosophicalWorldview
  has ResearchDesign
  has ResearchMethod

## Section 1: Introduction

an ontology of the research methodology domain

"A research scheme that is made up of a philosophical world view, a research design, and research methods ..."

A research scheme consists of:

- Philosophical worldview
- Research design
- Research methods

The research question:
What are the main concepts and relations that make up a research methodology that will guide and support students in their understanding of the domain?

"What are the main concepts and relations that make up a research methodology ... ?"

section 2
A review of the field of ontologies and ontology engineering.
section 3
The research methodology domain and its conceptualisation will then be described.
section 4
conclusions will be drawn and pointers to future work outlined.

## Section 2: Ontologies and ontology engineering

1. "Semantic" refers to the meaning of the data that is explicitly represented, and this meaning is transferred along with the data.
2. The individual facts or pieces of data are linked in a network of information.

Ontologies in Education

the way to resource discovery, a primary purpose of the Dublin Core standard.

An ontology provides structure to data by providing a shared, formal, and explicit conceptual model of a domain and allows a common understanding of data by providing a controlled and limited vocabulary that defines the concepts of a particular domain rigorously as well as defining the relationships among them.

"An ontology provides structure to data by providing a shared, formal, and explicit conceptual model of a domain ..."

An Ontology Engineering Approach

### Specification

The purpose of the ontology is to be a content- and communication-oriented ontology that describes the research methodology field/domain

### Conceptualisation
### Implementation

Figure 1: An ontology development process map
Ontology development process
- Specification
  - Identify stakeholders
  - Define purpose, goals, and requirements
  - Outline knowledge sources
  - Delimit scope and granularity
  - Plan quality assurance
  - Propose competence test
- Conceptualisation
  - Generate vocabulary
  - Formulate concepts
  - Define properties, relations, axioms
- Implementation

Research methodology / research scheme

A UML conceptual model can be transferred directly to OWL

## Section 3: A Conceptual model of the research methodology domain

Sage Research Methods Online (SRMO) http://srmo.sagepub.com

the Ontology of Clinical Research (OCRe)

Conceptual models for humans before making an ontology.

Research methodology has been used in various ways in the literature, from being a synonym for a research design, to being the research process, to being the specific implementation of the methods. Here it is taken to mean the overall justification, rationale, or logic for undertaking the research in terms of locating it within the larger body of scientific enquiry, explaining which, how, and why particular research designs should be applied in the research, and deciding and describing which appropriate methods will be employed.

A research scheme ... is a structure that describes the concepts that are included in a research methodology, and covers the choice of particular approaches and methods to meet the needs of the proposed overall methodology.
A research scheme is thus made up of a philosophical world view which underpins the research, a research design which provides the structure of the research, and research methods that are used in a design.

"A research scheme ... is a structure that describes the concepts that are included in a research methodology ..."

The ResearchScheme is
- underpinned by a single PhilosophicalWorldview
- has one or more ResearchDesigns

Common examples of philosophical world views include post-positivism, constructivisum, transformative/critical theory, pnterpretivism, and pragmatism.
There is also reference to qualitative and quantative paradigms in the literature on reserach methodologies.

Paper
  has Discipline
  has Field
  has MethodologyProfile

MethodologyProfile
  has ResearchDesign
  has DataGenerationMethod
  has TechnicalMethod
  has Task
  has Dataset
  has EvaluationMetric

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

    has Dataset:
      - WMT 2014 English-German dataset
      - WMT 2014 English-French dataset

    has EvaluationMetric:
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
