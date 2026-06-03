"""Pydantic schemas for Tracker Service."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ApplicationCreate(BaseModel):
    job_id: str
    status: str = Field(default="Saved", description="Enum: Saved, Applied, Interviews, Accepted, Rejected")

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    interview_date: Optional[datetime] = None

class ApplicationResponse(BaseModel):
    id: str
    user_id: str
    job_id: str
    status: str
    interview_date: Optional[datetime] = None
    date_added: datetime
    last_updated: datetime
