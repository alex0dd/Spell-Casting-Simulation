from queue import PriorityQueue

class EventQueue:

    def __init__(self):
        self.priority_queue = PriorityQueue()

    def dispatch_event(self, event, arrival_time):
        self.priority_queue.put_nowait((arrival_time, event))

    def empty(self):
        return self.priority_queue.empty()

    def pop_event(self):
        try:
            # (arrival_time, event) tuple
            item = self.priority_queue.get_nowait()
        except:
            item = None
        finally:
            return item
