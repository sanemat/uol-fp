from uol_fp.scoring import (
    ROLES,
    matches,
    normalize,
    precision_recall_f1,
    score_profile,
    score_role,
    score_role_judged,
    score_role_multi,
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


def test_score_role_multi_both_absent() -> None:
    assert score_role_multi(None, []) == (0, 0, 0, 1)


def test_score_role_multi_gold_only() -> None:
    assert score_role_multi("BERT", []) == (0, 0, 1, 0)


def test_score_role_multi_sys_only() -> None:
    assert score_role_multi(None, ["BERT"]) == (0, 1, 0, 0)


def test_score_role_multi_first_answer_matches() -> None:
    assert score_role_multi("machine translation", ["machine translation"]) == (
        1,
        0,
        0,
        0,
    )


def test_score_role_multi_second_answer_matches() -> None:
    # Transformer's Task case: primary answer "sequence transduction" misses
    # gold "machine translation", but a secondary answer at a different
    # granularity would hit -- this is the case the pilot targets.
    assert score_role_multi(
        "machine translation", ["sequence transduction", "machine translation"]
    ) == (1, 0, 0, 0)


def test_score_role_multi_no_answer_matches() -> None:
    assert score_role_multi("BERT", ["ResNet", "AlexNet"]) == (0, 1, 1, 0)


def test_score_role_judged_both_none() -> None:
    assert score_role_judged(None, None, judge=lambda g, s: True) == (0, 0, 0, 1)


def test_score_role_judged_gold_only() -> None:
    assert score_role_judged("BERT", None, judge=lambda g, s: True) == (0, 0, 1, 0)


def test_score_role_judged_sys_only() -> None:
    assert score_role_judged(None, "BERT", judge=lambda g, s: True) == (0, 1, 0, 0)


def test_score_role_judged_judge_says_match() -> None:
    # Same pair score_role would call a mismatch (no substring overlap), but
    # the injected judge says they're semantically the same task.
    assert score_role_judged(
        "distributed", "processing large data sets", judge=lambda g, s: True
    ) == (1, 0, 0, 0)


def test_score_role_judged_judge_says_no_match() -> None:
    assert score_role_judged("BERT", "ResNet", judge=lambda g, s: False) == (
        0,
        1,
        1,
        0,
    )


def test_score_role_judged_receives_gold_and_sys() -> None:
    seen = []
    score_role_judged("gold", "sys", judge=lambda g, s: seen.append((g, s)) or True)
    assert seen == [("gold", "sys")]


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
