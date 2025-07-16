"""
Error handling examples for Chronicler

This example demonstrates various error handling patterns when using
the Chronicler decorators and services.
"""

import asyncio

from chronicler_client.decorators import ActionMetadata, AuditConfig, chronicler
from chronicler_client.services import (
    AuditError,
    ChroniclerError,
    ChroniclerService,
    RegistryError,
)


@chronicler(agent_id="error_demo_agent", tool_id="error_demo_tool")
def function_with_potential_error(input_data: str) -> str:
    """Function that might raise an error"""
    if input_data == "error":
        raise ValueError("This is a test error")
    elif input_data == "type_error":
        raise TypeError("This is a type error")
    return f"Processed: {input_data}"


@chronicler(
    agent_id="safe_agent",
    tool_id="safe_tool",
    config=AuditConfig(enabled=True, log_input=True, log_output=True),
)
def safe_function_with_error_handling(input_data: str) -> str:
    """Function with built-in error handling"""
    try:
        if input_data == "error":
            raise ValueError("This is a test error")
        return f"Processed: {input_data}"
    except Exception as e:
        # The decorator will still log this error
        print(f"Error in safe_function: {e}")
        raise


async def service_error_handling_example():
    """Example of handling service errors"""
    service = ChroniclerService()

    try:
        # Try to log an action
        result = await service.log_action(
            action_id="test_action",
            agent_id="test_agent",
            tool_id="test_tool",
            input_data={"test": "data"},
            output_data={"result": "success"},
        )
        print(f"Action logged successfully: {result}")

    except ChroniclerError as e:
        print(f"Chronicler error: {e.message}")
        print(f"Error code: {e.code}")

    except Exception as e:
        print(f"Unexpected error: {e}")


async def registry_error_handling_example():
    """Example of handling registry errors"""
    from chronicler_client.services import RegistryService

    registry = RegistryService()

    try:
        # Try to register an agent
        result = await registry.register_agent(
            agent_id="test_agent",
            operator="0x1234567890123456789012345678901234567890",
            metadata_uri="ipfs://test_metadata",
        )
        print(f"Agent registered successfully: {result}")

    except RegistryError as e:
        print(f"Registry error: {e.message}")
        print(f"Error code: {e.code}")

    except Exception as e:
        print(f"Unexpected error: {e}")


async def audit_error_handling_example():
    """Example of handling audit errors"""
    from chronicler_client.services import AuditService

    audit = AuditService()

    try:
        # Try to verify an action
        is_verified = await audit.verify_action_in_batch(
            batch_id="test_batch", action_index=0, merkle_proof=["0x123", "0x456"]
        )
        print(f"Action verified: {is_verified}")

    except AuditError as e:
        print(f"Audit error: {e.message}")
        print(f"Error code: {e.code}")

    except Exception as e:
        print(f"Unexpected error: {e}")


def decorator_error_handling_example():
    """Example of error handling with decorators"""
    print("Testing function with potential error...")

    # Test successful execution
    try:
        result = function_with_potential_error("normal_input")
        print(f"Success: {result}")
    except Exception as e:
        print(f"Error: {e}")

    # Test error case
    try:
        result = function_with_potential_error("error")
        print(f"Success: {result}")
    except Exception as e:
        print(f"Expected error: {e}")

    # Test safe function
    try:
        result = safe_function_with_error_handling("error")
        print(f"Success: {result}")
    except Exception as e:
        print(f"Handled error: {e}")


async def comprehensive_error_handling():
    """Comprehensive error handling example"""
    print("=== Comprehensive Error Handling Example ===")

    # Test decorator error handling
    print("\n1. Decorator Error Handling:")
    decorator_error_handling_example()

    # Test service error handling
    print("\n2. Service Error Handling:")
    await service_error_handling_example()

    # Test registry error handling
    print("\n3. Registry Error Handling:")
    await registry_error_handling_example()

    # Test audit error handling
    print("\n4. Audit Error Handling:")
    await audit_error_handling_example()


if __name__ == "__main__":
    # Run the comprehensive example
    asyncio.run(comprehensive_error_handling())
