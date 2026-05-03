from uol_fp.design_detector import detect_design
from uol_fp.models import DesignType


def test_detects_experiment() -> None:
    text = "We conducted an experiment to evaluate our method."
    assert detect_design(text) == DesignType.EXPERIMENT


def test_detects_survey() -> None:
    text = "We performed a systematic review of the literature."
    assert detect_design(text) == DesignType.SURVEY


def test_detects_case_study() -> None:
    text = "We present a case study of applying the method."
    assert detect_design(text) == DesignType.CASE_STUDY


def test_detects_theoretical() -> None:
    text = "We provide a theoretical analysis and formal proof."
    assert detect_design(text) == DesignType.THEORETICAL


def test_detects_algorithm_development() -> None:
    text = "We propose a novel algorithm for text classification."
    assert detect_design(text) == DesignType.ALGORITHM_DEVELOPMENT


def test_unknown_for_empty_text() -> None:
    assert detect_design("") == DesignType.UNKNOWN
