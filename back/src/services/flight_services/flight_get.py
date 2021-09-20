
from src.models.request_data.flights import FlightValidationData, FlightRequestData, CheapestFlightResponse
from . import API_URLS
from src.config import BaseConfig
import requests

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
            'partner': BaseConfig.SKY_API_PARTNER
        }
        response = requests.get(end_point, params=params)

        if response.status_code != 200:
            raise Exception('Exception while getting flights: {}'.format(response.json()))

        return response.json()

    def get_cheapest_flight(self, flight_request_data: FlightRequestData)->CheapestFlightResponse:
        flights = self.get_flights(flight_request_data)

        data = flights['data']

        cheapest_flight = self.get_flight_with_min_price(data)

        return CheapestFlightResponse(cheapest_flight, flights)

    def get_flight_with_min_price(self, flights_data: list):
        cheapest_flight = min(flights_data, key=lambda x:x['price'])
        return cheapest_flight