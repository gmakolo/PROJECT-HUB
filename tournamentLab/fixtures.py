def generate_fixtures(teams, existing_fixtures=None):
    if not 4 <= len(teams) <= 8:
        raise ValueError("Register 4–8 teams first")

    if existing_fixtures:
        raise ValueError("Fixtures already generated")

    fixtures = []

    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            fixture = {
                "id": f"M{len(fixtures) + 1:03d}",
                "home_id": teams[i]["id"],
                "away_id": teams[j]["id"],
                "status": "pending",
                "home_score": None,
                "away_score": None
            }

            fixtures.append(fixture)

    return fixtures