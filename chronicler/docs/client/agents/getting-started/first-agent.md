# Creating Your First Agent

Step-by-step guide to creating your first Chronicler agent.

## Overview

This guide will walk you through creating a simple agent that can perform basic operations.

## Step 1: Basic Setup

```python
import asyncio
from chronicler_client.agents import (
    AgentManager,
    AgentManagerConfig,
    AgentCapability,
    AgentType
)
```

## Step 2: Create Agent Manager

```python
# Configure the manager
config = AgentManagerConfig(
    enable_auto_registration=True,
    enable_health_checks=True,
    log_level="INFO"
)

# Create manager instance
manager = AgentManager(config)
```

## Step 3: Create Your Agent

```python
# Define agent configuration
agent_config = {
    "agent_id": "my_first_agent",
    "name": "My First Agent",
    "description": "A simple test agent for learning",
    "capabilities": [
        AgentCapability.TEXT_GENERATION,
        AgentCapability.AUDIT_LOGGING
    ]
}

# Create and register the agent
agent = await create_and_register_chronicler_agent(
    manager=manager,
    **agent_config
)

print(f"✅ Created agent: {agent.agent_id}")
```

## Step 4: Execute Your First Request

```python
# Simple text generation request
request_data = {
    "action_type": "audit",
    "action_data": {
        "agent_id": "user_123",
        "tool_id": "text_generator",
        "data": {"message": "Hello, Chronicler!"}
    }
}

# Execute the request
response = await manager.execute_request(
    "my_first_agent",
    request_data
)

# Check the response
if response:
    print(f"✅ Request completed!")
    print(f"   Status: {response.status}")
    print(f"   Execution time: {response.execution_time:.3f}s")
    print(f"   Output: {response.output_data}")
else:
    print("❌ Request failed")
```

## Step 5: Check Agent Status

```python
# Get agent health status
status = await manager.get_agent_status("my_first_agent")
print(f"Agent status: {status}")

# Get manager statistics
stats = await manager.get_manager_stats()
print(f"Manager stats: {stats}")
```

## Step 6: Cleanup

```python
# Always shutdown the manager
await manager.shutdown()
print("✅ Cleanup completed")
```

## Complete Example

```python
import asyncio
from chronicler_client.agents import (
    AgentManager,
    AgentManagerConfig,
    AgentCapability,
    create_and_register_chronicler_agent
)

async def main():
    # Setup
    manager = AgentManager(AgentManagerConfig())

    try:
        # Create agent
        agent = await create_and_register_chronicler_agent(
            manager=manager,
            agent_id="demo_agent",
            name="Demo Agent",
            description="Demonstration agent",
            capabilities=[AgentCapability.AUDIT_LOGGING]
        )

        # Execute request
        response = await manager.execute_request(
            "demo_agent",
            {
                "action_type": "audit",
                "action_data": {"test": "Hello, World!"}
            }
        )

        print(f"Response: {response.output_data}")

    finally:
        await manager.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
```

## Next Steps

- [Custom Agent Creation](../guides/custom-agents.md)
- [MCP Integration](../guides/mcp-integration.md)
- [Advanced Patterns](../examples/advanced-patterns.md)