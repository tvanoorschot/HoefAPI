import string
import random

from sqlmodel import Session, select

from API.db import engine
from API.gebruiker.gebruiker import Gebruiker, GebruikerDTO


def update_kamer(gebruiker_id, kamer):
    with Session(engine) as session:
        statement = select(Gebruiker).where(Gebruiker.kamer == kamer)
        kamer_gebruiker = session.exec(statement).first()
        if kamer_gebruiker is None:
            statement = select(Gebruiker).where(Gebruiker.id == gebruiker_id)
            gebruiker = session.exec(statement).first()
            if gebruiker is not None:
                gebruiker.kamer = kamer
                session.commit()
                return True
        return False


def update_naam(gebruiker_id, naam):
    with Session(engine) as session:
        statement = select(Gebruiker).where(Gebruiker.id == gebruiker_id)
        gebruiker = session.exec(statement).first()
        if gebruiker is not None:
            gebruiker.naam = naam
            session.commit()


def get_gebruiker_by_key(api_key):
    with Session(engine) as session:
        statement = select(Gebruiker).where(Gebruiker.api_key == api_key)
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
                    gebruiker.api_key = generate_password()
                    session.commit()
                return gebruiker.api_key
            else:
                return None
        else:
            gebruiker = Gebruiker(naam=naam, kamer=kamer, token=token, api_key=generate_password())
            session.add(gebruiker)
            session.commit()
            return gebruiker.api_key


def get_all_gebruikers():
    with Session(engine) as session:
        statement = select(Gebruiker)
        result = session.exec(statement).all()
        return result


def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(11))
    return password
