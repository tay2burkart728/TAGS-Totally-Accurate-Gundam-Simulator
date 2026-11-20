import random

ANNOUNCERS = [
    "Abigail Burkart", 
    "Joe Burkart II", 
    "Toby Burkart"
]
def broadcast():
    """Spice"""
    return f"[{random.choice(ANNOUNCERS)}]"
def attack_order(attacker, defender):
    """Reports whos on first"""
    msg = f"{broadcast()} {attacker.name} acts before {defender.name}!"
    print(msg)
    return msg
# ----------------------------------------------------------------------
# BASIC TOURNAMENT AND TOURNAMENT BRACKET TRACKERS
# ----------------------------------------------------------------------
def announce(text):
    """General format"""
    msg = f"{broadcast()} {text}"
    print(msg)
    return msg
def announce_round_start(name):
    """Round format"""
    msg = f"{broadcast()} --- {name.upper()} BEGINS ---"
    print(msg)
    return msg
def announce_turn_start(turn_number):
    """Turn format"""
    msg = f"{broadcast()} --- TURN {turn_number} ---"
    print(msg)
    return msg
def announce_match_start(p1, p2, arena):
    """Pairing format"""
    msg = f"{broadcast()} {p1.name} vs {p2.name} in {arena}!"
    print(msg)
    return msg
def announce_elimination(loser):
    """Death format"""
    msg = f"{broadcast()} {loser.name} has been eliminated from the tournament!"
    print(msg)
    return msg
def announce_champion(champion):
    """Winner format"""
    msg = f"{broadcast()} {champion.name} is the Gundam Grand Champion!"
    print(msg)
    return msg
# ----------------------------------------------------------------------
# COMBAT ENCOUNTER LOG READOUT SEQUENCES
# ----------------------------------------------------------------------
def announce_attack(attacker, defender, damage, attack_type):
    """Attack format"""
    if damage <= 0:
        msg = f"{broadcast()} {attacker.name}'s attack misses {defender.name}!"
        print(msg)
    else:
        msg = f"{broadcast()} {attacker.name} strikes {defender.name} with a {attack_type} attack for {damage} damage!"
        print(msg)
    return msg
def announce_special(attacker, move_name):
    """Special format"""
    if not move_name:
        move_name = "SPECIAL MOVE"
    msg = f"{broadcast()} {attacker.name} activates SPECIAL MOVE: {move_name}!"
    print(msg)
    return msg
def announce_dodge(defender):
    """Dodge unique format"""
    msg = f"{broadcast()} {defender.name} dodges the attack!"
    print(msg)
    return msg
def announce_parry(defender):
    """Parry unique format """
    msg = f"{broadcast()} {defender.name} parries the attack!"
    print(msg)
    return msg
def announce_dot(target, damage, dot_type):
    """DOT unique format"""
    msg = f"{broadcast()} {target.name} suffers {damage} damage from {dot_type}!"
    print(msg)
    return msg
def announce_echo(target, echo_type, damage):
    """Echo unique format"""
    msg = f"{broadcast()} Echo damage! {target.name} takes {damage} from {echo_type}!"
    print(msg)
    return msg
def announce_revive(pilot):
    """Revive uniwue format"""
    msg = f"{broadcast()} {pilot.name} miraculously returns to the fight!"
    print(msg)
    return msg
def announce_ko(winner, loser):
    """KO format"""
    msg = f"{broadcast()} {loser.name} is defeated! {winner.name} wins the match!"
    print(msg)
    return msg
