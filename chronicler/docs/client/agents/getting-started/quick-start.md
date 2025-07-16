# Quick Start Guide

Get up and running with Chronicler Agents in minutes.

## Prerequisites

- Python 3.10+
- pip or uv package manager
- Basic understanding of async Python

## Installation

```bash
# Install the client
pip install chronicler-client

# Or with uv
uv add chronicler-client
```

## Your First Agent

```python
import asyncio
from chronicler_client.agents import (
    AgentManager,
    AgentManagerConfig,
    AgentCapability,
    create_and_register_chronicler_agent
)

async def main():
    # Create agent manager
    manager = AgentManager(AgentManagerConfig())

    # Create your first agent
    agent = await create_and_register_chronicler_agent(
        manager=manager,
        agent_id="my_first_agent",
        name="My First Agent",
        description="A simple test agent",
        capabilities=[AgentCapability.AUDIT_LOGGING]
    )

    # Execute a simple request
    response = await manager.execute_request(
        "my_first_agent",
        {
            "action_type": "audit",
            "action_data": {"message": "Hello, World!"}
        }
    )

    print(f"Response: {response.output_data}")

    await manager.shutdown()

asyncio.run(main())
```

## Running the MCP Server

```python
from chronicler_client.agents.mcp_server import create_mcp_server
import uvicorn

# Create and run server
server = create_mcp_server()
uvicorn.run(server.app, host="localhost", port=8000)
```

## Next Steps

- [Create Custom Agents](../guides/custom-agents.md)
- [MCP Integration](../guides/mcp-integration.md)
- [API Reference](../api/)