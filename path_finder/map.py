from typing import Tuple, List

import numpy as np
from vertex import Vertex
from const import *


class Map:

    def __init__(self):
        self.goal = (0, 0)
        self.vertexes = np.array([[Vertex(x, y) for x in range(0, MAX_X+1, STEP)] for y in range(0, MAX_Y+1, STEP)])
        self.costs = np.array([[(0.0, 0.0) for _ in range(0, N+1)] for _ in range(0, N+1)])

    @classmethod
    def id_by_coors(cls, y: int, x: int) -> int:
        return int(y / STEP) * (MAX_J+1) + int(x / STEP)

    @classmethod
    def index_by_coors(cls, y: int, x: int) -> Tuple[int, int]:
        return int(y / STEP), int(x / STEP)

    def set_new_goal(self, y: int, x: int):
        self.goal = (y, x)
        map(lambda vertex_list: map(lambda _vertex: _vertex.reduce(y, x), vertex_list), self.vertexes)

    def get_neighbours(self, y: int, x: int) -> List[Tuple[int, int]]:
        neighbours = [(y - STEP, x - STEP),
                      (y - STEP, x),
                      (y - STEP, x + STEP),
                      (y, x - STEP),
                      (y, x),
                      (y, x + STEP),
                      (y + STEP, x - STEP),
                      (y + STEP, x),
                      (y + STEP, x + STEP)
                      ]
        for i, (_y, _x) in neighbours:
            if not (0 <= _y <= MAX_Y and 0 <= _x <= MAX_X):
                neighbours.pop(i)
        return neighbours

    def __set_vertex_state(self, y: int, x: int, state: int) -> None:
        _id = self.id_by_coors(y, x)
        i, j = self.index_by_coors(y, x)

        self.vertexes[i][j] = state

        neighbours = self.get_neighbours(y, x)
        for (_y, _x) in neighbours:
            _neighbour_id = self.id_by_coors(_y, _x)
            if state == STATE_OBSTACLE:
                self.costs[_neighbour_id][_id] = (OBSTACLE_TRANSITION, OBSTACLE_TRANSITION)
            elif state == STATE_CLEAR:
                if _y == y or _x == x:
                    self.costs[_neighbour_id][_id] = (DIRECT_TRANSITION, DIRECT_TRANSITION)
                else:
                    self.costs[_neighbour_id][_id] = (DIAGONAL_TRANSITION, DIAGONAL_TRANSITION)

    def clear_vertex(self, y: int, x: int) -> None:
        self.__set_vertex_state(y, x, STATE_CLEAR)

    def obstacle_vertex(self, y: int, x: int) -> None:
        self.__set_vertex_state(y, x, STATE_OBSTACLE)

    def get_vertex_state(self, y: int, x: int) -> int:
        i, j = self.index_by_coors(y, x)
        return self.vertexes[i][j].state
