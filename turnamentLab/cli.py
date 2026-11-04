
"""
Engineer B owns the command-line menu and connects the features.
"""

import json
from pathlib import Path

from teams import register_team, list_teams
from fixtures import generate_fixtures
from results import record_result
from standings import compute_standings, champion
from storage import save_season, load_season

SAVE_FILE = Path("tournament.json")


def show_standings(teams, fixtures):
    standings = compute_standings(teams, fixtures)

    print("\nLEAGUE TABLE")
    print("Team | P | W | D | L | GF | GA | GD | Points")

    for row in standings:
        print(
            f"{row['team']} | {row['played']} | "
            f"{row['wins']} | {row['draws']} | "
            f"{row['losses']} | {row['gf']} | "
            f"{row['ga']} | {row['gd']} | {row['points']}"
        )

    winner = champion(teams, fixtures)

    if winner:
        print(f"\nChampion: {winner}")
    else:
        print("\nLeague in progress.")


def run():
    teams = []
    fixtures = []

    while True:
        print("""
WELCOME TO TOURNAMENT LAB!
PLEASE CHOOSE AN OPTION :
1. Register team
2. List teams
3. Generate fixtures
4. List fixtures
5. Record result
6. Show standings
7. Save season
8. Load season
0. Quit
""")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                team = register_team(teams, input("Team name: "))
                print("Registered:", team["name"])

            elif choice == "2":
                for team in list_teams(teams):
                    print(team["id"], team["name"])

            elif choice == "3":
                fixtures = generate_fixtures(teams, fixtures)
                print("Fixtures generated:", len(fixtures))

            elif choice == "4":
                for match in fixtures:
                    home = next(
                        t["name"] for t in teams
                        if t["id"] == match["home_id"]
                    )
                    away = next(
                        t["name"] for t in teams
                        if t["id"] == match["away_id"]
                    )

                    if match["status"] == "played":
                        result = (
                            f"{match['home_score']}-"
                            f"{match['away_score']}"
                        )
                    else:
                        result = "Pending"

                    print(match["id"], home, "vs", away, result)

            elif choice == "5":
                fixture_id = input("Fixture ID: ").strip().upper()

                home_score = int(input("Home score: "))
                away_score = int(input("Away score: "))

                record_result(
                    fixtures,
                    fixture_id,
                    home_score,
                    away_score
                )

                print("Result recorded.")

            elif choice == "6":
                show_standings(teams, fixtures)

            elif choice == "7":
                save_season(SAVE_FILE, teams, fixtures)
                print("Season saved.")

            elif choice == "8":
                new_teams, new_fixtures = load_season(SAVE_FILE)
                teams, fixtures = new_teams, new_fixtures
                print("Season loaded.")

            elif choice == "0":
                print("Goodbye!")
                break

            else:
                print("Invalid menu choice.")

        except (ValueError, OSError, json.JSONDecodeError) as error:
            print("Error:", error)


if __name__ == "__main__":
    run()
