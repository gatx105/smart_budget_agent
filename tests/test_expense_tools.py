"""Focused validation tests for the expense Tool."""

import unittest
from unittest.mock import patch

from tools.expense_tools import record_expense


class ExpenseToolTests(unittest.TestCase):
    def test_valid_expense_calls_repository(self) -> None:
        with patch(
            "tools.expense_tools.insert_expense",
            return_value=12,
        ) as insert_expense:
            result = record_expense(
                item="午餐",
                amount=120,
                category="餐飲",
                expense_date="2026-11-22",
            )

        insert_expense.assert_called_once_with(
            "午餐",
            120,
            "餐飲",
            "2026-11-22",
            None,
        )
        self.assertEqual(result["id"], 12)

    def test_zero_amount_is_rejected(self) -> None:
        with patch("tools.expense_tools.insert_expense") as insert_expense:
            with self.assertRaisesRegex(ValueError, "greater than zero"):
                record_expense(
                    item="測試",
                    amount=0,
                    category="測試",
                    expense_date="2026-11-22",
                )

        insert_expense.assert_not_called()
