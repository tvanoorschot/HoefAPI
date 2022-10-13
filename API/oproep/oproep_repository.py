from datetime import datetime

from sqlmodel import Session, select

from API.db import engine
from API.gebruiker.gebruiker import Gebruiker
from API.oproep.oproep import Oproep
from Telefoon import cam


def select_open_oproep():
    with Session(engine) as session:
        statement = select(Oproep).where(Oproep.opnemer_id == None).order_by(Oproep.id.desc()).limit(1)
        oproep = session.exec(statement).first()

        return oproep


def create_oproep():
    time = datetime.now().strftime('%Y-%m-%d %H:%M')
    picture = cam.take_picture(time)
    with Session(engine) as session:
        oproep = Oproep(time=time, picture=picture)
        session.add(oproep)
        session.commit()
        session.refresh(oproep)

        return oproep


def select_oproep(oproep_id):
    with Session(engine) as session:
        statement = select(Oproep).join(Gebruiker).where(Oproep.id == oproep_id)
        oproep = session.exec(statement).first()

        return oproep


def oproep_opnemen(id, opnemer_id):
    with Session(engine) as session:
        statement = select(Oproep).where(Oproep.id == id)
        oproep = session.exec(statement).first()

        oproep.opnemer_id = opnemer_id
        session.commit()


def oproep_reageren(id, reactie):
    with Session(engine) as session:
        statement = select(Oproep).where(Oproep.id == id)
        oproep = session.exec(statement).first()

        oproep.reactie = reactie
        session.commit()


def get_all_closed_oproepen():
    with Session(engine) as session:

        statement = select(Oproep).join(Gebruiker).order_by(Oproep.id.desc()).limit(25)
        oproepen = session.exec(statement).all()

        for oproep in oproepen:
            if oproep.opnemer is not None and oproep.reactie is not None:
                yield oproep
