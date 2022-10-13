import random
import string

from sqlmodel import Session, select

from API.db import engine
from API.gebruiker.gebruiker import Gebruiker


def update_kamer(gebruiker_id, kamer):
    with Session(engine) as session:
        statement = select(Gebruiker).where(Gebruiker.kamer == kamer)
        kamer_bezet = session.exec(statement).first() is not None

        if kamer_bezet:
            return False

        statement = select(Gebruiker).where(Gebruiker.id == gebruiker_id)
        gebruiker = session.exec(statement).first()

        gebruiker.kamer = kamer

        session.commit()

        return True


def update_naam(gebruiker_id, naam):
    with Session(engine) as session:
        statement = select(Gebruiker).where(Gebruiker.id == gebruiker_id)
        gebruiker = session.exec(statement).first()

        gebruiker.naam = naam

        session.commit()

        return True


def get_gebruiker_by_key(api_key):
    with Session(engine) as session:
        statement = select(Gebruiker).where(Gebruiker.api_key == api_key)
        gebruiker = session.exec(statement).first()

        return gebruiker


def authenticate(naam, kamer, token):
    with Session(engine) as session:
        statement = select(Gebruiker).where(Gebruiker.kamer == kamer and Gebruiker.naam == naam)
        gebruiker = session.exec(statement).first()

        if gebruiker is None:
            gebruiker = Gebruiker(naam=naam, kamer=kamer, token=token, api_key=generate_password())
            session.add(gebruiker)
            session.commit()
            return gebruiker

        if gebruiker.token != token:
            gebruiker.token = token
            gebruiker.api_key = generate_password()
            session.commit()

        return gebruiker


def get_all_gebruikers():
    with Session(engine) as session:
        statement = select(Gebruiker)
        result = session.exec(statement).all()
        return result


def get_all_gebruikers_with_token():
    with Session(engine) as session:
        statement = select(Gebruiker).where(Gebruiker.token != None)
        result = session.exec(statement).all()
        return result


def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(11))
    return password
