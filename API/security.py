
from fastapi.security import APIKeyHeader
from fastapi import HTTPException, Security

from API.gebruiker.gebruiker_repository import get_gebruiker_by_key

api_key_header = APIKeyHeader(name="key", auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header),):
    return api_key


def auth_gebruiker(api_key):
    gebruiker = get_gebruiker_by_key(api_key)
    if gebruiker is None:
        raise HTTPException(status_code=403, detail="Gebruiker key niet correct of absent")
    return gebruiker