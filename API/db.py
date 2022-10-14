from sqlmodel import Session
from sqlmodel import create_engine

import settings

if settings.development:
    engine = create_engine("postgresql+psycopg2://pi:basishoef98@192.168.1.235:5432/basishoefdev", echo=False)
    # engine = create_engine("postgresql+psycopg2://postgres:0000@192.168.86.246:5432/basishoef", echo=False)
else:
    engine = create_engine("postgresql+psycopg2://pi:basishoef98@localhost:5432/basishoef", echo=False)
session = Session(bind=engine)
