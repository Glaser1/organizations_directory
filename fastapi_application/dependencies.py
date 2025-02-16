from fastapi import Header, HTTPException, status, Security
from fastapi.security import APIKeyHeader

from config import settings

api_key_header = APIKeyHeader(name=settings.API_KEY, auto_error=False)


async def validate_api_key(api_key: str = Security(api_key_header)) -> str:
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
    return api_key
