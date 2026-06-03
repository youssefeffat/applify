from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from config import SUPABASE_URL, SUPABASE_KEY, JWT_SECRET
from Repositories.Implementations.SupaBase.supaBase_trackerRepository import SupaBaseTrackerRepository

_repo_instance: Optional[SupaBaseTrackerRepository] = None

def get_tracker_repo() -> SupaBaseTrackerRepository:
    global _repo_instance
    if _repo_instance is None:
        _repo_instance = SupaBaseTrackerRepository(SUPABASE_URL, SUPABASE_KEY)
    return _repo_instance

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_id
