from observer.observer import Observer
from typing import List, Tuple


class Subject:
    def __init__(self):
        self.observers = []
        self.moved: List[Tuple[int, int]] = []
        self.objects: List[Tuple[int, int]] = []

    def attach(self, o: Observer) -> None:
        self.observers.append(o)

    def notify_observers(self) -> None:
        if len(self.objects) > 0:
            for o in self.observers:
                o.update()

    def set_objects(self, _objects: List[Tuple[int, int]]) -> None:
        changed_objects = []
        preserved_objects = []
        for _obj in _objects:
            if _obj not in self.objects:
                changed_objects.append(_obj)
            else:
                preserved_objects.append(_obj)
        moved_objects = []
        for obj in self.objects:
            if obj not in preserved_objects:
                moved_objects.append(obj)

        self.objects = changed_objects
        self.moved = moved_objects