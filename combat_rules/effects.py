import random
from game_core.turns import turn_state
from game_core.alignment import get_path_rule, get_special
from presentation import announcer
# ============================================================
#  SHIELD
# ============================================================
def apply_shield(pilot, incoming_damage, turn_state):
    """Deduct shield health instead of gundam health"""
    shields = turn_state.get("shield_effect", {})
    if pilot not in shields:
        return incoming_damage
    shield = shields[pilot]
    amount = shield["amount"]
    if incoming_damage <= amount:
        shield["amount"] -= incoming_damage
        return 0
    leftover = incoming_damage - amount
    del shields[pilot]
    return leftover
# ============================================================
#  PARRY
# ============================================================
def apply_parry(pilot, incoming_damage, turn_state):
    "Reduces dmg"
    parry = turn_state["parry_effects"].pop(pilot, None)
    if not parry:
        return incoming_damage
    reduce_pct = parry.get("reduce", 0)
    return max(0, int(incoming_damage * (1 - reduce_pct)))
# ============================================================
#  HUNT REACTION
# ============================================================
def apply_hunt_reaction(pilot, turn_state):
    """Hunt maneuvers"""
    return turn_state["hunt_reaction"].pop(pilot, None)
# ============================================================
#  DOT
# ============================================================
def apply_dot_effects(pilot, gundam, turn_state):
    """Applies dot at the start of a turn"""
    if pilot not in turn_state["dot_effect"]:
        return 0
    effect = turn_state["dot_effect"][pilot]
    etype = effect["type"]
    total_damage = 0
    if etype == "burn":
        dmg = effect["damage"]
        gundam.health -= dmg
        total_damage += dmg
    elif etype == "decay":
        gundam.melee -= effect["atk_down"]
        gundam.ranged -= effect["atk_down"]
        gundam.defense -= effect["def_down"]
        gundam.speed -= effect["speed_down"]
    special = get_special(pilot)
    if special:
        rule = get_path_rule(special.path)
        if rule and rule.on_turn_start:
            rule.on_turn_start(pilot)
    effect["turns"] -= 1
    if effect["turns"] <= 0:
        del turn_state["dot_effect"][pilot]
    return total_damage
# ============================================================
#  STUN
# ============================================================
def is_stunned(pilot, turn_state):
    """Traps in stun lock"""
    return pilot in turn_state.get("stun_effect", {})
# ============================================================
#  FREEZE
# ============================================================
def is_frozen(pilot, turn_state):
    """Traps in frozen state"""
    return pilot in turn_state.get("freeze_effect", {})
# ============================================================
#  REVIVE
# ============================================================
def check_revive(pilot, gundam, turn_state):
    """Restores health if defeated"""
    revive_map = turn_state.get("revive_effect", {})
    if pilot not in revive_map:
        return False
    if gundam.health > 0:
        return False
    gundam.health = revive_map[pilot]["hp"]
    del revive_map[pilot]
    announcer.announce_revive(pilot)
    return True
# ============================================================
#  ECHO ENGINE
# ============================================================
def resolve_echo_effects(attacker, attacker_gundam, defender, defender_gundam):
    """Handles secondary actions"""
    if attacker not in turn_state.get("echo_effects", {}):
        return []
    effect = turn_state["echo_effects"].pop(attacker)
    etype = effect["type"]
    results = []
    def _mitigate(target_pilot, raw_dmg):
        mitigated = apply_parry(target_pilot, raw_dmg, turn_state)
        return apply_shield(target_pilot, mitigated, turn_state)
    if etype == "immediate_burst":
        dmg = _mitigate(defender, effect["damage"])
        defender_gundam.health -= dmg
        results.append({"type": "burst", "damage": dmg})
    elif etype == "armor_pierce":
        ignore = effect["ignore_defense"]
        eff_def = defender_gundam.defense * (1 - ignore)
        A = attacker_gundam.melee
        raw_dmg = int(A * (A / (A + eff_def))) if (A + eff_def) > 0 else A
        dmg = _mitigate(defender, raw_dmg)
        defender_gundam.health -= dmg
        results.append({"type": "armor_pierce", "damage": dmg})
    elif etype in ["rifle_burst", "multi_hit_melee"]:
        raw_dmg = effect["hits"] * effect["damage_per_hit"]
        dmg = _mitigate(defender, raw_dmg)
        defender_gundam.health -= dmg
        results.append({"type": etype, "damage": dmg})
    elif etype == "counterattack":
        dmg = _mitigate(attacker, effect["damage"])
        attacker_gundam.health -= dmg
        results.append({"type": "counterattack", "damage": dmg})
    elif etype == "missile_barrage":
        raw_dmg = effect["hits"] * effect["damage_per_hit"]
        dmg = _mitigate(defender, raw_dmg)
        defender_gundam.health -= dmg
        results.append({"type": "missile_barrage", "damage": dmg})
        if random.random() < effect["stun_chance"]:
            turn_state.setdefault("stun_effect", {})
            turn_state["stun_effect"][defender] = {"turns": effect["turns"]}
    elif etype == "charge_detonation":
        dmg = _mitigate(defender, effect["damage"])
        defender_gundam.health -= dmg
        results.append({"type": "charge_detonation", "damage": dmg})
    elif etype == "follow_up":
        raw_dmg = int(attacker_gundam.melee * effect["percent"])
        dmg = _mitigate(defender, raw_dmg)
        defender_gundam.health -= dmg
        results.append({"type": "follow_up", "damage": dmg})
    return results