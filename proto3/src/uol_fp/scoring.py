ROLES = ["TechnicalMethod", "Task", "Dataset", "EvaluationMetric"]


def normalize(s: str | None) -> str | None:
    if s is None:
        return None
    return " ".join(s.lower().split())


def matches(gold: str, sys: str) -> bool:
    g, s = normalize(gold), normalize(sys)
    assert g is not None and s is not None
    return g in s or s in g


def score_role(gold: str | None, sys: str | None) -> tuple[int, int, int, int]:
    """Return (tp, fp, fn, tn) for one (paper, role) slot."""
    if gold is None:
        if sys is None:
            return (0, 0, 0, 1)
        return (0, 1, 0, 0)
    if sys is None:
        return (0, 0, 1, 0)
    if matches(gold, sys):
        return (1, 0, 0, 0)
    # both present but do not match: a confident wrong answer costs both
    # precision and recall
    return (0, 1, 1, 0)


def score_profile(
    gold_answers: dict[str, str | None], sys_answers: dict[str, str | None]
) -> dict[str, tuple[int, int, int, int]]:
    return {
        role: score_role(gold_answers.get(role), sys_answers.get(role))
        for role in ROLES
    }


def precision_recall_f1(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return precision, recall, f1
