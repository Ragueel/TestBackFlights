from falcon import testing
import datetime

from src.services.flight_services.flight_get import FlightGetSerivce, FlightRequestData
from src.services.flight_services.flights_service import FlightsService
from src.services.flight_services.flight_validator import FlightValidatorService

class TestFlightService(testing.TestCase):

    def setUp(self):
        self.flight_get_service = FlightGetSerivce()
        self.flight_validator_service = FlightValidatorService()
        self.flight_service = FlightsService(self.flight_get_service, self.flight_validator_service)

        current_date = datetime.date.today() 
        end_date = current_date + datetime.timedelta(1)

        self.date_format = '%d/%m/%Y'

        f_current_date = current_date.strftime(self.date_format)
        f_end_date = end_date.strftime(self.date_format)
        self.request_data = FlightRequestData('ALA', 'TSE',f_current_date, f_end_date)

    def test_check_single_flight(self):
        checked_flight = self.flight_service.get_cheapest_checked_flight(self.request_data)
        assert checked_flight is not None
        assert checked_flight['flights_checked']