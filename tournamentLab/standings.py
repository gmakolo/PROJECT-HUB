"""
engerr B
"""
def compute_standings(teams, fixtures):
    table = {}

    for team in teams:
        table[team["id"]] = {
            "team_id": team["id"],
            "team": team["name"],
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "gf": 0,
            "ga": 0,
            "gd": 0,
            "points": 0
        }

    for match in fixtures:
        if match["status"] != "played":
            continue

        home = table[match["home_id"]]
        away = table[match["away_id"]]

        hs = match["home_score"]
        aws = match["away_score"]

        home["played"] += 1
        away["played"] += 1

        home["gf"] += hs
        home["ga"] += aws

        away["gf"] += aws
        away["ga"] += hs

        if hs > aws:
            home["wins"] += 1
            away["losses"] += 1
            home["points"] += 3

        elif hs < aws:
            away["wins"] += 1
            home["losses"] += 1
            away["points"] += 3

        else:
            home["draws"] += 1
            away["draws"] += 1
            home["points"] += 1
            away["points"] += 1

    for row in table.values():
        row["gd"] = row["gf"] - row["ga"]

    return sorted(
        table.values(),
        key=lambda row: (
            -row["points"],
            -row["gd"],
            -row["gf"],
            row["team"].casefold()
        )
    )


def league_complete(fixtures):
    return bool(fixtures) and all(
        match["status"] == "played"
        for match in fixtures
    )


def champion(teams, fixtures):
    if not league_complete(fixtures):
        return None

    standings = compute_standings(teams, fixtures)

    if standings:
        return standings[0]["team"]

    return None