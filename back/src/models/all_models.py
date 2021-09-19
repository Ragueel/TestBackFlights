from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Flight(Base):
    __tablename__='flight'
    id = Column(Integer,primary_key=True)
    flight_from = Column(String)
    flight_to = Column(String)
    price = Column(Numeric, default=0.0)

    def to_json(self):
        return {'id': self.id, 'flight_from': self.flight_from, 'flight_to': self.flight_to, 'price': float(self.price)}

def create_all(engine):
    Base.metadata.bind = engine
    Base.metadata.drop_all()
    Base.metadata.create_all()