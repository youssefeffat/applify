from typing import List, Optional
from fastapi import APIRouter, Depends
from Schemas.catalogSchemas import JobSchema
from Controllers import catalogControllers
from Repositories.Interfaces.catalogInterface import CatalogRepositoryInterface
from dependencies import get_catalog_repo

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

@router.get("", response_model=List[JobSchema])
async def get_jobs(
    search: Optional[str] = None,
    mode: Optional[str] = None,
    contract: Optional[str] = None,
    repo: CatalogRepositoryInterface = Depends(get_catalog_repo)
):
    return catalogControllers.get_jobs(search, mode, contract, repo)

@router.get("/{job_id}", response_model=JobSchema)
async def get_job_by_id(
    job_id: str,
    repo: CatalogRepositoryInterface = Depends(get_catalog_repo)
):
    return catalogControllers.get_job_by_id(job_id, repo)
