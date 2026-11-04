import json
from pathlib import Path

SCHEMA_VERSION = 1


def save_season(path, teams, fixtures):
    data = {
        "schema_version": SCHEMA_VERSION,
        "teams": teams,
        "fixtures": fixtures
    }

    Path(path).write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )


def validate_season(data):
    if not isinstance(data, dict):
        raise ValueError("Invalid save file")

    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Unsupported save version")

    teams = data.get("teams")
    fixtures = data.get("fixtures")

    if not isinstance(teams, list) or not isinstance(fixtures, list):
        raise ValueError("Teams and fixtures must be lists")

    team_ids = set()
    team_names = set()

    for team in teams:
        if not isinstance(team, dict) or set(team) != {"id", "name"}:
            raise ValueError("Invalid team record")

        name = team["name"]

        if not isinstance(name, str) or not 2 <= len(name.strip()) <= 30:
            raise ValueError("Invalid team name")

        if not isinstance(team["id"], str) or not team["id"]:
            raise ValueError("Invalid team ID")

        if team["id"] in team_ids:
            raise ValueError("Duplicate team ID")

        if name.strip().casefold() in team_names:
            raise ValueError("Duplicate team name")

        team_ids.add(team["id"])
        team_names.add(name.strip().casefold())

    fixture_ids = set()
    pairs = set()

    required = {
        "id", "home_id", "away_id",
        "status", "home_score", "away_score"
    }

    for match in fixtures:
        if not isinstance(match, dict) or set(match) != required:
            raise ValueError("Invalid fixture record")

        if not isinstance(match["id"], str) or not match["id"]:
            raise ValueError("Invalid fixture ID")

        if match["id"] in fixture_ids:
            raise ValueError("Duplicate fixture ID")

        fixture_ids.add(match["id"])

        home = match["home_id"]
        away = match["away_id"]

        if home not in team_ids or away not in team_ids:
            raise ValueError("Fixture references unknown team")

        if home == away:
            raise ValueError("A team cannot play itself")

        pair = frozenset((home, away))

        if pair in pairs:
            raise ValueError("Duplicate team pairing")

        pairs.add(pair)

        hs = match["home_score"]
        aws = match["away_score"]

        if match["status"] == "pending":
            if hs is not None or aws is not None:
                raise ValueError("Pending fixture cannot have scores")

        elif match["status"] == "played":
            if (
                type(hs) is not int or hs < 0
                or type(aws) is not int or aws < 0
            ):
                raise ValueError("Invalid match scores")

        else:
            raise ValueError("Invalid fixture status")

    return teams, fixtures


def load_season(path):
    data = json.loads(
        Path(path).read_text(encoding="utf-8")
    )

    return validate_season(data)