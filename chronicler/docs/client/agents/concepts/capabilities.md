# Agent Capabilities

Understanding agent capabilities and how to use them effectively.

## AgentCapability Enum

```python
from chronicler_client.agents import AgentCapability

class AgentCapability(str, Enum):
    TEXT_GENERATION = "text_generation"
    CODE_GENERATION = "code_generation"
    DATA_ANALYSIS = "data_analysis"
    FILE_OPERATIONS = "file_operations"
    WEB_SEARCH = "web_search"
    BLOCKCHAIN_INTERACTION = "blockchain_interaction"
    AUDIT_LOGGING = "audit_logging"
    ACCESS_CONTROL = "access_control"
    REGISTRY_MANAGEMENT = "registry_management"
    MCP_PROTOCOL = "mcp_protocol"
```

## Capability Descriptions

### TEXT_GENERATION
Generate human-readable text content.

**Use Cases:**
- Content creation
- Summarization
- Translation
- Creative writing

**Example:**
```python
capabilities = [AgentCapability.TEXT_GENERATION]

# Request format
request_data = {
    "prompt": "Write a summary of AI trends",
    "max_tokens": 500,
    "temperature": 0.7
}
```

### CODE_GENERATION
Generate executable code in various languages.

**Use Cases:**
- Code completion
- Function generation
- Bug fixes
- Code refactoring

**Example:**
```python
capabilities = [AgentCapability.CODE_GENERATION]

# Request format
request_data = {
    "prompt": "Create a Python function to sort a list",
    "language": "python",
    "include_tests": True
}
```

### DATA_ANALYSIS
Analyze and process data sets.

**Use Cases:**
- Statistical analysis
- Data visualization
- Pattern recognition
- Predictive modeling

**Example:**
```python
capabilities = [AgentCapability.DATA_ANALYSIS]

# Request format
request_data = {
    "data": [...],
    "analysis_type": "statistical",
    "output_format": "chart"
}
```

### FILE_OPERATIONS
Perform file system operations.

**Use Cases:**
- File reading/writing
- Directory management
- File format conversion
- Backup operations

**Example:**
```python
capabilities = [AgentCapability.FILE_OPERATIONS]

# Request format
request_data = {
    "operation": "read",
    "file_path": "/path/to/file.txt",
    "encoding": "utf-8"
}
```

### WEB_SEARCH
Search and retrieve information from the web.

**Use Cases:**
- Information gathering
- Research
- News aggregation
- Fact checking

**Example:**
```python
capabilities = [AgentCapability.WEB_SEARCH]

# Request format
request_data = {
    "query": "latest AI developments",
    "max_results": 10,
    "sources": ["reliable"]
}
```

### BLOCKCHAIN_INTERACTION
Interact with blockchain networks.

**Use Cases:**
- Transaction submission
- Smart contract interaction
- Blockchain queries
- Wallet operations

**Example:**
```python
capabilities = [AgentCapability.BLOCKCHAIN_INTERACTION]

# Request format
request_data = {
    "action": "send_transaction",
    "to_address": "0x...",
    "amount": "1.0",
    "gas_limit": 21000
}
```

### AUDIT_LOGGING
Log actions to blockchain for audit purposes.

**Use Cases:**
- Compliance tracking
- Audit trails
- Action verification
- Transparency

**Example:**
```python
capabilities = [AgentCapability.AUDIT_LOGGING]

# Request format
request_data = {
    "action_type": "audit",
    "action_data": {
        "user_id": "user123",
        "action": "data_access",
        "timestamp": "2024-01-01T00:00:00Z"
    }
}
```

### ACCESS_CONTROL
Manage access permissions and policies.

**Use Cases:**
- Permission checking
- Policy enforcement
- Role management
- Security controls

**Example:**
```python
capabilities = [AgentCapability.ACCESS_CONTROL]

# Request format
request_data = {
    "operation": "check_permission",
    "user_id": "user123",
    "resource": "database",
    "action": "read"
}
```

### REGISTRY_MANAGEMENT
Manage agent and tool registries.

**Use Cases:**
- Agent registration
- Tool discovery
- Metadata management
- Version control

**Example:**
```python
capabilities = [AgentCapability.REGISTRY_MANAGEMENT]

# Request format
request_data = {
    "operation": "register_agent",
    "agent_data": {
        "id": "new_agent",
        "name": "New Agent",
        "capabilities": [...]
    }
}
```

### MCP_PROTOCOL
Support Model Context Protocol interactions.

**Use Cases:**
- Tool integration
- Cross-platform AI
- Extensible capabilities
- Standardized interfaces

**Example:**
```python
capabilities = [AgentCapability.MCP_PROTOCOL]

# Request format
request_data = {
    "prompt": "Use available tools to solve this problem",
    "tools": ["web_search", "calculator"],
    "model": "gpt-4"
}
```

## Capability Combinations

### General AI Assistant
```python
capabilities = [
    AgentCapability.TEXT_GENERATION,
    AgentCapability.CODE_GENERATION,
    AgentCapability.DATA_ANALYSIS
]
```

### Blockchain Specialist
```python
capabilities = [
    AgentCapability.BLOCKCHAIN_INTERACTION,
    AgentCapability.AUDIT_LOGGING,
    AgentCapability.ACCESS_CONTROL
]
```

### MCP Agent
```python
capabilities = [
    AgentCapability.MCP_PROTOCOL,
    AgentCapability.TEXT_GENERATION,
    AgentCapability.FILE_OPERATIONS
]
```

### System Administrator
```python
capabilities = [
    AgentCapability.REGISTRY_MANAGEMENT,
    AgentCapability.ACCESS_CONTROL,
    AgentCapability.FILE_OPERATIONS
]
```

## Finding Agents by Capability

```python
# Find agent with specific capability
agent_id = await manager.find_agent_by_capability(
    AgentCapability.TEXT_GENERATION
)

# Execute request using capability
response = await manager.execute_with_capability(
    AgentCapability.CODE_GENERATION,
    {"prompt": "Create a function"}
)
```

## Best Practices

1. **Minimal Capabilities**: Only include necessary capabilities
2. **Capability Groups**: Group related capabilities together
3. **Documentation**: Document capability requirements
4. **Testing**: Test each capability independently

## Related Topics

- [Agent Types](./agent-types.md)
- [Configuration](./configuration.md)
- [Custom Capabilities](../guides/custom-agents.md)