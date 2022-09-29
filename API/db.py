from sqlmodel import create_engine
from sqlmodel import Session

engine = create_engine("postgresql+psycopg2://pi:pi@192.168.86.245:5432/basishoef", echo=False)
session = Session(bind=engine)
