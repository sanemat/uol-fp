from dataclasses import dataclass

from uol_fp.models import DesignType, MethodologyProfile


@dataclass
class ConsistencyResult:
    is_valid: bool
    warnings: list[str]


def check_consistency(profile: MethodologyProfile) -> ConsistencyResult:
    warnings: list[str] = []

    if profile.design == DesignType.EXPERIMENT:
        if not profile.task:
            warnings.append("Experimental paper without Task is weak.")
        if not profile.method:
            warnings.append("Experimental paper without Method is weak.")

    if profile.method and not profile.task:
        warnings.append("Method without Task may be incomplete.")

    if profile.design == DesignType.THEORETICAL and profile.evaluation:
        warnings.append("Theoretical design with Evaluation may be a mismatch.")

    return ConsistencyResult(is_valid=len(warnings) == 0, warnings=warnings)
