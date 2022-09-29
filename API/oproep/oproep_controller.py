import asyncio
import json
import time
from typing import List, Dict

from fastapi import APIRouter
from pydantic import BaseModel

from API import apns
from API.oproep.oproep_repository import *
from API.oproep.oproep import *
from API.gebruiker.gebruiker_repository import *
from Telefoon import audio, telefoon

oproep_router = APIRouter(prefix="/oproep")


class Oproepen(BaseModel):
    oproepen: List[OproepDTO]


@oproep_router.post("", tags=["Test"])
async def bel_aan(time: str, picture: str):
    oproep = Oproep(time=time, picture=picture)
    save_oproep(oproep)

    for gebruiker in get_all_gebruikers():
        if gebruiker.token is not None:
            await apns.send_oproep_notification(gebruiker)

    return {"message": "Oproep is aangemaakt"}


@oproep_router.get("", response_model=Optional[OproepDTO], tags=["Oproep"])
async def get_open_oproep():
    return select_open_oproep()


@oproep_router.get("/all", response_model=Oproepen, tags=["Oproep"], response_model_exclude_unset=True)
async def get_all():
    return Oproepen(oproepen=get_all_oproepen())


@oproep_router.post("/{id}/{gebruiker_id}", tags=["Oproep"])
async def neem_op(id: int, gebruiker_id: int):
    oproep_opnemen(id, gebruiker_id)

    for gebruiker in get_all_gebruikers():
        if gebruiker.token is not None:
            await apns.clear_notifications(gebruiker)

    return {"message": "Oproep is opgenomen"}


@oproep_router.post("/{id}", tags=["Oproep"])
async def reageer(id: int, reactie: ReactieDTO):
    oproep_reageren(id, reactie.tekst)
    return {"message": "Reactie is aangemaakt"}
