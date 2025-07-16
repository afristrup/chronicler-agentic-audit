# Agent Types

Overview of different agent types in the Chronicler system.

## AgentType Enum

```python
from chronicler_client.agents import AgentType

class AgentType(str, Enum):
    GENERAL = "general"
    SPECIALIZED = "specialized"
    MCP = "mcp"
    AUDIT = "audit"
    REGISTRY = "registry"
    ACCESS_CONTROL = "access_control"
```

## Type Descriptions

### GENERAL
General-purpose agents that can handle multiple types of tasks.

**Use Cases:**
- Multi-purpose AI assistants
- Generic text processing
- Basic automation tasks

**Example:**
```python
config = AgentConfig(
    agent_id="general_agent",
    agent_type=AgentType.GENERAL,
    capabilities=[
        AgentCapability.TEXT_GENERATION,
        AgentCapability.CODE_GENERATION
    ]
)
```

### SPECIALIZED
Agents designed for specific domains or tasks.

**Use Cases:**
- Domain-specific AI (finance, healthcare, etc.)
- Specialized data processing
- Custom business logic

**Example:**
```python
config = AgentConfig(
    agent_id="finance_agent",
    agent_type=AgentType.SPECIALIZED,
    capabilities=[
        AgentCapability.DATA_ANALYSIS,
        AgentCapability.TEXT_GENERATION
    ]
)
```

### MCP
Agents that integrate with Model Context Protocol.

**Use Cases:**
- Tool-based AI interactions
- Cross-platform AI services
- Extensible AI capabilities

**Example:**
```python
config = AgentConfig(
    agent_id="mcp_agent",
    agent_type=AgentType.MCP,
    capabilities=[
        AgentCapability.MCP_PROTOCOL,
        AgentCapability.TEXT_GENERATION
    ],
    mcp_enabled=True,
    mcp_server_url="http://localhost:8000"
)
```

### AUDIT
Specialized agents for blockchain audit operations.

**Use Cases:**
- Blockchain transaction logging
- Audit trail management
- Compliance reporting

**Example:**
```python
config = AgentConfig(
    agent_id="audit_agent",
    agent_type=AgentType.AUDIT,
    capabilities=[
        AgentCapability.AUDIT_LOGGING,
        AgentCapability.BLOCKCHAIN_INTERACTION
    ]
)
```

### REGISTRY
Agents for managing agent and tool registries.

**Use Cases:**
- Agent registration and discovery
- Tool management
- Metadata management

**Example:**
```python
config = AgentConfig(
    agent_id="registry_agent",
    agent_type=AgentType.REGISTRY,
    capabilities=[
        AgentCapability.REGISTRY_MANAGEMENT
    ]
)
```

### ACCESS_CONTROL
Agents for managing access permissions and policies.

**Use Cases:**
- Permission management
- Policy enforcement
- Security controls

**Example:**
```python
config = AgentConfig(
    agent_id="access_agent",
    agent_type=AgentType.ACCESS_CONTROL,
    capabilities=[
        AgentCapability.ACCESS_CONTROL
    ]
)
```

## Choosing Agent Types

### For General AI Tasks
```python
AgentType.GENERAL
```

### For Specific Domains
```python
AgentType.SPECIALIZED
```

### For Tool Integration
```python
AgentType.MCP
```

### For Blockchain Operations
```python
AgentType.AUDIT
```

### For System Management
```python
AgentType.REGISTRY
AgentType.ACCESS_CONTROL
```

## Type-Specific Behavior

### MCP Agents
- Require MCP server configuration
- Support tool discovery and execution
- Handle structured data exchange

### Audit Agents
- Automatically register with blockchain
- Provide audit trail functionality
- Support transaction logging

### Registry Agents
- Manage agent metadata
- Handle registration workflows
- Provide discovery services

## Best Practices

1. **Choose Appropriate Type**: Match agent type to intended use case
2. **Combine Types**: Use multiple agents for complex systems
3. **Type Consistency**: Maintain consistent typing across similar agents
4. **Documentation**: Document type-specific requirements

## Related Topics

- [Capabilities](./capabilities.md)
- [Configuration](./configuration.md)
- [Custom Agents](../guides/custom-agents.md)