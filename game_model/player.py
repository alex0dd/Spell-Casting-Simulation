import math
from .ability import Ability, HealingAbility, DamagingAbility, RestoringAbility

class Player:

    def __init__(self, max_health, max_mana, health_per_unit_time=0, mana_per_unit_time=0, abilities = [], name="", game_class=""):
        self.max_health = max_health
        self.max_mana = max_mana
        self.health = max_health
        self.mana = max_mana
        self.health_per_unit_time = health_per_unit_time
        self.mana_per_unit_time = mana_per_unit_time
        self.abilities = abilities
        self.name = name
        self.game_class = game_class
        self.is_casting = False

    def is_casting(self):
        return self.is_casting

    def is_dead(self):
        return self.health <= 0

    def is_alive(self):
        return not self.is_dead()

    def apply_damage(self, damage):
        if not self.is_dead():
            self.health = self.health - damage
    
    def apply_heal(self, heal):
        # healing can't exceed the max health
        self.health = min(self.health + heal, self.max_health)

    def apply_restore(self, restore):
        # restoring can't exceed the max mana
        self.mana = min(self.mana + restore, self.max_mana)

    def restore_health_and_mana(self, health, mana):
        self.apply_heal(health)
        self.apply_restore(mana)

    def can_cast_ability(self, ability, target):
        can_be_casted = True
        cast_conditions = [
            not self.is_casting,
            self.health > 0,
            target.health > 0,
            ability.cost < self.mana, 
            ability in self.abilities
        ]
        for cond in cast_conditions:
            # chain of and operators because we might have multiple conditions
            can_be_casted = can_be_casted and cond
        return can_be_casted

    def cast_ability(self, ability, target, conditions_checked=True):
        """
        Applies an ability to a player target
        """
        damaging_ability = isinstance(ability, DamagingAbility)
        healing_ability = isinstance(ability, HealingAbility)
        restoring_ability = isinstance(ability, RestoringAbility)

        if self.can_cast_ability(ability, target) or conditions_checked:
            if damaging_ability:
                target.apply_damage(ability.damage)
            elif healing_ability:
                # healing ability
                target.apply_heal(ability.healing)
            elif restoring_ability:
                # restoring ability
                target.apply_restore(ability.restore)
            # reset casting state
            self.is_casting = False
            # able to cast
            return True
        else:
            # unable to cast (for unknown generic reason)
            return False