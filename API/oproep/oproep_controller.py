from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import APIKey

from API import apns, security
from API.oproep.oproep import *
from API.oproep.oproep_repository import *
from API.security import auth_gebruiker
from Telefoon import telefoon

oproep_router = APIRouter(prefix="/oproep")


@oproep_router.get("", response_model=Optional[OproepRead], tags=["Oproep"])
async def get_open_oproep(api_key: APIKey = Depends(security.get_api_key)):
    auth_gebruiker(api_key)

    oproep = select_open_oproep()

    if oproep is None:
        raise HTTPException(status_code=404, detail="Geen oproep gevonden")

    return OproepRead(
        id=oproep.id,
        time=oproep.time,
        picture=oproep.picture)


@oproep_router.get("/all", response_model=Oproepen, tags=["Oproep"])
async def get_all_gesloten_oproepen(api_key: APIKey = Depends(security.get_api_key)):
    auth_gebruiker(api_key)

    oproepen = []

    for oproep in get_all_closed_oproepen():
        oproepen.append(OproepRead(
            id=oproep.id,
            opnemer=oproep.opnemer.naam,
            time=oproep.time,
            picture=oproep.picture,
            reactie=oproep.reactie))

    return Oproepen(oproepen=oproepen)


@oproep_router.post("/{id}", tags=["Oproep"])
async def neem_oproep_op(id: int, api_key: APIKey = Depends(security.get_api_key)):
    gebruiker = auth_gebruiker(api_key)

    oproep_opnemen(id, gebruiker.id)

    await apns.send_clear_notifications()

    return {"message": "Oproep is opgenomen"}


@oproep_router.post("/{id}/reactie", tags=["Oproep"])
async def reageer(id: int, reactie: Reactie,
                  api_key: APIKey = Depends(security.get_api_key)):
    auth_gebruiker(api_key)

    oproep_reageren(id, reactie.tekst)

    if reactie.slagboom:
        telefoon.open_slagboom()

    return {"message": "Reactie is aangemaakt"}


@oproep_router.get("/belaan", tags=["Test"])
async def aanbellen(api_key: APIKey = Depends(security.get_api_key)):
    auth_gebruiker(api_key)

    create_oproep()

    await apns.send_oproep_notifications()

    return {"message": "Oproep aangemaakt"}
