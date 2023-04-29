import pickle

from enum import Enum

from typing import List


class A11y(Enum):
    WALK = 0
    WHEELCHAIR = 1


class Path:
    def __init__(self, time: int, a11y: List[A11y] = None):
        self._time = time
        self._a11y = a11y or [A11y.WALK, A11y.WHEELCHAIR]

    def get_time(self) -> int:
        return self._time

    def set_time(self, time:int):
        self._time = time

    def get_a11y(self):
        return self._a11y

    def set_a11y(self, a11y):
        self._a11y = a11y

    def __str__(self):
        a11y_str = ', '.join([str(a).split('.')[1] for a in self._a11y])  # turn A11y.WALKABLE into WALKABLE
        return f'Path: time={self._time}, a11y=[{a11y_str}]'

    def serialize(self):
        return {
            'time': self.get_time(),
            'a11y': [a11y.value for a11y in self._a11y]
        }
