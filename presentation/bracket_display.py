def show_bracket(pairs, winners=None, round_name=None):
    """Bracket dressup"""
    print("\n=== TOURNAMENT BRACKET ===")
    if round_name:
        print(f"--- {round_name.upper()} ---")
    for p1, p2 in pairs:
        status1 = "ELIMINATED" if p1.eliminated else "ACTIVE"
        status2 = "ELIMINATED" if p2.eliminated else "ACTIVE"
        line = f"{p1.name:<20} [{status1}]  vs  {p2.name:<20} [{status2}]"
        if winners:
            if p1 in winners:
                line += f"   --> {p1.name.upper()} ADVANCES"
            elif p2 in winners:
                line += f"   --> {p2.name.upper()} ADVANCES"
        print(line)
    print() 