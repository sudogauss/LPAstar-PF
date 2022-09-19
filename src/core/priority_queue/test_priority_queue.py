import pytest

@pytest.fixture
def priority_queue():
    from .PriorityQueue import PriorityQueue
    return PriorityQueue()

def test_insert_in_order_int_key(priority_queue):
    priority_queue.insert(2, (25, 34))
    priority_queue.insert(4, (25, 34))
    priority_queue.insert(0, (25, 34))

    assert priority_queue.pop()[0] == 0
    assert priority_queue.pop()[0] == 2
    assert priority_queue.pop()[0] == 4
