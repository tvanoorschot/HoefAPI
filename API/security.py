from datetime import datetime

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from API.gebruiker.gebruiker_repository import get_gebruiker_by_key

api_key_header = APIKeyHeader(name="key", auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header), ):
    return api_key


def auth_gebruiker(api_key):
    gebruiker = get_gebruiker_by_key(api_key)
    if gebruiker is None:
        raise HTTPException(status_code=403, detail="Gebruiker key absent of niet correct")
    else:
        print("Gebruiker:   {naam} ({kamer})   -   Time:    {time}".format(
            naam=gebruiker.naam,
            kamer=gebruiker.kamer,
            time=datetime.now().strftime("%H:%M:%S")))
    return gebruiker
