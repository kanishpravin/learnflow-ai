from slice.config import settings
from slice.store import Store
from slice import callback
from slice.runner import advance

st = settings()
store = Store("learnflow_test.db")
run_id = store.create_run("learnflow")

# 1. Original Input Block
store.append(
    run_id,
    "input",
    {
        "topic": "Ohm's Law",
        "notes": "Ohm's Law states V = I × R, so current is I = V / R.",
        "question": "A 12 V battery is connected to a 4 Ω resistor. What current flows?",
        "student_answer": "48 A",
    },
    produced_by="system",
)

# 2. Quiz Attempt Evaluation
store.append(
    run_id,
    "quiz_attempt",
    {
        "attempt_number": 1,
        "question": "A 12 V battery is connected to a 4 Ω resistor. What current flows?",
        "student_answer": "48 A",
        "correct": False,
        "likely_gap": "multiplication instead of division",
        "evidence": "Ohm's Law is I = V / R.",
        "mastery": False,
    },
    produced_by="agent:evaluator",
)

# 3. Human-in-the-loop Callback
question_id = callback.ask(
    store,
    run_id,
    question="Do you confirm the identified concept gap?",
    context={
        "resume_state": "probing",
        "attempt_number": 1,
        "likely_gap": "multiplication instead of division",
        "evidence": "I = V/R",
    },
    settings=st,
)

print("Question ID:", question_id)

# 4. Record the Follow-Up Answer directly to the callback response 
callback.answer(
    store,
    question_id,
    text="confirmed",
)

print("State:", store.get_state(run_id))

from demo.learnflow.flow import flow

state = advance(
    store,
    run_id,
    flow,
    st,
)

print("After advance:", state)