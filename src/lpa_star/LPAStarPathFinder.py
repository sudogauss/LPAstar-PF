from lpa_star.GAgent import GAgent
from lpa_star.ASensor import ASensor
from lpa_star.GMap import Gmap
from typing import Type, Tuple
from lpa_star.exception.MapInitializationException import MapInitializationException
from lpa_star.exception.PathDoesNotExistException import PathDoesNotExistException
import time
from priority_queue.PriorityQueue import PriorityQueue
import collections

class LPAStarPathFinder:

    def __init__(self, robot: Type[GAgent], sensor: Type[ASensor], params: Dict[str, int]):
        self.robot = robot
        self.sensor = sensor

        self.period = self.__param_getter("period", params)
        self.infinity = (self.map.rows * self.map.columns) ** 2

        self.goal = None
        self.start = None
        self.map = Gmap(obstacles = [], params = params)

        self.g = [[self.infinity for _ in range(self.map.columns)] for _ in range(self.map.rows)]
        self.rhs = [[self.infinity for _ in range(self.map.columns)] for _ in range(self.map.rows)]
        self.discover_order = PriorityQueue()
 

    def reset(self, goal: Tuple[float, float]) -> None:

        self.g = [[self.infinity for _ in range(self.map.columns)] for _ in range(self.map.rows)]
        self.rhs = [[self.infinity for _ in range(self.map.columns)] for _ in range(self.map.rows)]
        self.discover_order = PriorityQueue()

        self.goal = self.map.coors_to_indexes(*goal)
        x, y, _ = self.robot.get_position()
        i, j = self.map.coors_to_indexes(x, y)
        self.start = (i, j)
        rhs[i][j] = 0
        self.discover_order.insert((self.__calculate_key(i, j), (i, j)))


    def find_path(self, goal: Tuple[float, float]) -> None:

        self.reset(goal)

        while True:
            x, y, _ = self.robot.get_position()
            if (x - goal[0]) ** 2 + (y - goal[1]) <= (self.map.get_resolution() ** 2):
                self.robot.stop_trajectory()
                return
            
            current_obstacles = self.map.get_obstacles()
            new_obstacles = self.map.convert_obstacles_to_graph(self.sensor.scan(self.robot.get_position()))

            if not collections.Counter(current_obstacles) == collections.Counter(new_obstacles):

                self.map.set_obstacles(new_obstacles)

                for obstacle in new_obstacles:
                    if not obstacle in current_obstacles:
                        self.__update_vertex(obstacle)

                for obstacle in current_obstacles:
                    if not obstacle in new_obstacles:
                        self.__update_vertex(obstacle)

                try:
                    model_path = self.compute_shortest_path()
                except PathDoesNotExistException:
                    self.__pause()

                shrinked_path = self.__shrink_path(model_path)
                real_path = map(shrinked_path, lambda point: self.map.indexes_to_coors(*point))

                self.robot.follow_trajectory(real_path)

            self.__pause()
        
        if self.robot.worker.is_alive():
            self.robot.worker.kill()


    def __shrink_path(self, model_path: Iterable[Tuple[int, int]]) -> Iterable[Tuple[int, int]]:

        shrinked_path = []

        if len(model_path) > 2:
            direction = abs(model_path[0][0] - model_path[1][0]) + 2 * abs(model_path[0][1] - model_path[1][1]) 
            for i in range(1, len(model_path)):
                tmp = direction
                direction = abs(model_path[i-1][0] - model_path[i][0]) + 2 * abs(model_path[i-1][1] - model_path[i][1]) 
                if tmp != direction:
                    shrinked_path.append(model_path[i-1])
            shrinked_path.append(model_path[len(model_path) - 1])
        else:
            shrinked_path = model_path

        return shrinked_path


    def __calculate_key(self, i: int, j: int) -> Tuple[int, int]:
        return min(g[i][j], rhs[i][j]) + self.map.get_heurisitcs_cost((i, j), self.goal), min(g[i][j], rhs[i][j])


    def __update_vertex(self, v: Tuple[int, int]) -> None:
        i, j = v
        if v != self.start:
            rhs[i][j] = min(list(map(lambda x: g[x[0]][x[1]] + self.map.get_transition_cost(x, v), 
                self.map.get_neighbours(v))))
        self.discover_order.remove(v)
        if g[i][j] != rhs[i][j] self.discover_order.insert(self.__calculate_key(i, j), v)


    def compute_shortest_path(self) -> Iterable[Tuple[int, int]]:
        while ((self.discover_order.top_key() < self.__calculate_key(*self.goal)) or 
            (rhs[self.goal[0]][self.goal[1]] != g[self.goal[0]][self.goal[1]])):
            v = self.discover_order.pop()
            i, j = v
            if g[i][j] > rhs[i][j]:
                g[i][j] = rhs[i][j]
                for neighbour in self.map.get_neighbours(v):
                    self.__update_vertex(neighbour)
            else:
                g[i][j] = self.infinity
                for neighbour in self.map.get_neighbours(v):
                    self.__update_vertex(neighbour)
                self.__update_vertex(v)

        if g[self.goal[0]][self.goal[1]] == self.infinity:
            raise PathDoesNotExistException("Cannot go from " + str(self.start) + " to " + str(self.goal))

        s = self.goal
        path = [s]
        while s != self.start:
            neighbours = self.map.get_neighbours(s)
            pred = neighbours[0]
            min_pred = g[pred[0]][pred[1]] + self.map.get_transition_cost(pred, s)
            for neighbour in neighbours:
                x = g[neighbour[0]][neighbour[1]] + self.map.get_transition_cost(neighbour, s)
                if x < min_pred:
                    min_pred = x
                    pred = neighbour
            path.insert(0, pred)
            s = pred

        return path


    def __pause() -> None:
        time.sleep(self.period)


    def __param_getter(self, param_name: str, params: Dict[str, Any]) -> Any:
        if param_name in params.keys():
            return params[param_name]
        raise MapInitializationException("Parameter required, but not provided: " + param_name)