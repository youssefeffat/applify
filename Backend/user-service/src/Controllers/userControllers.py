from fastapi import HTTPException, status
from Schemas.userSchemas import UserSchema, UserSchemaUpdate
from Repositories.Interfaces.userInterface import UserRepositoryInterface

def get_my_profile(user_id: str, repo: UserRepositoryInterface) -> UserSchema:
    profile = repo.get_user_full_profile(user_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserSchema(**profile)

def update_my_profile(user_id: str, payload: UserSchemaUpdate, repo: UserRepositoryInterface) -> UserSchema:
    data = payload.model_dump(exclude_unset=True)
    if not data:
        return get_my_profile(user_id, repo)
        
    updated = repo.update_user_profile(user_id, data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update profile")
        
    return UserSchema(**updated)
