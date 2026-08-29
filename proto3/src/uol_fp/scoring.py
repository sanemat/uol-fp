from typing import Callable

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


def score_role_multi(
    gold: str | None, sys_answers: list[str]
) -> tuple[int, int, int, int]:
    """Return (tp, fp, fn, tn) for one (paper, role) slot, pilot multi-valued
    variant: sys_answers is a list of candidate answers (e.g. from
    MultiValuedRoleExtraction); a match against gold at any list position
    counts as a hit, same semantics as score_role otherwise."""
    if gold is None:
        if not sys_answers:
            return (0, 0, 0, 1)
        return (0, 1, 0, 0)
    if not sys_answers:
        return (0, 0, 1, 0)
    if any(matches(gold, sys) for sys in sys_answers):
        return (1, 0, 0, 0)
    # present but none match: a confident wrong answer costs both precision
    # and recall, same as score_role
    return (0, 1, 1, 0)


def score_role_judged(
    gold: str | None, sys: str | None, judge: Callable[[str, str], bool]
) -> tuple[int, int, int, int]:
    """Like score_role, but the both-present match check is delegated to
    `judge(gold, sys)` (e.g. an LLM-as-judge semantic-equivalence check)
    instead of matches(). Null-handling is identical to score_role. `judge`
    is dependency-injected so this stays testable without a live API."""
    if gold is None:
        if sys is None:
            return (0, 0, 0, 1)
        return (0, 1, 0, 0)
    if sys is None:
        return (0, 0, 1, 0)
    if judge(gold, sys):
        return (1, 0, 0, 0)
    # present but the judge says they don't match: costs both precision and
    # recall, same as score_role
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
