import game_simulation.events as events
from .event_queue import EventQueue

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

    def handle_ability_cast_started(self, sender, params):
        # sender will be the caster player
        ability = params["ability"]
        target = params["target"]

        new_params = {"ability": ability, "target": target, "target_health_before": target.health, "target_mana_before": target.mana}
        if sender.can_cast_ability(ability):
            # dispatch an end event with success
            sender.is_casting = True        
            new_params["success"] = True
            arrival_time = self.current_time + ability.cast_time
        else:
            # dispatch an end event with failure
            new_params["success"] = False
            arrival_time = self.current_time + 1
        
        # dispatch end of cast event
        event_to_dispatch = (events.AbilityCastEnded(sender, params=new_params), arrival_time)
        self.event_queue.dispatch_event(*event_to_dispatch)

    def handle_ability_cast_ended(self, sender, params):
        success = params["success"]
        # get ability and target params
        ability = params["ability"]
        target = params["target"]
        if success:
            # apply ability effect
            sender.cast_ability(ability, target)
        
        # TODO: handle this better (needed for visualization)
        new_params = params
        new_params["target_health_after"] = target.health
        new_params["target_mana_after"] = target.mana

        return success, new_params

    def handle_everyone_restore_health_and_resources(self, sender, params):
        # restore everyone's health (done by GameModel)
        sender.health_and_resources_restore()
        # send a new event on the next time step
        self.event_queue.dispatch_event(events.Event("EveryoneRestoreHealthAndResources", sender), self.current_time + 1)

    
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
            # apply individual events
            if isinstance(event, events.AbilityCastStarted):
                self.handle_ability_cast_started(sender, params)
                self.visualization.visualize_ability_cast_started(
                    self.current_time, 
                    sender, 
                    params["target"], 
                    params["ability"]
                )
            elif isinstance(event, events.AbilityCastEnded):
                success, new_params = self.handle_ability_cast_ended(sender, params)
                self.visualization.visualize_ability_cast_ended(self.current_time, 
                    sender, 
                    new_params["target"], 
                    new_params["ability"], 
                    new_params["target_health_before"], 
                    new_params["target_health_after"], 
                    success
                )
            elif event.name == "EveryoneRestoreHealthAndResources":
                self.handle_everyone_restore_health_and_resources(sender, params)
                self.visualization.visualize_everyone_restore_health_and_resources(
                    self.current_time, 
                    self.game_model.players
                )
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