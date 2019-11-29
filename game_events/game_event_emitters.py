import game_events.game_events as events
from simulation.events import EventEmitter
import random

class AbilityCastEventEmitter(EventEmitter):

    def __init__(self, emitter):
        super(AbilityCastEventEmitter, self).__init__(emitter)

    def emit(self, model):
        targets = list(set(model.players).difference(set([self.emitter])))
        emitted_event = None
        # if any available targets and abilities
        if len(targets) > 0 and len(self.emitter.abilities) > 0:
            ability = random.choice(self.emitter.abilities)
            target = random.choice(targets)
            emitted_event = events.AbilityCastStarted(self.emitter, {"ability": ability, "target": target})
        return emitted_event

class EveryoneRestoreEventEmitter(EventEmitter):

    def __init__(self, emitter):
        super(EveryoneRestoreEventEmitter, self).__init__(emitter)

    def emit(self, model):
        return events.EveryoneRestoreHealthAndResources(self.emitter)
        