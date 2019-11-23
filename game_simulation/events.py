class Event:

    def __init__(self, event_name, sender, params=None):
        """
        Defines an event.

        name: event name
        sender: who has sent the event
        params: dictionary of event parameters
        """
        self.event_name = event_name
        self.sender = sender
        self.params = params
    
    @property
    def name(self):
        return self.event_name

    def handle(self, simulation, sender, target):
        """
        Method that will be called when the event will need to be handled.
        Defined by a function: (simulation_instance, sender, target)->resulting_parameters
        """
        pass