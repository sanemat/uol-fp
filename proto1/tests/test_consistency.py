from uol_fp.consistency import check_consistency
from uol_fp.models import DesignType, MethodologyProfile


def test_experiment_with_data_and_evaluation_is_valid() -> None:
    profile = MethodologyProfile(
        design=DesignType.EXPERIMENT,
        method=["BERT"],
        data=["MNIST"],
        evaluation=["accuracy"],
    )
    result = check_consistency(profile)
    assert result.is_valid


def test_experiment_missing_data_warns() -> None:
    profile = MethodologyProfile(
        design=DesignType.EXPERIMENT,
        method=["BERT"],
        data=[],
        evaluation=["accuracy"],
    )
    result = check_consistency(profile)
    assert not result.is_valid
    assert any("Data" in w for w in result.warnings)


def test_experiment_missing_evaluation_warns() -> None:
    profile = MethodologyProfile(
        design=DesignType.EXPERIMENT,
        method=["BERT"],
        data=["MNIST"],
        evaluation=[],
    )
    result = check_consistency(profile)
    assert not result.is_valid
    assert any("Evaluation" in w for w in result.warnings)


def test_theoretical_without_data_is_valid() -> None:
    profile = MethodologyProfile(
        design=DesignType.THEORETICAL,
        method=["proof"],
        data=[],
        evaluation=[],
    )
    result = check_consistency(profile)
    assert result.is_valid


def test_method_and_evaluation_without_data_warns() -> None:
    profile = MethodologyProfile(
        design=DesignType.UNKNOWN,
        method=["CNN"],
        data=[],
        evaluation=["F1"],
    )
    result = check_consistency(profile)
    assert not result.is_valid
    assert any("incomplete" in w for w in result.warnings)
