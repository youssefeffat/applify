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

class UserProfileForCV(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    current_title: Optional[str] = None
    github_url: Optional[str] = None
    location: Optional[str] = None
    education: Optional[str] = None
    experience: Optional[str] = None
    skills: Optional[str] = None
    soft_skills: Optional[str] = None
    certificates: Optional[str] = None
    languages: Optional[str] = None
    long_resume: Optional[str] = None

class JobInfoForCV(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = []
    contract_type: Optional[str] = None
    employment_type: Optional[str] = None

class GenerateCVRequest(BaseModel):
    jobInfo: JobInfoForCV
    userProfile: UserProfileForCV

class GenerateCVResponse(BaseModel):
    cvContent: str   # Full HTML document
    filename: str    # Suggested download filename
