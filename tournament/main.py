from tournament.seeding import select_fighters, random_seeding
from tournament.bracket import run_round
from presentation.announcer import (announce, announce_round_start, announce_elimination, announce_champion)
from presentation.bracket_display import show_bracket
from presentation.image_tools import build_final_collage
from presentation.ui_controller import start_ui, update_ui_for_round, ui_draw_once, register_dots
from presentation.radar_display import make_fighter_dot
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
DOT_COLORS = [
    (255, 80, 80),
    (80, 160, 255),
    (80, 255, 120),
    (255, 200, 80),
    (200, 120, 255),
    (255, 120, 200),
    (120, 255, 220),
    (240, 240, 240),
]
def sync_radars(results, dots):
    """Put this round's fighters on the radar for the environment they fought in"""
    earth_fighters = []
    space_fighters = []
    for r in results:
        winner_dot = dots[r["winner"]]
        loser_dot = dots[r["loser"]]
        winner_dot["alive"] = True
        loser_dot["alive"] = False
        if r["environment"] == "Earth":
            earth_fighters.extend([winner_dot, loser_dot])
        else:
            space_fighters.extend([winner_dot, loser_dot])
    update_ui_for_round(earth_fighters, space_fighters)
    ui_draw_once()
def run_tournament(roster, use_ui=True):
    """Coordinates battles and brackets"""
    if len(roster) < 8:
        raise ValueError("Tournament requires at least 8 pilots.")
    fighters = select_fighters(roster)
    dots = {}
    if use_ui:
        start_ui(fighters)
        dots = {pilot: make_fighter_dot(pilot, color) for pilot, color in zip(fighters, DOT_COLORS)}
        register_dots(dots)
        ui_draw_once()
    q_pairs = random_seeding(fighters)
    show_tournament_start(fighters, q_pairs)
    # -----------------------------------------------------
    # QUARTERFINALS (8 Pilots -> 4 Winners)
    # -----------------------------------------------------
    announce_round_start("Quarterfinals")
    semi_fighters, q_results = run_round(q_pairs, "Quarterfinals")
    if use_ui:
        sync_radars(q_results, dots)
    show_round_results(q_results)
    show_bracket(q_pairs, winners=semi_fighters, round_name="Quarterfinals")
    # -----------------------------------------------------
    # SEMIFINALS (4 Pilots -> 2 Winners)
    # -----------------------------------------------------
    announce_round_start("Semifinals")
    s_pairs = list(zip(semi_fighters[0::2], semi_fighters[1::2]))
    finalists, s_results = run_round(s_pairs, "Semifinals")
    if use_ui:
        sync_radars(s_results, dots)
    show_round_results(s_results)
    show_bracket(s_pairs, winners=finalists, round_name="Semifinals")
    # -----------------------------------------------------
    # FINALS (2 Pilots -> 1 Champion)
    # -----------------------------------------------------
    announce_round_start("Finals")
    f_pairs = list(zip(finalists[0::2], finalists[1::2]))
    champion_list, f_results = run_round(f_pairs, "Finals")
    if use_ui:
        sync_radars(f_results, dots)
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
