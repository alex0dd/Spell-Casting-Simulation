from game_model import player, ability
from game_model.model import GameModel
import random as random

import os

def perform_ability_cast(source, target, ability):
    health_before = target.health
    success = source.cast_ability(ability, target)
    health_after = target.health

    return source, target, ability, health_before, health_after, success

def report_ability_cast(source, target, ability):
    print("{} is casting {} on {}".format(source.name, ability.name, target.name))
    source, target, ability, health_before, health_after, success = perform_ability_cast(source, target, ability)
    if success:
        print("{} has hit {} for {} damage, {} left.".format(
            source.name, 
            target.name, 
            health_before - health_after,
            health_after
        ))
    else:
        print("{} was not able to cast {} on {}.".format(source.name, ability.name, target.name))

frost_bolt_spell = ability.DamagingAbility(100, 200, name="Frost Bolt")
melee_attack_ability = ability.DamagingAbility(50, 1, name="Melee Attack")

player_1_abilities = [frost_bolt_spell]
boss_abilities = [melee_attack_ability]

player_1 = player.Player(500, 1000, abilities=player_1_abilities, health_per_unit_time=10, mana_per_unit_time=1, name="Alex", game_class="Mage")
boss_player = player.Player(1000, 100, abilities=boss_abilities, name="Boss", game_class="Warrior")

players_list = [player_1]
enemies_list = [boss_player]

game_model = GameModel(players_list+enemies_list)

while not player_1.is_dead() and not boss_player.is_dead():

    current_player = player_1
    if current_player.is_alive():
        ability = random.choice(current_player.abilities)
        report_ability_cast(current_player, boss_player, ability)

    # boss attack
    if boss_player.is_alive():
        attacked_by_boss = random.choice(players_list)
        boss_attack_ability = random.choice(boss_player.abilities)
        report_ability_cast(boss_player, attacked_by_boss, boss_attack_ability)

    # restore all the health and resources per unit time
    game_model.health_and_resources_restore()
    #os.sleep(2000)

print("{} is {}".format(player_1.name, "alive with {} hp".format(player_1.health) if player_1.is_alive() else "dead" ))
print("{} is {}".format(boss_player.name, "alive" if boss_player.is_alive() else "dead" ))