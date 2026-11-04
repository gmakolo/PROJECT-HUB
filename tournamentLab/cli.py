
import json
from pathlib import Path

from teams import register_team, list_teams
from fixtures import generate_fixtures
from results import record_result
from standings import compute_standings, champion, league_complete
from storage import save_season, load_season


SAVE_FILE = Path("tournament.json")


def setup_tournament():
    print("\n================================")
    print("WELCOME TO TOURNAMENT LAB!")
    print("================================")

    while True:
        tournament_name = input("Enter tournament name: ").strip()

        if tournament_name:
            break

        print("Tournament name cannot be empty.")

    while True:
        team_count = input("How many teams? Choose 4 or 8: ").strip()

        if team_count in ("4", "8"):
            team_count = int(team_count)
            break

        print("Please choose either 4 or 8.")

    teams = []

    print("\nREGISTER YOUR TEAMS")

    while len(teams) < team_count:
        number = len(teams) + 1

        print(f"\nTeam {number} of {team_count}")

        name = input("Enter team name: ")

        try:
            team = register_team(teams, name)
            print(f"{team['name']} registered successfully!")

        except ValueError as error:
            print("Error:", error)

    fixtures = generate_fixtures(teams)

    print("\n================================")
    print(f"{tournament_name} IS READY!")
    print(f"{len(teams)} teams registered.")
    print(f"{len(fixtures)} fixtures generated.")
    print("================================")

    return tournament_name, teams, fixtures


def show_teams(teams):
    print("\nREGISTERED TEAMS")

    for team in list_teams(teams):
        print(f"{team['id']} - {team['name']}")


def show_fixtures(teams, fixtures):
    print("\nTOURNAMENT FIXTURES")

    if not fixtures:
        print("No fixtures available.")
        return

    for match in fixtures:
        home = next(
            team["name"] for team in teams
            if team["id"] == match["home_id"]
        )

        away = next(
            team["name"] for team in teams
            if team["id"] == match["away_id"]
        )

        if match["status"] == "played":
            result = (
                f"{match['home_score']}-{match['away_score']}"
            )
        else:
            result = "Pending"

        print(f"{match['id']}: {home} vs {away} | {result}")


def show_standings(teams, fixtures):
    standings = compute_standings(teams, fixtures)

    print("\nLEAGUE TABLE")
    print("Team | P | W | D | L | GF | GA | GD | Points")

    for row in standings:
        print(
            f"{row['team']} | {row['played']} | "
            f"{row['wins']} | {row['draws']} | "
            f"{row['losses']} | {row['gf']} | "
            f"{row['ga']} | {row['gd']} | "
            f"{row['points']}"
        )

    winner = champion(teams, fixtures)

    if winner:
        print(f"\nCHAMPION: {winner}")
    else:
        print("\nTournament in progress.")


def show_team_statistics(teams, fixtures):
    standings = compute_standings(teams, fixtures)

    print("\nTEAM STATISTICS")

    for row in standings:
        print(f"\n{row['team']}")
        print(f"Matches played: {row['played']}")
        print(f"Wins: {row['wins']}")
        print(f"Draws: {row['draws']}")
        print(f"Losses: {row['losses']}")
        print(f"Goals scored: {row['gf']}")
        print(f"Goals conceded: {row['ga']}")
        print(f"Goal difference: {row['gd']}")
        print(f"Points: {row['points']}")


def show_tournament_awards(teams, fixtures):
    if not league_complete(fixtures):
        print("\nAwards will be announced when all matches are played.")
        return

    standings = compute_standings(teams, fixtures)

    if not standings:
        print("\nNo tournament statistics available.")
        return

    print("\nTOURNAMENT AWARDS")

    def show_winners(title, value, rows):
        winners = [
            row["team"] for row in rows
            if row[value] == rows[0][value]
        ]

        print(f"{title}: {', '.join(winners)}")

    show_winners(
        "Most wins",
        "wins",
        sorted(standings, key=lambda row: row["wins"], reverse=True)
    )

    show_winners(
        "Best attack",
        "gf",
        sorted(standings, key=lambda row: row["gf"], reverse=True)
    )

    show_winners(
        "Best defence",
        "ga",
        sorted(standings, key=lambda row: row["ga"])
    )

    show_winners(
        "Best goal difference",
        "gd",
        sorted(standings, key=lambda row: row["gd"], reverse=True)
    )

    biggest_difference = -1
    biggest_winners = []

    for match in fixtures:
        difference = abs(
            match["home_score"] - match["away_score"]
        )

        if difference > biggest_difference:
            biggest_difference = difference
            biggest_winners = [match]

        elif difference == biggest_difference:
            biggest_winners.append(match)

    print("\nBiggest winning margin:")

    for match in biggest_winners:
        home = next(
            team["name"] for team in teams
            if team["id"] == match["home_id"]
        )

        away = next(
            team["name"] for team in teams
            if team["id"] == match["away_id"]
        )

        print(
            f"{home} {match['home_score']}-"
            f"{match['away_score']} {away}"
        )


def run():
    tournament_name, teams, fixtures = setup_tournament()

  while True:
    print("\033[2J\033[H", end="")

    print(f"""
================================
{tournament_name.upper()}
================================

1. View teams
2. View fixtures
3. Record match results
4. View league table
5. View team statistics
6. View tournament awards
7. Save tournament
8. Load tournament
0. Exit
""")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                show_teams(teams)

            elif choice == "2":
                show_fixtures(teams, fixtures)

            elif choice == "3":
                show_fixtures(teams, fixtures)

                fixture_id = input(
                    "\nEnter fixture ID: "
                ).strip().upper()

                home_score = int(input("Home team score: "))
                away_score = int(input("Away team score: "))

                record_result(
                    fixtures,
                    fixture_id,
                    home_score,
                    away_score
                )

                print("Result recorded successfully!")

            elif choice == "4":
                show_standings(teams, fixtures)

            elif choice == "5":
                show_team_statistics(teams, fixtures)

            elif choice == "6":
                show_tournament_awards(teams, fixtures)

            elif choice == "7":
                save_season(SAVE_FILE, teams, fixtures)
                print("Tournament saved successfully!")

            elif choice == "8":
                new_teams, new_fixtures = load_season(SAVE_FILE)

                teams = new_teams
                fixtures = new_fixtures

                tournament_name = input(
                    "Enter the name for this loaded tournament: "
                ).strip()

                if not tournament_name:
                    tournament_name = "Loaded Tournament"

                print("Tournament loaded successfully!")

            elif choice == "0":
                print("Thanks for using TournamentLab!")
                break

            else:
                print("Invalid option. Please choose again.")

        except (ValueError, OSError, json.JSONDecodeError) as error:
            print("Error:", error)


if __name__ == "__main__":
    run()
