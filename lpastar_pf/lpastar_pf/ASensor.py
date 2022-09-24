from abc import ABC, abstractmethod
from typing import Iterable, Tuple


class ASensor(ABC):

    """ Abstract class ASensor that simulates any sensor. Your sensor class must
    inherit from it and override the scan methods.

    Methods
    -------

    scan(origin):
        Scans the environment and returns a list of
        absolute coordinates of obstacles.
    """

    @abstractmethod
    def scan(self, origin: Tuple[float, float, float]) -> Iterable[Tuple[float, float, float]]:
        """ Scans the environment according to the sensor
        position and returns a list of obstacles.

        Args:
            origin (Tuple[float, float, float]):
                The position of the sensor in the **[x, y, alpha]** format,
                where  **(x, y)** are the coordinates of the sensor and
                **alpha** is its orientation. It is used to transform
                relative obstacles' coordinates to absolute coordinates
                compared to map's origin.

        Returns:
            Iterable[Tuple[float, float, float]]: An Iterable(list generally)
            of the obstacles in the **[x, y, w]** format, where **(x, y)** are
            the absolute coordinates of the center of an obstacle and **w**
            is its width
        """
        pass
