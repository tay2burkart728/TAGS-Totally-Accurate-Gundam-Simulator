from tournament.match import run_match
def run_round(pairs, round_name):
    """all matchup data"""
    winners = []
    results = []
    for p1, p2 in pairs:
        result = run_match(p1, p2, tournament_round=round_name)
        winners.append(result["winner"])
        results.append(result)
    return winners, results