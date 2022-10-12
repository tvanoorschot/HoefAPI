from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import APIKey

from API import security
from API.gebruiker.gebruiker import GebruikerRead, GebruikerCreate
from API.gebruiker.gebruiker_repository import *
from API.security import auth_gebruiker

gebruiker_router = APIRouter(prefix="/gebruiker")


@gebruiker_router.post("", tags=["Login"])
async def authenticatie_gebruiker(gebruiker: GebruikerCreate):
    key = authenticate(gebruiker.naam, gebruiker.kamer, gebruiker.token)
    if key is None:
        raise HTTPException(status_code=401, detail="Gebruiker naam en/of kamer niet correct")
    return {"key": key}


@gebruiker_router.get("", response_model=GebruikerRead, tags=["Gebruiker"])
async def get_gebruiker(api_key: APIKey = Depends(security.get_api_key)):
    gebruiker = auth_gebruiker(api_key)

    return GebruikerRead(id=gebruiker.id, naam=gebruiker.naam, kamer=gebruiker.kamer)


@gebruiker_router.post("/naam", tags=["Gebruiker"])
async def update_naam_gebruiker(naam: str,
                                api_key: APIKey = Depends(security.get_api_key)):
    gebruiker = auth_gebruiker(api_key)
    if update_naam(gebruiker.id, naam):
        return {"message": "Naam is aangepast"}
    else:
        raise HTTPException(status_code=400, detail="Gebruiker naam is niet aangepast")


@gebruiker_router.post("/kamer", tags=["Gebruiker"])
async def update_kamer_gebruiker(kamer: str,
                                 api_key: APIKey = Depends(security.get_api_key)):
    gebruiker = auth_gebruiker(api_key)
    if update_kamer(gebruiker.id, kamer):
        raise HTTPException(status_code=409, detail="Kamer is al bezet")
    return {"message": "Kamer is aangepast"}
