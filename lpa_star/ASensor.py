from abc import ABC, abstractmethod
from typing import Iterable, Tuple


class ASensor(ABC):
    
    @abstractmethod
    def scan(self, origin: Tuple[float, float, float]) -> Iterable[Tuple[float, float, float]]:
        pass