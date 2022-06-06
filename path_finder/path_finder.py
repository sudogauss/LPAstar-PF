from queue import PriorityQueue
from path_finder.map import Map
from path_finder.sensor import Sensor
from path_finder.executor import Executor
from path_finder.const import *


class PathFinder:

    def __init__(self, _sensor: Sensor, _executor: Executor):
        self.open_queue = PriorityQueue()
        self.map = Map()
        self.start = (0, 0)
        self.goal = (0, 0)
        self.executor = _executor
        self.sensor = _sensor

    def init_new_path(self, y_start: int, x_start: int, y_goal: int, x_goal: int):
        self.start = (y_goal, x_goal)
        self.goal = (y_start, x_start)
        self.open_queue = PriorityQueue()
        self.map.set_new_goal(y_start, x_start)

    def update_vertex(self, y_vertex: int, x_vertex: int):
        pass

    def compute_path(self):
        pass

    def update(self):
        self.executor.stop()
        new_obstacles = self.sensor.get_data()
        for vertex in self.map.vertexes:
            if vertex.state == STATE_CLEAR and (vertex.y, vertex.x) in new_obstacles:
                self.map.obstacle_vertex(vertex.y, vertex.x)
                self.update_vertex(vertex.y, vertex.x)
            if vertex.state == STATE_OBSTACLE and (vertex.y, vertex.x) not in new_obstacles:
                self.map.clear_vertex(vertex.y, vertex.x)
                self.update_vertex(vertex.y, vertex.x)
        self.compute_path()
        i, j = self.map.index_by_coors(*self.goal)
        self.goal = self.map.vertexes[i][j].pred
        self.executor.move_to(*self.goal)

    def run(self):
        while self.goal != self.start:
            self.update()



