from falcon import testing
import datetime
from src.services.flight_services.flights_service import FlightGetSerivce, FlightRequestData


class TestFlightCacheService(testing.TestCase):

    def setUp(self):
        self.flight_cache_service = FlightGetSerivce()
        current_date = datetime.date.today() 
        end_date = current_date + datetime.timedelta(1)

        date_format = '%d/%m/%Y'

        f_current_date = current_date.strftime(date_format)
        f_end_date = end_date.strftime(date_format)
        request_data = FlightRequestData('ALA', 'TSE',f_current_date, f_end_date)
        self.request_data = request_data

    def test_get_flights(self):
        
        response = self.flight_cache_service.get_flights(self.request_data)
        
        assert response is not None 
        assert response.get('data', None) is not None
        assert len(response['data']) > 0

        for flight in response['data']:
            d_time = datetime.datetime.fromtimestamp(flight['dTimeUTC']).date()
            a_time = datetime.datetime.fromtimestamp(flight['aTimeUTC']).date()

            assert current_date <= d_time <= end_date

    def test_get_cheapest_flight(self):
        cheapest_flight = self.flight_cache_service.get_cheapest_flight(self.request_data)
        assert cheapest_flight is not None
        response = self.flight_cache_service.get_flights(self.request_data)

        data = response['data']

        min_price = 99999999999
        cheap_flight = {}
        for flight in data:
            if flight['price'] < min_price:
                cheap_flight = flight
                min_price = flight['price']

        assert cheap_flight['price'] == cheapest_flight['price']

        

