"""Tracker repository interface definitions."""
from typing import Protocol, Optional, Dict, Any, List

class TrackerRepositoryInterface(Protocol):
    def get_user_applications(self, user_id: str) -> List[Dict[str, Any]]:
        ...

    def get_application_by_id(self, app_id: str) -> Optional[Dict[str, Any]]:
        ...

    def create_application(self, data: Dict[str, Any]) -> Dict[str, Any]:
        ...

    def update_application(self, app_id: str, user_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        ...

    def delete_application(self, app_id: str, user_id: str) -> bool:
        ...
