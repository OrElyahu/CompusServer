import Path
import Waypoint
from objects.Utils import opposite_dir, Direction


class Area:
    """'
    _area_is typed str
    _wps_neighs typed dict(str:list[4 strings]) {'202':['203',None,None,'204'] }
    _wps typed dict(str:Waypoint) {'202':Waypoint}
    _paths typed dict(str:path) {'205_204':Path}
    ''"""

    def __init__(self, area_id: str, wps_neighs: dict = None, wps: dict = None, paths: dict = None):
        self._area_id = area_id
        self._wps_neighs = wps_neighs if wps_neighs is not None else {}
        self._wps = wps if wps is not None else {}
        self._paths = paths if paths is not None else {}

    def get_area_id(self):
        return self._area_id

    def set_area_id(self, area_id: str):
        self._area_id = area_id

    def get_wps_neighs(self):
        return self._wps_neighs

    def set_wps_neighs(self, wps_neighbors: dict):
        self._wps_neighs = wps_neighbors

    def get_wps(self):
        return self._wps

    def set_wps(self, wps: dict):
        self._wps = wps

    def get_paths(self):
        return self._paths

    def set_paths(self, paths: dict):
        self._paths = paths

    def add_wp(self, wp: Waypoint):
        _id = wp.get_id
        if _id not in self._wps_neighs.keys():
            self._wps[_id] = wp
            self._wps_neighs[_id] = [None, None, None, None]
            # TODO: obtain images from DB to values?

    def add_oneway_connection(self, wp_src_id, wp_dst_id, direction: Direction, path: Path):
        if wp_src_id and wp_dst_id in self._wps_neighs.keys():
            self._wps_neighs[wp_src_id][direction.value] = wp_dst_id
            self._paths[wp_src_id + '_' + wp_dst_id] = path

    def add_connection(self, wp_src_id, wp_dst_id, direction: Direction, path: Path):
        if wp_src_id and wp_dst_id in self._wps_neighs.keys():
            self.add_oneway_connection(wp_src_id, wp_dst_id, direction, path)
            self.add_oneway_connection(wp_dst_id, wp_src_id, opposite_dir(direction), path)

    def del_oneway_connection(self, wp_src_id, wp_dst_id):
        if wp_src_id and wp_dst_id in self._wps.keys():
            self._paths.pop(wp_src_id + '_' + wp_dst_id, None)
            src_neighs = self._wps_neighs[wp_src_id]
            dst_neighs = self._wps_neighs[wp_dst_id]
            src_neighs[src_neighs.index(wp_dst_id)] = None
            dst_neighs[dst_neighs.index(wp_src_id)] = None

    def del_connection(self, wp_src_id, wp_dst_id):
        self.del_oneway_connection(wp_src_id, wp_dst_id)
        self.del_oneway_connection(wp_dst_id, wp_src_id)

    def remove_wp(self, wp_id):
        if wp_id in self._wps.keys():
            for dir_index, _id in enumerate(self._wps_neighs[wp_id]):
                if _id:
                    self.del_connection(wp_id, _id)
            del self._wps[wp_id]

    def __eq__(self, obj):
        return self._area_id == obj.get_area_id
