import falcon
from .base_resource import BaseResource
from .responses.base_response import BaseResponse
from src.services.flight_services.flights_service import FlightsService

class FlightsResource(BaseResource):
    def __init__(self, flights_service: FlightsService) -> None:
        self.flights_service = flights_service

    async def on_get(self, req, resp):
        flights = self.flights_service.get_all_flights(req.context.session)
        return self.ok(resp, BaseResponse(falcon.HTTP_200, [x.to_json() for x in flights]))