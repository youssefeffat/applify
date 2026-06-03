from typing import List
from fastapi import HTTPException, status
from Schemas.trackerSchemas import ApplicationCreate, ApplicationUpdate, ApplicationResponse
from Repositories.Interfaces.trackerInterface import TrackerRepositoryInterface

def get_applications(user_id: str, repo: TrackerRepositoryInterface) -> List[ApplicationResponse]:
    apps = repo.get_user_applications(user_id)
    return [ApplicationResponse(**app) for app in apps]

def create_application(user_id: str, payload: ApplicationCreate, repo: TrackerRepositoryInterface) -> ApplicationResponse:
    data = payload.model_dump(exclude_unset=True)
    data["user_id"] = user_id
    try:
        created = repo.create_application(data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return ApplicationResponse(**created)

def update_application(app_id: str, user_id: str, payload: ApplicationUpdate, repo: TrackerRepositoryInterface) -> ApplicationResponse:
    app_data = repo.get_application_by_id(app_id)
    if not app_data or app_data.get("user_id") != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found or access denied")
    
    data = payload.model_dump(exclude_unset=True)
    if not data:
        return ApplicationResponse(**app_data)
        
    try:
        updated = repo.update_application(app_id, user_id, data)
        if not updated:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update application")
        return ApplicationResponse(**updated)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

def delete_application(app_id: str, user_id: str, repo: TrackerRepositoryInterface) -> None:
    try:
        success = repo.delete_application(app_id, user_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete application")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
