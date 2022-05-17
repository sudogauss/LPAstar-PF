from map import Map
from queue import PriorityQueue
from typing import Tuple
import math
from observer.observer import Observer
from observer.subject import Subject


class PathFinder(Observer):

    def __init__(self, _subject: Subject):
        super().__init__(_subject)
        self.open_queue = PriorityQueue()
        self.map = Map()
        self.start = (0, 0)
        self.goal = (0, 0)

    def __get_key(self, y: int, x: int):
        i, j = self.map.index_by_coors(y, x)
        return min(self.map.vertexes[i][j].g, self.map.vertexes[i][j].rhs) + self.map.vertexes[i][j].h, \
               min(self.map.vertexes[i][j].g, self.map.vertexes[i][j].rhs)

    def init_new_path(self, y_start: int, x_start: int, y_goal: int, x_goal: int):
        self.start = (y_start, x_start)
        self.goal = (y_goal, x_goal)
        self.open_queue = PriorityQueue()
        self.map.set_new_goal(y_goal, x_goal)
        i, j = self.map.index_by_coors(y_start, x_start)
        self.map.vertexes[i][j].rhs = 0
        self.open_queue.put((self.__get_key(y_start, x_start), (y_start, x_start)))

    def __get_minimal_priority(self) -> Tuple[int or float, int or float]:
        if self.open_queue.empty():
            return math.inf, math.inf
        return self.open_queue.queue[0][0]

    def update_vertex(self, y_vertex: int, x_vertex: int):
        y_start, x_start = self.start
        i, j = self.map.index_by_coors(y_vertex, x_vertex)
        _id = self.map.id_by_coors(y_vertex, x_vertex)

        if y_start != y_vertex and x_start != x_vertex:

            min_transition = math.inf

            for _neighbour in self.map.get_neighbours(y_vertex, x_vertex):
                _i, _j = self.map.index_by_coors(_neighbour[0], _neighbour[1])
                __id = self.map.id_by_coors(_neighbour[0], _neighbour[1])
                if min_transition < self.map.vertexes[_i][_j].g + self.map.costs[__id][_id]:
                    min_transition = self.map.vertexes[_i][_j].g + self.map.costs[__id][_id]
                    self.map.vertexes[i][j].pred = self.map.vertexes[_i][_j]

            self.map.vertexes[i][j].rhs = min_transition

        if (self.__get_key(y_vertex, x_vertex), (y_vertex, x_vertex)) in self.open_queue.queue:
            self.open_queue.queue.remove((self.__get_key(y_vertex, x_vertex), (y_vertex, x_vertex)))

        if self.map.vertexes[i][j].g != self.map.vertexes[i][j].rhs:
            self.open_queue.put((self.__get_key(y_vertex, x_vertex), (y_vertex, x_vertex)))

    def compute_path(self):
        i, j = self.map.index_by_coors(*self.goal)

        while self.__get_minimal_priority() < self.__get_key(*self.goal) or \
                self.map.vertexes[i][j].rhs != self.map.vertexes[i][j].g:

            _y, _x = self.open_queue.get()[1]
            _i, _j = self.map.index_by_coors(_y, _x)

            if self.map.vertexes[_i][_j].g > self.map.vertexes[_i][_j].rhs:
                self.map.vertexes[_i][_j].g = self.map.vertexes[_i][_j].rhs
            else:
                self.map.vertexes[_i][_j].g = math.inf
                self.update_vertex(_y, _x)

            for _neighbour in self.map.get_neighbours(_y, _x):
                self.update_vertex(*_neighbour)

    def update(self):
        # Stop path execution
        # TODO: send stop to microcontroller_proxy
        for (y, x) in self.subject.moved:
            self.map.clear_vertex(y, x)
            self.update_vertex(y, x)
        for (y, x) in self.subject.objects:
            self.map.obstacle_vertex(y, x)
            self.update_vertex(y, x)

        self.compute_path()

    def execute_path(self):
        # TODO: translate vertexes path to orders and send orders to microcontroller_proxy
        pass