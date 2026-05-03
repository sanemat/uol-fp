import re

from uol_fp.models import DesignType

_PATTERNS: list[tuple[DesignType, list[str]]] = [
    (DesignType.EXPERIMENT, [r"\bexperiment\w*\b", r"\buser study\b", r"\bablation\b"]),
    (
        DesignType.SURVEY,
        [r"\bsurvey\b", r"\bliterature review\b", r"\bsystematic review\b"],
    ),
    (DesignType.CASE_STUDY, [r"\bcase study\b", r"\bcase studies\b"]),
    (DesignType.THEORETICAL, [r"\btheor\w+\b", r"\bproof\b", r"\bformal\w*\b"]),
    (
        DesignType.ALGORITHM_DEVELOPMENT,
        [r"\balgorithm\w*\b", r"\barchitecture\b", r"\bpropose\w*\b", r"\bnovel\b"],
    ),
]


def detect_design(text: str) -> DesignType:
    text_lower = text.lower()
    scores: dict[DesignType, int] = {}
    for design_type, patterns in _PATTERNS:
        count = sum(len(re.findall(p, text_lower)) for p in patterns)
        if count > 0:
            scores[design_type] = count
    if not scores:
        return DesignType.UNKNOWN
    return max(scores, key=lambda k: scores[k])
