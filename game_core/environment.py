import random

class Environment:
    def __init__(self, name, melee_mod=0, ranged_mod=0, speed_mod=0, defense_mod=0):
        """Modifiers based on environment"""
        self.name = name
        self.melee_mod = melee_mod
        self.ranged_mod = ranged_mod
        self.speed_mod = speed_mod
        self.defense_mod = defense_mod

ENVIRONMENTS = {
    "Earth": Environment(
        "Earth",
        melee_mod=+150,
        defense_mod=+150,
        ranged_mod=-100,
        speed_mod=-100
    ),
    "Space": Environment(
        "Space",
        ranged_mod=+150,
        speed_mod=+150,
        melee_mod=-100,
        defense_mod=-100
    )
}

def choose_environment():
    """Randomizes between env"""
    return random.choice(list(ENVIRONMENTS.values()))

def apply_environment(gundam, environment):
    """Applies env mods"""
    gundam.reset()
    gundam.melee += environment.melee_mod
    gundam.ranged += environment.ranged_mod
    gundam.speed += environment.speed_mod
    gundam.defense += environment.defense_mod
    
