# Configuration

Configuration examples and patterns.

## Basic Configuration

```python
from chronicler_client.decorators import chronicler, AuditConfig

# Simple configuration
config = AuditConfig(
    enabled=True,
    log_input=True,
    log_output=True,
    batch_size=100
)

@chronicler(
    agent_id="my_agent",
    tool_id="text_processor",
    config=config
)
def process_text(text: str) -> str:
    return text.upper()
```

## Environment-Based Configuration

```python
import os
from chronicler_client.decorators import chronicler, AuditConfig

# Load configuration from environment
def get_audit_config():
    return AuditConfig(
        enabled=os.getenv("AUDIT_ENABLED", "true").lower() == "true",
        log_input=os.getenv("LOG_INPUT", "true").lower() == "true",
        log_output=os.getenv("LOG_OUTPUT", "true").lower() == "true",
        batch_size=int(os.getenv("BATCH_SIZE", "100")),
        timeout=int(os.getenv("TIMEOUT", "30000")),
        retry_attempts=int(os.getenv("RETRY_ATTEMPTS", "3"))
    )

@chronicler(
    agent_id="env_agent",
    tool_id="environment_processor",
    config=get_audit_config()
)
def process_with_env_config(data: str) -> str:
    return data.upper()
```

## Conditional Configuration

```python
from chronicler_client.decorators import chronicler, AuditConfig
import sys

# Different configs for different environments
def get_config_for_environment():
    if "test" in sys.argv:
        return AuditConfig(
            enabled=False,  # Disable in tests
            log_input=False,
            log_output=False
        )
    elif "development" in sys.argv:
        return AuditConfig(
            enabled=True,
            log_input=True,
            log_output=True,
            batch_size=10  # Smaller batches for dev
        )
    else:
        return AuditConfig(
            enabled=True,
            log_input=True,
            log_output=True,
            batch_size=100
        )

@chronicler(
    agent_id="conditional_agent",
    tool_id="conditional_processor",
    config=get_config_for_environment()
)
def process_with_conditional_config(data: str) -> str:
    return data.upper()
```

## Performance-Optimized Configuration

```python
from chronicler_client.decorators import chronicler, AuditConfig

# High-performance configuration
performance_config = AuditConfig(
    enabled=True,
    log_input=False,  # Skip input logging for performance
    log_output=True,
    batch_size=500,  # Larger batches
    timeout=15000,  # Shorter timeout
    retry_attempts=1  # Fewer retries
)

@chronicler(
    agent_id="performance_agent",
    tool_id="high_performance_processor",
    config=performance_config
)
def high_performance_process(data: str) -> str:
    return data.upper()
```

## Security-Focused Configuration

```python
from chronicler_client.decorators import chronicler, AuditConfig

# Security-focused configuration
security_config = AuditConfig(
    enabled=True,
    log_input=True,
    log_output=True,
    batch_size=1,  # Immediate logging
    timeout=60000,  # Longer timeout for security checks
    retry_attempts=5  # More retries for reliability
)

@chronicler(
    agent_id="security_agent",
    tool_id="secure_processor",
    config=security_config
)
def secure_process(sensitive_data: str) -> str:
    # Process sensitive data with full audit trail
    return sensitive_data.upper()
```

## Custom IPFS Configuration

```python
from chronicler_client.decorators import chronicler, AuditConfig

# Custom IPFS gateway configuration
ipfs_config = AuditConfig(
    enabled=True,
    log_input=True,
    log_output=True,
    batch_size=100,
    ipfs_gateway="https://gateway.pinata.cloud"  # Custom gateway
)

@chronicler(
    agent_id="ipfs_agent",
    tool_id="ipfs_processor",
    config=ipfs_config
)
def process_with_custom_ipfs(data: str) -> str:
    return data.upper()
```

## Configuration Factory

```python
from chronicler_client.decorators import chronicler, AuditConfig
from typing import Dict, Any

class ConfigFactory:
    @staticmethod
    def create_config(config_type: str, **kwargs) -> AuditConfig:
        base_config = {
            "enabled": True,
            "log_input": True,
            "log_output": True,
            "batch_size": 100,
            "timeout": 30000,
            "retry_attempts": 3
        }

        if config_type == "development":
            base_config.update({
                "batch_size": 10,
                "timeout": 60000
            })
        elif config_type == "production":
            base_config.update({
                "batch_size": 500,
                "timeout": 15000
            })
        elif config_type == "testing":
            base_config.update({
                "enabled": False
            })

        # Override with custom parameters
        base_config.update(kwargs)

        return AuditConfig(**base_config)

# Usage
dev_config = ConfigFactory.create_config("development")
prod_config = ConfigFactory.create_config("production", batch_size=1000)

@chronicler(
    agent_id="factory_agent",
    tool_id="factory_processor",
    config=dev_config
)
def process_with_factory_config(data: str) -> str:
    return data.upper()
```

## Dynamic Configuration

```python
from chronicler_client.decorators import chronicler, AuditConfig
import time

# Dynamic configuration that changes based on time
def get_dynamic_config():
    hour = time.localtime().tm_hour

    if 9 <= hour <= 17:  # Business hours
        return AuditConfig(
            enabled=True,
            log_input=True,
            log_output=True,
            batch_size=50
        )
    else:  # Off hours
        return AuditConfig(
            enabled=True,
            log_input=False,
            log_output=True,
            batch_size=200  # Larger batches during off hours
        )

@chronicler(
    agent_id="dynamic_agent",
    tool_id="dynamic_processor",
    config=get_dynamic_config()
)
def process_with_dynamic_config(data: str) -> str:
    return data.upper()
```