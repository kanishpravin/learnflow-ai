LearnFlow AI — Build Progress

## Current status

The core LearnFlow AI agent is complete and working. It supports a stateful learning loop for one topic: evaluate an answer, identify a likely misconception, request human confirmation, deliver a targeted explanation, generate a follow-up question, and decide whether the topic is mastered or unresolved.

## What has been built

- Persistent state machine built on the Agentic Slice Kit runner and SQLite store.
- Structured records for quiz attempts, human checks, and the saved topic state.
- Answer evaluation using the configured model provider and only the supplied topic notes.
- Human-in-the-loop diagnosis confirmation using `confirmed`, `rejected`, or `no_response`.
- Timeout handling: unanswered confirmations are recorded as `no_response`, not guessed.
- Targeted explanation generation based on the detected concept gap and evidence.
- Dynamic follow-up question generation based on the topic, notes, previous question, and gap.
- Mastery completion path after a correct follow-up answer.
- Safety limit: after a maximum of three failed evaluation cycles / two revisions, the run ends as unresolved rather than looping indefinitely.
- Persistent CLI demo script with a saved run ID for later resumption.
- Existing FastAPI callback page can be connected to the same SQLite database for browser-based human answers.

## Key files added or updated

| File | Purpose |
|---|---|
| `demo/learnflow/flow.py` | LearnFlow states, transitions, persistence, human checks, retry limits |
| `demo/learnflow/schema.py` | Typed contracts for attempts, human checks, explanations, and follow-up quizzes |
| `demo/learnflow/evaluator.py` | Evaluates student answers and identifies the likely gap |
| `demo/learnflow/explanation_generator.py` | Produces note-grounded targeted explanations |
| `demo/learnflow/quiz_generator.py` | Produces adaptive follow-up questions |
| `demo/learnflow/run_demo.py` | Starts or resumes a persistent terminal demo |
| `demo/learnflow/test_complete_flow.py` | Tests wrong answer → confirmation → correct follow-up → mastery |
| `demo/learnflow/test_limits.py` | Tests three failed attempts → unresolved stop |
| `demo/learnflow/test_timeout.py` | Tests unanswered confirmation → `no_response` → continued learning flow |

## Verification completed

The following checks passed:

- Complete LearnFlow mastery flow test: **passed**
- Retry-limit / unresolved-path test: **passed**
- Human-timeout / `no_response` test: **passed**
- Full project suite: **74 tests passed**

## Demonstrated flow

Example used during testing:

1. Student enters an Ohm’s Law question and the incorrect answer `48 A`.
2. The evaluator identifies multiplication instead of division as the likely misconception.
3. The student confirms the diagnosis.
4. LearnFlow generates a targeted explanation and a new follow-up question.
5. The student answers the follow-up correctly, for example `3 A` for `12 V / 4 Ω`.
6. The agent stores both attempts, the confirmation, and marks the topic as mastered.

## API-token note

Model calls consume API tokens during evaluation, explanation generation, and follow-up question generation. Editing files and ordinary non-LearnFlow checks do not consume tokens. During development, run the one relevant test file first; run the complete suite only at milestones.

## Remaining work

1. Connect the existing FastAPI callback page to `demo/learnflow/learnflow_demo.db` for browser-based answers.
2. Optionally build a full student-facing webpage for topic, notes, question, and answer submission.
3. Add a short README section with setup instructions, demo commands, agent states, limits, and API-key requirements.
4. Capture screenshots or a short recording showing the wrong-answer, follow-up, and mastery paths.
5. Commit the final source files. Do not commit `demo/learnflow/learnflow_demo.db`; add it to `.gitignore`.

## Overall completion estimate

Core agent behavior is complete. The project is approximately **90% complete**; the remaining work is frontend polish, documentation, and submission/demo evidence.
