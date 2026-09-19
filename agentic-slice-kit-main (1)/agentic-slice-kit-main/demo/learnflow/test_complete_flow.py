"""
Complete LearnFlow test: initial wrong answer → human confirmation →
follow-up generated → correct answer → mastery detected.
"""

from slice import callback
from slice.config import settings
from slice.records import RunState
from slice.runner import advance
from slice.store import Store

from demo.learnflow.flow import flow


def test_complete_flow_wrong_then_right():
    store = Store(":memory:")
    run_id = store.create_run(domain="learnflow")
    test_settings = settings()

    # Student submits an incorrect first answer.
    store.append(
        run_id,
        "input",
        {
            "topic": "Ohm's Law",
            "notes": (
                "Ohm's Law: I = V/R, where I is current, "
                "V is voltage, R is resistance."
            ),
            "question": (
                "A 12 V battery is connected to a 4 Ω resistor. "
                "What current flows?"
            ),
            "student_answer": "48 A",
        },
        produced_by="user",
    )

    store.set_state(run_id, RunState.DRAFTING)

    # First evaluation should request diagnosis confirmation.
    state = advance(store, run_id, flow, test_settings)

    assert state == RunState.AWAITING_EXPERT

    pending_questions = callback.pending(store, run_id)
    assert len(pending_questions) == 1

    diagnosis_question = pending_questions[0]
    assert (
        "concept gap" in diagnosis_question.question.lower()
        or "confirm" in diagnosis_question.question.lower()
    )

    first_attempt = store.latest(run_id, "quiz_attempt")
    assert first_attempt["correct"] is False
    assert first_attempt["mastery"] is False
    assert first_attempt["likely_gap"] is not None

    # Student confirms the diagnosis.
    callback.answer(store, diagnosis_question.id, "confirmed")

    # The system creates an explanation and asks the follow-up question.
    state = advance(store, run_id, flow, test_settings)

    assert state == RunState.AWAITING_EXPERT

    explanation = store.latest(run_id, "explanation")
    assert explanation is not None
    assert explanation["likely_gap"] == first_attempt["likely_gap"]

    follow_up = store.latest(run_id, "follow_up_quiz")
    assert follow_up is not None
    assert follow_up["question"]

    pending_questions = callback.pending(store, run_id)
    assert len(pending_questions) == 1

    follow_up_question = pending_questions[0]
    assert "answer" in follow_up_question.question.lower()

    # Student answers the follow-up correctly.
    callback.answer(store, follow_up_question.id, "3 A")

    # The system evaluates the follow-up and marks the topic complete.
    state = advance(store, run_id, flow, test_settings)

    assert state == RunState.COMPLETE

    # Store history returns Version objects, so read each record's payload.
    attempts = store.history(run_id, "quiz_attempt")
    assert len(attempts) == 2

    second_attempt = attempts[1].payload
    assert second_attempt["correct"] is True
    assert second_attempt["mastery"] is True
    assert second_attempt["student_answer"] == "3 A"

    final_state = store.latest(run_id, "student_topic_state")
    assert final_state["topic"] == "Ohm's Law"
    assert final_state["mastered"] is True
    assert len(final_state["attempts"]) == 2
    assert len(final_state["human_checks"]) == 1

    checks = store.history(run_id, "human_check")
    assert len(checks) == 1
    assert checks[0].payload["response"] == "confirmed"


if __name__ == "__main__":
    test_complete_flow_wrong_then_right()
    print("✓ Complete LearnFlow flow test passed")