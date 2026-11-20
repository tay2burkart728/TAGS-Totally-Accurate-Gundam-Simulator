from game_core.turns import turn_state, determine_order, next_turn
from combat_rules.effects import apply_dot_effects, is_stunned, is_frozen, check_revive
from battle_engine.actions import execute_action
from presentation import announcer

def run_turn(pilot1, pilot2):
    """Coordinates turn phase"""
    announcer.announce_turn_start(turn_state["turn_number"])
    g1 = pilot1.gundam
    g2 = pilot2.gundam
    # 1. Start of turn damage-over-time execution
    dot1 = apply_dot_effects(pilot1, g1, turn_state)
    dot2 = apply_dot_effects(pilot2, g2, turn_state)
    if dot1 > 0: announcer.announce_dot(pilot1, dot1, "DOT")
    if dot2 > 0: announcer.announce_dot(pilot2, dot2, "DOT")
    # Early KO verification
    if g1.health <= 0 and not check_revive(pilot1, g1, turn_state):
        return {"winner": pilot2, "loser": pilot1, "dot1": dot1, "dot2": dot2}
    if g2.health <= 0 and not check_revive(pilot2, g2, turn_state):
        return {"winner": pilot1, "loser": pilot2, "dot1": dot1, "dot2": dot2}
    # 2. Calculate initiative/attack sequence
    attacker, defender = determine_order(pilot1, g1, pilot2, g2)
    announcer.attack_order(attacker, defender)
    atk_g = attacker.gundam
    def_g = defender.gundam
    # 3. Attacker execution sequence
    action1 = {"type": "skipped", "damage": 0, "special": None}
    if not (is_stunned(attacker, turn_state) or is_frozen(attacker, turn_state)):
        action1 = execute_action(attacker, defender, atk_g, def_g)
        if action1["type"] == "special":
            announcer.announce_special(attacker, action1["special"])
            for echo in action1.get("echo", []):
                announcer.announce_echo(defender, echo["type"], echo["damage"])
        elif action1["type"] in ["attack", "melee", "ranged"]:
            final_dmg = action1.get("damage", 0)
            def_g.health -= final_dmg
            if final_dmg == 0:
                if defender in turn_state.get("shield_effect", {}):
                    announcer.announce(f"{defender.name}'s Beam Shield completely absorbs the impact!")
                else:
                    announcer.announce_parry(defender)
            else:
                announcer.announce_attack(attacker, defender, final_dmg, action1["type"])
    # Post-attacker KO verification
    if def_g.health <= 0 and not check_revive(defender, def_g, turn_state):
        return {"winner": attacker, "loser": defender, "dot1": dot1, "dot2": dot2, "action": action1}
    # 4. Defender execution sequence (FIXED ENTITY PASS)
    action2 = {"type": "skipped", "damage": 0, "special": None}
    if not (is_stunned(defender, turn_state) or is_frozen(defender, turn_state)):
        action2 = execute_action(defender, attacker, def_g, atk_g) 
        if action2["type"] == "special":
            announcer.announce_special(defender, action2["special"])
            for echo in action2.get("echo", []):
                announcer.announce_echo(attacker, echo["type"], echo["damage"])
        elif action2["type"] in ["attack", "melee", "ranged"]:
            final_dmg = action2.get("damage", 0)
            atk_g.health -= final_dmg
            if final_dmg == 0:
                if attacker in turn_state.get("shield_effect", {}):
                    announcer.announce(f"{attacker.name}'s Beam Shield completely absorbs the impact!")
                else:
                    announcer.announce_parry(attacker)
            else:
                announcer.announce_attack(defender, attacker, final_dmg, action2["type"])

    # Post-defender strike verification incorporates fallback revive checks
    if atk_g.health <= 0 and not check_revive(attacker, atk_g, turn_state):
        return {"winner": defender, "loser": attacker, "dot1": dot1, "dot2": dot2, "action": action2}
    # 5. Decrement turn states
    for status_key in ["stun_effect", "freeze_effect"]:
        for pilot in list(turn_state.get(status_key, {}).keys()):
            turn_state[status_key][pilot]["turns"] -= 1
            if turn_state[status_key][pilot]["turns"] <= 0:
                del turn_state[status_key][pilot]

    next_turn()

    return {"winner": None, "loser": None, "dot1": dot1, "dot2": dot2, "action": (action1, action2)}