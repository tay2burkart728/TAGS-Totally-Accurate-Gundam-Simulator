from game_core.turns import turn_state
from presentation.announcer import announce_dot
from game_core.alignment import get_special, get_path_rule
import random
# ============================================================
# HELPERS
# ============================================================
def _schedule_echo(attacker, effect):
    """Tracks immediate or delayed echo"""
    turn_state.setdefault("echo_effects", {})
    turn_state["echo_effects"][attacker] = effect
def _schedule_dot(target, effect):
    """Tracks DOT"""
    turn_state.setdefault("dot_effect", {})
    turn_state["dot_effect"][target] = effect
def _schedule_status(key, target, effect):
    """Tracks status"""
    turn_state.setdefault(key, {})
    turn_state[key][target] = effect
# ============================================================
# DESTRUCTION PATH
# ============================================================
def handle_berserk(attacker, target, effect, attacker_gundam, target_gundam):
    """Increase melee, decrease defense"""
    attacker_gundam.melee += effect["melee_bonus"]
    attacker_gundam.defense += effect["defense_penalty"]
    return {"type": "berserk_ready"}
def handle_burst(attacker, target, effect, attacker_gundam, target_gundam):
    """Burst of pure damage"""
    _schedule_echo(attacker, {
        "type": "immediate_burst",
        "damage": effect["damage"]
    })
    return {"type": "burst_scheduled"}
def handle_armor_pierce(attacker, target, effect, attacker_gundam, target_gundam):
    """ATK ignores defense"""
    _schedule_echo(attacker, {
        "type": "armor_pierce",
        "ignore_defense": effect["ignore_defense"]
    })
    return {"type": "armor_pierce_scheduled"}
# ============================================================
# HUNT
# ============================================================
def handle_dodge(attacker, target, effect, attacker_gundam, target_gundam):
    """Avoids next hit"""
    _schedule_status("hunt_reaction", target, {"type": "dodge"})
    return {"type": "dodge_scheduled"}
def handle_rifle_burst(attacker, target, effect, attacker_gundam, target_gundam):
    "Double hits"
    _schedule_echo(attacker, {
        "type": "rifle_burst",
        "hits": effect["hits"],
        "damage_per_hit": effect["damage_per_hit"]
    })
    return {"type": "rifle_burst_scheduled"}
# ============================================================
# ERUDITION
# ============================================================
def handle_missile_barrage(attacker, target, effect, attacker_gundam, target_gundam):
    """Multiple hits w/ stun"""
    _schedule_echo(attacker, {
        "type": "missile_barrage",
        "hits": effect["hits"],
        "damage_per_hit": effect["damage_per_hit"],
        "stun_chance": effect["stun_chance"],
        "turns": effect.get("turns", 1)
    })
    return {"type": "missile_barrage_scheduled"}
def handle_charge_detonation(attacker, target, effect, attacker_gundam, target_gundam):
    """Ticking bomb"""
    _schedule_echo(attacker, {
        "type": "charge_detonation",
        "damage": effect["damage"]
    })
    return {"type": "charge_detonation_scheduled"}
# ============================================================
# HARMONY
# ============================================================
def handle_speed_buff(attacker, target, effect, attacker_gundam, target_gundam):
    """Mods base speed"""
    attacker_gundam.speed += effect["amount"]
    return {"type": "speed_buff_applied"}
def handle_follow_up(attacker, target, effect, attacker_gundam, target_gundam):
    """Attacks again"""
    _schedule_echo(attacker, {
        "type": "follow_up",
        "percent": effect["percent"]
    })
    return {"type": "follow_up_scheduled"}
# ============================================================
# NIHILITY
# ============================================================
def handle_burn(attacker, target, effect, attacker_gundam, target_gundam):
    """Hope it burns"""
    _schedule_dot(target, {
        "type": "burn",
        "damage_per_turn": effect["damage_per_turn"],
        "turns": effect["turns"]
    })
    announce_dot(target, effect["damage_per_turn"], "burn")
    return {"type": "burn_applied"}
def handle_decay(attacker, target, effect, attacker_gundam, target_gundam):
    """All stats decrease"""
    _schedule_dot(target, {
        "type": "decay",
        "atk_down": effect["atk_down"],
        "def_down": effect["def_down"],
        "speed_down": effect["speed_down"],
        "turns": effect["turns"]
    })
    return {"type": "decay_applied"}
# ============================================================
# PRESERVATION
# ============================================================
def handle_parry(attacker, target, effect, attacker_gundam, target_gundam):
    """the platypus. lol no Guards hits and counterattacks"""
    _schedule_status("parry_effects", attacker, {"reduce": effect["reduce"]})
    _schedule_echo(attacker, {
        "type": "counterattack",
        "damage": effect["counter_damage"]
    })
    return {"type": "parry_scheduled"}
def handle_shield(attacker, target, effect, attacker_gundam, target_gundam):
    """Health buffer"""
    turn_state.setdefault("shield_effect", {})
    turn_state["shield_effect"][attacker] = {"amount": effect["amount"]}
    return {"type": "shield_applied"}
# ============================================================
# ABUNDANCE
# ============================================================
def handle_heal(attacker, target, effect, attacker_gundam, target_gundam):
    """Restores some health"""
    heal_amount = effect["amount"]
    special = get_special(attacker)
    if special:
        rule = get_path_rule(special.path)
        if rule and rule.modify_heal:
            heal_amount = rule.modify_heal(attacker, heal_amount)
    attacker_gundam.health = min(attacker_gundam.max_health, attacker_gundam.health + heal_amount)
    return {"type": "heal_applied"}
def handle_revive(attacker, target, effect, attacker_gundam, target_gundam):
    """Resurrection"""
    turn_state.setdefault("revive_effect", {})
    turn_state["revive_effect"][attacker] = {"hp": effect["hp"]}
    return {"type": "revive_scheduled"}
# ============================================================
# REMEMBRANCE
# ============================================================
def handle_stun(attacker, target, effect, attacker_gundam, target_gundam):
    "Stuns target"
    if random.random() < effect["chance"]:
        _schedule_status("stun_effect", target, {
            "turns": effect["turns"]
        })
        return {"type": "stun_success"}
    return {"type": "stun_failed"}
def handle_self_mutilation(attacker, target, effect, attacker_gundam, target_gundam):
    """Takes dmg when frozen"""
    _schedule_status("freeze_effect", target, {
        "turns": effect["freeze_turns"]
    })
    attacker_gundam.health -= effect["self_damage"]
    return {"type": "mutilation_applied"}
# ============================================================
# PROPAGATION
# ============================================================
def handle_multi_hit(attacker, target, effect, attacker_gundam, target_gundam):
    """Several hits"""
    _schedule_echo(attacker, {
        "type": "multi_hit_melee",
        "hits": effect["hits"],
        "damage_per_hit": effect["damage_per_hit"]
    })
    return {"type": "multi_hit_scheduled"}
# ============================================================
# TABLE
# ============================================================
SPECIAL_HANDLERS = {
    "berserk": handle_berserk,
    "burst": handle_burst,
    "armor_pierce": handle_armor_pierce,
    "dodge": handle_dodge,
    "rifle_burst": handle_rifle_burst,
    "missile_barrage": handle_missile_barrage,
    "charge_detonation": handle_charge_detonation,
    "speed_buff": handle_speed_buff,
    "follow_up": handle_follow_up,
    "burn": handle_burn,
    "system_decay": handle_decay,
    "parry": handle_parry,
    "shield": handle_shield,
    "heal": handle_heal,
    "revive": handle_revive,
    "stun": handle_stun,
    "self_mutilation": handle_self_mutilation,
    "multi_hit_melee": handle_multi_hit,
}