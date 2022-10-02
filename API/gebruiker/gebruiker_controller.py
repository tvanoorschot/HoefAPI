from fastapi import APIRouter, Depends
from fastapi.openapi.models import APIKey

from API import security
from API.gebruiker.gebruiker_repository import *
from API.security import auth_gebruiker

gebruiker_router = APIRouter(prefix="/gebruiker")


@gebruiker_router.post("", tags=["Login"])
async def authenticatie_gebruiker(gebruiker: GebruikerDTO):
    key = authenticate(gebruiker.naam, gebruiker.kamer, gebruiker.token)
    return {"key": key}


@gebruiker_router.get("", response_model=GebruikerDTO, tags=["Gebruiker"])
async def get_gebruiker(api_key: APIKey = Depends(security.get_api_key)):
    gebruiker = auth_gebruiker(api_key)
    return gebruiker


@gebruiker_router.post("/naam/{naam}", tags=["Gebruiker"])
async def update_naam_gebruiker(naam: str,
                                api_key: APIKey = Depends(security.get_api_key)):
    gebruiker = auth_gebruiker(api_key)
    update_naam(gebruiker.id, naam)
    return {"message": "Naam is aangepast"}


@gebruiker_router.post("/kamer/{kamer}", tags=["Gebruiker"])
async def update_kamer_gebruiker(kamer: str,
                                 api_key: APIKey = Depends(security.get_api_key)):
    gebruiker = auth_gebruiker(api_key)
    update_kamer(gebruiker.id, kamer)
    return {"message": "Kamer is aangepast"}