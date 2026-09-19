from __future__ import annotations

from pydantic import BaseModel


class QuizAttempt(BaseModel):
    attempt_number: int
    question: str
    student_answer: str
    correct: bool
    likely_gap: str | None
    evidence: str | None
    mastery: bool


class HumanCheck(BaseModel):
    attempt_number: int
    response: str  # confirmed, rejected, or no_response


class StudentTopicState(BaseModel):
    topic: str
    attempts: list[QuizAttempt]
    human_checks: list[HumanCheck]
    mastered: bool