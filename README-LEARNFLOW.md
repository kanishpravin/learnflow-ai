# LearnFlow AI

An AI tutor that teaches from your notes, then evaluates your understanding.

## How It Works

1. **Student Input**: Paste a topic and study notes
2. **AI Lesson**: Get a short lesson based on your notes
3. **Teach Back**: Explain the topic in your own words
4. **Evaluation**: AI evaluates your explanation for gaps
5. **Targeted Feedback**: Get explanations for concepts you missed
6. **Follow-up Quiz**: Answer follow-up questions to master the concept
7. **Cycle**: Up to 3 revision cycles to achieve mastery
8. **Next Topic**: Unlock the next topic when mastered

## Features

- ✅ AI-powered lesson generation from student notes
- ✅ Concept gap detection
- ✅ Targeted explanation generation
- ✅ Follow-up quiz generation
- ✅ Retry limit enforcement (MAX_CYCLES=3)
- ✅ State persistence with SQLite
- ✅ Fallback mode when AI provider unavailable
- ✅ Multi-topic learning path
- ✅ "Learn Next Topic" button for progression

## Tech Stack

- **Backend**: FastAPI, Uvicorn
- **AI**: OpenRouter API (Claude, GPT, etc.)
- **Database**: SQLite (production-ready for PostgreSQL)
- **Frontend**: HTML/CSS (server-rendered)

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/learnflow-ai.git
cd learnflow-ai
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create a `.env` file in the project root:
```
OPENROUTER_API_KEY=your_api_key_here
LEARNFLOW_DB=learnflow.db
```

Get your OpenRouter API key: https://openrouter.ai/keys

### 5. Run the Server
```bash
python -m uvicorn app:app --reload --port 8001
```

Visit: http://127.0.0.1:8001

## Deployment

### Vercel (Easiest)
```bash
npm install -g vercel
vercel --prod
```

### Railway (Recommended for databases)
```bash
npm install -g railway
railway login
railway init
railway up
```

### Render (Free tier available)
1. Go to https://render.com
2. Create new Web Service
3. Connect your GitHub repo
4. Set start command: `python -m uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy

### Docker
```bash
docker build -t learnflow-ai .
docker run -p 8001:8000 -e OPENROUTER_API_KEY=your_key learnflow-ai
```

## Project Status

### ✅ Completed
- Core infrastructure (runner, callbacks, LLM integration)
- Schema definitions (QuizAttempt, HumanCheck, StudentTopicState)
- Evaluator working with real LLM
- Initial answer evaluation and concept gap detection
- Human confirmation flow
- Targeted explanation generation
- Follow-up quiz generation
- State transitions
- Next topic unlock button

### ⏳ In Progress
- Follow-up mastery evaluation
- Retry limits enforcement
- Full state persistence

### 📋 Planned
- Quiz generator (dynamic generation)
- Resume-after-close capability
- Adversarial input testing
- CLI integration
- End-to-end validation

## API Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home page, create new session |
| `/start` | POST | Begin lesson from topic + notes |
| `/run/{run_id}` | GET | View lesson and evaluation state |
| `/run/{run_id}/teach` | POST | Submit teach-back explanation |
| `/run/{run_id}/confirm` | POST | Confirm gap diagnosis |

## Project Structure

```
learnflow-ai/
├── app.py                 # FastAPI app, routes, HTML rendering
├── learnflow/
│   ├── schema.py         # Pydantic models for evaluation
│   ├── service.py        # AI evaluation & lesson generation
│   └── ...
├── slice/
│   └── store.py          # SQLite storage layer
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── learnflow.db         # SQLite database (auto-created)
```

## License

MIT

## Author

Kanish - Independent Web Developer