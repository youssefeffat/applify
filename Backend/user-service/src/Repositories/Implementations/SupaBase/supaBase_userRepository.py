from typing import Optional, Dict, Any
import requests

class SupaBaseUserRepository:
    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase_url = supabase_url.rstrip("/")
        self.supabase_key = supabase_key
        self.headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _endpoint(self, table: str) -> str:
        return f"{self.supabase_url}/rest/v1/{table}"

    def get_user_full_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        # Fetch base user to ensure they exist and get email
        user_resp = requests.get(self._endpoint("users"), headers=self.headers, params={"id": f"eq.{user_id}", "select": "id,email"})
        if user_resp.status_code != 200 or not user_resp.json():
            return None
        base_user = user_resp.json()[0]

        # Fetch profile
        profile_resp = requests.get(self._endpoint("profiles"), headers=self.headers, params={"user_id": f"eq.{user_id}", "select": "*"})
        profile = profile_resp.json()[0] if (profile_resp.status_code == 200 and profile_resp.json()) else {}

        # Fetch preferences
        prefs_resp = requests.get(self._endpoint("job_preferences"), headers=self.headers, params={"user_id": f"eq.{user_id}", "select": "*"})
        prefs = prefs_resp.json()[0] if (prefs_resp.status_code == 200 and prefs_resp.json()) else None

        # Fetch background
        bg_resp = requests.get(self._endpoint("professional_background"), headers=self.headers, params={"user_id": f"eq.{user_id}", "select": "*"})
        bg = bg_resp.json()[0] if (bg_resp.status_code == 200 and bg_resp.json()) else None

        return {
            "id": base_user["id"],
            "email": base_user["email"],
            "first_name": profile.get("first_name"),
            "last_name": profile.get("last_name"),
            "current_title": profile.get("current_title"),
            "github_url": profile.get("github_url"),
            "location": profile.get("location"),
            "long_resume": profile.get("long_resume"),
            "job_preferences": prefs,
            "professional_background": bg
        }

    def update_user_profile(self, user_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        upsert_headers = self.headers.copy()
        upsert_headers["Prefer"] = "resolution=merge-duplicates,return=representation"

        # 1. Upsert profile (conflict on user_id unique constraint)
        profile_data = {k: v for k, v in data.items() if k not in ["job_preferences", "professional_background"]}
        if profile_data:
            profile_data["user_id"] = user_id
            requests.post(
                self._endpoint("profiles") + "?on_conflict=user_id",
                headers=upsert_headers,
                json=profile_data
            )

        # 2. Upsert job_preferences
        if "job_preferences" in data and data["job_preferences"] is not None:
            prefs_data = data["job_preferences"]
            prefs_data["user_id"] = user_id
            requests.post(
                self._endpoint("job_preferences") + "?on_conflict=user_id",
                headers=upsert_headers,
                json=prefs_data
            )

        # 3. Upsert professional_background
        if "professional_background" in data and data["professional_background"] is not None:
            bg_data = data["professional_background"]
            bg_data["user_id"] = user_id
            requests.post(
                self._endpoint("professional_background") + "?on_conflict=user_id",
                headers=upsert_headers,
                json=bg_data
            )

        return self.get_user_full_profile(user_id)