import json
from enum import Enum
from flask.json import JSONEncoder

from objects.Area import Area
from objects.Graph import Graph
from objects.Path import Path
from objects.Place import Place
from objects.Report import Report
from objects.Site import Site
from objects.Waypoint import Waypoint


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class JsonEncoder(JSONEncoder):
    def default(self, obj):
        if any([isinstance(obj, c) for c in [Waypoint, Path, Site, Graph, Place, Area, Report]]):
            return obj.serialize()
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)


def opposite_dir(direction: Direction):
    return Direction((direction.value + 2) % len(Direction))


def get_config(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data
