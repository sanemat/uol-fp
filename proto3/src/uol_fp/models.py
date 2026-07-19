from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

ROLES = ["TechnicalMethod", "Task", "Dataset", "EvaluationMetric"]


class Evidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    section: str = Field(description="Exact section heading containing the quote.")
    quote: str = Field(
        description="One sentence quoted verbatim from the paper, supporting answer."
    )


class RoleExtraction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answer: str | None = Field(
        description="Shortest identifying term (e.g. 'Transformer'), or null if absent."
    )
    evidence: Evidence | None = Field(
        description="Evidence supporting the answer, or null when not present."
    )

    @model_validator(mode="after")
    def answer_and_evidence_must_match(self) -> Self:
        if (self.answer is None) != (self.evidence is None):
            raise ValueError(
                "answer and evidence must either both be null or both be present"
            )
        return self


class MethodologyProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    TechnicalMethod: RoleExtraction
    Task: RoleExtraction
    Dataset: RoleExtraction
    EvaluationMetric: RoleExtraction
