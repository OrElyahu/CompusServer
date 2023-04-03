from objects.Area import Area
import heapq


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

    def shortest_path(self, start, end):
        distances = {}
        for area in self._areas:
            for wp in area.get_wps().values():
                distances[wp.get_id()] = float('inf')
        distances[start.get_id()] = 0
        heap = [(0, start.get_id())]
        visited = set()

        while heap:
            (current_distance, current_waypoint_id) = heapq.heappop(heap)
            if current_waypoint_id in visited:
                continue

            visited.add(current_waypoint_id)
            current_waypoint = self.get_waypoint_by_id(current_waypoint_id)

            if current_waypoint == end:
                path = []
                while current_waypoint.get_id() != start.get_id():
                    path.append(current_waypoint)
                    current_waypoint = distances[current_waypoint.get_id()][1]
                path.append(start)
                path.reverse()
                return path

            for neighbor in current_waypoint.get_neighbors():
                if neighbor.get_id() not in visited:
                    new_distance = distances[current_waypoint.get_id()] + neighbor.get_travel_cost()
                    if new_distance < distances[neighbor.get_id()]:
                        distances[neighbor.get_id()] = new_distance
                        heapq.heappush(heap, (new_distance, neighbor.get_id()))

    def get_waypoint_by_id(self, waypoint_id):
        for area in self._areas:
            for waypoint in area.get_wps().values():
                if waypoint.get_id() == waypoint_id:
                    return waypoint

        return None
