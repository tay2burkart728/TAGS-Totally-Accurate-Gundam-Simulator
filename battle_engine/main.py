from game_core.turns import reset_turn_state
from game_core.environment import choose_environment, apply_environment
from battle_engine.turn import run_turn
from presentation.announcer import announce_match_start, announce_ko
def run_battle(p1, p2):
    """gundamvgundam time"""
    reset_turn_state()
    environment = choose_environment()
    apply_environment(p1.gundam, environment)
    apply_environment(p2.gundam, environment)
    battle_log = []
    announce_match_start(p1, p2, environment.name)
    while True:
        turn_result = run_turn(p1, p2)
        battle_log.append(turn_result)
        if turn_result["winner"] is not None:
            winner = turn_result["winner"]
            loser = turn_result["loser"]
            announce_ko(winner, loser)
            return {
                "winner": winner,
                "loser": loser,
                "log": battle_log,
                "environment": environment.name,
            }