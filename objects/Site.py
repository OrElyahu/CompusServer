from typing import List

from objects.Graph import Graph


class Site:
    def __init__(self, site_name, graphs: List[Graph]):
        self._site_name = site_name
        self._graphs = graphs if graphs is not None else []

    def get_site_name(self):
        return self._site_name

    def set_site_name(self, site_name):
        self._site_name = site_name

    def get_graphs(self):
        return self._graphs

    def set_graphs(self, graphs: List[Graph]):
        self._graphs = graphs

    def add_graph(self, graph: Graph):
        for g in self._graphs:
            if g.__eq__(graph):
                return
        self._graphs.append(graph)

    def remove_graph(self, graph_name):
        self._graphs = [graph for graph in self._graphs if graph.get_graph_name() != graph_name]

    def __eq__(self, obj):
        return isinstance(obj, Site) and self._site_name == obj._site_name
