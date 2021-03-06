""" 
Provides the main interfaces for the OC Transpo API
"""

import logging
from octranspolib.protocol import Api
from octranspolib import model
from octranspolib import parser

class Client(object):
    """
    Main client class. It will interact with the OC Transpo API and expose interfaces
    """

    def __init__(self, app_id, api_key):
        """
        Contructor will initialize a new client object.

        :param app_id: This is the application ID, you should send with each API request.
        :type app_id: str

        :param api_key: These are application keys used to authenticate requests.
        :type api_key: str

        """

        # Initialize the logger
        self.log = logging.getLogger('{0.__module__}.{0.__name__})'.format(self.__class__))

        self.protocol = Api(app_id=app_id, api_key=api_key)

    def get_route_summary_for_stop(self, stop_number):
        """
        Retrieves the routes for a given stop number

        https://api.octranspo1.com/v1.2/GetRouteSummaryForStop

        :param stop_number: Required. 4-digit stop number found on bus stops.
        :type stop_number int

        :return :class:`octranspolib.model.StopSummary` object
        :rtype: :class:`StopSummary`
        """

        raw = self.protocol.post('/GetRouteSummaryForStop', stopNo=stop_number)
        json_obj = parser.StopSummary(raw.content).parse()

        return model.StopSummary.deserialize(json_obj)


    def get_next_trips_for_stop(self, stop_number, route_number):
        """
        Retrieves next three trips on the route for a given stop number

        https://api.octranspo1.com/v1.2/GetNextTripsForStop

        :param route_number: Required. Bus route number.
        :param stop_number: Requited. 4-digit stop number found on bus stops.

        :return :class:`octranspolib.model.NextTrips` object
        :rtype: :class:`NextTrips`
        """

        raw = self.protocol.post('/GetNextTripsForStop', stopNo=stop_number, routeNo=route_number)
        json_obj = parser.NextTrips(raw.content).parse()

        return model.NextTrips.deserialize(json_obj)


    def get_next_trips_for_stop_all_routes(self, stop_number, format=None):
        """
        Retrieves next three trips for all routes for a given stop number.

        https://api.octranspo1.com/v1.2/GetNextTripsForStop

        :param route_number: Required. Bus route number.
        :param stop_number: Requited. 4-digit stop number found on bus stops.

        :return :class:`octranspolib.model.NextTrips` object
        :rtype: :class:`NextTrips`
        """

        raw = self.protocol.post('/GetNextTripsForStopAllRoutes', stopNo=stop_number)
        json_obj = parser.NextTrips(raw.content).parse()

        return model.NextTrips.deserialize(json_obj)