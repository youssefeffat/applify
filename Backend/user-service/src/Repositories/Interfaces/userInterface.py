from typing import Protocol, Optional, Dict, Any

class UserRepositoryInterface(Protocol):
    def get_user_full_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        ...

    def update_user_profile(self, user_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        ...
