from .event_queue import EventQueue

import game_simulation.game_events as events

class GameSimulation:

    def __init__(self, game_model, visualization=None):
        self.game_model = game_model
        # current simulation time
        self.current_time = 0
        # queue for incoming events
        self.event_queue = EventQueue()
        # event that might has been popped but its time has not arrived yet 
        # (as we can't check time via peek, due to EventQueue implementation)
        self.active_event = None
        self.active_event_time = None
        # visualizer instance
        self.visualization = visualization
    
    def step(self):
        """
        Performs a discrete event simulation step.
        """

        """
        Working principle:
            1) Extract an event from the event queue (ordered by timestamp)
            2) Interpret the event and execute the relative actions
            3) If there are more events with current simulation time timestamp, 
               then go to 1), otherwise go to 4)
            4) Update simulation timer
        """

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

            out_params = event.handle(self, sender, params)
            new_params = {**out_params}
            new_params["current_time"] = self.current_time
            new_params["sender"] = sender
            # TODO: remove the event classification completly from this method
            # apply individual events
            if isinstance(event, events.AbilityCastStarted):
                self.visualization.visualize_ability_cast_started(new_params)
            elif isinstance(event, events.AbilityCastEnded):
                self.visualization.visualize_ability_cast_ended(new_params)
            elif isinstance(event, events.EveryoneRestoreHealthAndResources):
                self.visualization.visualize_everyone_restore_health_and_resources(new_params)
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