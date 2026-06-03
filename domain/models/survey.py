from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class SurveyAnswerModel:
    answer: str
    image: Optional[str] = None


@dataclass
class SurveyModel:
    id: str
    question: str
    answers: List[SurveyAnswerModel]
    date: datetime = field(default_factory=datetime.utcnow)
    did_answer: bool = False
