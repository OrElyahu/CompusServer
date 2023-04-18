class Area:
    def __init__(self, area_id, area_map, wps_ids: set = None):
        self._area_id = area_id
        self._area_map = area_map
        self._wps_ids = wps_ids if wps_ids is not None else set()

    def get_area_id(self):
        return self._area_id

    def set_area_id(self, area_id):
        self._area_id = area_id

    def get_area_map(self):
        return self._area_map

    def set_area_map(self, area_map):
        self._area_map = area_map

    def get_wps_ids(self):
        return self._wps_ids

    def set_wps_ids(self, wps_ids):
        self._wps_ids = wps_ids

    def add_wp_id(self, wp_id):
        self._wps_ids.add(wp_id)

    def remove_wp_id(self, wp_id):
        self._wps_ids.discard(wp_id)

    def __eq__(self, obj):
        return isinstance(obj, Area) and self._area_id == obj._area_id
