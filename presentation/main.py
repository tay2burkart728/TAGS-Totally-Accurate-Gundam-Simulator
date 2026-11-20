from game_core.pilot_roster import ROSTER
from tournament.main import run_tournament
from presentation.announcer import announce
def main():
    """FINAL PART YAY"""
    announce("Initializing Gundam Tournament System...")
    results = run_tournament(ROSTER)
    champion = results["champion"]
    announce(f"The tournament has concluded. Final Champion: {champion.name}!")
    for pilot in ROSTER:
        if getattr(pilot, "gundam", None):
            pilot.gundam.reset()
if __name__ == "__main__":
    main()
