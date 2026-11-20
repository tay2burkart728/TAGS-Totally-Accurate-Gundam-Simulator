from game_core.pilot_roster import ROSTER
from tournament.main import run_tournament
from presentation.announcer import announce
from presentation.ui_controller import wait_for_start, ui_loop
def main():
    """FINAL PART YAY"""
    wait_for_start()
    announce("Initializing Gundam Tournament System...")
    results = run_tournament(ROSTER)
    champion = results["champion"]
    announce(f"The tournament has concluded. Final Champion: {champion.name}!")
    for pilot in ROSTER:
        if getattr(pilot, "gundam", None):
            pilot.gundam.reset()
    ui_loop()
if __name__ == "__main__":
    main()
