from enum import Enum


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def opposite_dir(direction: Direction):
    return Direction((direction.value + 2) % len(Direction))



