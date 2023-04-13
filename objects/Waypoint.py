import pickle


class Waypoint:
    def __init__(self, waypoint_id: str = None, poi: str = None, place_id=None, area_id=None):
        self._id = waypoint_id
        self._poi = poi
        self._place_id = place_id
        self._area_id = area_id

    def get_id(self):
        return self._id

    def set_id(self, waypoint_id):
        self._id = waypoint_id

    def get_poi(self):
        return self._poi

    def set_poi(self, poi):
        self._poi = poi

    def get_place_id(self):
        return self._place_id

    def set_place_id(self, place_id):
        self._place_id = place_id

    def get_area_id(self):
        return self._area_id

    def set_area_id(self, area_id):
        self._area_id = area_id

    def __eq__(self, obj):
        return isinstance(obj, Waypoint) and obj._id == self._id

    # serialization
    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(serialized_data):
        return pickle.loads(serialized_data)
