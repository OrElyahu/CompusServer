import pickle

from typing import List


class Waypoint:
    def __init__(self, waypoint_id: str = None, neighbor_ids: List[str] = None):
        self._id = waypoint_id
        self._neighbor_ids = neighbor_ids if neighbor_ids is not None else []

    def getId(self):
        return self._id

    def setId(self, waypoint_id):
        self._id = waypoint_id

    def get_neighbor_ids(self):
        return self._neighbor_ids

    def setNeighborIds(self, neighbor_ids):
        self._neighbor_ids = neighbor_ids if neighbor_ids is not None else []

    def __str__(self):
        return "Waypoint{" + \
               "id='" + str(self._id) + '\'' + \
               ", neighborIds=" + str(self._neighbor_ids) + \
               '}'

    # serialization
    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(serialized_data):
        return pickle.loads(serialized_data)