import pytest
from pydantic import ValidationError

from uol_fp.models import (
    Evidence,
    MultiValuedRoleExtraction,
    ReasoningFirstRoleExtraction,
    RoleAnswer,
    RoleExtraction,
    SameTaskVerdict,
)


def _evidence() -> Evidence:
    return Evidence(section="Abstract", quote="We propose a new architecture.")


def test_role_extraction_both_none() -> None:
    role = RoleExtraction(answer=None, evidence=None)
    assert role.answer is None
    assert role.evidence is None


def test_role_extraction_both_present() -> None:
    role = RoleExtraction(answer="Transformer", evidence=_evidence())
    assert role.answer == "Transformer"
    assert role.evidence == _evidence()


def test_role_extraction_answer_without_evidence_rejected() -> None:
    with pytest.raises(ValidationError):
        RoleExtraction(answer="Transformer", evidence=None)


def test_role_extraction_evidence_without_answer_rejected() -> None:
    with pytest.raises(ValidationError):
        RoleExtraction(answer=None, evidence=_evidence())


def test_multi_valued_role_extraction_empty_list() -> None:
    role = MultiValuedRoleExtraction(answers=[])
    assert role.answers == []


def test_multi_valued_role_extraction_multiple_answers_ordered() -> None:
    role = MultiValuedRoleExtraction(
        answers=[
            RoleAnswer(answer="machine translation", evidence=_evidence()),
            RoleAnswer(answer="sequence transduction", evidence=_evidence()),
        ]
    )
    assert [a.answer for a in role.answers] == [
        "machine translation",
        "sequence transduction",
    ]


def test_role_answer_requires_evidence() -> None:
    with pytest.raises(ValidationError):
        RoleAnswer(answer="Transformer")  # type: ignore[call-arg]


def test_same_task_verdict_true() -> None:
    verdict = SameTaskVerdict(same_task=True)
    assert verdict.same_task is True


def test_same_task_verdict_false() -> None:
    verdict = SameTaskVerdict(same_task=False)
    assert verdict.same_task is False


def test_reasoning_first_both_present() -> None:
    role = ReasoningFirstRoleExtraction(
        reasoning="Candidate 2 is the specific evaluated task; 1 is too broad.",
        answer="machine translation",
        evidence=_evidence(),
    )
    assert role.reasoning.startswith("Candidate 2")
    assert role.answer == "machine translation"
    assert role.evidence == _evidence()


def test_reasoning_first_null_answer_allowed() -> None:
    role = ReasoningFirstRoleExtraction(
        reasoning="No candidate names the task the experiments evaluate.",
        answer=None,
        evidence=None,
    )
    assert role.answer is None
    assert role.evidence is None


def test_reasoning_first_answer_without_evidence_rejected() -> None:
    with pytest.raises(ValidationError):
        ReasoningFirstRoleExtraction(
            reasoning="...", answer="machine translation", evidence=None
        )


def test_reasoning_first_evidence_without_answer_rejected() -> None:
    with pytest.raises(ValidationError):
        ReasoningFirstRoleExtraction(reasoning="...", answer=None, evidence=_evidence())


def test_reasoning_first_requires_reasoning() -> None:
    with pytest.raises(ValidationError):
        ReasoningFirstRoleExtraction(  # type: ignore[call-arg]
            answer="machine translation", evidence=_evidence()
        )


def test_reasoning_first_reasoning_field_is_first() -> None:
    props = list(ReasoningFirstRoleExtraction.model_json_schema()["properties"])
    assert props[0] == "reasoning"
