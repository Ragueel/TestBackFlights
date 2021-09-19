from falcon import testing
import datetime
from src.services.flight_services.flights_service import FlightGetSerivce, FlightRequestData, FlightValidatorService, FlightValidationData

class TestFlightValidatorService(testing.TestCase):

    def setUp(self):
        self.flight_cache_service = FlightGetSerivce()
        self.flight_validator = FlightValidatorService()
        current_date = datetime.date.today() 
        end_date = current_date + datetime.timedelta(1)

        self.date_format = '%d/%m/%Y'

        f_current_date = current_date.strftime(self.date_format)
        f_end_date = end_date.strftime(self.date_format)
        self.request_data = FlightRequestData('ALA', 'TSE',f_current_date, f_end_date)

        cheapest_flight = self.flight_cache_service.get_cheapest_flight(self.request_data).cheapest_flight
        self.data = cheapest_flight

    def test_get_validation_data(self):
        flight_validation_data = FlightValidationData(self.data['booking_token'], 1, 'EUR',1)
        validation_response = self.flight_validator.get_flight_check(flight_validation_data)
        assert validation_response is not None
        assert self.data['booking_token'] == validation_response['booking_token'] 

    def test_until_checked(self):
        flight_validation_data = FlightValidationData(self.data['booking_token'], 1, 'EUR',1)
        validation_response = self.flight_validator.validate_until_checked(flight_validation_data)

        assert validation_response is not None
        assert validation_response['flights_checked'] or validation_response['flights_invalid']

        
