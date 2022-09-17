import multiprocessing as mp
from typing import Iterable, Tuple


class GAgent:
    
    """ A class which contains robot's methods to implement for path finding.
    Your robot class must inherit from this class and override get_position, move and stop methods.

    Attributes
    ----------
    worker: mp.Process
        A worker process to run agent's movement methods

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

    def __init__(self):
        """ Initializes robot's worker process to None.
        """
        self.worker = None

    def follow_trajectory(self, points: Iterable[Tuple[float, float]]) -> None:
        """ Makes an agent follow a trajectory passed in parameters. Creates an auxiliary function which is run in
        the worker process. Uses move function.

        Args:
            points (Iterable[Tuple[float, float]]): A trajectory to follow. Each point is a tuple of the next
            position to go to.
        """

        self.stop_trajectory()

        def follow(_points):
            for point in _points:
                self.move(*point)

        self.worker = mp.Process(target=follow, args=(points, ))
        self.worker.start()

    def stop_trajectory(self) -> None:
        """ Prevents agent from continuing the trajectory. Kills the worker process to stop giving movement commands.
        Sends a stop command to the agent.
        """
        self.worker.terminate()
        self.stop()
            
    def get_position(self) -> Tuple[float, float, float]:
        """ Gets agent's position.

        Returns:
            Tuple[float, float, float]: The position of the agent in **[x, y, alpha]** format, where
            **(x, y)** are the coordinates of the agent and **alpha** is its orientation
        """
        pass

    def move(self, x: float, y: float) -> None:
        """ Moves agent to **(x, y)**

        Args:
            x (float): The x-coordinate to move to
            y (float): The y-coordinate to move to
        """
        pass

    def stop(self) -> None:
        """ Stops all movements of the agent
        """
        pass
