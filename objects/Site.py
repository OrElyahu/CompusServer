from typing import List

from google.type.latlng_pb2 import LatLng

from objects.Graph import Graph


class Site:
    def __init__(self, site_name, graphs: List[Graph], entrances: dict):
        self._site_name = site_name
        self._graphs = graphs or []
        self._entrances = entrances or {}

    def get_site_name(self):
        return self._site_name

    def set_site_name(self, site_name):
        self._site_name = site_name

    def get_graphs(self):
        return self._graphs

    def set_graphs(self, graphs: List[Graph]):
        self._graphs = graphs

    def get_entrances(self):
        return self._entrances

    def set_entrances(self, entrances: dict):
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

    def __eq__(self, obj):
        return isinstance(obj, Site) and self._site_name == obj._site_name
