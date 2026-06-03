"""Pydantic schemas for Job Catalog Service."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class JobSchema(BaseModel):
    id: str
    title: str
    company: str
    location: Optional[str] = None
    employment_type: Optional[str] = None
    contract_type: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = []
    compatibilityScore: int = 0
    created_at: datetime
    updated_at: datetime
