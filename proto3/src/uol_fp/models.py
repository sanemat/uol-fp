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


class RoleAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answer: str = Field(description="Shortest identifying term for this valid answer.")
    evidence: Evidence = Field(description="Evidence supporting this specific answer.")


class MultiValuedRoleExtraction(BaseModel):
    """Pilot: a role that may legitimately have more than one valid answer at
    different granularities (e.g. a paper's broad self-description vs. the
    specific benchmark it evaluates on) -- see proto3/memo.md "Architecture
    reconsideration" result note (2026-08-29)."""

    model_config = ConfigDict(extra="forbid")

    answers: list[RoleAnswer] = Field(
        description=(
            "One or more valid answers for this role, ordered primary "
            "(most specific / directly evaluated) first. Empty list if the "
            "role is not present in the paper."
        )
    )


class SameTaskVerdict(BaseModel):
    """LLM-as-judge output for `uol_fp.scoring.score_role_judged`'s `judge`
    argument -- semantic-equivalence check between a gold answer and a system
    answer, allowing different specificity or wording. See proto3/memo.md
    "Multi-valued roles" for the design rationale (2026-08-29)."""

    model_config = ConfigDict(extra="forbid")

    same_task: bool = Field(
        description=(
            "True if the two phrases refer to the same task or concept, "
            "even if worded differently or at a different level of "
            "specificity. False if they describe genuinely different tasks."
        )
    )
