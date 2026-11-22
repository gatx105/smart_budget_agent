"""Tools for recording and querying expenses."""

from database.repository import insert_expense


def record_expense(
    item: str,
    amount: int,
    category: str,
    expense_date: str,
    note: str | None = None,
) -> dict[str, int | str]:
    """Record a validated expense through the database repository."""
    if not isinstance(item, str) or not item.strip():
        raise ValueError("Expense item cannot be empty.")
    if isinstance(amount, bool) or not isinstance(amount, int):
        raise ValueError("Expense amount must be an integer.")
    if amount <= 0:
        raise ValueError("Expense amount must be greater than zero.")
    if not isinstance(category, str) or not category.strip():
        raise ValueError("Expense category cannot be empty.")
    if not isinstance(expense_date, str) or not expense_date.strip():
        raise ValueError("Expense date cannot be empty.")

    expense_id = insert_expense(item, amount, category, expense_date, note)
    return {"id": expense_id, "item": item, "amount": amount}
