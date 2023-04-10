from objects.Area import Area
import heapq

from objects.Path import Path
from objects.Utils import Direction, opposite_dir
from objects.Waypoint import Waypoint


class Graph:
    """'
    _areas list contain all areas
    _wps_neighs typed dict(str:list[4 strings]) {'202':['203',None,None,'204'] }
    _paths typed dict(str:path) {'205_204':Path}
    ''"""
    def __init__(self, areas: list, wps_neighs: dict = None, paths: dict = None):
        self._areas = areas if areas is not None else []
        self._wps_neighs = wps_neighs if wps_neighs is not None else {}
        self._paths = paths if paths is not None else {}

    def get_areas(self):
        return self._areas

    def set_areas(self, areas: list):
        self._areas = areas

    def get_wps_neighs(self):
        return self._wps_neighs

    def set_wps_neighs(self, wps_neighbors: dict):
        self._wps_neighs = wps_neighbors

    def get_paths(self):
        return self._paths

    def set_paths(self, paths: dict):
        self._paths = paths

    def add_area(self, area: Area):
        if area not in self._areas:
            self._areas.append(area)

    def add_wp(self, area_id, wp: Waypoint):
        for area in self._areas:
            if area.get_area_id() == area_id:
                area.add_wp(wp)
                self._wps_neighs[wp.get_id()] = [None, None, None, None]
                break

    def add_oneway_connection(self, wp_src_id, wp_dst_id, direction: Direction, path: Path):
        if wp_src_id and wp_dst_id in self._wps_neighs.keys():
            self._wps_neighs[wp_src_id][direction.value] = wp_dst_id
            self._paths[wp_src_id + '_' + wp_dst_id] = path

    def add_connection(self, wp_src_id, wp_dst_id, direction: Direction, path: Path):
        if wp_src_id and wp_dst_id in self._wps_neighs.keys():
            self.add_oneway_connection(wp_src_id, wp_dst_id, direction, path)
            self.add_oneway_connection(wp_dst_id, wp_src_id, opposite_dir(direction), path)

    def del_oneway_connection(self, wp_src_id, wp_dst_id):
        if wp_src_id in self._wps_neighs.keys():
            self._paths.pop(wp_src_id + '_' + wp_dst_id, None)
            src_neighs = self._wps_neighs[wp_src_id]
            try:
                src_neighs[src_neighs.index(wp_dst_id)] = None
            except ValueError:
                pass

    def del_connection(self, wp_src_id, wp_dst_id):
        self.del_oneway_connection(wp_src_id, wp_dst_id)
        self.del_oneway_connection(wp_dst_id, wp_src_id)

    def remove_wp(self, wp_id):
        for area in self._areas:
            if wp_id in area.get_wps().keys():
                for dir_index, _id in enumerate(self._wps_neighs[wp_id]):
                    if _id:
                        self.del_connection(wp_id, _id)
                area.remove_wp(wp_id)
                break

    def shortest_path(self, start_id, end_id):
        distances = {}
        for area in self._areas:
            for wp_id in area.get_wps().keys():
                distances[wp_id] = float('inf')
        distances[start_id] = 0
        heap = [(0, start_id)]
        visited = set()

        while heap:
            (curr_distance, curr_wp_id) = heapq.heappop(heap)
            if curr_wp_id in visited:
                continue

            visited.add(curr_wp_id)
            curr_area = self.get_area_by_wp_id(curr_wp_id)
            curr_wp = curr_area.get_wps()[curr_wp_id]

            if curr_wp_id == end_id:
                path = []
                while curr_wp.get_id() != start_id:
                    path.append(curr_wp)
                    curr_wp = distances[curr_wp.get_id()][1]
                path.append(self.get_area_by_wp_id(start_id).get_wps()[start_id])
                path.reverse()
                return path

            neighs_id = self._wps_neighs[curr_wp_id]
            for _id in neighs_id:
                if _id and _id not in visited:
                    new_distance = distances[curr_wp_id] + self._paths[curr_wp_id + '_' + _id].get_time()
                    if new_distance < distances[_id]:
                        distances[_id] = (new_distance, curr_wp)
                        heapq.heappush(heap, (new_distance, _id))

        return None

    def get_area_by_wp_id(self, waypoint_id):
        for area in self._areas:
            if waypoint_id in area.get_wps().keys():
                return area

        return None
