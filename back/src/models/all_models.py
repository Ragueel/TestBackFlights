from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Flight(Base):
    __tablename__='flight'
    id = Column(Integer,primary_key=True)
    flight_from = Column(String)
    flight_to = Column(String)
    price = Column(Numeric, default=0.0)

def create_all(engine):
    Base.metadata.bind = engine
    Base.metadata.drop_all()
    Base.metadata.create_all()