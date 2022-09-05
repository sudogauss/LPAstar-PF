from abc import ABC, abstractmethod


class ARobot(ABC):

    @abstractmethod
    def get_position(self) -> Tuple[float, float, float]:
        pass

    @abstractmethod
    def move(self, x: int, y: int) -> None:
        pass
