from src.models.request_data.flights import FlightValidationData
from . import API_URLS
from time import sleep
import requests

class FlightValidatorService(object):

    def get_flight_check(self, flight_check_data: FlightValidationData)->dict:
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

    def validate_until_checked(self, flight_check_data: FlightValidationData)->dict:
        flight_check = self.get_flight_check(flight_check_data)

        while not flight_check['flights_checked'] or flight_check['flights_invalid']:
            sleep(20)
            flight_check = self.get_flight_check(flight_check_data)

        return flight_check
