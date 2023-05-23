class Waypoint:
    def __init__(self, _id: str = None, place_id=None, area_id=None, pos=None):
        self._id = _id
        self._place_id = place_id
        self._area_id = area_id
        self._pos = pos

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

    def get_pos(self):
        return self._pos

    def set_pos(self, pos):
        self._pos = pos

    def __str__(self):
        return f'Waypoint: id={self._id}, place={self._place_id}, area={self._area_id}, pos = {self._pos}'

    def __eq__(self, obj):
        return isinstance(obj, Waypoint) and obj._id == self._id

    def serialize(self):
        return {
            'id': self.get_id(),
            'place_id': self.get_place_id(),
            'area_id': self.get_area_id(),
            'pos': self.get_pos()
        }

    def deserialize(self, data):
        self._id = data['id']
        self._place_id = data['place_id']
        self._area_id = data['area_id']
        self._pos = data.get('pos')

        # for k, v in data['paths'].items():
        #     val = Path(0)
        #     val.deserialize(v)
        #     self._paths[k] = val


