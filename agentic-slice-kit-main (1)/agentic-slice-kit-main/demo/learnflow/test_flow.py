from demo.learnflow.evaluator import evaluate_answer


class DummyBudget:
    pass


result = evaluate_answer(
    settings=None,
    budget=DummyBudget(),
    topic="Ohm's Law",
    notes="Ohm's Law is V = IR. Therefore, I = V/R.",
    question="A 12 V battery is connected to a 4 Ω resistor. What current flows?",
    student_answer="48 A",
    attempt_number=1,
)

print(result.model_dump())