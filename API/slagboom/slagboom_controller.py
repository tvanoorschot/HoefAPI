from fastapi import APIRouter, Depends
from fastapi.openapi.models import APIKey

from API import security
from API.security import auth_gebruiker
from Telefoon import telefoon

slagboom_router = APIRouter(prefix="/slagboom")


@slagboom_router.post("", tags=["Slagboom"])
async def open_slagboom(api_key: APIKey = Depends(security.get_api_key)):
    auth_gebruiker(api_key)

    telefoon.open_slagboom()

    return {"message": "Slagboom is geopend"}
