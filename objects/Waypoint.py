from flask.json import JSONDecoder, JSONEncoder


class Waypoint:
    def __init__(self, _id: str = None, place_id=None, area_id=None):
        self._id = _id
        self._place_id = place_id
        self._area_id = area_id

    def get_id(self):
        return self._id

    def set_id(self, waypoint_id):
        self._id = waypoint_id

    def get_place_id(self):
        return self._place_id

    def set_place_id(self, place_id):
        self._place_id = place_id

    def get_area_id(self):
        return self._area_id

    def set_area_id(self, area_id):
        self._area_id = area_id

    def __str__(self):
        return f'Waypoint: id={self._id}, place={self._place_id}, area={self._area_id}'

    def __eq__(self, obj):
        return isinstance(obj, Waypoint) and obj._id == self._id

    def serialize(self):
        return {
            '_id': self.get_id(),
            '_place_id': self.get_place_id(),
            '_area_id': self.get_area_id(),
        }


# TODO: make generic encoder
class JsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Waypoint):
            return obj.serialize()
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)
