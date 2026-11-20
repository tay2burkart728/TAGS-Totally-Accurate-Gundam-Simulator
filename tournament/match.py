from battle_engine.main import run_battle
def run_match(pilot1, pilot2, tournament_round=None):
    """match up"""
    # Forward the combatants directly to the battle loop orchestrator
    result = run_battle(pilot1, pilot2)
    winner = result["winner"]
    loser = result["loser"]
    loser.eliminated = True
    winner.wins += 1
    loser.losses += 1
    if tournament_round:
        clean_round = tournament_round.lower()
        if "quarter" in clean_round:
            winner.quarterfinals += 1
            loser.quarterfinals += 1
        elif "semi" in clean_round:
            winner.semifinals += 1
            loser.semifinals += 1
        elif "final" in clean_round:
            winner.championships += 1  
    return {
        "winner": winner,
        "loser": loser,
        "environment": result["environment"],
        "log": result["log"],
    }
