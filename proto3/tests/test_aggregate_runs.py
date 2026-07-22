import importlib.util
import math
from pathlib import Path
from types import ModuleType

SCRIPT_PATH = Path(__file__).resolve().parent.parent / "aggregate_runs.py"


def _load_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("aggregate_runs", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


aggregate_runs = _load_module()


def test_wilson_interval_known_value() -> None:
    # Textbook check: 8/10 successes, 95% Wilson interval is approximately
    # [0.492, 0.943] (Wikipedia "binomial proportion confidence interval").
    lo, hi = aggregate_runs.wilson_interval(8, 10)
    assert math.isclose(lo, 0.492, abs_tol=0.005)
    assert math.isclose(hi, 0.943, abs_tol=0.005)


def test_wilson_interval_zero_trials() -> None:
    assert aggregate_runs.wilson_interval(0, 0) == (0.0, 0.0)


def test_wilson_interval_all_successes_stays_within_bounds() -> None:
    lo, hi = aggregate_runs.wilson_interval(5, 5)
    assert 0.0 <= lo <= hi <= 1.0


def test_aggregate_scores_matches_score_profile() -> None:
    gold = {
        "paper": {
            "TechnicalMethod": "BERT",
            "Task": None,
            "Dataset": "ImageNet",
            "EvaluationMetric": "BLEU",
        }
    }
    results = {
        "paper": {
            "TechnicalMethod": "bert",
            "Task": "GLUE",
            "Dataset": None,
            "EvaluationMetric": "ROUGE",
        }
    }

    totals = aggregate_runs.aggregate_scores(results, gold)

    assert totals["TechnicalMethod"] == (1, 0, 0, 0)
    assert totals["Task"] == (0, 1, 0, 0)
    assert totals["Dataset"] == (0, 0, 1, 0)
    assert totals["EvaluationMetric"] == (0, 1, 1, 0)


def test_aggregate_scores_sums_across_papers() -> None:
    gold = {
        "a": {
            "TechnicalMethod": "BERT",
            "Task": None,
            "Dataset": None,
            "EvaluationMetric": None,
        },
        "b": {
            "TechnicalMethod": "ResNet",
            "Task": None,
            "Dataset": None,
            "EvaluationMetric": None,
        },
    }
    results = {
        "a": {
            "TechnicalMethod": "bert",
            "Task": None,
            "Dataset": None,
            "EvaluationMetric": None,
        },
        "b": {
            "TechnicalMethod": "wrong",
            "Task": None,
            "Dataset": None,
            "EvaluationMetric": None,
        },
    }

    totals = aggregate_runs.aggregate_scores(results, gold)

    tp, fp, fn, _tn = totals["TechnicalMethod"]
    assert (tp, fp, fn) == (1, 1, 1)
