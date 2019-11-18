class Event:

    def __init__(self, sender, params=None, event_finished_callback=None):
        """
        sender: who has sent the event
        params: dictionary of event parameters
        event_finished_callback: method that will be called once the event is finished
        """
        self.sender = sender
        self.params = params
        self.event_finished_callback = event_finished_callback

    def finish_event(self):
        self.event_finished_callback()

class AbilityCastStarted(Event):

    def __init__(self, sender, params, event_finished_callback=None):
        super(AbilityCastStarted, self).__init__(
            sender,
            params=params,
            event_finished_callback=event_finished_callback
        )

class AbilityCastEnded(Event):

    def __init__(self, sender, params=None, event_finished_callback=None):
        super(AbilityCastEnded, self).__init__(
            sender, 
            params=params, 
            event_finished_callback=event_finished_callback
        )