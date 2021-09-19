from falcon import testing
from src.app import backend_app
from src.config import BaseConfig
from src.repository.flights_repository import FlightsRepository
from src.models.all_models import Flight

class TestFlightRepository(testing.TestCase):

    def setUp(self):
        app = backend_app.create_app(BaseConfig())
        self.flights_repository= FlightsRepository()
        self.app = backend_app
        self.session = self.app.session_maker()

    def test_add_flight(self):
        flight = self.flights_repository.add_flight(self.session, {'flight_from': 'SSS', 'flight_to':'DDD', 'price': 100})
        assert flight is not None
        found_flight = self.session.query(Flight).filter_by(id=flight.id).first()
        
        assert found_flight is not None
        assert flight.flight_from == found_flight.flight_from
        assert flight.flight_to == found_flight.flight_to

        self.session.delete(found_flight)
        self.session.commit()

    def test_get_flight(self):
        flight = self.flights_repository.add_flight(self.session, {'flight_from': 'ZCX', 'flight_to':'CXZ', 'price': 100})
        found_flight = self.flights_repository.get_flight(self.session,flight.flight_from, flight.flight_to)
        assert found_flight is not None
        assert found_flight.flight_from == flight.flight_from
        assert found_flight.flight_to == flight.flight_to
        self.session.delete(found_flight)
        self.session.commit()

    def test_update_flight(self):
        flight = self.flights_repository.add_flight(self.session, {'flight_from': 'ZCX', 'flight_to':'CXZ', 'price': 100})
        flight.price = 555
        updated_flight = self.flights_repository.update_flight_price(self.session, flight)
        found_flight = self.session.query(Flight).filter_by(id=flight.id).first()
        assert found_flight.price == 555

    def test_get_all_flights(self):
        flights = []
        for i in range(10):
            flight = self.flights_repository.add_flight(self.session, {'flight_from': 'ZCX', 'flight_to':'CXZ', 'price': 100})
            flights.append(flight)

        all_flights = self.flights_repository.get_flights(self.session)
        assert all_flights is not None
        assert len(all_flights) == len(flights)

