import random
#What happens in a turn
turn_state = {
    "dot_effect": {}, 
    "freeze_effect": {},
    "stun_effect": {},
    "echo_effects": {},
    "parry_effects": {},
    "shield_effect": {},
    "revive_effect": {},
    "hunt_reaction": {},      
    "turn_number": 1,
}
def reset_turn_state():
    """Effect baptism"""
    turn_state["dot_effect"] = {}
    turn_state["freeze_effect"] = {}
    turn_state["stun_effect"] = {}
    turn_state["echo_effects"] = {}
    turn_state["parry_effects"] = {}
    turn_state["shield_effect"] = {}
    turn_state["revive_effect"] = {}
    turn_state["turn_number"] = 1
# ---------------------------------------------------------
# TURN ORDER
# ---------------------------------------------------------
def determine_order(pilot1, gundam1, pilot2, gundam2):
    """Determine which pilot acts first this turn."""
    s1 = gundam1.speed
    s2 = gundam2.speed
    if s1 > s2:
        return pilot1, pilot2
    if s2 > s1:
        return pilot2, pilot1
    # Tie in speeds
    return random.choice([(pilot1, pilot2), (pilot2, pilot1)])
# ---------------------------------------------------------
# TURN ADVANCEMENT
# ---------------------------------------------------------
def next_turn():
    """Round count"""
    turn_state["turn_number"] += 1
