class Visualizer:

    def __init__(self):
        pass

    def visualize_ability_cast_started(self, time, source, target, ability):
        pass

    def visualize_ability_cast_ended(self, time, source, target, ability, success):
        pass


class TextualVisualizer(Visualizer):

    def __init__(self):
        pass

    def visualize_ability_cast_started(self, time, source, target, ability):
        print("[Time: {}] {} is casting {} on {}".format(time, source.name, ability.name, target.name))

    def visualize_ability_cast_ended(self, time, source, target, ability, health_before, health_after, success):
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