"""Supabase-backed catalog repository implementation using PostgREST."""
from typing import Optional, Dict, Any, List
import requests

class SupaBaseCatalogRepository:
    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase_url = supabase_url.rstrip("/")
        self.supabase_key = supabase_key
        self.table = "jobs"
        self.tags_table = "job_tags"
        self.headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _endpoint(self, table: str) -> str:
        return f"{self.supabase_url}/rest/v1/{table}"

    def get_jobs(self, search: Optional[str] = None, mode: Optional[str] = None, contract: Optional[str] = None) -> List[Dict[str, Any]]:
        # For simplicity, returning all active jobs with basic filtering
        params = {"is_active": "eq.true", "select": "*"}
        if mode:
            params["employment_type"] = f"ilike.*{mode}*"
        if contract:
            params["contract_type"] = f"ilike.*{contract}*"
            
        # If text search is needed, we could use PostgREST's ilike or fts
        if search:
            params["title"] = f"ilike.*{search}*"
            
        resp = requests.get(self._endpoint(self.table), headers=self.headers, params=params)
        if resp.status_code == 200:
            return resp.json()
        return []

    def get_job_by_id(self, job_id: str) -> Optional[Dict[str, Any]]:
        params = {"id": f"eq.{job_id}", "select": "*"}
        resp = requests.get(self._endpoint(self.table), headers=self.headers, params=params)
        if resp.status_code == 200:
            data = resp.json()
            if data:
                # Also fetch tags
                tags_resp = requests.get(self._endpoint(self.tags_table), headers=self.headers, params={"job_id": f"eq.{job_id}"})
                tags = []
                if tags_resp.status_code == 200:
                    tags = [t.get("tag_name") for t in tags_resp.json()]
                job_data = data[0]
                job_data["tags"] = tags
                return job_data
        return None
