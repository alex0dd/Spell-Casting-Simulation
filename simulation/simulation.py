from .event_queue import EventQueue

class DiscreteEventsSimulation:

    def __init__(self, model, event_emitters=[], visualizers=[]):
        """
        Discrete events simulation with a time step counter

        model: world model of the simulation
        event_emitters: simulation entities that will emit events with some policy
        visualizers: list of visualizers
        """
        self.model = model
        # current simulation time
        self.current_time = 0
        # queue for incoming events
        self.event_queue = EventQueue()
        # event that might has been popped but its time has not arrived yet 
        # (as we can't check time via peek, due to EventQueue implementation)
        self.active_event = None
        self.active_event_time = None
        self.event_emitters = event_emitters
        # visualizer instance
        self.visualizers = visualizers
    
    def step(self):
        """
        Performs a discrete event simulation step.
        """

        """
        Working principle:
            1) For each event emitter (source) emit an event
            2) Extract an event from the event queue (ordered by timestamp)
            3) Interpret the event and execute the relative actions
            4) If there are more events with current simulation time timestamp, 
               then go to 1), otherwise go to 4)
            5) Update simulation timer
        """

        # make event emitters emit their events
        for emitter in self.event_emitters:
            emitted_event = emitter.emit(self.model)
            # if its a valid emittable event (not None), then dispatch it
            if emitted_event:
                self.event_queue.dispatch_event(emitted_event, self.current_time)

        # if there are no active events
        if self.active_event == None:
            # if there's at least one event in the event queue
            if not self.event_queue.empty():
                # consider the current event extracted from the event queue (Time Ordered Queue)
                self.active_event = self.event_queue.pop_event()

        # while there's an event, and it's at correct time
        while self.active_event != None and self.active_event[0] == self.current_time:
            # get the event instance from self.active_event tuple
            event = self.active_event[1] 
            # get the sender and params
            sender = event.sender
            params = event.params

            # handle event
            out_params = event.handle(self, sender, params)
            new_params = {**out_params}
            new_params["current_time"] = self.current_time
            new_params["sender"] = sender
            # visualize the event via the passed visualizers
            for visualizer in self.visualizers:
                visualizer.visualize(event, new_params)
            # look for the next event
            next_event = self.event_queue.peek_event()
            # if it has the same timestamp as current time
            if next_event != None and next_event[0] == self.current_time:
                # then update the active event and perform a new iteration
                self.active_event = self.event_queue.pop_event()
            else:
                self.active_event = None 

        # increment simulation time for the next step
        self.current_time += 1