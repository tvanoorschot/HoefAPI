from sqlmodel import Session, select

from API.db import engine
from API.gebruiker.gebruiker import Gebruiker, GebruikerDTO


def get_all_gebruikers():
    with Session(engine) as session:
        statement = select(Gebruiker)
        result = session.exec(statement).all()
        return result


def get_gebruiker_by_kamer(kamer):
    with Session(engine) as session:
        statement = select(Gebruiker).where(Gebruiker.kamer == kamer)
        gebruiker = session.exec(statement).first()
        return GebruikerDTO(naam=gebruiker.naam, kamer=gebruiker.kamer, id=gebruiker.id, token=gebruiker.token)


def get_gebruiker_by_id(id):
    with Session(engine) as session:
        statement = select(Gebruiker).where(Gebruiker.id == id)
        result = session.exec(statement).first()
        return result


def authenticate(naam, kamer, token):
    with Session(engine) as session:
        statement = select(Gebruiker).where(Gebruiker.kamer == kamer)
        gebruiker = session.exec(statement).first()
        if gebruiker is not None:
            if gebruiker.naam == naam:
                if gebruiker.token != token:
                    gebruiker.token = token
                    session.commit()
                return GebruikerDTO(naam=gebruiker.naam, kamer=gebruiker.kamer, id=gebruiker.id, token=gebruiker.token)
            else:
                return None
        else:
            gebruiker = Gebruiker(naam=naam, kamer=kamer, token=token)
            session.add(gebruiker)
            session.commit()
            session.refresh(gebruiker)
            return GebruikerDTO(naam=gebruiker.naam, kamer=gebruiker.kamer, id=gebruiker.id, token=gebruiker.token)
