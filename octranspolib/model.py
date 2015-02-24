
import logging
from octranspolib.attributes import (META, SUMMARY, DETAILED, Attribute, EntityCollection)
class BaseEntity(object):
    """
    A base class for all entities in the system
    """

    def __init__(self, **kwargs):
        self.log = logging.getLogger('{0.__module__}.{0.__name__}'.format(self.__class__))
        self.from_dict(kwargs)

    def from_dict(self, d):
        """
        Populates this object from specified dict.

        Only defined attributes will be set; warnings will be logged for invalid attributes.
        """
        for (k, v) in d.items():
            # Only set defined attributes.
            if hasattr(self.__class__, k):
                self.log.debug("Setting attribute `{0}` [{1}] on entity {2} with value {3!r}".format(k, getattr(self.__class__, k).__class__.__name__, self, v))
                try:
                    setattr(self, k, v)
                except AttributeError as x:
                    raise AttributeError("Could not find attribute `{0}` on entity {1}, value: {2!r}.  (Original: {3!r})".format(k, self, v, x))
            else:
                self.log.warning("No such attribute {0} on entity {1}".format(k, self))

    @classmethod
    def deserialize(cls, v):
        """
        Creates a new object based on serialized (dict) struct.
        """
        o = cls()
        o.from_dict(v)
        return o

    def __repr__(self):
        attrs = []
        if hasattr(self.__class__, 'id'):
            attrs.append('id={0}'.format(self.id))
        if hasattr(self.__class__, 'name'):
            attrs.append('name={0!r}'.format(self.name))
        if hasattr(self.__class__, 'resource_state'):
            attrs.append('resource_state={0}'.format(self.resource_state))

        return '<{0} {1}>'.format(self.__class__.__name__, ' '.join(attrs))

class Trip(BaseEntity):
    trip_destination = Attribute(unicode, (DETAILED,))
    trip_start_time = Attribute(unicode, (DETAILED,))
    adjusted_schedule_time = Attribute(unicode, (DETAILED,))
    adjustment_age = Attribute(unicode, (DETAILED,))
    last_trip_of_schedule = Attribute(unicode, (DETAILED,))
    bus_type = Attribute(unicode, (DETAILED,))
    latitude = Attribute(unicode, (DETAILED,))
    longitude = Attribute(unicode, (DETAILED,))
    gps_speed = Attribute(unicode, (DETAILED,))


class Route(BaseEntity):
    """
    Information about a Route
    """
    number = Attribute(unicode, (DETAILED,))  #:
    direction_id = Attribute(unicode, (DETAILED,))  #:
    direction = Attribute(unicode, (DETAILED,))  #:
    heading = Attribute(unicode, (DETAILED,))  #:


class StopSummary(BaseEntity):
    """
    Information about the Routes at a stop
    """
    number = Attribute(unicode, (META, DETAILED))  #: Numeric stop #.
    description = Attribute(unicode, (DETAILED))  #: The description of the stop
    routes = EntityCollection(Route, (DETAILED))  #: The routes for the stop

class NextTrips(BaseEntity):
    """
    Information about the next trips at a stop (and route).
    """

    number = Attribute(unicode, (META, DETAILED))  #: Numeric stop #.
    label = Attribute(unicode, (DETAILED))  #: The stop label
    routes = EntityCollection(Route, (DETAILED))  #: The routes for the stop





