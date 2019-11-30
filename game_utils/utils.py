import json
from game_model.ability import DamagingAbility, HealingAbility, RestoringAbility

def _deserialize_abilities(abilities):
    deserialized = {"abilities": {}}
    for ability in abilities["abilities"]:
        d_ability = None
        if ability["type"] == "damage":
            d_ability = DamagingAbility(
                ability["BaseDamage"], 
                ability["Cost"], 
                cast_time=ability["CastTime"], 
                name=ability["Name"]
            )
        elif ability["type"] == "heal":
            d_ability = HealingAbility(
                ability["BaseHeal"], 
                ability["Cost"], 
                cast_time=ability["CastTime"], 
                name=ability["Name"]
            )
        elif ability["type"] == "restoration":
            d_ability = RestoringAbility(
                ability["BaseRestored"], 
                ability["Cost"], 
                cast_time=ability["CastTime"], 
                name=ability["Name"]
            )
        if d_ability:
            deserialized["abilities"][ability["id"]] = d_ability
    return deserialized

def load_abilities(abilities_file_path):
    abilities = {"abilities": {}}
    with open(abilities_file_path, 'r') as file:
        abilities = json.load(file)
        abilities = _deserialize_abilities(abilities)
    return abilities["abilities"]
