import Waypoint
import Path
from enum import Enum


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Area:

    def __init__(self, area_id: int, wps: dict = None, paths: dict = None):
        self._area_id = area_id
        self._wps = dict if wps is not None else {}
        self._paths = paths if paths is not None else {}

    def get_area_id(self):
        return self._area_id

    def set_area_id(self, area_id: int):
        self._area_id = area_id

    def get_waypoints(self):
        return self._wps

    def set_waypoints(self, wps: dict):
        self._wps = wps

    def create_wp(self, wp):
        if wp not in self._wps.keys():
            self._wps[wp] = ([None, None, None, None])

    def add_oneway_connection(self, wp_src_id, wp_dst_id, direction, path: Path):
        src_ref = self._wps.get(wp_src_id)
        dst_ref = self._wps.get(wp_dst_id)
        if src_ref and dst_ref is not None:
            src_ref[direction] = path

    def add_connection(self, wp_src_id, wp_dst_id, direction, path: Path):
        self.add_oneway_connection(wp_src_id, wp_dst_id, direction, path)
        self.add_oneway_connection(wp_dst_id, wp_src_id, (direction + 2) % len(Direction), path)

