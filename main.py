import asyncio
import threading
import time
import uvicorn
import settings

from sqlmodel import SQLModel
from fastapi import FastAPI

from API.gebruiker.gebruiker_controller import gebruiker_router
from API.oproep.oproep_controller import oproep_router
from API.slagboom.slagboom_controller import slagboom_router
from Telefoon import basisbel


tags_metadata = [
    {
        "name": "Login",
        "description": "De endpoint voor de login en registratie",
    },
    {
        "name": "Oproep",
        "description": "Alle endpoints voor de oproepen",
    },
    {
        "name": "Gebruiker",
        "description": "Alle endpoints voor de gebruikers",
    },
    {
        "name": "Slagboom",
        "description": "Alle endpoints voor de slagboom",
    },
]

app = FastAPI(openapi_tags=tags_metadata,
              title="HoefAPI",
              description="De API voor het intercom systeem van de Hoefseweg 1",
              version="2.0",
              contact={
                  "name": "Thomas van Oorschot",
                  "email": "oorschot98@gmail.com",
              },)

app.include_router(gebruiker_router, prefix="/restservices")
app.include_router(oproep_router, prefix="/restservices")
app.include_router(slagboom_router, prefix="/restservices")


class BackgroundTasks(threading.Thread):

    def run(self, *args, **kwargs):
        print("Start Basisbel background tasks")
        while True:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            loop.run_until_complete(basisbel.start())
            time.sleep(1)
            loop.close()


if __name__ == '__main__':
    # SQLModel.metadata.create_all(db.engine)

    if settings.development:
        uvicorn.run('main:app', host="0.0.0.0", port=8081, reload=True)
    else:
        t = BackgroundTasks()
        t.start()
        uvicorn.run('main:app', host="0.0.0.0", port=8080, reload=True)
