import pytest
from pydantic import ValidationError

from uol_fp.models import (
    Evidence,
    MultiValuedRoleExtraction,
    RoleAnswer,
    RoleExtraction,
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
