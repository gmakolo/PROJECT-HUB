def validate_team_name(name):
    if not isinstance(name, str):
        raise ValueError("Team name must be text")

    name = name.strip()

    if len(name) < 2 or len(name) > 30:
        raise ValueError("Name must be 2–30 characters")

    return name


def register_team(teams, name):
    name = validate_team_name(name)

    for team in teams:
        if team["name"].casefold() == name.casefold():
            raise ValueError("Team already exists")

    if len(teams) >= 8:
        raise ValueError("Maximum of 8 teams allowed")

    team = {
        "id": f"TM{len(teams) + 1:03d}",
        "name": name
    }

    teams.append(team)
    return team


def list_teams(teams):
    return list(teams)