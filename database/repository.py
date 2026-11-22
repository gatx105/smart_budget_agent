"""Database access functions used by application tools."""

from database.db_setup import get_connection, initialize_database


def insert_expense(
    item: str,
    amount: int,
    category: str,
    expense_date: str,
    note: str | None = None,
) -> int:
    """Insert one expense and return its generated identifier."""
    initialize_database()
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            INSERT INTO expenses (item, amount, category, expense_date, note)
            VALUES (?, ?, ?, ?, ?)
            """,
            (item, amount, category, expense_date, note),
        )
        connection.commit()
        return int(cursor.lastrowid)
    finally:
        connection.close()
