from typing import Optional
from fastapi import Depends, HTTPException, status
from config import SUPABASE_URL, SUPABASE_KEY
from Repositories.Implementations.SupaBase.supaBase_catalogRepository import SupaBaseCatalogRepository

_repo_instance: Optional[SupaBaseCatalogRepository] = None

def get_catalog_repo() -> SupaBaseCatalogRepository:
    global _repo_instance
    if _repo_instance is None:
        _repo_instance = SupaBaseCatalogRepository(SUPABASE_URL, SUPABASE_KEY)
    return _repo_instance
