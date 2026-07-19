import pytest
from pydantic import ValidationError

from uol_fp.models import Evidence, RoleExtraction


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
