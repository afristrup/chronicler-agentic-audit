# Services

Client service interfaces and usage.

## ChroniclerService

Main service for blockchain interaction.

```python
from chronicler_client.services import ChroniclerService

service = ChroniclerService()

# Log an action
result = await service.log_action(
    action_id="action_123",
    agent_id="my_agent",
    tool_id="text_processor",
    input_data={"text": "hello"},
    output_data={"result": "HELLO"},
    status="success"
)
```

## RegistryService

Agent and tool registration service.

```python
from chronicler_client.services import RegistryService

registry = RegistryService()

# Register an agent
await registry.register_agent(
    agent_id="my_agent",
    operator="0x...",
    metadata_uri="ipfs://..."
)

# Check agent validity
is_valid = await registry.is_valid_agent("my_agent")

# Get agent info
agent_info = await registry.get_agent("my_agent")
```

## AuditService

Audit logging and verification service.

```python
from chronicler_client.services import AuditService

audit = AuditService()

# Log action to blockchain
tx_hash = await audit.log_action(
    action_id="action_123",
    agent_id="my_agent",
    tool_id="text_processor",
    data_hash="0x...",
    status="success"
)

# Verify action inclusion
is_included = await audit.verify_action_in_batch(
    batch_id="batch_456",
    action_index=0,
    merkle_proof=["0x...", "0x..."]
)
```

## AccessControlService

Permission and rate limiting service.

```python
from chronicler_client.services import AccessControlService

access = AccessControlService()

# Check if action is allowed
is_allowed, reason = await access.check_action_allowed(
    agent_id="my_agent",
    tool_id="text_processor",
    gas_used=50000
)

# Get agent policy
policy = await access.get_agent_policy("my_agent")
```

## Service Configuration

```python
from chronicler_client.services import ServiceConfig

config = ServiceConfig(
    timeout=30000,
    retry_attempts=3,
    batch_size=100,
    ipfs_gateway="https://ipfs.io"
)

service = ChroniclerService(config=config)
```

## Error Handling

```python
from chronicler_client.services import ChroniclerError

try:
    result = await service.log_action(...)
except ChroniclerError as e:
    print(f"Service error: {e.message}")
    print(f"Error code: {e.code}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Async Support

All services support async/await:

```python
import asyncio

async def main():
    service = ChroniclerService()

    # Concurrent operations
    tasks = [
        service.log_action(...),
        service.log_action(...),
        service.log_action(...)
    ]

    results = await asyncio.gather(*tasks)

asyncio.run(main())
```