"""
endineeer B
"""
def record_result(fixtures, fixture_id, home_score, away_score):
    if type(home_score) is not int or home_score < 0:
        raise ValueError("Invalid home score")

    if type(away_score) is not int or away_score < 0:
        raise ValueError("Invalid away score")

    fixture = None

    for match in fixtures:
        if match["id"] == fixture_id:
            fixture = match
            break

    if fixture is None:
        raise ValueError("Fixture not found")

    if fixture["status"] != "pending":
        raise ValueError("Result already recorded")

    fixture["home_score"] = home_score
    fixture["away_score"] = away_score
    fixture["status"] = "played"

    return fixture