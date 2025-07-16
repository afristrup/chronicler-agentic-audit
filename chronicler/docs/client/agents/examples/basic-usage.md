# Basic Usage Examples

Simple examples to get you started with Chronicler Agents.

## Simple Agent Creation

```python
import asyncio
from chronicler_client.agents import (
    AgentManager,
    AgentManagerConfig,
    AgentCapability,
    create_and_register_chronicler_agent
)

async def main():
    # Create manager
    manager = AgentManager(AgentManagerConfig())

    try:
        # Create agent
        agent = await create_and_register_chronicler_agent(
            manager=manager,
            agent_id="simple_agent",
            name="Simple Agent",
            description="A basic test agent",
            capabilities=[AgentCapability.AUDIT_LOGGING]
        )

        # Execute request
        response = await manager.execute_request(
            "simple_agent",
            {"action_type": "audit", "data": {"message": "Hello"}}
        )

        print(f"Response: {response.output_data}")

    finally:
        await manager.shutdown()

asyncio.run(main())
```

## Multiple Agents

```python
import asyncio
from chronicler_client.agents import (
    AgentManager,
    AgentCapability,
    create_and_register_chronicler_agent
)

async def main():
    manager = AgentManager()

    try:
        # Create multiple agents
        agents = []

        # Text generation agent
        text_agent = await create_and_register_chronicler_agent(
            manager=manager,
            agent_id="text_agent",
            name="Text Generator",
            description="Generates text content",
            capabilities=[AgentCapability.TEXT_GENERATION]
        )
        agents.append(text_agent)

        # Code generation agent
        code_agent = await create_and_register_chronicler_agent(
            manager=manager,
            agent_id="code_agent",
            name="Code Generator",
            description="Generates code",
            capabilities=[AgentCapability.CODE_GENERATION]
        )
        agents.append(code_agent)

        # Execute requests on different agents
        text_response = await manager.execute_request(
            "text_agent",
            {"prompt": "Write a short story"}
        )

        code_response = await manager.execute_request(
            "code_agent",
            {"prompt": "Create a Python function"}
        )

        print(f"Text: {text_response.output_data}")
        print(f"Code: {code_response.output_data}")

    finally:
        await manager.shutdown()

asyncio.run(main())
```

## Agent Discovery

```python
import asyncio
from chronicler_client.agents import (
    AgentManager,
    AgentCapability,
    create_and_register_chronicler_agent
)

async def main():
    manager = AgentManager()

    try:
        # Create agents
        await create_and_register_chronicler_agent(
            manager=manager,
            agent_id="audit_agent",
            name="Audit Agent",
            capabilities=[AgentCapability.AUDIT_LOGGING]
        )

        await create_and_register_chronicler_agent(
            manager=manager,
            agent_id="text_agent",
            name="Text Agent",
            capabilities=[AgentCapability.TEXT_GENERATION]
        )

        # Find agents by capability
        audit_agent = await manager.find_agent_by_capability(
            AgentCapability.AUDIT_LOGGING
        )
        print(f"Audit agent: {audit_agent}")

        text_agent = await manager.find_agent_by_capability(
            AgentCapability.TEXT_GENERATION
        )
        print(f"Text agent: {text_agent}")

        # Get all agent metadata
        metadata = await manager.get_all_agent_metadata()
        for agent_id, meta in metadata.items():
            print(f"{agent_id}: {meta.name} - {meta.agent_type}")

    finally:
        await manager.shutdown()

asyncio.run(main())
```

## Error Handling

```python
import asyncio
from chronicler_client.agents import (
    AgentManager,
    AgentCapability,
    create_and_register_chronicler_agent
)

async def main():
    manager = AgentManager()

    try:
        # Create agent
        await create_and_register_chronicler_agent(
            manager=manager,
            agent_id="test_agent",
            name="Test Agent",
            capabilities=[AgentCapability.AUDIT_LOGGING]
        )

        # Execute with error handling
        try:
            response = await manager.execute_request(
                "test_agent",
                {"invalid": "data"}
            )

            if response:
                print(f"Success: {response.output_data}")
            else:
                print("Request failed")

        except Exception as e:
            print(f"Error: {e}")

        # Check agent status
        status = await manager.get_agent_status("test_agent")
        print(f"Agent status: {status}")

    finally:
        await manager.shutdown()

asyncio.run(main())
```

## Health Monitoring

```python
import asyncio
from chronicler_client.agents import (
    AgentManager,
    AgentCapability,
    create_and_register_chronicler_agent
)

async def monitor_health(manager: AgentManager):
    """Monitor agent health"""
    while True:
        try:
            # Get manager stats
            stats = await manager.get_manager_stats()
            print(f"Manager stats: {stats}")

            # Get all agent statuses
            statuses = await manager.get_all_agent_statuses()
            for agent_id, status in statuses.items():
                print(f"{agent_id}: {status['status']}")

            await asyncio.sleep(30)  # Check every 30 seconds

        except Exception as e:
            print(f"Health check error: {e}")
            await asyncio.sleep(60)

async def main():
    manager = AgentManager()

    try:
        # Create agent
        await create_and_register_chronicler_agent(
            manager=manager,
            agent_id="monitored_agent",
            name="Monitored Agent",
            capabilities=[AgentCapability.AUDIT_LOGGING]
        )

        # Start health monitoring
        monitor_task = asyncio.create_task(monitor_health(manager))

        # Execute some requests
        for i in range(5):
            response = await manager.execute_request(
                "monitored_agent",
                {"action_type": "audit", "data": {"count": i}}
            )
            print(f"Request {i}: {response.output_data}")
            await asyncio.sleep(10)

        # Stop monitoring
        monitor_task.cancel()

    finally:
        await manager.shutdown()

asyncio.run(main())
```

## Configuration Examples

```python
import asyncio
from chronicler_client.agents import (
    AgentManager,
    AgentManagerConfig,
    AgentConfig,
    AgentType,
    AgentCapability,
    create_and_register_chronicler_agent
)

async def main():
    # Custom manager configuration
    manager_config = AgentManagerConfig(
        max_concurrent_agents=5,
        agent_timeout=300,
        enable_health_checks=True,
        log_level="INFO"
    )

    manager = AgentManager(manager_config)

    try:
        # Custom agent configuration
        agent_config = AgentConfig(
            agent_id="configured_agent",
            name="Configured Agent",
            description="Agent with custom configuration",
            agent_type=AgentType.SPECIALIZED,
            capabilities=[
                AgentCapability.AUDIT_LOGGING,
                AgentCapability.TEXT_GENERATION
            ],
            audit_enabled=True,
            log_input=True,
            log_output=True,
            timeout=600,
            retry_attempts=3
        )

        # Create agent with custom config
        agent = await create_and_register_chronicler_agent(
            manager=manager,
            **agent_config.model_dump()
        )

        # Execute request
        response = await manager.execute_request(
            "configured_agent",
            {"action_type": "audit", "data": {"test": "configuration"}}
        )

        print(f"Response: {response.output_data}")

    finally:
        await manager.shutdown()

asyncio.run(main())
```

## Related Topics

- [Advanced Examples](./advanced-patterns.md)
- [MCP Examples](./mcp-examples.md)
- [Blockchain Examples](./blockchain-examples.md)
- [API Reference](../api/)