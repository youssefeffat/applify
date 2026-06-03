from typing import List, Optional
from fastapi import HTTPException, status
from Schemas.catalogSchemas import JobSchema
from Repositories.Interfaces.catalogInterface import CatalogRepositoryInterface

def get_jobs(search: Optional[str], mode: Optional[str], contract: Optional[str], repo: CatalogRepositoryInterface) -> List[JobSchema]:
    jobs = repo.get_jobs(search, mode, contract)
    return [JobSchema(**job) for job in jobs]

def get_job_by_id(job_id: str, repo: CatalogRepositoryInterface) -> JobSchema:
    job = repo.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return JobSchema(**job)
