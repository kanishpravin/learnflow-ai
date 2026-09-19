from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field


class TeachBackEvaluation(BaseModel):
    understanding: Literal["mastered", "partial", "gap"]
    score: int = Field(ge=0, le=100)
    likely_gap: str | None = None
    evidence_from_notes: str | None = None
    feedback: str
    targeted_explanation: str | None = None
    follow_up_question: str | None = None


class TeachBackInput(BaseModel):
    topic: str
    notes: str
    teach_back: str
