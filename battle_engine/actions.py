import random
from combat_rules.router import route_action
from combat_rules.damage import calculate_damage
from combat_rules.effects import resolve_echo_effects, is_frozen, is_stunned
from game_core.alignment import get_special
from game_core.turns import turn_state

def execute_action(attacker, defender, attacker_gundam, defender_gundam):
    """Applies combat_rules"""
    attack_type = random.choice(["melee", "ranged", "special"])
    special = None
    if attack_type == "special":
        special = get_special(attacker)
        if special and (is_frozen(defender, turn_state) or is_stunned(defender, turn_state)):
            attack_type = random.choice(["melee", "ranged"])
            special = None
        elif not special:
            attack_type = "melee" 
    route_result = route_action(
        attack_type, attacker, defender, attacker_gundam, defender_gundam, special
    )
    #global
    result = {
        "type": attack_type,
        "attacker": attacker.name,
        "defender": defender.name,
        "damage": 0,
        "special": special.name if special else None,
        "echo": [],
        "resolved_by": "router_pipeline"
    }
    #within turn
    context = {
        "hits": 1,
        "acted_last": defender if turn_state["turn_number"] > 1 else None
    }
    if attack_type == "special":
        echo_results = resolve_echo_effects(
            attacker, attacker_gundam, defender, defender_gundam
        )
        result["echo"] = echo_results
        result["handler_result"] = route_result.get("result")
    else:
        dmg = calculate_damage(
            attacker, defender, attacker_gundam, defender_gundam, attack_type, context
        )
        result["damage"] = dmg

    return result
