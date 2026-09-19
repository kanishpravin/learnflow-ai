# LearnFlow AI

Students paste one topic's notes. LearnFlow first teaches a short lesson, then asks
the student to teach the idea back in their own words.
The AI checks the explanation only against those notes, identifies a specific gap,
asks the student to confirm or reject that diagnosis, then explains it and generates
a targeted next question. Each cycle is saved in SQLite.
After three cycles, it either marks the topic mastered or stops honestly with the
remaining revision focus.

## Run it

1. Copy `.env.example` to `.env` and add `OPENROUTER_API_KEY=...`.
2. Optionally set `LEARNFLOW_MODEL`; it otherwise uses the kit's `SLICE_MODEL`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Start: `python -m uvicorn web.learnflow:app --reload`.
5. Open `http://127.0.0.1:8000`.

Keep `.env` private; it is ignored by Git. Without a key, the app saves the
student's work and clearly reports that live evaluation needs a key.
