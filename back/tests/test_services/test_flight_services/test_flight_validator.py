from falcon import testing
import datetime
from src.services.flight_services.flights_service import FlightGetSerivce, FlightRequestData

class TestFlightValidatorService(testing.TestCase):

    def setUp(self):
        self.flight_cache_service = FlightGetSerivce()
        current_date = datetime.date.today() 
        end_date = current_date + datetime.timedelta(1)

        date_format = '%d/%m/%Y'

        f_current_date = current_date.strftime(date_format)
        f_end_date = end_date.strftime(date_format)
        request_data = FlightRequestData('ALA', 'TSE',f_current_date, f_end_date)

    def test_get_validation_data(self):
        pass