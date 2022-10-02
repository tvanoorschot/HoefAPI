from sqlmodel import SQLModel, Field
from typing import Optional


class Gebruiker(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    naam: str = Field(index=True)
    kamer: str = Field(index=True)
    api_key: str = Field(index=True)
    token: Optional[str] = Field(index=True)


class GebruikerDTO(SQLModel):
    id: Optional[int] = Field(primary_key=True)
    naam: str
    kamer: str
    token: Optional[str]
