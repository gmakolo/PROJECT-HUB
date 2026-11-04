import unittest

from teams import register_team
from fixtures import generate_fixtures


class EngineerATests(unittest.TestCase):

    def test_register_team(self):
        teams = []
        team = register_team(teams, "Thunder")
        self.assertEqual(team["name"], "Thunder")

    def test_reject_duplicate_name(self):
        teams = []
        register_team(teams, "Thunder")

        with self.assertRaises(ValueError):
            register_team(teams, " thunder ")

    def test_four_teams_make_six_fixtures(self):
        teams = []

        for name in ["Aces", "Blaze", "Comets", "Dragons"]:
            register_team(teams, name)

        fixtures = generate_fixtures(teams)

        self.assertEqual(len(fixtures), 6)

    def test_no_duplicate_pairings(self):
        teams = []

        for name in ["Aces", "Blaze", "Comets", "Dragons"]:
            register_team(teams, name)

        fixtures = generate_fixtures(teams)

        pairs = [
            frozenset((m["home_id"], m["away_id"]))
            for m in fixtures
        ]

        self.assertEqual(len(pairs), len(set(pairs)))


if __name__ == "__main__":
    unittest.main()