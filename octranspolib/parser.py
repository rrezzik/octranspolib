import lxml.etree as ET
from StringIO import StringIO


class StopSummary(object):

    ROOT_NODE = "GetRouteSummaryForStopResult"

    def __init__(self, data):
        self.data = data

    def route(self, node):
        route = {}
        route["number"] = node.xpath("//*[local-name() = 'RouteNo']")[0].text
        route["direction_id"] = node.xpath("//*[local-name() = 'DirectionID']")[0].text
        route["direction"] = node.xpath("//*[local-name() = 'Direction']")[0].text
        route["heading"] = node.xpath("//*[local-name() = 'RouteHeading']")[0].text

        return route

    # Call starts parsing the StopSummary xml response
    def parse(self):

        parser = ET.XMLParser(ns_clean=True)
        f = StringIO(self.data)
        tree = ET.parse(f, parser)

        stop_data = tree.xpath("//*[local-name() = 'GetRouteSummaryForStopResult']")[0]

        summary = {}
        summary["number"] = stop_data.xpath("//*[local-name() = 'StopNo']")[0].text
        summary["description"] = stop_data.xpath("//*[local-name() = 'StopDescription']")[0].text
        summary["routes"] = map(self.route, stop_data.xpath("//*[local-name() = 'Route']"))

        return summary


