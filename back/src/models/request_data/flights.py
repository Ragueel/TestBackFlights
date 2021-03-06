import json

class BaseJsonObject:

    def to_json(self):
        return json.dumps( self.__dict__)

class FlightRequestData(BaseJsonObject):

    def __init__(self, flight_from, flight_to, start_date, end_date) -> None:
        self.flight_from = flight_from
        self.flight_to = flight_to
        self.start_date = start_date
        self.end_date = end_date
        

class FlightValidationData(BaseJsonObject):
    def __init__(self, booking_token, pnum, currency, adults) -> None:
        self.booking_token = booking_token
        self.pnum = pnum
        self.currency = currency
        self.adults = adults

class CheapestFlightResponse(BaseJsonObject):

    def __init__(self, cheapest_flight, all_flights) -> None:
        self.cheapest_flight = cheapest_flight
        self.all_flights = all_flights

