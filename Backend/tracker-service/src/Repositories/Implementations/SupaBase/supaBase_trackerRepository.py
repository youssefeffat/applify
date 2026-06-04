"""Supabase-backed tracker repository implementation using PostgREST."""
from typing import Optional, Dict, Any, List
from datetime import datetime
import requests

class SupaBaseTrackerRepository:
    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase_url = supabase_url.rstrip("/")
        self.supabase_key = supabase_key
        self.table = "applications"
        self.headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _endpoint(self) -> str:
        return f"{self.supabase_url}/rest/v1/{self.table}"

    def _serialize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert datetime objects to ISO strings for JSON serialization."""
        serialized = {}
        for key, value in data.items():
            if isinstance(value, datetime):
                serialized[key] = value.isoformat()
            else:
                serialized[key] = value
        return serialized

    def get_user_applications(self, user_id: str) -> List[Dict[str, Any]]:
        params = {"user_id": f"eq.{user_id}", "select": "*"}
        resp = requests.get(self._endpoint(), headers=self.headers, params=params)
        if resp.status_code == 200:
            return resp.json()
        return []

    def get_application_by_id(self, app_id: str) -> Optional[Dict[str, Any]]:
        params = {"id": f"eq.{app_id}", "select": "*"}
        resp = requests.get(self._endpoint(), headers=self.headers, params=params)
        if resp.status_code == 200:
            data = resp.json()
            if data:
                return data[0]
        return None

    def create_application(self, data: Dict[str, Any]) -> Dict[str, Any]:
        headers = self.headers.copy()
        headers["Prefer"] = "return=representation"
        resp = requests.post(self._endpoint(), headers=headers, json=self._serialize_data(data))
        if resp.status_code in (200, 201):
            return resp.json()[0]
        raise ValueError(f"Failed to create application: {resp.status_code} - {resp.text}")

    def update_application(self, app_id: str, user_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        headers = self.headers.copy()
        headers["Prefer"] = "return=representation"
        params = {"id": f"eq.{app_id}", "user_id": f"eq.{user_id}"}
        resp = requests.patch(self._endpoint(), headers=headers, params=params, json=self._serialize_data(data))
        if resp.status_code in (200, 204):
            # 204 doesn't return body by default unless Prefer=return=representation is respected
            # PostgREST returns 200 with representation
            if resp.status_code == 200 and resp.text:
                res_data = resp.json()
                if res_data:
                    return res_data[0]
            return self.get_application_by_id(app_id)
        raise ValueError(f"Failed to update application: {resp.status_code} - {resp.text}")

    def delete_application(self, app_id: str, user_id: str) -> bool:
        params = {"id": f"eq.{app_id}", "user_id": f"eq.{user_id}"}
        resp = requests.delete(self._endpoint(), headers=self.headers, params=params)
        if resp.status_code in (200, 204):
            return True
        raise ValueError(f"Failed to delete application: {resp.status_code} - {resp.text}")

