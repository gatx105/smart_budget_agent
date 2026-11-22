"""Tools for setting and checking budgets."""


def set_budget(
    category: str,
    amount: int,
    period_start: str,
    period_end: str,
) -> dict[str, str | int]:
    """Define the interface for creating a category budget."""
    raise NotImplementedError("Budget persistence will be implemented next.")


def check_budget(category: str, period_start: str, period_end: str) -> dict:
    """Define the interface for calculating remaining budget."""
    raise NotImplementedError("Budget calculation will be implemented next.")
