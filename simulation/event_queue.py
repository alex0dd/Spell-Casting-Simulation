from itertools import count

class TimeOrderedQueue:

    def __init__(self):
        # queue where the entries are sorted by their activation time (ascending order)
        self.queue = []
        # event counter, used for ordering items within the same time frame
        self.counter = count()

    def empty(self):
        return len(self.queue) <= 0

    def put(self, time, item):
        n_items = len(self.queue)
        current_item = 0
        current_id = next(self.counter)
        while current_item < n_items and time > self.queue[current_item][0]:
            current_item += 1
        # within the same time frame, find the first position that has lower id than current id (within frame ordering)
        while current_item < n_items and time == self.queue[current_item][0] and current_id > self.queue[current_item][1]:
            current_item += 1
        
        self.queue.insert(current_item, (time, current_id, item))

    def peek(self):
        return self.queue[0] if not self.empty() else None

    def pop(self):
        # remove item from the front
        item = self.queue.pop(0)
        # return (time, event)
        return (item[0], item[2])

class EventQueue:

    def __init__(self):
        """
        Defines an event queue ordered by events time in ascending order.
        """
        self.timed_queue = TimeOrderedQueue()

    def dispatch_event(self, event, arrival_time):
        self.timed_queue.put(arrival_time, event)

    def empty(self):
        return self.timed_queue.empty()

    def peek_event(self):
        """
        Returns an event as (time, event) tuple without removing it from the queue.
        """
        return self.timed_queue.peek()

    def pop_event(self):
        """
        Returns an event as (time, event) tuple, after removing it from the queue.
        In case of empty queue, None is returned
        """
        try:
            # (arrival_time, event) tuple
            item = self.timed_queue.pop()
        except:
            item = None
        finally:
            return item
