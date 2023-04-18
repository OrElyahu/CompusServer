class Area:
    def __init__(self, area_id, area_map, wp_ids: set = None):
        self._area_id = area_id
        self._area_map = area_map
        self._wp_ids = wp_ids or set()

    def get_area_id(self):
        return self._area_id

    def set_area_id(self, area_id):
        self._area_id = area_id

    def get_area_map(self):
        return self._area_map

    def set_area_map(self, area_map):
        self._area_map = area_map

    def get_wp_ids(self):
        return self._wp_ids

    def set_wp_ids(self, wp_ids):
        self._wp_ids = wp_ids

    def add_wp_id(self, wp_id):
        self._wp_ids.add(wp_id)

    def remove_wp_id(self, wp_id):
        self._wp_ids.discard(wp_id)

    def __eq__(self, obj):
        return isinstance(obj, Area) and self._area_id == obj._area_id
