
import unittest
import tempfile
from pathlib import Path

from storage import save_season, load_season


class StorageTests(unittest.TestCase):

    def setUp(self):
        self.teams = [
            {"id": "TM001", "name": "Aces"},
            {"id": "TM002", "name": "Blaze"},
            {"id": "TM003", "name": "Comets"},
            {"id": "TM004", "name": "Dragons"}
        ]

        self.fixtures = [
            {
                "id": "M001",
                "home_id": "TM001",
                "away_id": "TM002",
                "status": "played",
                "home_score": 2,
                "away_score": 1
            },
            {
                "id": "M002",
                "home_id": "TM001",
                "away_id": "TM003",
                "status": "pending",
                "home_score": None,
                "away_score": None
            }
        ]

    def test_save_and_load_season(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "season.json"

            save_season(path, self.teams, self.fixtures)

            loaded_teams, loaded_fixtures = load_season(path)

            self.assertEqual(loaded_teams, self.teams)
            self.assertEqual(loaded_fixtures, self.fixtures)

    def test_saved_file_exists(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "season.json"

            save_season(path, self.teams, self.fixtures)

            self.assertTrue(path.exists())

    def test_reject_invalid_schema_version(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "season.json"

            path.write_text(
                '{"schema_version": 99, "teams": [], "fixtures": []}'
            )

            with self.assertRaises(ValueError):
                load_season(path)

    def test_reject_duplicate_team_names(self):
        teams = [
            {"id": "TM001", "name": "Aces"},
            {"id": "TM002", "name": "aces"}
        ]

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "season.json"

            save_season(path, teams, [])

            with self.assertRaises(ValueError):
                load_season(path)

    def test_reject_negative_saved_scores(self):
        fixtures = [
            {
                "id": "M001",
                "home_id": "TM001",
                "away_id": "TM002",
                "status": "played",
                "home_score": -1,
                "away_score": 2
            }
        ]

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "season.json"

            save_season(path, self.teams, fixtures)

            with self.assertRaises(ValueError):
                load_season(path)


if __name__ == "__main__":
    unittest.main()
