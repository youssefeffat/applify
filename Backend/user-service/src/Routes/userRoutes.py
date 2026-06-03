from fastapi import APIRouter, Depends
from Schemas.userSchemas import UserSchema, UserSchemaUpdate
from Controllers import userControllers
from Repositories.Interfaces.userInterface import UserRepositoryInterface
from dependencies import get_user_repo, get_current_user

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/me", response_model=UserSchema)
async def get_my_profile(
    user_id: str = Depends(get_current_user),
    repo: UserRepositoryInterface = Depends(get_user_repo)
):
    return userControllers.get_my_profile(user_id, repo)

@router.put("/me", response_model=UserSchema)
async def update_my_profile(
    payload: UserSchemaUpdate,
    user_id: str = Depends(get_current_user),
    repo: UserRepositoryInterface = Depends(get_user_repo)
):
    return userControllers.update_my_profile(user_id, payload, repo)
