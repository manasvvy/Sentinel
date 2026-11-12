from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router
import os

app = FastAPI(
    title="Sentinel",
    description="AI with confidence transparency, safety governance, and learning signals",
    version="0.1.0"
)

# CORS — allow Vercel frontend and local dev
# In production, set ALLOWED_ORIGINS env var to your Vercel domain
_origins_env = os.getenv("ALLOWED_ORIGINS", "")
allowed_origins = (
    [o.strip() for o in _origins_env.split(",") if o.strip()]
    if _origins_env
    else ["*"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)


@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}
