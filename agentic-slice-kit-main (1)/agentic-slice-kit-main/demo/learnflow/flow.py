from __future__ import annotations

from types import SimpleNamespace

from slice import callback
from slice.llm import complete
from slice.records import RunState

from .evaluator import evaluate_answer
from .schema import HumanCheck, QuizAttempt, StudentTopicState

MAX_CYCLES = 3
MAX_REVISIONS = 2


def build_flow(call=complete):
    """Build the LearnFlow state machine."""

    def handle_drafting(ctx) -> RunState:
        data = ctx.latest("input")

        attempt = evaluate_answer(
            settings=ctx.settings,
            budget=ctx.budget,
            topic=data["topic"],
            notes=data["notes"],
            question=data["question"],
            student_answer=data["student_answer"],
            attempt_number=len(ctx.history("quiz_attempt")) + 1,
        )

        ctx.append(
            "quiz_attempt",
            attempt.model_dump(),
            produced_by="agent:evaluator",
        )

        return RunState.GATING

    def handle_gating(ctx) -> RunState:
        attempt = ctx.latest("quiz_attempt")

        if attempt["mastery"]:
            ctx.append(
                "student_topic_state",
                {
                    "topic": ctx.latest("input")["topic"],
                    "attempts": [attempt],
                    "human_checks": [],
                    "mastered": True,
                },
                produced_by="system",
            )
            return RunState.COMPLETE

        callback.ask(
            ctx.store,
            ctx.run_id,
            question=(
                "Do you confirm the evaluator's diagnosis of the student's "
                f"concept gap: {attempt['likely_gap']}?"
            ),
            context={
                "resume_state": RunState.PROBING.value,
                "attempt_number": attempt["attempt_number"],
                "likely_gap": attempt["likely_gap"],
                "evidence": attempt["evidence"],
            },
            settings=ctx.settings,
        )

        return RunState.AWAITING_EXPERT

    def handle_human_confirmation(ctx) -> RunState:
        question = callback.pending(ctx.store, ctx.run_id)

        if question:
            return RunState.AWAITING_EXPERT

        return RunState.DRAFTING

    def handle_probing(ctx) -> RunState:
        attempt = ctx.latest("quiz_attempt")

        ctx.append(
            "explanation",
            {
                "topic": ctx.latest("input")["topic"],
                "likely_gap": attempt["likely_gap"],
                "evidence": attempt["evidence"],
                "text": (
                    "Review the identified concept gap before attempting "
                    "the follow-up question."
                ),
            },
            produced_by="agent:explanation",
        )

        return RunState.PROBING

    return SimpleNamespace(
        name="learnflow",
        handlers={
            RunState.DRAFTING: handle_drafting,
            RunState.GATING: handle_gating,
            RunState.AWAITING_EXPERT: handle_human_confirmation,
            RunState.PROBING: handle_probing,
        },
    )