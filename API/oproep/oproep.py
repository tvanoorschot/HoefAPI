from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from API.gebruiker.gebruiker import Gebruiker


class Oproep(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    time: str = Field(index=True)
    picture: str = Field(index=True)
    reactie: Optional[str] = Field(index=True)
    opnemer_id: Optional[int] = Field(default=None, foreign_key='gebruiker.id')
    opnemer: Optional[Gebruiker] = Relationship()


class ReactieDTO(SQLModel):
    tekst: str
    slagboom: bool


class OproepDTO(SQLModel):
    id: Optional[int] = Field(primary_key=True)
    time: str = Field(index=True)
    picture: str = Field(index=True)
    reactie: Optional[str] = Field(index=True)
    opnemer: Optional[str] = Field(index=True)
