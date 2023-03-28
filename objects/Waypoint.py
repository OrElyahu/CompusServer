import pickle

from typing import List
from enum import Enum


class Direction(Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'


class Waypoint:
    def __init__(self, waypoint_id: str = None, neighbors_views=None):
        self._id = waypoint_id
        self._neighbors_views = neighbors_views if neighbors_views is not None \
            else {Direction.UP: None, Direction.DOWN: None, Direction.LEFT: None, Direction.RIGHT: None}

    def getId(self):
        return self._id

    def setId(self, waypoint_id):
        self._id = waypoint_id

    def get_neighbor_views(self):
        return self._neighbors_views

    def set_neighbors_views(self, neighbors_ids):
        self._neighbors_views = neighbors_ids if neighbors_ids is not None else self._neighbors_views

    def set_neighbor_view(self, neighbor_id, direction):
        if direction in self._neighbors_views.keys():
            self._neighbors_views[direction] = neighbor_id

    def __str__(self):
        return "Waypoint{" + \
               "id='" + str(self._id) + '\'' + \
               ", neighborIds=" + str(self._neighbors_views) + \
               '}'

    # serialization
    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(serialized_data):
        return pickle.loads(serialized_data)
