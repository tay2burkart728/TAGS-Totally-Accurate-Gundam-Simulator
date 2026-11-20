from game_core.alignment import get_path_rule, get_special
from game_core.turns import turn_state
from combat_rules.effects import apply_parry, apply_shield, apply_hunt_reaction
from presentation import announcer
def calculate_damage(attacker, defender, attacker_gundam, defender_gundam, attack_type="melee", context=None):
    """Final damage dealt based on atk_type and path"""
    if context is None:
        context = {}
    # ------------------------------------------------------------------
    # 1. RAW ATTACK
    # ------------------------------------------------------------------
    if attack_type == "melee":
        attack_stat = attacker_gundam.melee
    else:
        attack_stat = attacker_gundam.ranged
    defense_stat = defender_gundam.defense
    # ------------------------------------------------------------------
    # 2. CORE DAMAGE EQUATIONS
    # ------------------------------------------------------------------
    if attack_type == "melee":
        base_calc = (attack_stat * attack_stat) / (attack_stat + defense_stat) if (attack_stat + defense_stat) > 0 else attack_stat
        calculated_damage = base_calc * 1.10
    else:
        # Ranged atk ignores 15% of defender's def
        effective_defense = defense_stat * 0.85
        calculated_damage = (attack_stat * attack_stat) / (attack_stat + effective_defense) if (attack_stat + effective_defense) > 0 else attack_stat
    final_damage = max(1, int(calculated_damage))
    # ------------------------------------------------------------------
    # 3. PATH RULE MODS (ATTACKER)
    # ------------------------------------------------------------------
    attacker_special = get_special(attacker)
    if attacker_special:
        attacker_rule = get_path_rule(attacker_special.path)
        if attacker_rule and attacker_rule.modify_damage:
            final_damage = attacker_rule.modify_damage(
                attacker,
                defender,
                final_damage,
                context
            )
    # ------------------------------------------------------------------
    # 4. PATH RULE MODS (DEFENDER)
    # ------------------------------------------------------------------
    defender_special = get_special(defender)
    if defender_special:
        defender_rule = get_path_rule(defender_special.path)
        if defender_rule and defender_rule.modify_damage:
            final_damage = defender_rule.modify_damage(
                attacker,
                defender,
                final_damage,
                context
            )
    # ==================================================================
    # 5. MITIGATION LAYER
    # ==================================================================
    if context.get("ignore_dodge") == True:
        apply_hunt_reaction(defender, turn_state)
    else:
        dodge_active = apply_hunt_reaction(defender, turn_state)
        if dodge_active and dodge_active.get("type") == "dodge": 
            announcer.announce_dodge(defender)
            return 0
    return max(0, int(final_damage))