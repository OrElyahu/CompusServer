import Waypoint


class Area:
    """'
    _area_id typed str
    _wps typed dict(str:Waypoint) {'202':Waypoint}
    ''"""
    def __init__(self, area_id: str, wps: dict = None):
        self._area_id = area_id
        self._wps = wps if wps is not None else {}

    def get_area_id(self):
        return self._area_id

    def set_area_id(self, area_id: str):
        self._area_id = area_id

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
        return self._area_id == obj.get_area_id
