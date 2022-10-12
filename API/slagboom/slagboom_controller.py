from fastapi import APIRouter, Depends
from fastapi.openapi.models import APIKey

import settings
from API import security
from API.security import auth_gebruiker

if not settings.development:
    from Telefoon import telefoon

slagboom_router = APIRouter(prefix="/slagboom")


@slagboom_router.post("", tags=["Slagboom"])
async def open_slagboom(api_key: APIKey = Depends(security.get_api_key)):
    gebruiker = auth_gebruiker(api_key)

    if not settings.development:
        telefoon.open_slagboom()
    return {"message": "Slagboom is geopend"}
