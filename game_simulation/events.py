class Event:

    def __init__(self, event_name, sender, params=None, event_finished_callback=None):
        """
        Defines an event.
        name: event name
        sender: who has sent the event
        params: dictionary of event parameters
        event_finished_callback: method that will be called once the event is finished
        """
        self.event_name = event_name
        self.sender = sender
        self.params = params
        self.event_finished_callback = event_finished_callback

    
    @property
    def name(self):
        return self.event_name

    def finish_event(self):
        self.event_finished_callback()

class AbilityCastStarted(Event):

    def __init__(self, sender, params, event_finished_callback=None):
        super(AbilityCastStarted, self).__init__(
            "AbilityCastStarted",
            sender,
            params=params,
            event_finished_callback=event_finished_callback
        )

class AbilityCastEnded(Event):

    def __init__(self, sender, params=None, event_finished_callback=None):
        super(AbilityCastEnded, self).__init__(
            "AbilityCastEnded",
            sender, 
            params=params, 
            event_finished_callback=event_finished_callback
        )