from simulation.events import Event

class AbilityCastStarted(Event):

    def __init__(self, sender, params):
        super(AbilityCastStarted, self).__init__(
            "AbilityCastStarted",
            sender,
            params=params
        )

    def handle(self, simulation, sender, params):
        # sender will be the caster player
        ability = params["ability"]
        target = params["target"]

        new_params = {"ability": ability, "target": target, "target_health_before": target.health, "target_mana_before": target.mana}
        if sender.can_cast_ability(ability, target):
            # dispatch an end event with success
            sender.is_casting = True        
            new_params["success"] = True
            arrival_time = simulation.current_time + ability.cast_time
        else:
            # dispatch an end event with failure
            new_params["success"] = False
            arrival_time = simulation.current_time + 1
        
        # dispatch end of cast event
        event_to_dispatch = (AbilityCastEnded(sender, params=new_params), arrival_time)
        simulation.dispatch_event(*event_to_dispatch)
        # return output parameters
        return new_params    

class AbilityCastEnded(Event):

    def __init__(self, sender, params=None):
        super(AbilityCastEnded, self).__init__(
            "AbilityCastEnded",
            sender, 
            params=params
        )

    def handle(self, simulation, sender, params):
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
        new_params["success"] = success
        # return output parameters
        return new_params

class EveryoneRestoreHealthAndResources(Event):

    def __init__(self, sender, params=None):
        super(EveryoneRestoreHealthAndResources, self).__init__(
            "EveryoneRestoreHealthAndResources",
            sender, 
            params=params
        )

    def handle(self, simulation, sender, params):
        # restore everyone's health (done by GameModel)
        sender.health_and_resources_restore()
        # return output parameters
        return {}