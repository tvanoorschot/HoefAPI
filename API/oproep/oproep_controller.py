from typing import List

from fastapi import APIRouter, Depends
from fastapi.openapi.models import APIKey
from pydantic import BaseModel

from API import apns, security
from API.oproep.oproep_repository import *
from API.oproep.oproep import *
from API.gebruiker.gebruiker_repository import *
from API.security import auth_gebruiker
from Telefoon import telefoon

oproep_router = APIRouter(prefix="/oproep")


class Oproepen(BaseModel):
    oproepen: List[OproepDTO]


@oproep_router.get("", response_model=Optional[OproepDTO], tags=["Oproep"])
async def get_open_oproep(api_key: APIKey = Depends(security.get_api_key)):
    gebruiker = auth_gebruiker(api_key)
    return select_open_oproep()


@oproep_router.get("/all", response_model=Oproepen, tags=["Oproep"], response_model_exclude_unset=True)
async def get_all_gesloten_oproepen(api_key: APIKey = Depends(security.get_api_key)):
    gebruiker = auth_gebruiker(api_key)

    oproepen = get_all_closed_oproepen()

    return Oproepen(oproepen=oproepen)


@oproep_router.post("/{id}", tags=["Oproep"])
async def neem_oproep_op(id: int, api_key: APIKey = Depends(security.get_api_key)):
    gebruiker = auth_gebruiker(api_key)

    oproep_opnemen(id, gebruiker.id)

    await apns.clear_notifications()

    return {"message": "Oproep is opgenomen"}


@oproep_router.post("/{id}/reactie", tags=["Oproep"])
async def reageer(id: int, reactie: ReactieDTO,
                  api_key: APIKey = Depends(security.get_api_key)):
    gebruiker = auth_gebruiker(api_key)

    oproep_reageren(id, reactie.tekst)

    if reactie.slagboom:
        telefoon.open_slagboom()

    return {"message": "Reactie is aangemaakt"}
