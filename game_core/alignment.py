from game_core.turns import turn_state

class PathRule:
    def __init__(self, name, desc, modify_damage=None, modify_heal=None, on_special_used=None, on_turn_start=None, on_turn_end=None):
        """
        Allows stat manipulation based of path
        """
        self.name = name
        self.desc = desc
        self.modify_damage = modify_damage
        self.modify_heal = modify_heal
        self.on_special_used = on_special_used
        self.on_turn_start = on_turn_start
        self.on_turn_end = on_turn_end

# -------------------------
# Destruction — Overkill
# -------------------------
def destruction_modify_damage(attacker, defender, dmg, context):
    """
    Scales damage based of defender's missing health
    """
    def_gundam = defender.gundam
    missing = def_gundam.max_health - def_gundam.health
    bonus = int(missing * 0.10)
    return dmg + bonus

# -------------------------
# Hunt — Precision
# -------------------------
def hunt_modify_damage(attacker, defender, dmg, context):
    """Ignores evasion"""
    context["ignore_dodge"] = True
    return dmg

# -------------------------
# Erudition — Amplify
# -------------------------
def erudition_modify_damage(attacker, defender, dmg, context):
    """Amplifies dmg if attacker is slower"""
    if context.get("acted_last") == defender:
        return int(dmg * 1.20)
    return dmg

# -------------------------
# Harmony — Echo (FIXED to pass a valid deterministic type block)
# -------------------------
def harmony_on_special_used(attacker, defender, effect):
    """Queues repeating attack"""
    echo_type = effect["type"] if effect["type"] in ["burst", "armor_pierce", "rifle_burst", "multi_hit_melee"] else "follow_up"
    turn_state.setdefault("echo_effects", {})
    turn_state["echo_effects"][attacker] = {
        "type": echo_type,
        "percent": 0.50,
        "damage": effect.get("damage", 100),
        "delayed": True
    }

# -------------------------
# Nihility — Corrosion
# -------------------------
def nihility_on_special_used(attacker, defender, effect):
    """DOT debuffs"""
    if effect["type"] != "system_decay":
        return
    total_debuff = effect["atk_down"] + effect["def_down"] + effect["speed_down"]
    dot = int(total_debuff * 0.10)
    turn_state.setdefault("dot_effect", {})
    turn_state["dot_effect"][defender] = {
        "type": "burn",
        "damage": dot,
        "turns": 1
    }

# -------------------------
# Preservation — Guard
# -------------------------
def preservation_on_special_used(attacker, defender, effect):
    """Reduces incoming dmg"""
    turn_state.setdefault("parry_effects", {})
    turn_state["parry_effects"][attacker] = {
        "reduce": 0.20
    }

# -------------------------
# Abundance — Overflow
# -------------------------
def abundance_modify_heal(attacker, heal_amount):
    """Heals self"""
    atk_gundam = attacker.gundam
    if atk_gundam.health < atk_gundam.max_health * 0.50:
        return int(heal_amount * 1.10)
    return heal_amount

# -------------------------
# Remembrance — Freeze
# -------------------------
def remembrance_on_special_used(attacker, defender, effect):
    """Stuns defender for 1 round"""
    turn_state.setdefault("freeze_effect", {})
    turn_state["freeze_effect"][defender] = {
        "turns": 1
    }

# -------------------------
# Propagation — Momentum
# -------------------------
def propagation_modify_damage(attacker, defender, dmg, context):
    """Scales dmg based on total hits"""
    hits = context.get("hits", 1)
    if hits > 1:
        bonus = int(dmg * 0.10 * (hits - 1))
        return dmg + bonus
    return dmg

path_rules = {
    "Destruction": PathRule("Destruction", "Overkill", modify_damage=destruction_modify_damage),
    "Hunt": PathRule("Hunt", "Precision", modify_damage=hunt_modify_damage),
    "Erudition": PathRule("Erudition", "Amplify", modify_damage=erudition_modify_damage),
    "Harmony": PathRule("Harmony", "Echo", on_special_used=harmony_on_special_used),
    "Nihility": PathRule("Nihility", "Corrosion", on_special_used=nihility_on_special_used),
    "Preservation": PathRule("Preservation", "Guard", on_special_used=preservation_on_special_used),
    "Abundance": PathRule("Abundance", "Overflow", modify_heal=abundance_modify_heal),
    "Remembrance": PathRule("Remembrance", "Freeze", on_special_used=remembrance_on_special_used),
    "Propagation": PathRule("Propagation", "Momentum", modify_damage=propagation_modify_damage),
}

class SpecialMove:
    def __init__(self, name, path, desc, effect):
        """Blueprint for specials"""
        self.name = name
        self.path = path
        self.desc = desc
        self.effect = effect

specials = {
    "Berserker": SpecialMove("Berserker", "Destruction", "Boost", {"type": "berserk", "melee_bonus": 200, "defense_penalty": -100}),
    "Beam Magnum": SpecialMove("Beam Magnum", "Destruction", "Burst", {"type": "burst", "damage": 350}),
    "Mace": SpecialMove("Mace", "Destruction", "Pierce", {"type": "armor_pierce", "ignore_defense": 0.40}),
    "Newtype Awakened": SpecialMove("Newtype Awakened", "Hunt", "Evade", {"type": "dodge"}),
    "Twin Buster Rifles": SpecialMove("Twin Buster Rifles", "Hunt", "Burst", {"type": "rifle_burst", "hits": 2, "damage_per_hit": 120}),
    "Missile Pod Ambush": SpecialMove("Missile Pod Ambush", "Erudition", "Barrage", {"type": "missile_barrage", "hits": 3, "damage_per_hit": 100, "stun_chance": 0.20}),
    "Full-Burst Dragoon": SpecialMove("Full-Burst Dragoon", "Erudition", "Detonate", {"type": "charge_detonation", "delay": 1, "damage": 400}),
    "Red Comet": SpecialMove("Red Comet", "Harmony", "Speed", {"type": "speed_buff", "amount": 40}),
    "Follow-Up Strike": SpecialMove("Follow-Up Strike", "Harmony", "Follow", {"type": "follow_up", "percent": 0.50}),
    "Permet Overheat": SpecialMove("Permet Overheat", "Nihility", "Burn", {"type": "burn", "damage_per_turn": 80, "turns": 2}),
    "ECM": SpecialMove("ECM", "Nihility", "Decay", {"type": "system_decay", "atk_down": 40, "def_down": 40, "speed_down": 20, "turns": 3}),
    "Retaliate": SpecialMove("Retaliate", "Preservation", "Parry", {"type": "parry", "reduce": 0.50, "counter_damage": 150}),
    "Beam Shield": SpecialMove("Beam Shield", "Preservation", "Shield", {"type": "shield", "amount": 300}),
    "Field Repair": SpecialMove("Field Repair", "Abundance", "Heal", {"type": "heal", "amount": 500}),
    "Last Stand": SpecialMove("Last Stand", "Abundance", "Revive", {"type": "revive", "hp": 200}),
    "Afterimage Stun": SpecialMove("Afterimage Stun", "Remembrance", "Stun", {"type": "stun", "chance": 0.30, "turns": 1}),
    "Mutilation": SpecialMove("Mutilation", "Remembrance", "Freeze", {"type": "self_mutilation", "freeze_turns": 1, "self_damage": 150}),
    "Quad Funnels": SpecialMove("Quad Funnels", "Propagation", "Multi", {"type": "multi_hit_melee", "hits": 4, "damage_per_hit": 90}),
}

def get_path_rule(path_name):
    """Helper used across combat engines to retrieve rules."""
    return path_rules.get(path_name)

def get_special(pilot):
    """Retrieves a pilot's assigned unique Special Move based on configuration."""
    if not pilot or not getattr(pilot, "gundam", None):
        return None
    special_name = getattr(pilot.gundam, "special", None)
    return specials.get(special_name)
