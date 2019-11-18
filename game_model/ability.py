class Ability:

    def __init__(self, resource_cost, cast_time=0, name=""):
        self.name = name
        self.cost = resource_cost
        self.cast_time = cast_time


class HealingAbility(Ability):

    def __init__(self, healing_applied, mana_cost, **kwargs):
        super(HealingAbility, self).__init__(mana_cost, **kwargs)
        self.healing_applied = healing_applied

    @property
    def healing(self):
        return self.healing_applied

class RestoringAbility(Ability):

    def __init__(self, mana_restored, mana_cost, **kwargs):
        super(RestoringAbility, self).__init__(mana_cost, **kwargs)
        self.mana_restored = mana_restored

    @property
    def restored(self):
        return self.mana_restored

class DamagingAbility(Ability):

    def __init__(self, damage_applied, mana_cost, **kwargs):
        super(DamagingAbility, self).__init__(mana_cost, **kwargs)
        self.damage_applied = damage_applied

    @property
    def damage(self):
        return self.damage_applied