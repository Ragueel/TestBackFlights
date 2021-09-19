from typing import List
from src.models.request_data.flights import FlightValidationData, FlightRequestData
from celery import shared_task
from celery.utils.log import get_task_logger
from .flight_validator import FlightValidatorService
from .flight_get import FlightGetSerivce
from src.repository.flights_repository import FlightsRepository
from sqlalchemy.orm import Session
from src.celery import celery_controller
import json

logger = get_task_logger(__name__)

@shared_task(bind=True,name='find_cheapest_flight_schedule')
def find_cheapest_flight_schedule(self, flight_request_data):
    flight_request_data = json.loads(flight_request_data)
    flight_request_data = FlightRequestData(**flight_request_data)
    
    flight_service = FlightsService(FlightGetSerivce(), FlightValidatorService(), FlightsRepository())
    cheapest_flight = flight_service.get_cheapest_checked_flight(flight_request_data)

    flight_data = {
        'flight_from': flight_request_data.flight_from,
        'flight_to': flight_request_data.flight_to,
        'price': cheapest_flight['total']
    }
    
    flight_service.add_flight(celery_controller.session_maker(), flight_data)        
    logger.info('Cached into database')
    return cheapest_flight

class FlightsService(object):

    def __init__(self, flight_get_service : FlightGetSerivce, flight_validator_service: FlightValidatorService, flights_repository: FlightsRepository) -> None:
        self.flight_get_service = flight_get_service
        self.flight_validator_service = flight_validator_service
        self.flights_repository = flights_repository

    def collect_data_from_server(self, flight_requests: list) -> None:
        for flight in flight_requests:
            find_cheapest_flight_schedule.delay(flight.to_json())

    def get_all_flights(self, session: Session):
        return self.flights_repository.get_flights(session)

    def add_flight(self, session, flight):
        found_flight = self.flights_repository.get_flight(session, flight['flight_from'], flight['flight_to'])
        if found_flight is not None:
            found_flight.price = flight['price']
            self.flights_repository.update_flight_price(session, found_flight)
            return

        self.flights_repository.add_flight(session, flight)

    def get_cheapest_checked_flight(self, flight_request_data: FlightRequestData)->dict:
        flight_data = self.flight_get_service.get_cheapest_flight(flight_request_data)

        all_flights = flight_data.all_flights
        cheapest_flight = flight_data.cheapest_flight

        flight_validation_data = FlightValidationData(cheapest_flight['booking_token'],1,'EUR',1)
        validated_flight_data = self.flight_validator_service.validate_until_checked(flight_validation_data)

        while validated_flight_data['flights_invalid']:
            all_flights['data']= all_flights['data'].remove(cheapest_flight)

            if len(all_flights['data']) == 0:
                raise Exception('No available flights were found')

            cheapest_flight = self.flight_get_service.get_flight_with_min_price(all_flights['data'])
            flight_validation_data = FlightValidationData(cheapest_flight['booking_token'],1,'EUR',1)
            validated_flight_data = self.flight_validator_service.validate_until_checked(flight_validation_data)

        return validated_flight_data

        