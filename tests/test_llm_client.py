"""Tests for the OpenAI-compatible LLM client configuration."""

import unittest

from agent.llm_client import OpenAICompatibleClient


class LLMClientTests(unittest.TestCase):
    def test_gpt_6_luna_is_the_default_model(self) -> None:
        client = OpenAICompatibleClient(api_key="test-key")

        self.assertEqual(client.model, "gpt-6-luna")

    def test_gpt_6_luna_payload_disables_reasoning(self) -> None:
        client = OpenAICompatibleClient(api_key="test-key", model="gpt-6-luna")

        payload = client.build_payload([], [])

        self.assertEqual(payload["model"], "gpt-6-luna")
        self.assertEqual(payload["reasoning_effort"], "none")

    def test_other_model_payload_has_no_reasoning_effort(self) -> None:
        client = OpenAICompatibleClient(
            api_key="test-key",
            model="gpt-5.4-nano",
        )

        payload = client.build_payload([], [])

        self.assertNotIn("reasoning_effort", payload)
