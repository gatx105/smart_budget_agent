"""Focused tests for database initialization."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from database.db_setup import get_connection, initialize_database


class DatabaseSetupTests(unittest.TestCase):
    def test_initialize_database_creates_required_tables(self) -> None:
        with TemporaryDirectory() as directory:
            db_path = Path(directory) / "test.db"

            initialize_database(db_path)

            connection = get_connection(db_path)
            try:
                tables = {
                    row["name"]
                    for row in connection.execute(
                        "SELECT name FROM sqlite_master WHERE type = 'table'"
                    )
                }
            finally:
                connection.close()

            self.assertTrue({"expenses", "budgets"}.issubset(tables))
