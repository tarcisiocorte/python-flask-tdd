from dataclasses import dataclass
from datetime import datetime


@dataclass
class SurveyResultModel:
    """Represents a survey result entity"""
    id: str
    survey_id: str
    account_id: str
    answer: str
    date: datetime

