from typing import List, Dict
from google.type.latlng_pb2 import LatLng
from objects.Graph import Graph


class Site:
    def __init__(self, site_name, graphs: List[Graph], entrances: Dict[str, LatLng]):
        self._site_name = site_name
        self._graphs = graphs or []
        self._entrances = entrances or {}

    def get_site_name(self):
        return self._site_name

    def set_site_name(self, site_name):
        self._site_name = site_name

    def get_graphs(self) -> List[Graph]:
        return self._graphs

    def set_graphs(self, graphs: List[Graph]):
        self._graphs = graphs

    def get_entrances(self) -> Dict[str, LatLng]:
        return self._entrances

    def set_entrances(self, entrances: Dict[str, LatLng]):
        self._entrances = entrances

    def add_entrance(self, wp_id, latlng: LatLng):
        if wp_id not in self._entrances:
            self._entrances[wp_id] = latlng

    def delete_entrance(self, wp_id):
        self._entrances.pop(wp_id, None)

    def add_graph(self, graph: Graph):
        for g in self._graphs:
            if g.__eq__(graph):
                return
        self._graphs.append(graph)

    def remove_graph(self, graph_name):
        self._graphs = [graph for graph in self._graphs if graph.get_graph_name() != graph_name]

    def __dict__(self):
        return {
            'entrances': self._entrances
        }

    def __eq__(self, obj):
        return isinstance(obj, Site) and self._site_name == obj._site_name

    def __str__(self):
        parts = {'Entrances': '\n'.join([f'wp_id: {wp}, {str(latlng)}' for wp, latlng in self._entrances.items()]),
                 'Graphs': '\n'.join([str(graph) for graph in self._graphs])}
        parts_str = '\n'.join([f'{key}:\n{value}' for key, value in parts.items()])
        return f'Site: {self._site_name} \n{parts_str}'

    def serialize(self):
        return {
            'site_name': self.get_site_name(),
            'graphs': [graph.serialize() for graph in self._graphs],
            'entrances': self._entrances
        }

    def deserialize(self, data):
        self._site_name = data['site_name']
        self._graphs = []
        for graph_data in data['graphs']:
            val = Graph('', [], {}, {}, {}, {})
            val.deserialize(graph_data)
            self._graphs.append(val)
        self._entrances = {k: LatLng(**v) for k, v in data['entrances'].items()}
