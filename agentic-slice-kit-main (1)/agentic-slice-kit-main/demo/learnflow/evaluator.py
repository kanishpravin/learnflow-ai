from __future__ import annotations

from slice.llm import complete

from .schema import QuizAttempt


def evaluate_answer(
    *,
    settings,
    budget,
    topic: str,
    notes: str,
    question: str,
    student_answer: str,
    attempt_number: int,
) -> QuizAttempt:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a learning evaluator. "
                "Evaluate the student's answer using only the supplied topic "
                "notes and question. Identify whether the answer is correct. "
                "If incorrect, identify the most likely concept gap and provide "
                "brief evidence from the notes. Decide whether mastery is "
                "demonstrated. Return only the required structured object."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Topic:\n{topic}\n\n"
                f"Notes:\n{notes}\n\n"
                f"Question:\n{question}\n\n"
                f"Student answer:\n{student_answer}\n\n"
                f"Attempt number:\n{attempt_number}"
            ),
        },
    ]

    return complete(
        settings=settings,
        budget=budget,
        messages=messages,
        schema=QuizAttempt,
        step="learnflow_evaluate",
    )