from dataclasses import dataclass, field
from enum import Enum


class DesignType(str, Enum):
    EXPERIMENT = "experiment"
    SURVEY = "survey"
    CASE_STUDY = "case_study"
    THEORETICAL = "theoretical"
    ALGORITHM_DEVELOPMENT = "algorithm_development"
    UNKNOWN = "unknown"


@dataclass
class MethodologyProfile:
    design: DesignType = DesignType.UNKNOWN
    method: list[str] = field(default_factory=list)
    data: list[str] = field(default_factory=list)
    evaluation: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "Design": self.design.value,
            "Method": self.method,
            "Data": self.data,
            "Evaluation": self.evaluation,
        }
