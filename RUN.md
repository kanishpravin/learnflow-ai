# LearnFlow AI - Run Instructions

## Prerequisites

- Python 3.11+
- pip (Python package manager)
- Git
- OpenRouter API key (free at https://openrouter.ai/keys)

---

## Setup (First Time Only)

### 1. Clone Repository
```bash
git clone https://github.com/kanishpravin/learnflow-ai.git
cd learnflow-ai
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install pypdf
```

### 4. Create .env File
Create a file named `.env` in project root:
```
OPENROUTER_API_KEY=your_api_key_here
LEARNFLOW_DB=learnflow.db
```

Get API key: https://openrouter.ai/keys

---

## Run

### Start Server
```bash
python -m uvicorn web.learnflow:app --port 8001
```

### Open Browser
```
http://127.0.0.1:8001
```

That's it. App is running.

---

## Stop Server
```bash
Ctrl + C
```

---

## Reset Database (Clear All History)
```bash
rm learnflow.db
```

Then restart server. Fresh database created automatically.

---

## Troubleshooting

### "Module not found: web.learnflow"
Check you're in project root:
```bash
pwd  # or cd to project folder
```

### "No module named 'pypdf'"
Install it:
```bash
pip install pypdf
```

### "OPENROUTER_API_KEY not found"
Create `.env` file with your API key (see Setup step 4)

### "Port 8001 already in use"
Use different port:
```bash
python -m uvicorn web.learnflow:app --port 8002
```

---

## Quick Commands

| Action | Command |
|--------|---------|
| Start app | `python -m uvicorn web.learnflow:app --port 8001` |
| Stop app | `Ctrl + C` |
| Reset data | `rm learnflow.db` |
| Check env | `cat .env` (Mac/Linux) or `type .env` (Windows) |
| View logs | Check terminal output |

---

## Development

### Without Auto-Reload (current)
```bash
python -m uvicorn web.learnflow:app --port 8001
```

### With Auto-Reload (dev mode)
```bash
python -m uvicorn web.learnflow:app --reload --port 8001
```

---

## Deploy to Vercel

```bash
npm install -g vercel
vercel login
vercel --prod
```

Set env variable: `OPENROUTER_API_KEY` in Vercel dashboard.

---

## That's It

Your app is live at `http://127.0.0.1:8001`

Enjoy learning! 🚀