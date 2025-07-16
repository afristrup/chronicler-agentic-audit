"""
Basic usage example for Chronicler decorator
"""

import os
from typing import Any, Dict

from chronicler_client.decorators import ActionMetadata, AuditConfig, chronicler


# Example 1: Basic function decoration
@chronicler(
    agent_id="example_agent_001",
    tool_id="text_processor",
    metadata=ActionMetadata(
        agent_id="example_agent_001",
        tool_id="text_processor",
        description="Process text input",
        risk_level=1,
    ),
)
def process_text(text: str) -> Dict[str, Any]:
    """Process text and return analysis"""
    # Simulate text processing
    word_count = len(text.split())
    char_count = len(text)

    return {
        "original_text": text,
        "word_count": word_count,
        "char_count": char_count,
        "processed": True,
    }


# Example 2: Function with custom configuration
@chronicler(
    agent_id="data_analyzer_002",
    tool_id="data_analysis",
    config=AuditConfig(enabled=True, log_input=True, log_output=True, batch_size=50),
    metadata=ActionMetadata(
        agent_id="data_analyzer_002",
        tool_id="data_analysis",
        description="Analyze numerical data",
        risk_level=2,
        tags={"category": "analytics", "sensitive": False},
    ),
)
def analyze_data(data: list) -> Dict[str, Any]:
    """Analyze numerical data"""
    if not data:
        return {"error": "No data provided"}

    total = sum(data)
    average = total / len(data)
    maximum = max(data)
    minimum = min(data)

    return {
        "total": total,
        "average": average,
        "maximum": maximum,
        "minimum": minimum,
        "count": len(data),
    }


# Example 3: Function that might fail
@chronicler(
    agent_id="calculator_003",
    tool_id="math_operations",
    metadata=ActionMetadata(
        agent_id="calculator_003",
        tool_id="math_operations",
        description="Perform mathematical operations",
        risk_level=1,
    ),
)
def divide_numbers(a: float, b: float) -> float:
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def run_basic_examples():
    """Run all basic examples"""
    print("=== Chronicler Basic Usage Examples ===\n")

    # Example 1: Text processing
    print("1. Text Processing:")
    try:
        result = process_text("Hello world! This is a test.")
        print(f"   Result: {result}")
        if hasattr(result, "_audit_info"):
            print(f"   Audit Info: {result._audit_info}")
    except Exception as e:
        print(f"   Error: {e}")
    print()

    # Example 2: Data analysis
    print("2. Data Analysis:")
    try:
        result = analyze_data([1, 2, 3, 4, 5])
        print(f"   Result: {result}")
        if hasattr(result, "_audit_info"):
            print(f"   Audit Info: {result._audit_info}")
    except Exception as e:
        print(f"   Error: {e}")
    print()

    # Example 3: Math operations (success)
    print("3. Math Operations (Success):")
    try:
        result = divide_numbers(10, 2)
        print(f"   Result: {result}")
        if hasattr(result, "_audit_info"):
            print(f"   Audit Info: {result._audit_info}")
    except Exception as e:
        print(f"   Error: {e}")
    print()

    # Example 4: Math operations (failure)
    print("4. Math Operations (Failure):")
    try:
        result = divide_numbers(10, 0)
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   Error: {e}")
    print()


if __name__ == "__main__":
    # Set up environment variables for testing
    os.environ["REGISTRY_ADDRESS"] = "0x1234567890123456789012345678901234567890"
    os.environ["AUDIT_LOG_ADDRESS"] = "0x2345678901234567890123456789012345678901"
    os.environ["ACCESS_CONTROL_ADDRESS"] = "0x3456789012345678901234567890123456789012"

    run_basic_examples()
