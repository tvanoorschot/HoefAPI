from typing import List
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from API.gebruiker.gebruiker import Gebruiker


class OproepBase(SQLModel):
    time: str = Field(index=True)
    picture: str = Field(index=True)
    reactie: Optional[str] = Field(index=True)


class Oproep(OproepBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    opnemer_id: Optional[int] = Field(default=None, foreign_key='gebruiker.id')
    opnemer: Optional[Gebruiker] = Relationship()


class OproepRead(OproepBase):
    id: int
    opnemer: Optional[str]


class Oproepen(SQLModel):
    oproepen: List[OproepRead]


class Reactie(SQLModel):
    tekst: str
    slagboom: bool
