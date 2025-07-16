"""
Configuration examples for Chronicler

This example demonstrates various configuration patterns for the
Chronicler client, including environment variables and programmatic configuration.
"""

import asyncio
import os

from chronicler_client.config import ChroniclerConfig, get_config, set_config
from chronicler_client.decorators import ActionMetadata, AuditConfig, chronicler
from chronicler_client.services import ChroniclerService, ServiceConfig


def environment_configuration_example():
    """Example of configuration using environment variables"""
    print("=== Environment Configuration Example ===")

    # Set environment variables (in real usage, these would be in .env file)
    os.environ["CHAIN_ID"] = "1337"
    os.environ["RPC_URL"] = "http://localhost:8545"
    os.environ["REGISTRY_ADDRESS"] = "0x1234567890123456789012345678901234567890"
    os.environ["AUDIT_LOG_ADDRESS"] = "0x2345678901234567890123456789012345678901"
    os.environ["ACCESS_CONTROL_ADDRESS"] = "0x3456789012345678901234567890123456789012"
    os.environ["AUDIT_ENABLED"] = "true"
    os.environ["LOG_INPUT"] = "true"
    os.environ["LOG_OUTPUT"] = "true"
    os.environ["BATCH_SIZE"] = "100"
    os.environ["TIMEOUT"] = "30000"

    # Get configuration from environment
    config = get_config()
    print(f"Chain ID: {config.chain_id}")
    print(f"RPC URL: {config.rpc_url}")
    print(f"Registry Address: {config.registry_address}")
    print(f"Audit Enabled: {config.audit_enabled}")
    print(f"Batch Size: {config.batch_size}")


def programmatic_configuration_example():
    """Example of programmatic configuration"""
    print("\n=== Programmatic Configuration Example ===")

    # Create configuration programmatically
    config = ChroniclerConfig(
        chain_id=11155111,  # Sepolia testnet
        rpc_url="https://sepolia.infura.io/v3/YOUR_KEY",
        registry_address="0x1234567890123456789012345678901234567890",
        audit_log_address="0x2345678901234567890123456789012345678901",
        access_control_address="0x3456789012345678901234567890123456789012",
        audit_enabled=True,
        log_input=True,
        log_output=True,
        batch_size=200,
        timeout=60000,
        ipfs_gateway="https://ipfs.io",
        dashboard_port=3000,
    )

    # Set the global configuration
    set_config(config)

    # Verify configuration
    current_config = get_config()
    print(f"Chain ID: {current_config.chain_id}")
    print(f"RPC URL: {current_config.rpc_url}")
    print(f"Batch Size: {current_config.batch_size}")
    print(f"Timeout: {current_config.timeout}")


def service_configuration_example():
    """Example of service-specific configuration"""
    print("\n=== Service Configuration Example ===")

    # Create service configuration
    service_config = ServiceConfig(
        timeout=45000,
        retry_attempts=5,
        batch_size=150,
        ipfs_gateway="https://gateway.pinata.cloud",
        max_concurrent_requests=20,
        connection_pool_size=30,
    )

    print(f"Service Timeout: {service_config.timeout}")
    print(f"Retry Attempts: {service_config.retry_attempts}")
    print(f"Batch Size: {service_config.batch_size}")
    print(f"IPFS Gateway: {service_config.ipfs_gateway}")
    print(f"Max Concurrent Requests: {service_config.max_concurrent_requests}")


def decorator_configuration_example():
    """Example of decorator-specific configuration"""
    print("\n=== Decorator Configuration Example ===")

    # Create audit configuration
    audit_config = AuditConfig(
        enabled=True,
        log_input=True,
        log_output=True,
        log_metadata=True,
        batch_size=50,
        ipfs_gateway="https://ipfs.io",
        timeout=25000,
        retry_attempts=2,
    )

    # Create action metadata
    metadata = ActionMetadata(
        agent_id="config_demo_agent",
        tool_id="config_demo_tool",
        category_id="demo",
        risk_level=2,
        description="Configuration demonstration tool",
        tags={"type": "demo", "framework": "chronicler"},
        custom_data={"version": "1.0.0", "environment": "development"},
    )

    # Use configuration in decorator
    @chronicler(
        agent_id="config_demo_agent",
        tool_id="config_demo_tool",
        config=audit_config,
        metadata=metadata,
    )
    def configured_function(input_text: str) -> str:
        return f"Configured processing: {input_text.upper()}"

    # Test the configured function
    result = configured_function("hello world")
    print(f"Function result: {result}")


def environment_specific_configs():
    """Example of environment-specific configurations"""
    print("\n=== Environment-Specific Configurations ===")

    # Development configuration
    dev_config = ChroniclerConfig(
        chain_id=1337,
        rpc_url="http://localhost:8545",
        registry_address="0x1234567890123456789012345678901234567890",
        audit_log_address="0x2345678901234567890123456789012345678901",
        access_control_address="0x3456789012345678901234567890123456789012",
        audit_enabled=True,
        debug=True,
        log_input=True,
        log_output=True,
        batch_size=10,  # Smaller batch for development
        timeout=10000,  # Shorter timeout for development
    )

    # Testnet configuration
    testnet_config = ChroniclerConfig(
        chain_id=11155111,
        rpc_url="https://sepolia.infura.io/v3/YOUR_KEY",
        registry_address="0x1234567890123456789012345678901234567890",
        audit_log_address="0x2345678901234567890123456789012345678901",
        access_control_address="0x3456789012345678901234567890123456789012",
        audit_enabled=True,
        debug=False,
        log_input=True,
        log_output=True,
        batch_size=100,
        timeout=30000,
    )

    # Production configuration
    prod_config = ChroniclerConfig(
        chain_id=1,
        rpc_url="https://mainnet.infura.io/v3/YOUR_KEY",
        registry_address="0x1234567890123456789012345678901234567890",
        audit_log_address="0x2345678901234567890123456789012345678901",
        access_control_address="0x3456789012345678901234567890123456789012",
        audit_enabled=True,
        debug=False,
        log_input=True,
        log_output=True,
        batch_size=500,  # Larger batch for production
        timeout=60000,  # Longer timeout for production
    )

    print("Development Config:")
    print(f"  Chain ID: {dev_config.chain_id}")
    print(f"  Debug: {dev_config.debug}")
    print(f"  Batch Size: {dev_config.batch_size}")

    print("\nTestnet Config:")
    print(f"  Chain ID: {testnet_config.chain_id}")
    print(f"  Debug: {testnet_config.debug}")
    print(f"  Batch Size: {testnet_config.batch_size}")

    print("\nProduction Config:")
    print(f"  Chain ID: {prod_config.chain_id}")
    print(f"  Debug: {prod_config.debug}")
    print(f"  Batch Size: {prod_config.batch_size}")


async def configuration_validation_example():
    """Example of configuration validation"""
    print("\n=== Configuration Validation Example ===")

    try:
        # This should fail validation
        invalid_config = ChroniclerConfig(
            chain_id=1337,
            rpc_url="http://localhost:8545",
            registry_address="",  # Empty address should fail validation
            audit_log_address="0x2345678901234567890123456789012345678901",
            access_control_address="0x3456789012345678901234567890123456789012",
        )
        set_config(invalid_config)
    except ValueError as e:
        print(f"Validation error caught: {e}")

    try:
        # This should pass validation
        valid_config = ChroniclerConfig(
            chain_id=1337,
            rpc_url="http://localhost:8545",
            registry_address="0x1234567890123456789012345678901234567890",
            audit_log_address="0x2345678901234567890123456789012345678901",
            access_control_address="0x3456789012345678901234567890123456789012",
        )
        set_config(valid_config)
        print("Valid configuration set successfully")
    except ValueError as e:
        print(f"Unexpected validation error: {e}")


def main():
    """Run all configuration examples"""
    print("Chronicler Configuration Examples")
    print("=" * 50)

    # Environment configuration
    environment_configuration_example()

    # Programmatic configuration
    programmatic_configuration_example()

    # Service configuration
    service_configuration_example()

    # Decorator configuration
    decorator_configuration_example()

    # Environment-specific configs
    environment_specific_configs()

    # Configuration validation
    asyncio.run(configuration_validation_example())


if __name__ == "__main__":
    main()
