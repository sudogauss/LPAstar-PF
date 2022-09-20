import pytest
from .exception.EmptyQueueException import EmptyQueueException


@pytest.fixture
def priority_queue():
    from .PriorityQueue import PriorityQueue
    return PriorityQueue()


@pytest.fixture(autouse=True)
def before_each(priority_queue):
    priority_queue.insert(2, (25, 34))
    priority_queue.insert(4, (25, 34))
    priority_queue.insert(0, (25, 34))
    priority_queue.insert(10, (25, 34))
    priority_queue.insert(3, (25, 34))
    priority_queue.insert(8, (25, 34))

    yield


def test_length(priority_queue):

    assert len(priority_queue.h) == 6


def test_insert_in_order_int_key(priority_queue):

    assert priority_queue.pop()[0] == 0
    assert priority_queue.pop()[0] == 2
    assert priority_queue.pop()[0] == 3


def test_top_key(priority_queue):

    assert priority_queue.top_key() == 0
    priority_queue.pop()
    assert priority_queue.top_key() == 2
    assert len(priority_queue.h) == 5


def test_raise_empty_exception_top_key(priority_queue):
    for i in range(6):
        priority_queue.pop()
    assert len(priority_queue.h) == 0
    with pytest.raises(EmptyQueueException):
        priority_queue.top_key()


def test_raise_empty_exception_pop(priority_queue):
    for i in range(6):
        priority_queue.pop()
    assert len(priority_queue.h) == 0
    with pytest.raises(EmptyQueueException):
        priority_queue.pop()
