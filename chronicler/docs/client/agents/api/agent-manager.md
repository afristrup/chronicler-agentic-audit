# AgentManager API Reference

Complete API reference for the AgentManager class.

## Class Overview

```python
class AgentManager:
    """Manages and coordinates all Chronicler agents"""
```

## Constructor

```python
def __init__(self, config: Optional[AgentManagerConfig] = None):
    """
    Initialize the agent manager.

    Args:
        config: Configuration for the manager (optional)
    """
```

### Parameters

- `config` (Optional[AgentManagerConfig]): Manager configuration
  - Default: `AgentManagerConfig()`

### Example

```python
from chronicler_client.agents import AgentManager, AgentManagerConfig

# With default config
manager = AgentManager()

# With custom config
config = AgentManagerConfig(
    max_concurrent_agents=5,
    enable_health_checks=True
)
manager = AgentManager(config)
```

## Methods

### register_agent

```python
async def register_agent(self, agent: BaseAgent) -> bool:
    """
    Register an agent with the manager.

    Args:
        agent: The agent to register

    Returns:
        bool: True if registration successful, False otherwise
    """
```

**Example:**
```python
success = await manager.register_agent(my_agent)
if success:
    print("Agent registered successfully")
```

### unregister_agent

```python
async def unregister_agent(self, agent_id: str) -> bool:
    """
    Unregister an agent from the manager.

    Args:
        agent_id: ID of the agent to unregister

    Returns:
        bool: True if unregistration successful, False otherwise
    """
```

**Example:**
```python
success = await manager.unregister_agent("my_agent")
if success:
    print("Agent unregistered successfully")
```

### execute_request

```python
async def execute_request(
    self,
    agent_id: str,
    input_data: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None
) -> Optional[AgentResponse]:
    """
    Execute a request on a specific agent.

    Args:
        agent_id: ID of the agent to execute on
        input_data: Input data for the request
        metadata: Optional metadata for the request

    Returns:
        Optional[AgentResponse]: Response from the agent, or None if failed
    """
```

**Example:**
```python
response = await manager.execute_request(
    "my_agent",
    {"action_type": "audit", "data": {"test": "value"}},
    {"priority": "high"}
)

if response:
    print(f"Status: {response.status}")
    print(f"Output: {response.output_data}")
```

### find_agent_by_capability

```python
async def find_agent_by_capability(self, capability: AgentCapability) -> Optional[str]:
    """
    Find an agent with the specified capability.

    Args:
        capability: The capability to search for

    Returns:
        Optional[str]: Agent ID if found, None otherwise
    """
```

**Example:**
```python
agent_id = await manager.find_agent_by_capability(
    AgentCapability.TEXT_GENERATION
)

if agent_id:
    print(f"Found agent: {agent_id}")
```

### find_agent_by_type

```python
async def find_agent_by_type(self, agent_type: AgentType) -> Optional[str]:
    """
    Find an agent of the specified type.

    Args:
        agent_type: The agent type to search for

    Returns:
        Optional[str]: Agent ID if found, None otherwise
    """
```

**Example:**
```python
agent_id = await manager.find_agent_by_type(AgentType.MCP)
if agent_id:
    print(f"Found MCP agent: {agent_id}")
```

### execute_with_capability

```python
async def execute_with_capability(
    self,
    capability: AgentCapability,
    input_data: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None
) -> Optional[AgentResponse]:
    """
    Execute a request using an agent with the specified capability.

    Args:
        capability: Required capability
        input_data: Input data for the request
        metadata: Optional metadata for the request

    Returns:
        Optional[AgentResponse]: Response from the agent, or None if failed
    """
```

**Example:**
```python
response = await manager.execute_with_capability(
    AgentCapability.AUDIT_LOGGING,
    {"action_type": "audit", "data": {"event": "user_login"}}
)

if response:
    print(f"Audit logged: {response.output_data}")
```

### get_agent_status

```python
async def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
    """
    Get status of a specific agent.

    Args:
        agent_id: ID of the agent

    Returns:
        Optional[Dict[str, Any]]: Agent status, or None if not found
    """
```

**Example:**
```python
status = await manager.get_agent_status("my_agent")
if status:
    print(f"Status: {status['status']}")
    print(f"Request count: {status['request_count']}")
```

### get_all_agent_statuses

```python
async def get_all_agent_statuses(self) -> Dict[str, Dict[str, Any]]:
    """
    Get status of all agents.

    Returns:
        Dict[str, Dict[str, Any]]: Dictionary of agent statuses
    """
```

**Example:**
```python
statuses = await manager.get_all_agent_statuses()
for agent_id, status in statuses.items():
    print(f"{agent_id}: {status['status']}")
```

### get_agent_metadata

```python
async def get_agent_metadata(self, agent_id: str) -> Optional[AgentMetadata]:
    """
    Get metadata of a specific agent.

    Args:
        agent_id: ID of the agent

    Returns:
        Optional[AgentMetadata]: Agent metadata, or None if not found
    """
```

**Example:**
```python
metadata = await manager.get_agent_metadata("my_agent")
if metadata:
    print(f"Name: {metadata.name}")
    print(f"Capabilities: {[cap.value for cap in metadata.capabilities]}")
```

### get_all_agent_metadata

```python
async def get_all_agent_metadata(self) -> Dict[str, AgentMetadata]:
    """
    Get metadata of all agents.

    Returns:
        Dict[str, AgentMetadata]: Dictionary of agent metadata
    """
```

**Example:**
```python
metadata = await manager.get_all_agent_metadata()
for agent_id, meta in metadata.items():
    print(f"{agent_id}: {meta.name} ({meta.agent_type})")
```

### get_manager_stats

```python
async def get_manager_stats(self) -> AgentManagerStats:
    """
    Get manager statistics.

    Returns:
        AgentManagerStats: Manager statistics
    """
```

**Example:**
```python
stats = await manager.get_manager_stats()
print(f"Total agents: {stats.total_agents}")
print(f"Active agents: {stats.active_agents}")
print(f"Total requests: {stats.total_requests}")
```

### shutdown

```python
async def shutdown(self):
    """
    Shutdown the agent manager and all agents.
    """
```

**Example:**
```python
await manager.shutdown()
print("Manager shutdown complete")
```

## Properties

### agents
```python
agents: Dict[str, BaseAgent]
```
Dictionary of registered agents.

### agent_types
```python
agent_types: Dict[str, AgentType]
```
Dictionary mapping agent IDs to their types.

### agent_capabilities
```python
agent_capabilities: Dict[str, List[AgentCapability]]
```
Dictionary mapping agent IDs to their capabilities.

## Error Handling

The AgentManager handles errors gracefully:

- **Agent not found**: Returns `None` or `False`
- **Registration conflicts**: Returns `False`
- **Execution failures**: Returns `None` for responses
- **Network errors**: Logs and continues

## Thread Safety

The AgentManager is designed for async operations and should be used in an async context.

## Related

- [BaseAgent](./base-agent.md)
- [AgentManagerConfig](./models.md)
- [AgentResponse](./models.md)