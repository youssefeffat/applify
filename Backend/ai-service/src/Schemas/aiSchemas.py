"""Pydantic schemas for AI Service."""
from pydantic import BaseModel
from typing import List, Optional

class ParseCVResponse(BaseModel):
    education: Optional[str] = None
    experience: Optional[str] = None
    skills: Optional[str] = None
    softSkills: Optional[str] = None
    certificates: Optional[str] = None
    languages: Optional[str] = None

class CouncilChatRequest(BaseModel):
    currentField: str
    userMessage: str

class CouncilChatResponse(BaseModel):
    nextQuestion: str
    extractedData: dict = {}

class SuggestRolesRequest(BaseModel):
    description: str

class SuggestRolesResponse(BaseModel):
    suggestedRoles: List[str]

class GenerateCVRequest(BaseModel):
    jobId: str

class GenerateCVResponse(BaseModel):
    cvContent: str
