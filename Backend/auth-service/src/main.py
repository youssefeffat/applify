from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

import sys
import os
src_path = os.path.dirname(os.path.abspath(__file__))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Load .env for backwards compatibility
load_dotenv()

try:
    from config import ALLOWED_ORIGINS as CONFIG_ALLOWED_ORIGINS, PORT as CONFIG_PORT
except Exception:
    CONFIG_ALLOWED_ORIGINS = None
    CONFIG_PORT = None

app = FastAPI(
    title="Applify - Auth Service",
    description="Microservice handling User Authentication",
    version="1.0.0"
)

if CONFIG_ALLOWED_ORIGINS is not None:
    origins = CONFIG_ALLOWED_ORIGINS
else:
    origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from Routes.authRoutes import router as auth_router
app.include_router(auth_router)

class HealthResponse(BaseModel):
    status: str
    message: str

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    return {
        "status": "healthy",
        "message": "Auth Service is operational"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(CONFIG_PORT or os.getenv("PORT", 8001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
