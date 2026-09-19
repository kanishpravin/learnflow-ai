from __future__ import annotations

from .evaluator import evaluate_answer

from enum import Enum

from .schema import HumanCheck, QuizAttempt, StudentTopicState


class State(str, Enum):
    TOPIC_READY = "TOPIC_READY"
    ANSWER_RECEIVED = "ANSWER_RECEIVED"
    EVALUATING = "EVALUATING"
    HUMAN_CONFIRMATION = "HUMAN_CONFIRMATION"
    TARGETED_EXPLANATION = "TARGETED_EXPLANATION"
    FOLLOW_UP_QUIZ = "FOLLOW_UP_QUIZ"
    MASTERED = "MASTERED"
    UNRESOLVED = "UNRESOLVED"


MAX_CYCLES = 3
MAX_REVISIONS = 2


class LearnFlowAgent:
    def __init__(self, topic: str, notes: str, settings=None, budget=None):
        self.topic = topic
        self.notes = notes
        self.settings = settings
        self.budget = budget
        self.state = State.TOPIC_READY
        self.attempts: list[QuizAttempt] = []
        self.human_checks: list[HumanCheck] = []
        self.mastered = False
        self.cycle_count = 0
        self.revision_count = 0

    def receive_answer(self, question: str, answer: str) -> None:
        self.question = question
        self.student_answer = answer
        self.state = State.ANSWER_RECEIVED

    def evaluate(self) -> QuizAttempt:
        self.state = State.EVALUATING
        self.cycle_count += 1

        if self.settings is not None and self.budget is not None:
            attempt = evaluate_answer(
                settings=self.settings,
                budget=self.budget,
                topic=self.topic,
                notes=self.notes,
                question=self.question,
                student_answer=self.student_answer,
                attempt_number=len(self.attempts) + 1,
        )

            self.attempts.append(attempt)

            if attempt.mastery:
                self.mastered = True
                self.state = State.MASTERED
            else:
                self.state = State.HUMAN_CONFIRMATION

            return attempt

        correct = self.student_answer.strip() == "3 A"

        if correct:
            attempt = QuizAttempt(
                attempt_number=len(self.attempts) + 1,
                question=self.question,
                student_answer=self.student_answer,
                correct=True,
                likely_gap=None,
                evidence="Ohm's Law is V = IR, therefore I = V/R.",
                mastery=True,
            )
            self.mastered = True
            self.state = State.MASTERED
        else:
            attempt = QuizAttempt(
                attempt_number=len(self.attempts) + 1,
                question=self.question,
                student_answer=self.student_answer,
                correct=False,
                likely_gap="confusing multiplication with division in V = IR",
                evidence="Ohm's Law is V = IR, therefore I = V/R.",
                mastery=False,
            )
            self.state = State.HUMAN_CONFIRMATION

        self.attempts.append(attempt)
        return attempt

    def confirm_diagnosis(self, response: str) -> HumanCheck:
        check = HumanCheck(
            attempt_number=len(self.attempts),
            response=response,
        )
        self.human_checks.append(check)

        self.state = State.TARGETED_EXPLANATION
        return check

    def explain(self) -> str:
        self.state = State.TARGETED_EXPLANATION

        return (
            "Ohm's Law is V = IR. To find current, rearrange the equation "
            "to I = V/R. For a 12 V battery and a 4 Ω resistor, "
            "I = 12/4 = 3 A."
        )

    def generate_follow_up(self) -> str:
        self.state = State.FOLLOW_UP_QUIZ

        return (
            "A 12 V battery is connected to a 4 Ω resistor. "
            "What current flows?"
        )

    def handle_follow_up(self, answer: str) -> None:
        self.receive_answer(
            "A 12 V battery is connected to a 4 Ω resistor. "
            "What current flows?",
            answer,
        )

        if self.revision_count >= MAX_REVISIONS:
            self.state = State.UNRESOLVED
            return

        self.evaluate()

        if self.state != State.MASTERED:
            self.revision_count += 1

    def topic_state(self) -> StudentTopicState:
        return StudentTopicState(
            topic=self.topic,
            attempts=self.attempts,
            human_checks=self.human_checks,
            mastered=self.mastered,
        )