from GAgent import GAgent
from ASensor import ASensor
from GMap import GMap
from typing import Type, Tuple, Dict, Iterable, List, Any
from exception.MapInitializationException import MapInitializationException
from exception.PathDoesNotExistException import PathDoesNotExistException
import time
from priority_queue.PriorityQueue import PriorityQueue
import collections


class LPAStarPathFinder:

    """ A class which implements LPA* algorithm and method which is responsible to rescan the environment
        with a sensor and run execution of agent's movement method.

    Attributes
    ----------
    agent: GAgent

    sensor: ASensor

    period: int

    infinity: int

    goal: Tuple[int, int]

    start: Tuple[int, int]

    map: GMap

    g: List[List[int]]

    rhs: List[List[int]]

    discover_order: PriorityQueue

    Methods
    -------

    get_position():
        Retreives the position  of the agent in **[x, y, alpha]** format, where **(x, y)** are the coordinates of
        the agent and **alpha** is its orientation.

    follow_trajectory(points):
        Makes the agent follow the trajectory. Must use a worker process to execute the path.

    move(x, y):
        Moves the agent to (x,y).
    
    stop():
        Stops the agent.
    """

    def __init__(self, agent: Type[GAgent], sensor: Type[ASensor], params: Dict[str, int]):
        """ Uses __param_getter method to extract data from dictionary. Initializes agent and sensor.

        Args:
            agent (Type[GAgent]): An agent which executes path finding movement commands.
            sensor (Type[ASensor]): A sensor which is used to scan the map.
            params (Dict[str, int]): A dictionary with attributes to initialize.
        """
        self.agent = agent
        self.sensor = sensor

        self.map = GMap(params, obstacles=[])
        self.period = self.__param_getter("period", params)
        self.infinity = (self.map.rows * self.map.columns) ** 2

        self.goal = None
        self.start = None

        self.g = [[self.infinity for _ in range(self.map.columns)] for _ in range(self.map.rows)]
        self.rhs = [[self.infinity for _ in range(self.map.columns)] for _ in range(self.map.rows)]
        self.discover_order = PriorityQueue()

    def reset(self, goal: Tuple[float, float]) -> None:
        """ Resets g-values and rhs-values. Initializes start and goal positions for the algorithm.

        Args:
            goal (Tuple[float, float]): _description_
        """
        self.g = [[self.infinity for _ in range(self.map.columns)] for _ in range(self.map.rows)]
        self.rhs = [[self.infinity for _ in range(self.map.columns)] for _ in range(self.map.rows)]
        self.discover_order = PriorityQueue()

        self.goal = self.map.coors_to_indexes(*goal)
        x, y, _ = self.agent.get_position()
        i, j = self.map.coors_to_indexes(x, y)
        self.start = (i, j)
        self.rhs[i][j] = 0
        self.discover_order.insert((self.__calculate_key(i, j)), (i, j))

    def find_path(self, goal: Tuple[float, float]) -> None:
        """_summary_

        Args:
            goal (Tuple[float, float]): _description_
        """
        self.reset(goal)

        while True:
            x, y, _ = self.agent.get_position()
            if (x - goal[0]) ** 2 + (y - goal[1]) <= (self.map.get_resolution() ** 2):
                self.agent.stop_trajectory()
                break
            
            current_obstacles = self.map.get_obstacles()
            new_obstacles = self.map.convert_obstacles_to_graph(self.sensor.scan(self.agent.get_position()))

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
                    shrunk_path = self.__shrink_path(model_path)
                    real_path = map(lambda point: self.map.indexes_to_coors(*point), shrunk_path)

                    self.agent.follow_trajectory(real_path)
                except PathDoesNotExistException:
                    self.__pause()

            self.__pause()
        
        if self.agent.worker.is_alive():
            self.agent.worker.kill()
            self.agent.stop()

    def __shrink_path(self, model_path: List[Tuple[int, int]]) -> Iterable[Tuple[int, int]]:
        """_summary_

        Args:
            model_path (Iterable[Tuple[int, int]]): _description_

        Returns:
            Iterable[Tuple[int, int]]: _description_
        """
        shrunk_path = []

        if len(model_path) > 2:
            direction = abs(model_path[0][0] - model_path[1][0]) + 2 * abs(model_path[0][1] - model_path[1][1]) 
            for i in range(1, len(model_path)):
                tmp = direction
                direction = abs(model_path[i-1][0] - model_path[i][0]) + 2 * abs(model_path[i-1][1] - model_path[i][1]) 
                if tmp != direction:
                    shrunk_path.append(model_path[i-1])
            shrunk_path.append(model_path[len(model_path) - 1])
        else:
            shrunk_path = model_path

        return shrunk_path

    def __calculate_key(self, i: int, j: int) -> Tuple[int, int]:
        """_summary_

        Args:
            i (int): _description_
            j (int): _description_

        Returns:
            Tuple[int, int]: _description_
        """
        return min(self.g[i][j], self.rhs[i][j]) + self.map.get_heurisitcs_cost((i, j), self.goal), min(self.g[i][j], self.rhs[i][j])

    def __update_vertex(self, v: Tuple[int, int]) -> None:
        """_summary_

        Args:
            v (Tuple[int, int]): _description_
        """
        i, j = v
        if v != self.start:
            self.rhs[i][j] = min(list(map(lambda x: self.g[x[0]][x[1]] + self.map.get_transition_cost(x, v),
                                          self.map.get_neighbours(v))))
        self.discover_order.remove(v)
        if self.g[i][j] != self.rhs[i][j]:
            self.discover_order.insert(self.__calculate_key(i, j), v)

    def compute_shortest_path(self) -> List[Tuple[int, int]]:
        """_summary_

        Raises:
            PathDoesNotExistException: _description_

        Returns:
            Iterable[Tuple[int, int]]: _description_
        """
        while ((self.discover_order.top_key() < self.__calculate_key(*self.goal)) or 
            (self.rhs[self.goal[0]][self.goal[1]] != self.g[self.goal[0]][self.goal[1]])):
            v = self.discover_order.pop()
            i, j = v
            if self.g[i][j] > self.rhs[i][j]:
                self.g[i][j] = self.rhs[i][j]
                for neighbour in self.map.get_neighbours(v):
                    self.__update_vertex(neighbour)
            else:
                self.g[i][j] = self.infinity
                for neighbour in self.map.get_neighbours(v):
                    self.__update_vertex(neighbour)
                self.__update_vertex(v)

        if self.g[self.goal[0]][self.goal[1]] == self.infinity:
            raise PathDoesNotExistException("Cannot go from " + str(self.start) + " to " + str(self.goal))

        s = self.goal
        cur_vertex = self.map.coors_to_indexes(self.agent.get_position()[0], self.agent.get_position()[1])
        path = [s]
        while s != cur_vertex:
            neighbours = self.map.get_neighbours(s)
            pred = neighbours[0]
            min_pred = self.g[pred[0]][pred[1]] + self.map.get_transition_cost(pred, s)
            for neighbour in neighbours:
                x = self.g[neighbour[0]][neighbour[1]] + self.map.get_transition_cost(neighbour, s)
                if x < min_pred:
                    min_pred = x
                    pred = neighbour
            path.insert(0, pred)
            s = pred

        return path

    def __pause(self) -> None:
        """ Pauses current process for **period** milliseconds
        """
        time.sleep(self.period / 1000.0)

    def __param_getter(self, param_name: str, params: Dict[str, Any]) -> Any:
        """ A function which is used to extract data from dictionary and verify that all
            required arguments have been provided.

        Args:
            param_name (str): A name of an argument to extract
            params (Dict[str, Any]): A dictionary to extract from

        Raises:
            MapInitializationException: Occurs when the required argument is missing

        Returns:
            Any: A value extracted from **params** associated to the key **param_name**
        """
        if param_name in params.keys():
            return params[param_name]
        raise MapInitializationException("Parameter required, but not provided: " + param_name)