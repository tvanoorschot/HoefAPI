from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import APIKey
from sqlmodel import SQLModel

from API import security
from API.gebruiker.gebruiker import GebruikerRead, GebruikerCreate
from API.gebruiker.gebruiker_repository import *
from API.security import auth_gebruiker

gebruiker_router = APIRouter(prefix="/gebruiker")


class Naam(SQLModel):
    naam: str


class Kamer(SQLModel):
    kamer: str


@gebruiker_router.post("", tags=["Login"])
async def authenticatie_gebruiker(gebruiker: GebruikerCreate):
    gebruiker = authenticate(gebruiker.naam, gebruiker.kamer, gebruiker.token)

    if gebruiker.api_key is None:
        raise HTTPException(status_code=401, detail="Gebruiker naam en/of kamer niet correct")

    return {"key": gebruiker.api_key}


@gebruiker_router.get("", response_model=GebruikerRead, tags=["Gebruiker"])
async def get_gebruiker(api_key: APIKey = Depends(security.get_api_key)):
    gebruiker = auth_gebruiker(api_key)

    return GebruikerRead(id=gebruiker.id, naam=gebruiker.naam, kamer=gebruiker.kamer)


@gebruiker_router.post("/naam", tags=["Gebruiker"])
async def update_naam_gebruiker(naam: Naam,
                                api_key: APIKey = Depends(security.get_api_key)):
    gebruiker = auth_gebruiker(api_key)

    if not update_naam(gebruiker.id, naam.naam):
        raise HTTPException(status_code=400, detail="Gebruiker naam is niet aangepast")

    return {"message": "Naam is aangepast"}


@gebruiker_router.post("/kamer", tags=["Gebruiker"])
async def update_kamer_gebruiker(kamer: Kamer,
                                 api_key: APIKey = Depends(security.get_api_key)):
    gebruiker = auth_gebruiker(api_key)

    if not update_kamer(gebruiker.id, kamer):
        raise HTTPException(status_code=409, detail="Kamer is al bezet")

    return {"message": "Kamer is aangepast"}
