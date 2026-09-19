from __future__ import annotations

from types import SimpleNamespace

from slice import callback
from slice.llm import complete
from slice.records import RunState

from .evaluator import evaluate_answer
from .schema import HumanCheck, StudentTopicState

MAX_CYCLES = 3
MAX_REVISIONS = 2


def build_flow(call=complete):
    """Build the LearnFlow state machine."""

    def handle_drafting(ctx) -> RunState:
        data = ctx.latest("input")
        follow_up = ctx.latest("follow_up_quiz")

        # A follow-up answer resumes directly at DRAFTING.
        if follow_up:
            expert_answer = ctx.latest("expert_answer")
            question = follow_up["question"]
            student_answer = expert_answer["answer"] if expert_answer else ""

            ctx.append(
                "follow_up_answer",
                {
                    "answer": student_answer,
                    "attempt_number": len(ctx.history("quiz_attempt")) + 1,
                },
                produced_by="system",
            )
        else:
            question = data["question"]
            student_answer = data["student_answer"]

        attempt = evaluate_answer(
            settings=ctx.settings,
            budget=ctx.budget,
            topic=data["topic"],
            notes=data["notes"],
            question=question,
            student_answer=student_answer,
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
        attempt_records = ctx.history("quiz_attempt")
        attempts = [record.payload for record in attempt_records]
        human_checks = [
            record.payload for record in ctx.history("human_check")
        ]

        if attempt["mastery"]:
            state = StudentTopicState(
                topic=ctx.latest("input")["topic"],
                attempts=attempts,
                human_checks=human_checks,
                mastered=True,
            )

            ctx.append(
                "student_topic_state",
                state.model_dump(),
                produced_by="system",
            )

            return RunState.COMPLETE

        revision_count = max(0, len(attempt_records) - 1)

        if (
            len(attempt_records) >= MAX_CYCLES
            or revision_count >= MAX_REVISIONS
        ):
            state = StudentTopicState(
                topic=ctx.latest("input")["topic"],
                attempts=attempts,
                human_checks=human_checks,
                mastered=False,
            )

            ctx.append(
                "student_topic_state",
                state.model_dump(),
                produced_by="system",
            )

            return RunState.FAILED

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

    def handle_probing(ctx) -> RunState:
        attempt = ctx.latest("quiz_attempt")
        expert_answer = ctx.latest("expert_answer")

        # A timeout stores answer=None, which must become no_response.
        response = (
            expert_answer["answer"]
            if expert_answer
            and expert_answer["answer"] in ("confirmed", "rejected")
            else "no_response"
        )

        ctx.append(
            "human_check",
            HumanCheck(
                attempt_number=attempt["attempt_number"],
                response=response,
            ).model_dump(),
            produced_by="system",
        )

        ctx.append(
            "explanation",
            {
                "topic": ctx.latest("input")["topic"],
                "likely_gap": attempt["likely_gap"],
                "evidence": attempt["evidence"],
                "text": (
                    f"The concept gap identified is: {attempt['likely_gap']}\n"
                    f"Evidence from notes: {attempt['evidence']}\n"
                    "Please review this carefully before answering "
                    "the follow-up question."
                ),
            },
            produced_by="agent:explanation",
        )

        ctx.append(
            "follow_up_quiz",
            {
                "question": (
                    "A 12 V battery is connected to a 4 Ω resistor. "
                    "What current flows?"
                ),
                "likely_gap": attempt["likely_gap"],
            },
            produced_by="agent:quiz_generator",
        )

        callback.ask(
            ctx.store,
            ctx.run_id,
            question=(
                "Please answer this follow-up question:\n\n"
                f"{attempt['likely_gap']}\n\n"
                "What is your answer?"
            ),
            context={
                "resume_state": RunState.DRAFTING.value,
                "attempt_number": attempt["attempt_number"] + 1,
            },
            settings=ctx.settings,
        )

        return RunState.AWAITING_EXPERT

    return SimpleNamespace(
        name="learnflow",
        handlers={
            RunState.DRAFTING: handle_drafting,
            RunState.GATING: handle_gating,
            RunState.PROBING: handle_probing,
        },
    )


flow = build_flow()