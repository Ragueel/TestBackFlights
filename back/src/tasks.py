from celery import shared_task
from src.repository.flights_repository import FlightsRepository
from .services.flight_services.flights_service import FlightsService, FlightGetSerivce, FlightValidatorService, FlightRequestData
from celery.utils.log import get_task_logger
import datetime
logger = get_task_logger(__name__)

def get_request_data(flight_from, flight_to):
    current_date = datetime.date.today() 
    end_date = current_date + datetime.timedelta(1)

    date_format = '%d/%m/%Y'

    f_current_date = current_date.strftime(date_format)
    f_end_date = end_date.strftime(date_format)
    request_data = FlightRequestData(flight_from, flight_to,f_current_date, f_end_date)
    return request_data

@shared_task(bind=True, name='collect_flights', max_retries=3,soft_time_limit=9000)
def collect_flights(self):
    ala_tse = get_request_data('ALA','TSE')
    tse_ala = get_request_data('TSE','ALA')
    ala_mow = get_request_data('ALA','MOW')
    ala_cit = get_request_data('ALA','CIT')
    cit_ala = get_request_data('CIT','ALA')
    tse_mow = get_request_data('TSE','MOW')
    tse_led = get_request_data('TSE','LED')
    led_tse = get_request_data('LED','TSE')

    flight_service = FlightsService(FlightGetSerivce(), FlightValidatorService(), FlightsRepository())

    logger.info('Collecting data')
    flight_service.collect_data_from_server([ala_tse, tse_ala, ala_mow, ala_cit, cit_ala, tse_mow, tse_led, led_tse])

