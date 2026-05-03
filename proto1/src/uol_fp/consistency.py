from dataclasses import dataclass

from uol_fp.models import DesignType, MethodologyProfile


@dataclass
class ConsistencyResult:
    is_valid: bool
    warnings: list[str]


def check_consistency(profile: MethodologyProfile) -> ConsistencyResult:
    warnings: list[str] = []

    if profile.design == DesignType.EXPERIMENT:
        if not profile.data:
            warnings.append("Experimental paper should have Data.")
        if not profile.evaluation:
            warnings.append("Experimental paper should have Evaluation.")

    if profile.design == DesignType.SURVEY:
        if not profile.data:
            warnings.append("Survey paper should have Data.")

    if profile.method and profile.evaluation and not profile.data:
        warnings.append("Method + Evaluation without Data may be incomplete.")

    return ConsistencyResult(is_valid=len(warnings) == 0, warnings=warnings)
