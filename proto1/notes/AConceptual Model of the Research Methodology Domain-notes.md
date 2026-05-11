# Why this paper matters
Directly models the problem my project solves: provides a formal UML ontology of research methodology for computing and IS.
Validated by a focus group of 10 senior computing researchers.
Gives an explicit, structured vocabulary that can ground my schema design decisions.

# What it contributes to my project
Three-tier model: Philosophical Worldview → Research Design → Research Methods.
Tables 1–3 enumerate possible values for each concept type — usable as classification targets.
Distinguishes empirical designs (Case Study, Survey, Experiment) from non-empirical (Algorithm Development, Model/Theory Building, Literature Review).
Defines "research method" as atheoretical — the same method (e.g. interview) can appear in any design.
Ontology engineering methodology provides a validation framework I can apply to my own schema.

# Which schema fields it supports
Design — taxonomy of empirical and non-empirical research designs with explicit subtypes.
Method — categorised as qualitative, quantitative, or theoretical; specific types enumerated.
Data — data sources (observed, self-reported, archival, physical) and data formats (text, numeric, video, etc.).
Evaluation — analysis types (thematic analysis, grounded theory, descriptive/inferential statistics).

# What it does not cover
Automated or computational extraction from paper text — purely a conceptual model.
OWL/description-logic implementation — noted as future work.
Non-computing domains — explicitly scoped to computing and IS.
Hybrid or mixed-method studies with partial or overlapping designs.

# Useful definitions
Research scheme = structure made up of philosophical worldview + research design + research methods.
Research methodology = overall justification and rationale for which designs and methods are used and why.
Philosophical worldview = fundamental beliefs about reality and truth; underpins what is studied and how.
Research design = overall kind of study; provides structure for the entire research process.
Research method = tool or instrument used to gather data; atheoretical — can be used in any design.
Empirical design = based on data collection (Case Study, Survey, Experiment).
Non-empirical design = theoretical work (Algorithm Development, Model/Theory Building, Literature Review).
Ontology = shared formal explicit conceptual model providing controlled vocabulary and defining relationships.

# Useful evaluation method
Ontology engineering validation approach used in the paper itself:
- Specification: identify scope, stakeholders, competence questions
- Conceptualization: define concepts, attributes, relations
- Validation: focus group of domain experts reviews for clarity, completeness, acceptance
Competence questions: "Which methods are used by a particular design?" / "What are a design's assumptions?"

# Important quotes or sections
"All research is based on some (albeit sometimes undeclared and implicit) philosophical world view."
"A research scheme is thus made up of a philosophical world view which underpins the research, a research design which provides the structure of the research, and research methods that are used in a design."
"The methods themselves are atheoretical and do not have philosophical or methodological assumptions (and can thus be used in various research designs), and it is why they are chosen, and how they are applied, that is linked to such assumptions."
Tables 1–3 provide explicit enumeration of possible values for each concept type — use as classification targets.

# Risk of misusing this paper
Scoped to computing and IS; does not claim to cover all research disciplines.
Acknowledged simplification — real researchers use hybrid and adapted methodologies not captured in the model.
OWL implementation not provided; the model is conceptual, not an executable ontology.
Focus group was 10 researchers — small validation sample.
Do not treat the taxonomy as exhaustive when classifying papers from adjacent fields.
