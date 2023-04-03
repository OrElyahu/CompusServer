import pickle

from typing import List


class Waypoint:
    def __init__(self, waypoint_id: str = None, poi: str = None):
        self._id = waypoint_id
        self._poi = poi

    def get_id(self):
        return self._id

    def set_id(self, waypoint_id):
        self._id = waypoint_id

    def get_poi(self):
        return self._poi

    def set_poi(self, poi):
        self._poi = poi

    def __str__(self):
        return "Waypoint{" + \
               "id='" + str(self._id) + '\'' + \
               ", poi=" + str(self._poi) + \
               '}'

    def __eq__(self, obj):
        return isinstance(obj, Waypoint) and obj._id == self._id

    # serialization
    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(serialized_data):
        return pickle.loads(serialized_data)
