from tournament.seeding import select_fighters, random_seeding
from tournament.bracket import run_round
from presentation.announcer import (announce, announce_round_start, announce_elimination, announce_champion)
from presentation.bracket_display import show_bracket
from presentation.image_tools import build_final_collage
# ============================================================
# PRESENTATION HELPERS
# ============================================================

def show_tournament_start(fighters, initial_pairs):
    """Broadcast"""
    announce("Welcome to the Gundam Grand Tournament!")
    announce("Introducing the 8 contenders!")
    for p in fighters:
        announce(f"{p.name} piloting {p.gundam.name}")
    show_bracket(initial_pairs, winners=None, round_name="Initial Seeding")
def show_round_results(results):
    """Who wins and loses"""
    for r in results:
        winner = r["winner"]
        loser = r["loser"]
        env = r["environment"]
        announce(f"{winner.name} defeats {loser.name} in {env}!")
        announce_elimination(loser)
# ============================================================
# MAIN TOURNAMENT FLOW
# ============================================================
def run_tournament(roster):
    """Coordinates battles and brackets"""
    if len(roster) < 8:
        raise ValueError("Tournament requires at least 8 pilots.")
    fighters = select_fighters(roster)
    q_pairs = random_seeding(fighters)
    show_tournament_start(fighters, q_pairs)
    # -----------------------------------------------------
    # QUARTERFINALS (8 Pilots -> 4 Winners)
    # -----------------------------------------------------
    announce_round_start("Quarterfinals")
    semi_fighters, q_results = run_round(q_pairs, "Quarterfinals")
    show_round_results(q_results)
    show_bracket(q_pairs, winners=semi_fighters, round_name="Quarterfinals")
    # -----------------------------------------------------
    # SEMIFINALS (4 Pilots -> 2 Winners)
    # -----------------------------------------------------
    announce_round_start("Semifinals")
    s_pairs = list(zip(semi_fighters[0::2], semi_fighters[1::2]))
    finalists, s_results = run_round(s_pairs, "Semifinals")
    show_round_results(s_results)
    show_bracket(s_pairs, winners=finalists, round_name="Semifinals")
    # -----------------------------------------------------
    # FINALS (2 Pilots -> 1 Champion)
    # -----------------------------------------------------
    announce_round_start("Finals")
    f_pairs = list(zip(finalists[0::2], finalists[1::2]))
    champion_list, f_results = run_round(f_pairs, "Finals")
    champion = champion_list[0]
    champion.championships += 1
    show_round_results(f_results)
    show_bracket(f_pairs, winners=[champion], round_name="Finals")
    announce_champion(champion)
    # -----------------------------------------------------
    # FINAL ARTISTIC SUMMARY COLLAGE
    # -----------------------------------------------------
    build_final_collage(fighters, champion)
    return {
        "champion": champion,
        "quarterfinals": q_results,
        "semifinals": s_results,
        "finals": f_results,
        "fighters": fighters,
    }