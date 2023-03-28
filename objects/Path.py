import pickle

from enum import Enum

from typing import List


class A11y(Enum):
    WALKABLE = 0
    WHEEL_CHAIR = 1


class Path:
    def __init__(self, time=None, a11y: List[A11y] = None):
        self._time = time
        self._a11y = a11y if a11y is not None else [A11y.WALKABLE, A11y.WHEEL_CHAIR]

    def get_time(self):
        return self._time

    def set_time(self, time):
        self._time = time

    def get_a11y(self):
        return self._a11y

    def set_a11y(self, a11y):
        self._a11y = a11y

    # serialization
    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(serialized_data):
        return pickle.loads(serialized_data)
