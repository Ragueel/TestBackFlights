from sqlalchemy.orm import Session
from src.models.all_models import Flight

class FlightsRepository:

    def get_flights(self, session: Session):
        return session.query(Flight).all()

    def update_flight_price(self, session: Session, flight: Flight) -> Flight:
        previous_flight = self.get_flight(session, flight.flight_from, flight.flight_to)

        if previous_flight is None:
            return
        
        previous_flight.price = flight.price
        session.commit()
        return previous_flight

    def get_flight(self, session: Session, flight_from, flight_to) -> Flight:
        return session.query(Flight).filter_by(flight_from=flight_from).filter_by(flight_to=flight_to).first()

    def add_flight(self, session: Session, flight_data:dict):
        flight = Flight()
        flight.flight_from = flight_data['flight_from']
        flight.flight_to = flight_data['flight_to']
        flight.price = flight_data['price']
        session.add(flight)
        session.commit()
        return flight