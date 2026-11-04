import unittest

from teams import register_team
from fixtures import generate_fixtures
from results import record_result
from standings import compute_standings, champion


class EngineerBTests(unittest.TestCase):

    def setUp(self):
        self.teams = []

        for name in ["Aces", "Blaze", "Comets", "Dragons"]:
            register_team(self.teams, name)

        self.fixtures = generate_fixtures(self.teams)

    def test_winner_gets_three_points(self):
        record_result(self.fixtures, "M001", 2, 0)

        table = {
            row["team"]: row
            for row in compute_standings(
                self.teams, self.fixtures
            )
        }

        self.assertEqual(table["Aces"]["points"], 3)
        self.assertEqual(table["Blaze"]["points"], 0)

    def test_draw_gives_one_point_each(self):
        record_result(self.fixtures, "M001", 1, 1)

        table = {
            row["team"]: row
            for row in compute_standings(
                self.teams, self.fixtures
            )
        }

        self.assertEqual(table["Aces"]["points"], 1)
        self.assertEqual(table["Blaze"]["points"], 1)

    def test_negative_score_is_rejected(self):
        with self.assertRaises(ValueError):
            record_result(self.fixtures, "M001", -1, 0)

    def test_result_cannot_be_entered_twice(self):
        record_result(self.fixtures, "M001", 2, 0)

        with self.assertRaises(ValueError):
            record_result(self.fixtures, "M001", 1, 0)

    def test_champion_only_after_all_fixtures(self):
        self.assertIsNone(champion(self.teams, self.fixtures))

        for match in self.fixtures:
            record_result(
                self.fixtures, match["id"], 1, 0
            )

        self.assertIsNotNone(
            champion(self.teams, self.fixtures)
        )


if __name__ == "__main__":
    unittest.main()