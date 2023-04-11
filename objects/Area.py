import Waypoint


class Area:
    def __init__(self, area_name: str, area_map, wps: dict = None):
        self._area_name = area_name
        self._area_map = area_map
        self._wps = wps if wps is not None else {}

    def get_area_id(self):
        return self._area_name

    def set_area_id(self, area_id: str):
        self._area_name = area_id

    def get_area_map(self):
        return self._area_map

    def set_area_map(self, area_map):
        self._area_map = area_map

    def get_wps(self):
        return self._wps

    def set_wps(self, wps: dict):
        self._wps = wps

    def add_wp(self, wp: Waypoint):
        _id = wp.get_id
        if _id not in self._wps.keys():
            self._wps[_id] = wp

    def remove_wp(self, wp_id):
        if wp_id in self._wps.keys():
            del self._wps[wp_id]

    def __eq__(self, obj):
        return self._area_name == obj.get_area_id
