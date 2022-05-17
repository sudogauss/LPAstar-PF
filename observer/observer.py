from observer.subject import Subject


class Observer:
    def __init__(self, s: Subject):
        self.subject = s
        self.subject.attach(self)

    def update(self):
        pass