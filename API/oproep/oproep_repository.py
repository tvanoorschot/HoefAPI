from sqlmodel import Session, select

from API.db import engine
from API.gebruiker.gebruiker import Gebruiker
from API.oproep.oproep import Oproep, OproepDTO


def select_open_oproep():
    with Session(engine) as session:
        statement = select(Oproep).order_by(Oproep.id.desc()).limit(1)
        oproep = session.exec(statement).first()

        if oproep.opnemer_id is not None:
            return None
        else:
            return OproepDTO(
                id=oproep.id,
                time=oproep.time,
                picture=oproep.picture)


def save_oproep(oproep):
    with Session(engine) as session:
        session.add(oproep)
        session.commit()
        session.refresh(oproep)

        return oproep


def select_oproep(oproep_id):
    with Session(engine) as session:
        statement = select(Oproep).where(Oproep.id == oproep_id)
        oproep = session.exec(statement).first()

        statement = select(Gebruiker).where(Gebruiker.id == oproep.opnemer_id)
        opnemer = session.exec(statement).first()
        if opnemer is not None:
            return OproepDTO(
                id=oproep.id,
                opnemer=opnemer.naam,
                time=oproep.time,
                picture=oproep.picture,
                reactie=oproep.reactie)
        else:
            return OproepDTO(
                id=oproep.id,
                opnemer=None,
                time=oproep.time,
                picture=oproep.picture,
                reactie=oproep.reactie)


def oproep_opnemen(id, opnemer_id):
    with Session(engine) as session:
        statement = select(Oproep).where(Oproep.id == id)
        oproep = session.exec(statement).first()

        statement = select(Gebruiker).where(Gebruiker.id == opnemer_id)
        opnemer = session.exec(statement).first()

        oproep.opnemer_id = opnemer.id
        session.commit()
        session.refresh(oproep)


def oproep_reageren(id, reactie):
    with Session(engine) as session:
        statement = select(Oproep).where(Oproep.id == id)
        oproep = session.exec(statement).first()

        oproep.reactie = reactie
        session.commit()


def get_all_oproepen():
    with Session(engine) as session:
        oproepen_dtos = []

        statement = select(Oproep).order_by(Oproep.id.desc()).limit(25)
        oproepen = session.exec(statement).all()

        for oproep in oproepen:
            statement = select(Gebruiker).where(Gebruiker.id == oproep.opnemer_id)
            opnemer = session.exec(statement).first()
            if opnemer is not None:
                oproepen_dtos.append(OproepDTO(
                    id=oproep.id,
                    opnemer=opnemer.naam,
                    time=oproep.time,
                    picture=oproep.picture,
                    reactie=oproep.reactie))
            else:
                oproepen_dtos.append(OproepDTO(
                    id=oproep.id,
                    opnemer=None,
                    time=oproep.time,
                    picture=oproep.picture,
                    reactie=oproep.reactie))

        return oproepen_dtos


def get_all_closed_oproepen():
    with Session(engine) as session:
        oproepen_dtos = []

        statement = select(Oproep).order_by(Oproep.id.desc()).limit(25)
        oproepen = session.exec(statement).all()

        for oproep in oproepen:
            statement = select(Gebruiker).where(Gebruiker.id == oproep.opnemer_id)
            opnemer = session.exec(statement).first()
            if opnemer is not None and oproep.reactie is not None:
                oproepen_dtos.append(OproepDTO(
                    id=oproep.id,
                    opnemer=opnemer.naam,
                    time=oproep.time,
                    picture=oproep.picture,
                    reactie=oproep.reactie))

        return oproepen_dtos
