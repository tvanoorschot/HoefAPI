from sqlmodel import create_engine
from sqlmodel import Session

import settings

if settings.development:
    engine = create_engine("postgresql+psycopg2://pi:basishoef98@192.168.1.235:5432/basishoefdev", echo=False)
else:
    engine = create_engine("postgresql+psycopg2://pi:basishoef98@localhost:5432/basishoef", echo=False)
session = Session(bind=engine)
