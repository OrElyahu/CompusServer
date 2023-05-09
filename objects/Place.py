from typing import List
from objects.Area import Area


class Place:
    def __init__(self, place_name: str, areas: List[Area] = None):
        self._place_name = place_name
        self._areas = areas or []

    def get_place_name(self):
        return self._place_name

    def get_areas(self):
        return self._areas

    def set_place_name(self, place_name: str):
        self._place_name = place_name

    def set_areas(self, areas: List[Area]):
        self._areas = areas

    def add_area(self, area: Area):
        for a in self._areas:
            if a.__eq__(area):
                return
        self._areas.append(area)

    def remove_area(self, area_id):
        self._areas = [area for area in self._areas if area.get_area_id() != area_id]

    def __eq__(self, obj):
        return isinstance(obj, Place) and self._place_name == obj._place_name

    def __str__(self):
        if not self._areas:
            return f'Place: {self._place_name} \nAreas: None'
        areas_str = '\n'.join([str(area) for area in self._areas])
        return f'Place: {self._place_name} \nAreas:\n{areas_str}'

    def serialize(self):
        return {'place_name': self.get_place_name(),
                'areas': self.get_areas()}

    def deserialize(self, data):
        self._place_name = data['place_name']
        self._areas = []
        for area in data['areas']:
            val = Area('', '')
            val.deserialize(area)
            self._areas.append(val)
