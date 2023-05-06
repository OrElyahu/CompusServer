import heapq
from typing import List

from objects.Path import Path, A11y
from objects.Place import Place
from objects.Utils import Direction, opposite_dir
from objects.Waypoint import Waypoint


class Graph:

    def __init__(self, graph_name, places: List[Place], wps: dict = None, wp_neighs: dict = None,
                 paths: dict = None, poi_wps: dict = None):
        self._graph_name = graph_name
        self._places = places or []
        self._wps = wps or {}
        self._wp_neighs = wp_neighs or {}
        self._paths = paths or {}
        self._poi_wps = poi_wps or {}

    def get_graph_name(self):
        return self._graph_name

    def set_graph_name(self, graph_name):
        self._graph_name = graph_name

    def get_places(self):
        return self._places

    def set_places(self, places: List[Place]):
        self._places = places

    def get_wps(self):
        return self._wps

    def set_wps(self, wps: dict):
        self._wps = wps

    def get_wp_neighs(self):
        return self._wp_neighs

    def set_wp_neighs(self, wp_neighbors: dict):
        self._wp_neighs = wp_neighbors

    def get_paths(self):
        return self._paths

    def set_paths(self, paths: dict):
        self._paths = paths

    def get_poi_wps(self):
        return self._poi_wps

    def set_poi_wps(self, poi_wps: dict):
        self._poi_wps = poi_wps

    def add_poi_wp(self, poi, wp_id):
        if poi not in self._poi_wps:
            self._poi_wps[poi] = wp_id

    def remove_poi_wp(self, poi):
        self._poi_wps.pop(poi, None)

    def add_place(self, place: Place):
        for p in self._places:
            if p.__eq__(place):
                return
        self._places.append(place)

    def remove_place(self, place_name):
        self._places = [place for place in self._places if place.get_place_name() != place_name]

    def add_wp(self, wp: Waypoint):
        _id = wp.get_id()
        if _id not in self._wps:
            self._places[wp.get_place_id()].get_areas()[wp.get_area_id()].add_wp_id(_id)
            self._wps[_id] = wp
            self._wp_neighs[_id] = [None, None, None, None]

    def remove_wp(self, wp_id):
        if wp_id in self._wps:
            wp = self._wps[wp_id]
            self._places[wp.get_place_id()].get_areas()[wp.get_area_id()].remove_wp_id(wp_id)
            [self.del_connection(wp_id, _id) for _id in self._wp_neighs[wp_id] if _id]
            self._wps.pop(wp_id, None)

    def add_oneway_connection(self, wp_src_id, wp_dst_id, direction: Direction, path: Path):
        if wp_src_id and wp_dst_id in self._wp_neighs:
            self._wp_neighs[wp_src_id][direction.value] = wp_dst_id
            self._paths[wp_src_id + '_' + wp_dst_id] = path

    def add_connection(self, wp_src_id, wp_dst_id, direction: Direction, path: Path):
        if wp_src_id and wp_dst_id in self._wp_neighs:
            self.add_oneway_connection(wp_src_id, wp_dst_id, direction, path)
            self.add_oneway_connection(wp_dst_id, wp_src_id, opposite_dir(direction), path)

    def del_oneway_connection(self, wp_src_id, wp_dst_id):
        if wp_src_id in self._wp_neighs:
            self._paths.pop(wp_src_id + '_' + wp_dst_id, None)
            src_neighs = self._wp_neighs[wp_src_id]
            try:
                src_neighs[src_neighs.index(wp_dst_id)] = None
            except ValueError:
                pass

    def del_connection(self, wp_src_id, wp_dst_id):
        self.del_oneway_connection(wp_src_id, wp_dst_id)
        self.del_oneway_connection(wp_dst_id, wp_src_id)

    """'
    @Input: 2 WPs ids : start_id, end_id
    @Output: a list of WPs from start to the end with the shortest time estimation,
            None if path doesn't exist
    
    This algorithm try to find the quickest path to reach from start WP to end WP.
    It begins with the start WP, and maps all of its neighbors to the distance between the start and the neighbors.
    It continues with a loop until end WP is found. (Case not found - the algorithm will return None)
    ''"""

    def shortest_path(self, start_id, end_id, mode_of_transport: A11y = A11y.WALK):
        """'
            distances: a dictionary that assigns infinity value to each wp_id, except the start_id sets to zero.
            heap: is a priority queue to all the wp that haven't been visited, and their distance from the start WP.
            visited: is a set contain all the visited WPs.
        ''"""
        # TODO: Change stairs to WALK only & Not accessible for WHEELCHAIR msg
        accessible_paths = {_id: path for _id, path in self._paths.items() if mode_of_transport in path.get_a11y()}
        distances = {_id: float('inf') for _id in self._wps.keys()}
        distances[start_id] = 0
        heap = [(0, start_id)]
        visited = set()

        """'
            While heap isn't empty there are still WP that can lead to shorter path.
            Case WP is in visited set - we skip to the next iteration.
        ''"""
        while heap:
            (curr_distance, curr_wp_id) = heapq.heappop(heap)
            if curr_wp_id in visited:
                continue

            visited.add(curr_wp_id)

            """'
                If we reached to the end WP, according to heap - the priority is the shortest,
                therefore this is the quickest path from start to end.
                Let build path from the end, to the start, using the distance dictionary, reverse it and
                return the list.
            ''"""
            if curr_wp_id == end_id:
                path = []
                while curr_wp_id != start_id:
                    path.append(self._wps[curr_wp_id])
                    curr_wp_id = distances[curr_wp_id][1]
                path.append(self._wps[start_id])
                path.reverse()
                return path

            """'
                Explore every neighbor of the current WP, and calculate their distances.
                If the distance is shorter from what appears in the distance dictionary - replace it, and
                add it to heap.
            ''"""
            neigh_ids = self._wp_neighs[curr_wp_id]
            for _id in neigh_ids:
                path_id = f'{curr_wp_id}_{_id}'
                if _id and _id not in visited and path_id in accessible_paths:
                    cur_dis = distances[curr_wp_id]
                    if type(cur_dis) is tuple:
                        cur_dis = cur_dis[0]
                    new_distance = cur_dis + accessible_paths[path_id].get_time()
                    if new_distance < distances[_id]:
                        distances[_id] = (new_distance, curr_wp_id)
                        heapq.heappush(heap, (new_distance, _id))

        """'
            Case heap is empty and end WP wasn't found - return None
        ''"""
        return None

    def __dict__(self):
        return {
            'wp_neighs': self.get_wp_neighs(),
            'poi_wps': self.get_poi_wps()
        }

    def __eq__(self, obj):
        return isinstance(obj, Graph) and self._graph_name == obj._graph_name

    def __str__(self):
        parts = {'Places': '\n'.join([str(place) for place in self._places]),
                 'Waypoints dict': '\n'.join([f'wp_id: {wp_id}, {str(wp)}' for wp_id, wp in self._wps.items()]),
                 'Paths dict': '\n'.join([f'path_id: {p_id}, {str(path)}' for p_id, path in self._paths.items()]),
                 'Waypoint Neighbors': '\n'.join([f'Neighbors: {wp_id}: {neighs}' for wp_id, neighs in self._wp_neighs.items()]),
                 'POI to Waypoints': '\n'.join([f'POI: {poi_id}: {wp_ids}' for poi_id, wp_ids in self._poi_wps.items()])}
        parts_str = '\n'.join([f'{key}:\n{value}' for key, value in parts.items()])

        return f'Graph: {self._graph_name} \n{parts_str}'

    def serialize(self):
        return {
            'graph_name': self.get_graph_name(),
            'places': self.get_places(),
            'wps': self.get_wps(),
            'wp_neighs': self.get_wp_neighs(),
            'paths': self.get_paths(),
            'poi_wps': self.get_poi_wps()
            }

    def deserialize(self, data):
        self._graph_name = data['graph_name']
        self._places = []
        for place in data['places']:
            val = Place('')
            val.deserialize(place)
            self._places.append(val)
        self._wps = {}
        for k, v in data['wps'].items():
            val = Waypoint()
            val.deserialize(v)
            self._wps[k] = val
        self._wp_neighs = data['wp_neighs']
        self._paths = {}
        for k, v in data['paths'].items():
            val = Path(0)
            val.deserialize(v)
            self._paths[k] = val
        self._poi_wps = data['poi_wps']


        # self._places = data['places']
        # self._wps = data['wps']
        # self._paths = data['paths']
        # self._poi_wps = data['poi_wps']