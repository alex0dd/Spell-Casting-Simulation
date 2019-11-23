class Visualizer:

    def __init__(self):
        pass

    def visualize_ability_cast_started(self, params):
        pass

    def visualize_ability_cast_ended(self, params):
        pass

    def visualize_everyone_restore_health_and_resources(self, params):
        pass


class TextualVisualizer(Visualizer):

    def __init__(self):
        pass

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
            print("[Time: {}] {} has hit {} for {} damage, {} left.".format(
                time,
                source.name, 
                target.name, 
                health_before - health_after,
                health_after
            ))
        else:
            print("[Time: {}] {} was not able to cast {} on {}.".format(time, source.name, ability.name, target.name))

    def visualize_everyone_restore_health_and_resources(self, params):
        time = params["current_time"]
        players = params["sender"].players
        # pass