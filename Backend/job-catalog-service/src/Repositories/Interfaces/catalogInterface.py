"""Job Catalog repository interface definitions."""
from typing import Protocol, Optional, Dict, Any, List

class CatalogRepositoryInterface(Protocol):
    def get_jobs(self, search: Optional[str] = None, mode: Optional[str] = None, contract: Optional[str] = None) -> List[Dict[str, Any]]:
        ...

    def get_job_by_id(self, job_id: str) -> Optional[Dict[str, Any]]:
        ...
