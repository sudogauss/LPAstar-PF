import multiprocessing as mp
from typing import Iterable, Tuple


class GAgent():
    
    """ A class which contains robot's methods to implement for path finding.
    Your robot class must inherit from this class and override get_position, move and stop methods.

    Methods
    -------

    get_position():
        Retreives the position [x, y, angle] of the robot.

    follow_trajectory(points):
        Makes the robot to follow the trajectory. Must use a worker thread executing the path.

    move(x, y):
        Moves the robot to (x,y)
    
    stop():
        Stops the robot
    """

    def __init__(self):
        """ Initializes robot's worker process
        """
        self.worker = None

    def follow_trajectory(self, points: Iterable[Tuple[float, float]]) -> None:

        self.stop_trajectory()

        def follow(points):
            for point in points:
                self.move(*point)

        self.worker = mp.Process(target=follow, args=(shrinked_trajectory, ))
        self.worker.start()

    def stop_trajectory(self) -> None:
        self.worker.terminate()
            

    def get_position(self) -> Tuple[float, float, float]:
        pass

    def move(self, x: float, y: float) -> None:
        pass

    def stop(self) -> None:
        pass
