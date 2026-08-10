# Sentinel - Full Stack Setup

## One-Command Quick Start (macOS/Linux)

```bash
#!/bin/bash

# Backend setup
echo "🔧 Setting up backend..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
echo "⚠️  Edit .env and add your OPENAI_API_KEY"

# Frontend setup
echo "🎨 Setting up frontend..."
cd frontend
npm install
cp .env.example .env.local
cd ..

echo "✅ Setup complete!"
echo ""
echo "To run locally:"
echo "  Terminal 1: python run.py"
echo "  Terminal 2: cd frontend && npm run dev"
echo ""
echo "Then open http://localhost:3000"
```

Save as `setup.sh`, run with `bash setup.sh`

---

## Windows Quick Start

```cmd
# Backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
REM Edit .env with your OPENAI_API_KEY

# Frontend
cd frontend
npm install
copy .env.example .env.local
cd ..

echo Setup complete!
echo Terminal 1: python run.py
echo Terminal 2: cd frontend && npm run dev
```

---

## Docker Quick Start

### Run Both Services with Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./audit.log:/app/audit.log

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend
```

```bash
echo "OPENAI_API_KEY=sk-..." > .env
docker-compose up
```

Then open `http://localhost:3000`

---

## Manual Setup (Detailed)

### Backend (Python/FastAPI)

```bash
# 1. Virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env - add your OPENAI_API_KEY

# 4. Run server
python run.py
```

**Expected output**:
```
🚀 Starting Sentinel backend on 0.0.0.0:8000
📊 Audit logs: audit.log

API Documentation: http://0.0.0.0:8000/docs
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Frontend (Next.js/React)

In a new terminal:

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Configure environment
cp .env.example .env.local
# Verify NEXT_PUBLIC_API_URL=http://localhost:8000

# 4. Run development server
npm run dev
```

**Expected output**:
```
  ▲ Next.js 14.0.0
  - Local:        http://localhost:3000
  - Environments: .env.local
```

---

## Testing the System

### 1. Health Check

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```

### 2. Send a Message

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "What is quantum computing?",
    "session_id": "test-session-1"
  }'
```

### 3. Check Logs

```bash
cat audit.log | tail -20
```

### 4. View Swagger UI

Open http://localhost:8000/docs in your browser

### 5. Test Frontend

Open http://localhost:3000 in your browser and:
- Type a question
- See response with confidence badge
- Click "This response is wrong"
- Check Session Metrics

---

## Performance Verification

### Backend Response Time

```bash
time curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Hello", "session_id": "test"}'
```

Expected: 1-3 seconds (depends on OpenAI model)

### Frontend Performance

In browser DevTools (F12):
1. Go to Performance tab
2. Click Record
3. Interact with chat
4. Stop recording
5. Check metrics:
   - FCP (First Contentful Paint) < 1s
   - LCP (Largest Contentful Paint) < 2.5s

---

## Environment Configuration

### Backend (.env)

```env
# Required
OPENAI_API_KEY=sk-...

# Optional
HOST=0.0.0.0
PORT=8000
LOG_FILE=audit.log
LOG_LEVEL=INFO
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_FEEDBACK=true
```

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `OPENAI_API_KEY not set` | Edit `.env`, add your API key, restart |
| `Port 8000 already in use` | `PORT=8001 python run.py` |
| `Frontend can't reach backend` | Verify `NEXT_PUBLIC_API_URL`, check CORS |
| `"Module not found"` | Activate venv, run `pip install -r requirements.txt` |
| `No responses from chat` | Check OpenAI API key, account credits |
| `Blank page on frontend` | Check browser console (F12), network errors |

---

## Production Deployment

### Deploy Backend to Railway/Render

1. Create account at [Railway.app](https://railway.app) or [Render.com](https://render.com)
2. Connect GitHub repo
3. Set environment variables
4. Deploy from `implement-core-systems` branch

### Deploy Frontend to Vercel

```bash
npm install -g vercel
cd frontend
vercel
```

Set `NEXT_PUBLIC_API_URL` to your backend URL during deployment

---

## Next Steps After Setup

1. ✅ Backend working (health check passes)
2. ✅ Frontend loads (http://localhost:3000)
3. ✅ Can send messages and see responses
4. ✅ Confidence badges display correctly
5. ✅ Can record corrections
6. 📊 Check audit logs for all interactions
7. 🚀 Ready to customize and deploy!

---

**Questions?** Check the main README.md or review the SETUP.md files in backend/frontend directories.
