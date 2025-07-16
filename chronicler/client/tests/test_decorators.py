"""
Tests for Chronicler decorators
"""

import os
import unittest
from unittest.mock import MagicMock, patch

from chronicler_client.decorators import (
    ActionMetadata,
    ActionStatus,
    AuditConfig,
    chronicler,
)


class TestChroniclerDecorator(unittest.TestCase):
    """Test the chronicler decorator functionality"""

    def setUp(self):
        """Set up test environment"""
        # Set up environment variables for testing
        os.environ["REGISTRY_ADDRESS"] = "0x1234567890123456789012345678901234567890"
        os.environ["AUDIT_LOG_ADDRESS"] = "0x2345678901234567890123456789012345678901"
        os.environ["ACCESS_CONTROL_ADDRESS"] = (
            "0x3456789012345678901234567890123456789012"
        )

    def test_basic_decorator(self):
        """Test basic decorator functionality"""

        @chronicler(agent_id="test_agent", tool_id="test_tool")
        def test_function(x: int) -> int:
            return x * 2

        result = test_function(5)
        self.assertEqual(result, 10)

    def test_decorator_with_metadata(self):
        """Test decorator with custom metadata"""
        metadata = ActionMetadata(
            agent_id="test_agent",
            tool_id="test_tool",
            description="Test function",
            risk_level=1,
        )

        @chronicler(agent_id="test_agent", tool_id="test_tool", metadata=metadata)
        def test_function(text: str) -> str:
            return text.upper()

        result = test_function("hello")
        self.assertEqual(result, "HELLO")

    def test_decorator_with_config(self):
        """Test decorator with custom configuration"""
        config = AuditConfig(
            enabled=True, log_input=True, log_output=True, batch_size=50
        )

        @chronicler(agent_id="test_agent", tool_id="test_tool", config=config)
        def test_function(a: int, b: int) -> int:
            return a + b

        result = test_function(3, 4)
        self.assertEqual(result, 7)

    def test_decorator_error_handling(self):
        """Test decorator error handling"""

        @chronicler(agent_id="test_agent", tool_id="test_tool")
        def test_function(x: int) -> int:
            if x == 0:
                raise ValueError("Cannot divide by zero")
            return 10 / x

        # Should raise the original exception
        with self.assertRaises(ValueError):
            test_function(0)

    def test_decorator_disabled(self):
        """Test decorator when audit is disabled"""
        config = AuditConfig(enabled=False)

        @chronicler(agent_id="test_agent", tool_id="test_tool", config=config)
        def test_function(x: int) -> int:
            return x * 3

        result = test_function(4)
        self.assertEqual(result, 12)

    @patch("chronicler_client.decorators.chronicler.ChroniclerClient")
    def test_blockchain_interaction(self, mock_client):
        """Test blockchain interaction (mocked)"""
        # Mock the client
        mock_instance = MagicMock()
        mock_instance.log_action.return_value = ActionStatus.SUCCESS
        mock_client.return_value = mock_instance

        @chronicler(agent_id="test_agent", tool_id="test_tool")
        def test_function(data: str) -> str:
            return f"processed: {data}"

        result = test_function("test")
        self.assertEqual(result, "processed: test")

        # Verify client was called
        mock_client.assert_called_once()


if __name__ == "__main__":
    unittest.main()
