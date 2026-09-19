from __future__ import annotations

import html
import os
from pathlib import Path

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from learnflow.schema import TeachBackEvaluation
from learnflow.service import LearnFlowModelError, evaluate, teach
from slice.store import Store

app = FastAPI(title="LearnFlow AI")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB = os.environ.get("LEARNFLOW_DB", str(PROJECT_ROOT / "learnflow.db"))
MAX_CYCLES = 3


def store() -> Store:
    return Store(DB)


STYLE = """<style>body{font:16px/1.55 system-ui,sans-serif;max-width:760px;margin:0 auto;padding:32px 18px;background:#f8fafc;color:#172033}.card{background:white;border:1px solid #dbe3ee;border-radius:14px;padding:22px;margin:16px 0}textarea,input{box-sizing:border-box;width:100%;font:inherit;padding:10px;border:1px solid #b9c6d8;border-radius:8px}textarea{min-height:130px}button{background:#4f46e5;color:white;border:0;border-radius:8px;padding:11px 16px;font-weight:700;cursor:pointer}.muted{color:#64748b}.tag{display:inline-block;background:#e0e7ff;color:#3730a3;border-radius:99px;padding:3px 9px;font-size:.8rem;font-weight:700}.good{color:#047857}.warn{color:#b45309}pre{white-space:pre-wrap;font-family:inherit;background:#f1f5f9;padding:12px;border-radius:8px}.btn-home{background:#10b981;margin-top:12px;display:inline-block;text-decoration:none}.btn-home:hover{background:#059669}a.btn-home{color:white}</style>"""


def page(title: str, body: str) -> HTMLResponse:
    return HTMLResponse(f"<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>{html.escape(title)}</title>{STYLE}<h1>{html.escape(title)}</h1>{body}")


@app.get("/", response_class=HTMLResponse)
def home():
    runs = store().list_runs()
    history = "".join(f"<li><a href='/run/{r['id']}'>{html.escape(r['id'])}</a> — {html.escape(r['state'])}</li>" for r in runs)
    return page("LearnFlow AI", "<p class=muted>LearnFlow teaches from your notes first, then evaluates your explanation—not just a final answer.</p><div class=card><form method=post action=/start><label>Topic<br><input name=topic required placeholder='e.g. Ohm's Law'></label><p><label>Notes or textbook excerpt<br><textarea name=notes required placeholder='Paste the material you studied…'></textarea></label></p><button>Begin lesson</button></form></div><h2>Saved learning sessions</h2><ul>" + (history or "<li class=muted>None yet.</li>") + "</ul>")


@app.post("/start")
def start(topic: str = Form(...), notes: str = Form(...)):
    s = store(); run_id = s.create_run("learnflow", {"topic": topic.strip()})
    s.append(run_id, "topic", {"topic": topic.strip(), "notes": notes.strip()}, "student")
    try:
        lesson = teach(topic=topic.strip(), notes=notes.strip())
        s.append(run_id, "lesson", {"text": lesson}, "agent:tutor")
    except Exception:
        # A provider response must never prevent the student from beginning.
        # The notes remain the source of truth and provide a safe offline lesson.
        fallback = (f"Let's start with {topic.strip()}. Read this short source lesson, then explain it back in your own words:\n\n"
                    f"{notes.strip()}\n\nWhat is the main idea, and how would you use it in an example?")
        s.append(run_id, "lesson", {"text": fallback}, "system:notes_lesson")
    return RedirectResponse(f"/run/{run_id}", 303)


@app.get("/run/{run_id}", response_class=HTMLResponse)
def run(run_id: str):
    s = store(); topic = s.latest(run_id, "topic"); attempts = s.history(run_id, "teach_back")
    if not topic: return page("Not found", "<p>This session no longer exists.</p>")
    latest = s.latest(run_id, "evaluation")
    lesson = s.latest(run_id, "lesson")
    title = html.escape(topic["topic"])
    intro = f"<p><span class=tag>Cycle {len(attempts) + 1} of {MAX_CYCLES}</span></p>"
    if latest and latest["understanding"] == "mastered":
        return page("Mastered: " + topic["topic"], f"<div class=card><h2 class=good>You demonstrated understanding.</h2><p>{html.escape(latest['feedback'])}</p><p>Your next topic is now unlocked.</p><a href='/' class=btn-home><button class=btn-home>Learn Next Topic</button></a></div>" + history_html(s, run_id))
    if latest and len(attempts) >= MAX_CYCLES:
        return page("Needs more revision: " + topic["topic"], f"<div class=card><h2 class=warn>Revision limit reached</h2><p>{html.escape(latest['feedback'])}</p><p>Focus on: {html.escape(latest.get('likely_gap') or 'the key idea')}.</p></div>" + history_html(s, run_id))
    guidance = ""
    if latest:
        checks = s.history(run_id, "human_check")
        checked = any(c.payload.get("cycle") == latest["cycle"] for c in checks)
        guidance = f"<div class=card><h2>Targeted feedback</h2><p>{html.escape(latest['feedback'])}</p><p><b>Likely gap:</b> {html.escape(latest.get('likely_gap') or 'Not specified')}</p><pre>{html.escape(latest.get('targeted_explanation') or '')}</pre><p><b>Try this:</b> {html.escape(latest.get('follow_up_question') or '')}</p></div>"
        if not checked:
            confirmation = f"<div class=card><h2>Check the diagnosis</h2><p>Does this sound right, or did you simply misread the question?</p><form method=post action='/run/{run_id}/confirm'><input type=hidden name=cycle value='{latest['cycle']}'><button name=response value=confirmed>Yes, that sounds right</button> <button name=response value=rejected>I misread it / disagree</button></form></div>"
            return page("Learn: " + topic["topic"], intro + guidance + confirmation + history_html(s, run_id))
    first_lesson = ""
    if not attempts and lesson:
        first_lesson = f"<div class=card><h2>Your mini-lesson</h2><pre>{html.escape(lesson['text'])}</pre></div>"
    form = f"<div class=card><h2>Teach it back</h2><p class=muted>Explain the idea, why it works, and an example—without copying the notes. I'll evaluate what you understood.</p><form method=post action='/run/{run_id}/teach'><textarea name=teach_back required placeholder='Here is what I learned…'></textarea><p><button>Evaluate my explanation</button></p></form></div>"
    return page("Learn: " + topic["topic"], intro + first_lesson + guidance + form + history_html(s, run_id))


@app.post("/run/{run_id}/teach")
def teach(run_id: str, teach_back: str = Form(...)):
    s = store(); topic = s.latest(run_id, "topic")
    if not topic: return RedirectResponse("/", 303)
    cycle = len(s.history(run_id, "teach_back")) + 1
    s.append(run_id, "teach_back", {"cycle": cycle, "text": teach_back.strip()}, "student")
    try:
        result = evaluate(topic=topic["topic"], notes=topic["notes"], teach_back=teach_back, schema=TeachBackEvaluation)
        payload = result.model_dump()
    except LearnFlowModelError as exc:
        payload = {"understanding": "gap", "score": 0, "likely_gap": "Live evaluation unavailable", "evidence_from_notes": None, "feedback": str(exc), "targeted_explanation": None, "follow_up_question": None}
    payload["cycle"] = cycle
    s.append(run_id, "evaluation", payload, "agent:evaluator")
    return RedirectResponse(f"/run/{run_id}", 303)


@app.post("/run/{run_id}/confirm")
def confirm(run_id: str, cycle: int = Form(...), response: str = Form(...)):
    s = store()
    s.append(run_id, "human_check", {"cycle": cycle, "response": response}, "student")
    return RedirectResponse(f"/run/{run_id}", 303)


def history_html(s: Store, run_id: str) -> str:
    rows = []
    for attempt, evaluation in zip(s.history(run_id, "teach_back"), s.history(run_id, "evaluation")):
        rows.append(f"<details><summary>Cycle {attempt.payload['cycle']} — {html.escape(evaluation.payload['understanding'])} ({evaluation.payload['score']}%)</summary><p><b>Your explanation:</b> {html.escape(attempt.payload['text'])}</p><p>{html.escape(evaluation.payload['feedback'])}</p></details>")
    return "<div class=card><h2>Learning record</h2>" + ("".join(rows) or "<p class=muted>Your attempts will be saved here.</p>") + "</div>"