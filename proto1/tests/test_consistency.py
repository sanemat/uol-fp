from uol_fp.consistency import check_consistency
from uol_fp.models import DesignType, MethodologyProfile


def test_experiment_with_method_and_task_is_valid() -> None:
    profile = MethodologyProfile(
        design=DesignType.EXPERIMENT,
        method=["BERT"],
        task=["question answering"],
    )
    result = check_consistency(profile)
    assert result.is_valid


def test_experiment_missing_task_warns() -> None:
    profile = MethodologyProfile(
        design=DesignType.EXPERIMENT,
        method=["BERT"],
        task=[],
    )
    result = check_consistency(profile)
    assert not result.is_valid
    assert any("Task" in w for w in result.warnings)


def test_experiment_missing_method_warns() -> None:
    profile = MethodologyProfile(
        design=DesignType.EXPERIMENT,
        task=["image classification"],
    )
    result = check_consistency(profile)
    assert not result.is_valid
    assert any("Method" in w for w in result.warnings)


def test_method_without_task_warns() -> None:
    profile = MethodologyProfile(
        design=DesignType.UNKNOWN,
        method=["CNN"],
        task=[],
    )
    result = check_consistency(profile)
    assert not result.is_valid
    assert any("incomplete" in w for w in result.warnings)


def test_theoretical_with_evaluation_warns() -> None:
    profile = MethodologyProfile(
        design=DesignType.THEORETICAL,
        evaluation=["accuracy"],
    )
    result = check_consistency(profile)
    assert not result.is_valid
    assert any("mismatch" in w for w in result.warnings)


def test_theoretical_without_evaluation_is_valid() -> None:
    profile = MethodologyProfile(
        design=DesignType.THEORETICAL,
        method=["proof"],
        task=["formal verification"],
    )
    result = check_consistency(profile)
    assert result.is_valid
