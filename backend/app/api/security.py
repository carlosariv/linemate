from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

API_KEY = "linemate-local-key"

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def require_api_key(key: str | None = Security(_api_key_header)) -> str:
    if key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid X-API-Key"
        )
    return key