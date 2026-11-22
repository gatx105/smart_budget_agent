"""Tool registration and dispatch."""

from collections.abc import Callable
from typing import Any


EXPENSE_TOOL_SCHEMA: dict[str, object] = {
    "type": "function",
    "function": {
        "name": "record_expense",
        "description": "記錄一筆使用者的日常消費。",
        "parameters": {
            "type": "object",
            "properties": {
                "item": {"type": "string", "description": "消費品項"},
                "amount": {"type": "integer", "minimum": 1, "description": "大於零的消費金額"},
                "category": {"type": "string", "description": "消費分類"},
                "expense_date": {
                    "type": "string",
                    "description": "消費日期，格式為 YYYY-MM-DD",
                },
                "note": {"type": "string", "description": "選填備註"},
            },
            "required": ["item", "amount", "category", "expense_date"],
            "additionalProperties": False,
        },
    },
}


class ToolRegistry:
    """Store executable tools that can be selected by the agent."""

    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Any]] = {}

    def register(self, name: str, function: Callable[..., Any]) -> None:
        """Register a callable under a stable tool name."""
        if not name:
            raise ValueError("Tool name cannot be empty.")
        self._tools[name] = function

    def call(self, name: str, **arguments: Any) -> Any:
        """Execute a registered tool and surface unknown-tool errors."""
        try:
            function = self._tools[name]
        except KeyError as exc:
            raise ValueError(f"Unknown tool: {name}") from exc
        return function(**arguments)

    def names(self) -> tuple[str, ...]:
        """Return registered tool names."""
        return tuple(self._tools)