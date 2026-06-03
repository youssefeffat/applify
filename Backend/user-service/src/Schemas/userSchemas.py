from pydantic import BaseModel
from typing import List, Optional

class JobPreferences(BaseModel):
    target_years_experience: Optional[str] = None
    target_roles: List[str] = []
    employment_types: List[str] = []
    experience_levels: List[str] = []

class ProfessionalBackground(BaseModel):
    education: Optional[str] = None
    experience: Optional[str] = None
    skills: Optional[str] = None
    soft_skills: Optional[str] = None
    certificates: Optional[str] = None
    languages: Optional[str] = None

class UserSchema(BaseModel):
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    current_title: Optional[str] = None
    github_url: Optional[str] = None
    location: Optional[str] = None
    long_resume: Optional[str] = None
    
    # Nested schemas
    job_preferences: Optional[JobPreferences] = None
    professional_background: Optional[ProfessionalBackground] = None

class UserSchemaUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    current_title: Optional[str] = None
    github_url: Optional[str] = None
    location: Optional[str] = None
    long_resume: Optional[str] = None
    
    # Nested schemas
    job_preferences: Optional[JobPreferences] = None
    professional_background: Optional[ProfessionalBackground] = None
