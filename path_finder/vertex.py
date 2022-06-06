from path_finder.const import *
import math


class Vertex:
    def __init__(self, x: int, y: int) -> None:
        self.tag = NEW
        self.g = math.inf
        self.rhs = math.inf
        self.h = 0.0
        self.pred = None
        self.x = x
        self.y = y
        self.id = int(y / STEP) * (MAX_J + 1) + int(x / STEP)
        self.state = STATE_CLEAR

    def heuristic(self, y: int, x: int) -> None:
        self.h = math.sqrt((y - self.y) ** 2 + (x - self.x) ** 2)

    def reduce(self, y: int, x: int) -> None:
        self.g = math.inf
        self.rhs = math.inf
        self.heuristic(y, x)
        self.pred = None
