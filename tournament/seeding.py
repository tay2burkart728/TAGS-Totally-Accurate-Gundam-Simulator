import random
def select_fighters(roster, count=8):
    """Randomizes pilots for tournament"""
    if len(roster) < count:
        raise ValueError(f"Roster has only {len(roster)} pilots, but {count} are required.")
    fighters = random.sample(roster, count)
    for pilot in fighters:
        pilot.eliminated = False
        if getattr(pilot, "gundam", None):
            pilot.gundam.reset()
    return fighters
def random_seeding(fighters):
    """Pairs fighters"""
    if len(fighters) % 2 != 0:
        raise ValueError("Fighter count must be even for bracket pairing.")
    shuffled_pool = fighters[:]
    random.shuffle(shuffled_pool)
    half_index = len(shuffled_pool) // 2
    top_bracket = shuffled_pool[:half_index]
    bottom_bracket = list(reversed(shuffled_pool[half_index:]))
    bracket_pairs = list(zip(top_bracket, bottom_bracket))
    return bracket_pairs
