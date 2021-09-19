from celery import shared_task
from .services.flight_services.flights_service import FlightsService, FlightGetSerivce, FlightValidatorService, FlightRequestData
from celery.utils.log import get_task_logger
import datetime
logger = get_task_logger(__name__)

@shared_task(bind=True, name='collect_flights', max_retries=3,soft_time_limit=9000)
def collect_flights(self):
    current_date = datetime.date.today() 
    end_date = current_date + datetime.timedelta(1)

    self.date_format = '%d/%m/%Y'

    f_current_date = current_date.strftime(self.date_format)
    f_end_date = end_date.strftime(self.date_format)
    request_data = FlightRequestData('ALA', 'TSE',f_current_date, f_end_date)
    
    flight_service = FlightsService(FlightGetSerivce(), FlightValidatorService())

    logger.info('Collecting data')
    flight_service.collect_data_from_server([request_data])

