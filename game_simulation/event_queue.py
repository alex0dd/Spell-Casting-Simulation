class TimeOrderedQueue:

    def __init__(self):
        # queue where the entries are sorted by their activation time (ascending order)
        self.queue = []

    def empty(self):
        return len(self.queue) <= 0

    def put(self, time, item):
        n_items = len(self.queue)
        current_item = 0
        while current_item < n_items and time > self.queue[current_item][0]:
            current_item += 1
        self.queue.insert(current_item, (time, item))

    def peek(self):
        return self.queue[0] if not self.empty() else None

    def pop(self):
        # remove item from the front
        return self.queue.pop(0)

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
