from combat_rules.special_handlers import SPECIAL_HANDLERS
from game_core.alignment import get_path_rule

# ============================================================
# SPECIAL DISPATCH
# ============================================================
def special_attack(attacker, defender, attacker_gundam, defender_gundam, special):
    """Connects long lost specials"""
    effect = special.effect
    stype = effect["type"]
    handler = SPECIAL_HANDLERS.get(stype)
    if not handler:
        return {
            "type": "unknown_special",
            "special": special.name
        }
    result = handler(
        attacker,
        defender,
        effect,
        attacker_gundam,
        defender_gundam
    )
    rule = get_path_rule(special.path)
    if rule and rule.on_special_used:
        rule.on_special_used(attacker, defender, effect)
    return result
# ============================================================
# ROUTER
# ============================================================
def route_action(action_type, attacker, defender, attacker_gundam, defender_gundam, special=None):
    """Highway patrol"""
    # ---------------------------------------------------------
    # SPECIAL PATH
    # ---------------------------------------------------------
    if action_type == "special" and special:
        return {
            "type": "special",
            "special": special.name,
            "result": special_attack(
                attacker,
                defender,
                attacker_gundam,
                defender_gundam,
                special
            )
        }
    # ---------------------------------------------------------
    # NORMAL ATTACK PATH (no execution here)
    # ---------------------------------------------------------
    return {
        "type": "attack"
    }