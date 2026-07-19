from uol_fp.scoring import (
    ROLES,
    matches,
    normalize,
    precision_recall_f1,
    score_profile,
    score_role,
)


def test_normalize_none() -> None:
    assert normalize(None) is None


def test_normalize_lowercases_and_collapses_whitespace() -> None:
    assert normalize("  BERT   Model ") == "bert model"


def test_matches_substring_either_direction() -> None:
    assert matches("BERT", "bert model") is True
    assert matches("bert model", "BERT") is True


def test_matches_no_overlap() -> None:
    assert matches("BERT", "ResNet") is False


def test_score_role_both_none() -> None:
    assert score_role(None, None) == (0, 0, 0, 1)


def test_score_role_gold_only() -> None:
    assert score_role("BERT", None) == (0, 0, 1, 0)


def test_score_role_sys_only() -> None:
    assert score_role(None, "BERT") == (0, 1, 0, 0)


def test_score_role_match() -> None:
    assert score_role("BERT", "bert") == (1, 0, 0, 0)


def test_score_role_mismatch() -> None:
    assert score_role("BERT", "ResNet") == (0, 1, 1, 0)


def test_score_profile_covers_all_roles() -> None:
    gold: dict[str, str | None] = {
        "TechnicalMethod": "BERT",
        "Task": None,
        "Dataset": "ImageNet",
        "EvaluationMetric": "BLEU",
    }
    sys: dict[str, str | None] = {
        "TechnicalMethod": "bert",
        "Task": "GLUE",
        "Dataset": None,
        "EvaluationMetric": "ROUGE",
    }

    result = score_profile(gold, sys)

    assert set(result) == set(ROLES)
    assert result["TechnicalMethod"] == (1, 0, 0, 0)
    assert result["Task"] == (0, 1, 0, 0)
    assert result["Dataset"] == (0, 0, 1, 0)
    assert result["EvaluationMetric"] == (0, 1, 1, 0)


def test_precision_recall_f1_normal_case() -> None:
    assert precision_recall_f1(3, 1, 1) == (0.75, 0.75, 0.75)


def test_precision_recall_f1_zero_tp_fp() -> None:
    assert precision_recall_f1(0, 0, 5) == (0.0, 0.0, 0.0)


def test_precision_recall_f1_zero_tp_fn() -> None:
    assert precision_recall_f1(0, 5, 0) == (0.0, 0.0, 0.0)


def test_precision_recall_f1_all_zero() -> None:
    assert precision_recall_f1(0, 0, 0) == (0.0, 0.0, 0.0)
