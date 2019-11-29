from simulation.visualization import Visualizer
import game_events.game_events as events

class TextualVisualizer(Visualizer):

    def __init__(self):
        pass

    def visualize(self, event, params):
        if isinstance(event, events.AbilityCastStarted):
            self.visualize_ability_cast_started(params)
        elif isinstance(event, events.AbilityCastEnded):
            self.visualize_ability_cast_ended(params)
        elif isinstance(event, events.EveryoneRestoreHealthAndResources):
            self.visualize_everyone_restore_health_and_resources(params)

    def visualize_ability_cast_started(self, params):
        time = params["current_time"]
        source = params["sender"]
        target = params["target"]
        ability = params["ability"]
        print("[Time: {}] {} is casting {} on {}".format(time, source.name, ability.name, target.name))

    def visualize_ability_cast_ended(self, params):
        time = params["current_time"]
        source = params["sender"]
        target = params["target"]
        ability = params["ability"]
        health_before = params["target_health_before"]
        health_after = params["target_health_after"]
        success = params["success"]
        if success:
            if health_after > 0:
                print("[Time: {}] {} has hit {} for {} damage, {} left.".format(
                    time,
                    source.name, 
                    target.name, 
                    health_before - health_after,
                    health_after
                ))
            else:
                print("[Time: {}] {} has hit {} for {} damage, {} has died.".format(
                    time,
                    source.name, 
                    target.name, 
                    health_before - health_after,
                    target.name
                ))
        else:
            print("[Time: {}] {} was not able to cast {} on {}.".format(time, source.name, ability.name, target.name))

    def visualize_everyone_restore_health_and_resources(self, params):
        time = params["current_time"]
        players = params["sender"].players
        # pass