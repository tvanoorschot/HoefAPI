from typing import Optional

from sqlmodel import SQLModel, Field


class GebruikerBase(SQLModel):
    naam: str = Field(index=True)
    kamer: str = Field(index=True)


class Gebruiker(GebruikerBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    token: Optional[str] = Field(index=True)
    api_key: str = Field(index=True)


class GebruikerCreate(GebruikerBase):
    token: Optional[str] = Field(index=True)


class GebruikerRead(GebruikerBase):
    pass
