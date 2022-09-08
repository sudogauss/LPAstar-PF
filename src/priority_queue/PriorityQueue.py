from typing import Tuple, Union
import typing_extensions.extensions as extensions
import heapq

class PriorityQueue:

    def __init__(self):
        self.h = []

    def insert(self, key: extensions.comparable_t, value: extensions.comparable_t):
        heapq.heappush(self.h, (key, value))

    def pop(self):
        return heapq.heappop(self.h)

    def top_key(self):
        if len(self.h) == 0:
            raise EmptyQueueException
        return self.h[0][0]

    def remove(self, value: extensions.comparable_t) -> None:
        pos = -1
        for i in len(self.h):
            if self.h[i][1] == value:
                pos = i
                break

        if pos == -1:
            return

        self.h[pos] = self.h[-1]
        self.h.pop()
        heapq.heapify(self.h)