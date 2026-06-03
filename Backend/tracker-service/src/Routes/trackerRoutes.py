from typing import List
from fastapi import APIRouter, Depends, status
from Schemas.trackerSchemas import ApplicationCreate, ApplicationUpdate, ApplicationResponse
from Controllers import trackerControllers
from Repositories.Interfaces.trackerInterface import TrackerRepositoryInterface
from dependencies import get_tracker_repo, get_current_user

router = APIRouter(prefix="/api/applications", tags=["Applications"])

@router.get("", response_model=List[ApplicationResponse])
async def get_applications(
    user_id: str = Depends(get_current_user),
    repo: TrackerRepositoryInterface = Depends(get_tracker_repo)
):
    return trackerControllers.get_applications(user_id, repo)

@router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(
    payload: ApplicationCreate,
    user_id: str = Depends(get_current_user),
    repo: TrackerRepositoryInterface = Depends(get_tracker_repo)
):
    return trackerControllers.create_application(user_id, payload, repo)

@router.patch("/{app_id}", response_model=ApplicationResponse)
async def update_application(
    app_id: str,
    payload: ApplicationUpdate,
    user_id: str = Depends(get_current_user),
    repo: TrackerRepositoryInterface = Depends(get_tracker_repo)
):
    return trackerControllers.update_application(app_id, user_id, payload, repo)

@router.delete("/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(
    app_id: str,
    user_id: str = Depends(get_current_user),
    repo: TrackerRepositoryInterface = Depends(get_tracker_repo)
):
    trackerControllers.delete_application(app_id, user_id, repo)
