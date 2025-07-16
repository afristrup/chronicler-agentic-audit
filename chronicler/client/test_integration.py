#!/usr/bin/env python3
"""
Simple test script for Chronicler Python integration
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chronicler_client.decorators import ActionMetadata, chronicler


@chronicler(
    agent_id="test_agent",
    tool_id="test_tool",
    metadata=ActionMetadata(
        agent_id="test_agent",
        tool_id="test_tool",
        description="Test function",
        risk_level=1,
    ),
)
def my_decorated_function(text: str) -> str:
    """Test function that processes text"""
    return text.upper()


def test_chronicler_decorator_integration():
    """Run the test"""
    print("=== Chronicler Python Integration Test ===\n")

    # Test the decorated function
    try:
        result = my_decorated_function("hello world")
        print(f"✅ Function executed successfully: {result}")

        # Check if audit info was attached
        if hasattr(result, "_audit_info"):
            print(f"✅ Audit info attached: {result._audit_info}")
        else:
            print("ℹ️  No audit info attached (audit may be disabled)")

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    print("\n✅ Integration test completed successfully!")
    return 0


if __name__ == "__main__":
    exit(test_chronicler_decorator_integration())
