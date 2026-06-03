from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class SurveyResultAnswerModel:
    answer: str
    count: int
    percent: int
    is_current_account_answer: bool = False
    image: Optional[str] = None


@dataclass
class SurveyResultModel:
    survey_id: str
    id: Optional[str] = None
    account_id: Optional[str] = None
    answer: Optional[str] = None
    question: str = ""
    answers: List[SurveyResultAnswerModel] = field(default_factory=list)
    date: datetime = field(default_factory=datetime.utcnow)
