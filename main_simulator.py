from game_model import player, ability
from game_model.model import GameModel
import game_events.game_events as events
from game_events.game_event_emitters import AbilityCastEventEmitter, RestoreEveryoneEventEmitter
from simulation.simulation import DiscreteEventsSimulation
from game_visualizers.textual_visualizer import TextualVisualizer
import random as random


frost_bolt_spell = ability.DamagingAbility(100, 200, cast_time=5, name="Frost Bolt")
melee_attack_ability = ability.DamagingAbility(50, 1, cast_time=1, name="Melee Attack")

player_1_abilities = [frost_bolt_spell]
boss_abilities = [melee_attack_ability]

player_1 = player.Player(500, 1000, abilities=player_1_abilities, health_per_unit_time=1, mana_per_unit_time=1, name="Alex", game_class="Mage")
boss_player = player.Player(1000, 100, abilities=boss_abilities, name="Boss", game_class="Warrior")

players_list = [player_1]
enemies_list = [boss_player]

game_model = GameModel(players_list+enemies_list)

everyone_restore_emitter = EveryoneRestoreEventEmitter(game_model)
player_1_cast_emitter = AbilityCastEventEmitter(player_1)
boss_cast_emitter = AbilityCastEventEmitter(boss_player)

game_simulation = DiscreteEventsSimulation(
    game_model, 
    event_emitters=[
        everyone_restore_emitter, player_1_cast_emitter, boss_cast_emitter
    ], 
    visualizers=[TextualVisualizer()]
)

# manually dispatch some events
# dispatch initial event that starts health and resources restoration for everyone
#game_simulation.event_queue.dispatch_event(events.EveryoneRestoreHealthAndResources(game_model), 0)
#game_simulation.event_queue.dispatch_event(events.AbilityCastStarted(player_1, {"ability": frost_bolt_spell, "target": boss_player}), 2)
#game_simulation.event_queue.dispatch_event(events.AbilityCastStarted(boss_player, {"ability": melee_attack_ability, "target": player_1}), 2)
#game_simulation.event_queue.dispatch_event(events.AbilityCastStarted(player_1, {"ability": frost_bolt_spell, "target": boss_player}), 4)


steps = 30
t = 0
while t < steps:
    game_simulation.step()
    t = t + 1

print("{} is {}".format(player_1.name, "alive with {} hp".format(player_1.health) if player_1.is_alive() else "dead" ))
print("{} is {}".format(boss_player.name, "alive with {} hp".format(boss_player.health) if boss_player.is_alive() else "dead" ))