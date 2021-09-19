from typing import List
from src.models.request_data.flights import FlightValidationData, FlightRequestData, CheapestFlightResponse
from time import sleep
import requests

class API_URLS:
    SKY_PICKER = 'https://api.skypicker.com'

class FlightValidatorService(object):

    def get_flight_check(self, flight_check_data: FlightValidationData):
        end_point = '/'.join([API_URLS.SKY_PICKER, 'api/v0.1/check_flights'])
        params = {
            'booking_token' : flight_check_data.booking_token,
            'pnum': flight_check_data.pnum,
            'currency': flight_check_data.currency,
            'adults': flight_check_data.adults,
            'children': 0,
            'infants': 0,
            'bnum': 0
        }

        response = requests.get(end_point, params=params)

        if response.status_code != 200:
            raise Exception('Exception while validating: {}'.format(response.json()))

        return response.json()

    def validate_until_checked(self, flight_check_data: FlightValidationData):
        flight_check = self.get_flight_check(flight_check_data)

        while not flight_check['flights_checked'] or flight_check['flights_invalid']:
            sleep(20)
            flight_check = self.get_flight_check(flight_check_data)

        return flight_check


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
        response = requests.get(end_point, params=params)


        if response.status_code != 200:
            raise Exception('Exception while getting flights: {}'.format(response.json()))

        return response.json()

    def get_cheapest_flight(self, flight_request_data: FlightRequestData)->CheapestFlightResponse:
        flights = self.get_flights(flight_request_data)

        data = flights['data']

        cheapest_flight = min(data, key=lambda x:x['price'])

        return CheapestFlightResponse(cheapest_flight, flights)



class FlightsService(object):

    def __init__(self, flight_get_service : FlightGetSerivce, flight_validator_service: FlightValidatorService) -> None:
        self.flight_get_service = flight_get_service
        self.flight_validator_service = flight_validator_service

    def collect_data_from_server(self, flight_requests: list) -> None:
        
        pass

        