from fastapi import APIRouter
from Telefoon import telefoon

slagboom_router = APIRouter(prefix="/slagboom")


@slagboom_router.post("", tags=["Slagboom"])
async def open_slagboom():
    telefoon.open_slagboom()
    return {"message": "Slagboom is geopend"}
