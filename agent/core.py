"""Agent orchestration and conversation flow."""

import json
from datetime import date
from typing import Any

from agent.llm_client import OpenAICompatibleClient
from agent.prompt import SYSTEM_PROMPT
from agent.tool import EXPENSE_TOOL_SCHEMA, ToolRegistry
from tools.expense_tools import record_expense


class SmartBudgetAgent:
    """Coordinate user input, LLM parsing, tools, and response formatting."""

    def __init__(
        self,
        llm_client: OpenAICompatibleClient | None = None,
        tool_registry: ToolRegistry | None = None,
    ) -> None:
        self.llm = llm_client or OpenAICompatibleClient()
        self.tools = tool_registry or ToolRegistry()
        if not self.tools.names():
            self.tools.register("record_expense", record_expense)

    def handle(self, user_input: str) -> str:
        """Process one user message and execute at most one selected tool."""
        if not user_input:
            return "請輸入記帳內容或查詢指令。"

        system_prompt = (
            f"{SYSTEM_PROMPT}\n今天日期是 {date.today().isoformat()}。"
            "若使用者未提供日期，請使用今天日期。"
        )
        response = self.llm.create_chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            tools=[EXPENSE_TOOL_SCHEMA],
        )
        message = self._get_message(response)
        tool_calls = message.get("tool_calls")
        if not tool_calls:
            content = message.get("content")
            if not isinstance(content, str) or not content.strip():
                raise ValueError("LLM response contains neither a tool call nor text.")
            return content.strip()

        if not isinstance(tool_calls, list) or len(tool_calls) != 1:
            raise ValueError("This version supports exactly one Tool Call per request.")
        tool_call = tool_calls[0]
        name, arguments = self._get_tool_call(tool_call)
        try:
            result = self.tools.call(name, **arguments)
        except (TypeError, ValueError) as exc:
            return f"無法記錄消費：{exc}"
        return self._format_result(result)

    @staticmethod
    def _get_message(response: dict[str, Any]) -> dict[str, Any]:
        choices = response.get("choices")
        if not isinstance(choices, list) or not choices:
            raise ValueError("LLM response does not contain choices.")
        first_choice = choices[0]
        if not isinstance(first_choice, dict):
            raise ValueError("LLM response contains an invalid choice.")
        message = first_choice.get("message")
        if not isinstance(message, dict):
            raise ValueError("LLM response does not contain a valid message.")
        return message

    @staticmethod
    def _get_tool_call(tool_call: Any) -> tuple[str, dict[str, Any]]:
        if not isinstance(tool_call, dict):
            raise ValueError("LLM returned an invalid Tool Call.")
        function = tool_call.get("function")
        if not isinstance(function, dict):
            raise ValueError("Tool Call does not contain a function.")
        name = function.get("name")
        raw_arguments = function.get("arguments")
        if not isinstance(name, str) or not isinstance(raw_arguments, str):
            raise ValueError("Tool Call contains invalid name or arguments.")
        try:
            arguments = json.loads(raw_arguments)
        except json.JSONDecodeError as exc:
            raise ValueError("Tool Call arguments are not valid JSON.") from exc
        if not isinstance(arguments, dict):
            raise ValueError("Tool Call arguments must be a JSON object.")
        return name, arguments

    @staticmethod
    def _format_result(result: Any) -> str:
        if not isinstance(result, dict):
            raise ValueError("Tool returned an invalid result.")
        return (
            f"已記錄：{result['item']}，{result['amount']} 元。"
            f"（編號：{result['id']}）"
        )