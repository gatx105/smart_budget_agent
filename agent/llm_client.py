"""Minimal OpenAI-compatible chat-completions client using the standard library."""

import json
import os
from collections.abc import Mapping
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

load_dotenv()


class LLMClientError(RuntimeError):
    """Raised when the model cannot be called or returns an invalid response."""


class OpenAICompatibleClient:
    """Call a provider exposing the OpenAI chat-completions HTTP contract."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = (
            base_url or os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1"
        ).rstrip("/")
        self.model = model or os.getenv("OPENAI_MODEL") or "gpt-6-luna"
        self.timeout = timeout

    def create_chat_completion(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, object]],
    ) -> Mapping[str, object]:
        """Send one tool-capable chat completion request."""
        if not self.api_key:
            raise LLMClientError(
                "OPENAI_API_KEY is not configured. Set it before starting the agent."
            )
        if not self.model:
            raise LLMClientError(
                "OPENAI_MODEL is not configured. Set it before starting the agent."
            )

        payload = self.build_payload(messages, tools)
        request = Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.timeout) as response:
                body = response.read().decode("utf-8")
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise LLMClientError(
                f"LLM request failed with HTTP {exc.code}: {detail}"
            ) from exc
        except URLError as exc:
            raise LLMClientError(f"LLM request failed: {exc.reason}") from exc

        try:
            result = json.loads(body)
        except json.JSONDecodeError as exc:
            raise LLMClientError("LLM returned invalid JSON.") from exc
        if not isinstance(result, dict):
            raise LLMClientError("LLM response must be a JSON object.")
        return result

    def build_payload(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, object]],
    ) -> dict[str, object]:
        """Build the Chat Completions payload used by the OpenAI API."""
        payload: dict[str, object] = {
            "model": self.model,
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto",
        }
        if self.model == "gpt-6-luna":
            payload["reasoning_effort"] = "none"
        return payload
