# Sentinel

**Status**: Active flagship project

Sentinel is a backend-focused AI system built to solve a single problem: people trust AI systems more than they should, and they don't know when to slow down.

As AI tools become faster and more convincing, users start treating them like Google or an authority instead of something to think with. This leads to confident-wrong answers being accepted, poor decision-making, and overconfidence in AI outputs.

Sentinel sits between users and large language models and adds the parts most systems skip: **confidence transparency, memory with consent, monitoring, and governance**.

This project focuses on internal AI adoption and real system behavior. It is not a demo and not a chatbot wrapper.

---

## Architecture

```
User Browser (http://localhost:3000)
         ↓
   Frontend (Next.js)
         ↓
   Backend API (http://localhost:8000)
      ├→ LLM Client (OpenAI)
      ├→ Confidence Engine
      ├→ Session Manager
      └→ Audit Logger
```

---

## Quick Start (Local Testing)

### Prerequisites
- Python 3.9+
- Node.js 18+
- OpenAI API key

### Step 1: Set Up Backend

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Add your OpenAI API key
# Edit .env and set: OPENAI_API_KEY=sk-...

# Run backend server
python run.py
```

Backend will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs` (Swagger UI)

### Step 2: Set Up Frontend

In a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env.local

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

### Step 3: Test the System

1. **Open Frontend**: Go to http://localhost:3000
2. **Ask a Question**: Type something like "What is machine learning?"
3. **Review Response**: 
   - See the model's answer
   - Check the confidence level (Confident/Cautious/Guessing)
   - Read the reasoning explanation
4. **Record Correction**: Click "This response is wrong" if inaccurate
5. **Check Metrics**: Session metrics update in real-time

---

## Project Structure

```
.
├── app/                    # Backend (Python/FastAPI)
│   ├── main.py            # Server entry point
│   ├── api/
│   │   └── chat.py        # Chat endpoints
│   ├── core/
│   │   ├── confidence.py  # Confidence evaluation logic
│   │   ├── session.py     # Session management
│   │   └── logging.py     # Audit logging
│   ├── models/
│   │   └── llm_client.py  # OpenAI integration
│   └── schemas/
│       └── chat.py        # Request/response types
├── frontend/               # Frontend (Next.js/React)
│   ├── src/
│   │   ├── app/           # Next.js pages
│   │   ├── components/    # React components
│   │   ├── config/        # API configuration
│   │   ├── hooks/         # Custom React hooks
│   │   └── store/         # Zustand state
│   └── package.json
├── requirements.txt        # Python dependencies
└── README.md
```

---

## Testing Checklist

- [ ] Backend starts without errors
- [ ] Health check works: `curl http://localhost:8000/health`
- [ ] Frontend loads at http://localhost:3000
- [ ] Can send a chat message
- [ ] Confidence badge displays (color + score)
- [ ] Reasoning section expands
- [ ] Can click "This response is wrong"
- [ ] Session metrics update
- [ ] Messages persist on page reload

---

## Troubleshooting

### Backend Issues

**Error: `OPENAI_API_KEY not set`**
- Check `.env` file exists
- Verify `OPENAI_API_KEY=sk-...` is set
- Restart backend after editing `.env`

**Error: `Connection refused on port 8000`**
- Port 8000 already in use
- Kill existing process: `lsof -i :8000` (Mac/Linux)
- Run on different port: `PORT=8001 python run.py`

**Error: `Module not found`**
- Ensure virtual environment is activated
- Run: `pip install -r requirements.txt`

### Frontend Issues

**Error: `Cannot fetch from localhost:8000`**
- Ensure backend is running
- Check CORS headers in backend
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`

**Error: `Module not found`**
- Run: `npm install` in frontend directory
- Clear cache: `rm -rf node_modules && npm install`

**Blank page or loading forever**
- Check browser console for errors (F12)
- Check Network tab for failed requests
- Ensure backend is responding: `curl http://localhost:8000/health`

---

## API Endpoints

### Chat
**POST** `/chat`
```json
{
  "user_input": "What is machine learning?",
  "session_id": "session-1234-abc"
}
```

Response:
```json
{
  "response_text": "Machine learning is...",
  "confidence_state": "confident",
  "confidence_score": 0.85,
  "reasoning": [
    "Multiple reasoning paths present",
    "Response includes citations/evidence"
  ]
}
```

### Record Correction
**POST** `/correct`
```json
{
  "session_id": "session-1234-abc",
  "correct_info": "Actually, machine learning also...",
  "note": "Missing key concept"
}
```

### Session Summary
**GET** `/session/{session_id}/summary`

Response:
```json
{
  "session_id": "session-1234-abc",
  "created_at": "2026-01-15T10:30:00",
  "total_messages": 5,
  "total_corrections": 2,
  "correction_rate": 0.4,
  "avg_confidence": 0.72,
  "confidence_trend": [0.85, 0.65, 0.72, 0.80]
}
```

### Health Check
**GET** `/health`

Response:
```json
{"status": "ok"}
```

---

## Key Features

### Backend
- ✅ FastAPI with async support
- ✅ Real OpenAI integration
- ✅ Confidence evaluation (3-level: confident/cautious/guessing)
- ✅ Session management with correction tracking
- ✅ Immutable audit logging
- ✅ Type-safe schemas with Pydantic
- ✅ Error handling and validation

### Frontend
- ✅ Next.js 14 with App Router
- ✅ Real-time chat interface
- ✅ Confidence badge with color coding
- ✅ Expandable reasoning explanations
- ✅ One-click correction reporting
- ✅ Session metrics dashboard
- ✅ Auto-resizing message input
- ✅ Persistent state (localStorage)
- ✅ TypeScript for type safety
- ✅ Tailwind CSS for styling

---

## Branches

- `main` - Production-ready (current)
- `implement-core-systems` - Backend implementation
- `implement-frontend` - Frontend implementation

---

## Next Steps

1. **Test Locally** - Follow Quick Start above
2. **Merge Branches** - PR review, then merge to main
3. **Add Features** - Dark mode, markdown rendering, export
4. **Deploy** - Vercel (frontend) + Railway/Render (backend)
5. **Monitor** - Check audit logs and metrics

---

## Performance Metrics

### Frontend
- **LCP** (Largest Contentful Paint): < 2.5s
- **FID** (First Input Delay): < 100ms
- **CLS** (Cumulative Layout Shift): < 0.1
- **Bundle Size**: ~50KB (gzipped)

### Backend
- **Chat Response Time**: 1-3s (varies by model)
- **Confidence Evaluation**: < 10ms
- **Session Query**: < 5ms

---

## Design Principles

1. **Confidence is Transparent** - Every response includes confidence level and reasoning
2. **Corrections Drive Learning** - User corrections are the primary signal, not confidence scores
3. **All Decisions are Logged** - Governance requires full audit trails
4. **Simple Systems Survive** - Architecture prioritizes clarity over complexity
5. **Backend-First Safety** - All trust decisions live in the backend, not the UI

---

## Support & Questions

For issues:
1. Check troubleshooting section above
2. Review backend logs (stdout)
3. Check frontend console (F12)
4. Check API responses in Network tab

---

**Ready to test?** Start with the Quick Start section above! 🚀
