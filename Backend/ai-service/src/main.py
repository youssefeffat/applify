from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import sys

src_path = os.path.dirname(os.path.abspath(__file__))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

load_dotenv()

app = FastAPI(
    title="Applify - AI Service",
    description="Microservice handling LLM parsing and generation",
    version="1.0.0"
)

from Routes.aiRoutes import router as ai_router
app.include_router(ai_router)

origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    status: str
    message: str

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    return {
        "status": "healthy",
        "message": "AI Service is operational"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8005))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
