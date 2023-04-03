from objects.Area import Area


class Graph:

    def __init__(self, areas: list):
        self._areas = areas if areas is not None else []

    def get_areas(self):
        return self._areas

    def set_areas(self, areas: list):
        self._areas = areas

    def add_area(self, area: Area):
        if area not in self._areas:
            self._areas.append(area)


