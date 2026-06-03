from fastapi import APIRouter, Depends, UploadFile, File
from Schemas.aiSchemas import (
    ParseCVResponse,
    CouncilChatRequest,
    CouncilChatResponse,
    SuggestRolesRequest,
    SuggestRolesResponse,
    GenerateCVRequest,
    GenerateCVResponse,
)
from Controllers import aiControllers
from dependencies import get_current_user

router = APIRouter(prefix="/api/ai", tags=["AI Integration"])

@router.post("/parse-cv", response_model=ParseCVResponse)
async def parse_cv(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user)
):
    content = await file.read()
    return aiControllers.parse_cv(content, file.filename)

@router.post("/council-chat", response_model=CouncilChatResponse)
async def council_chat(
    payload: CouncilChatRequest,
    user_id: str = Depends(get_current_user)
):
    return aiControllers.council_chat(payload)

@router.post("/suggest-roles", response_model=SuggestRolesResponse)
async def suggest_roles(
    payload: SuggestRolesRequest,
    user_id: str = Depends(get_current_user)
):
    return aiControllers.suggest_roles(payload)

@router.post("/generate-custom-cv", response_model=GenerateCVResponse)
async def generate_custom_cv(
    payload: GenerateCVRequest,
    user_id: str = Depends(get_current_user)
):
    return aiControllers.generate_custom_cv(payload)
