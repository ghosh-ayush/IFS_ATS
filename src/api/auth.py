from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from decouple import config

JWT_SECRET = config("JWT_SECRET", default="dev-secret")
ALGORITHM = "HS256"
security = HTTPBearer()

def create_token(user_id: int, expires_minutes: int = 60) -> str:
    payload = {"sub": str(user_id), "exp": datetime.utcnow() + timedelta(minutes=expires_minutes)}
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except (JWTError, KeyError):
        raise HTTPException(status_code=401, detail="Invalid authentication")
