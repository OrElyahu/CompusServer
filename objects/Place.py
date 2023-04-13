from objects.Area import Area


class Place:
    def __init__(self, place_name: str, areas: dict = None):
        self._place_name = place_name
        self._areas = areas if areas is not None else {}

    def get_place_name(self):
        return self._place_name

    def get_areas(self):
        return self._areas

    def set_place_name(self, place_name: str):
        self._place_name = place_name

    def set_areas(self, areas: dict):
        self._areas = areas

    def add_area(self, area_id: str, area: Area):
        if area_id not in self._areas:
            self._areas[area_id] = area

    def remove_area(self, area_id):
        self._areas.pop(area_id, None)

    def __eq__(self, obj):
        return self._place_name == obj.get_place_name()
