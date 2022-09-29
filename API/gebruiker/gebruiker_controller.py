from typing import Optional

from fastapi import APIRouter
from API.gebruiker.gebruiker_repository import *

gebruiker_router = APIRouter(prefix="/gebruiker")


@gebruiker_router.post("", response_model=Optional[GebruikerDTO], tags=["Gebruiker"])
async def registreer(gebruiker: GebruikerDTO):
    gebruiker = authenticate(gebruiker.naam, gebruiker.kamer, gebruiker.token)
    return gebruiker


@gebruiker_router.get("/{kamer}", response_model=GebruikerDTO, tags=["Gebruiker"])
async def get_gebruiker(kamer: str):
    gebruiker = get_gebruiker_by_kamer(kamer)
    return gebruiker
