from src.models.request_data.flights import FlightCheckData, FlightRequestData
import requests

class API_URLS:
    SKY_PICKER = 'https://api.skypicker.com'

class FlightsService(object):

    def __init__(self) -> None:
        # super().__init__()
        pass

    def collect_data_from_server(self) -> None:
        pass

        
class FlightValidatorService(object):

    def get_flight_validation(self, flight_check_data: FlightCheckData):
        end_point = '/'.join(API_URLS.SKY_PICKER, 'api/v0.1/check_flights')
        params = {
            'boooking_token' : flight_check_data.booking_token,
            'pnum': flight_check_data.pnum,
            'currency': flight_check_data.currency,
            'adults': flight_check_data.adults,
            'children': 0,
            'infants': 0
        }
        response = requests.get(end_point, params=params).json()

        return response



class FlightGetSerivce(object):

    def __init__(self) -> None:
        super().__init__()

    def get_flights(self, flight_request_data: FlightRequestData)->dict:
        end_point = '/'.join([API_URLS.SKY_PICKER, 'flights'])
        params = {
            'fly_from': flight_request_data.flight_from,
            'fly_to': flight_request_data.flight_to,
            'date_from': flight_request_data.start_date,
            'date_to': flight_request_data.end_date,
            'adults': 1,
            'partner': 'ragueelnomad'
        }
        response = requests.get(end_point, params=params).json()
        return response

    def get_cheapest_flight(self, flight_request_data: FlightRequestData)->dict:
        flights = self.get_flights(flight_request_data)

        data = flights['data']

        cheapest_flight = min(data, key=lambda x:x['price'])

        return cheapest_flight