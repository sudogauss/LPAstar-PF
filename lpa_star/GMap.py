from typing import Iterable, Dict, Tuple, Any
from lpa_star.exception.MapInitializationException import MapInitializationException
from math import sqrt

class GMap():
    def __init__(self, obstacles: Iterable[Tuple[float, float, float]], params: Dict[int]) -> None:
        self.width = self.__param_getter("width", params)
        self.height = self.__param_getter("height", params)
        self.resolution = self.__param_getter("resolution", params)

        self.rows = int(self.height / self.resolution)
        self.columns = int(self.width / self.resolution)

        self.free_case_value = self.__param_getter("free_case_value", params)
        self.obstacle_case_value = self.__param_getter("obstacle_case_value", params)

        self.obstacles = self.__convert_obstacles_to_graph(obstacles)

        self.heuristics_multiplier = self.__param_getter("heuristics_multiplier", params)

    def __param_getter(self, param_name: str, params: Dict[Any]) -> Any:
        if param_name in params.keys():
            return params[param_name]
        raise MapInitializationException("Parameter required, but not provided: " + param_name)

    def __convert_obstacles_to_grpah(obstacles: Iterable[Tuple[float, float, float]]) -> Iterable[Tuple[int ,int]]:
        model_obstacles = []
        for obstacle in obstacles:
            x = obstacle[0]
            y = obstacle[1]
            w = obstacle[2] / 2

            square_left_i, square_top_j = self.coors_to_indexes(max(0, x - w), max(0, y - w))
            square_right_i, square_bottom_j = self.coors_to_indexes(min(width, x + w), min(height, y + w))

            for i in range(square_left_i, square_right_i + 1):
                for j in range(square_top_j, square_bottom_j + 1):
                    model_obstacles.append((i, j))

        return model_obstacles


    def coors_to_indexes(self, x: float, y: float) -> Tuple[int, int]:
        return int(x / self.resolution), int(y / self.resolution)
    
    def indexes_to_coors(self, i: int, j: int) -> Tuple[float, float]:
        return float(i * self.resolution), float(j * self.resolution)

    def get_transition_cost(self, _from: Tuple[int, int], _to: Tuple[int, int]) -> float:
        if abs(_from[0] - _to[0]) > 1 or abs(_from[1] - _to[1]) > 1:
            raise ImpossibleTransitionException("Impossible transition from (" + _from[0] + "," + _from[1] + ") to (" + _to[0] + "," + _to[1])
        if  _to in self.obstacles:
            return self.obstacle_case_value
        else:
            return self.free_case_value * sqrt(abs(_from[1] - _to[1]) + abs(_from[0] - _to[0])) 

    def get_heurisitcs_cost(self, _from: Tuple[int, int], _to: Tuple[int, int]) -> float:
        return self.heurisitcs_multiplier * sqrt(abs(_from[1] - _to[1]) ** 2 + abs(_from[0] - _to[0]) ** 2)


    


