from game_events.game_events import AbilityCastStarted
from simulation.events import EventEmitter
import random

class AbilityCastEventEmitter(EventEmitter):

    def __init__(self, emitter):
        super(AbilityCastEventEmitter, self).__init__(emitter)

    def emit(self, model):
        targets = list(set(model.players).difference(set([self.emitter])))
        emitted_event = None
        if len(targets) > 0 and len(self.emitter.abilities) > 0:
            ability = random.choice(self.emitter.abilities)
            target = random.choice(targets)
            emitted_event = AbilityCastStarted(self.emitter, {"ability": ability, "target": target})
        return emitted_event

