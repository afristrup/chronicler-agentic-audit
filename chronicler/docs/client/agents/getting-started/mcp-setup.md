# MCP Setup Guide

Setting up Model Context Protocol (MCP) integration with Chronicler Agents.

## What is MCP?

Model Context Protocol (MCP) is a standard for AI model interactions that enables:
- Tool discovery and execution
- Structured data exchange
- Cross-platform compatibility
- Extensible capabilities

## Prerequisites

- Chronicler Agents installed
- Python 3.10+
- Network access for MCP server

## Basic MCP Setup

### 1. Install MCP Dependencies

```bash
# Install with MCP extras
pip install chronicler-client[mcp]

# Or install separately
pip install fastapi-mcp
```

### 2. Create MCP Agent

```python
from chronicler_client.agents import create_mcp_agent

# Create MCP agent
agent = create_mcp_agent(
    agent_id="mcp_agent",
    name="MCP Agent",
    description="Agent with MCP capabilities",
    mcp_server_url="http://localhost:8000",
    capabilities=[
        AgentCapability.MCP_PROTOCOL,
        AgentCapability.TEXT_GENERATION
    ]
)
```

### 3. Run MCP Server

```python
from chronicler_client.agents.mcp_server import create_mcp_server
import uvicorn

# Create server
server = create_mcp_server()

# Run server
uvicorn.run(
    server.app,
    host="localhost",
    port=8000,
    log_level="info"
)
```

## Advanced MCP Configuration

### Environment Variables

```bash
# MCP Configuration
MCP_SERVER_URL=http://localhost:8000
MCP_API_KEY=your_api_key_here
MCP_SERVER_PORT=8000
MCP_SERVER_HOST=localhost
```

### Custom MCP Client

```python
from fastapi_mcp import MCPClient
from chronicler_client.agents import MCPAgent, AgentConfig

# Create custom MCP client
mcp_client = MCPClient(
    server_url="http://localhost:8000",
    api_key="your_api_key"
)

# Create agent with custom client
config = AgentConfig(
    agent_id="custom_mcp",
    name="Custom MCP Agent",
    agent_type=AgentType.MCP,
    capabilities=[AgentCapability.MCP_PROTOCOL],
    mcp_enabled=True,
    mcp_server_url="http://localhost:8000"
)

agent = MCPAgent(config, mcp_client=mcp_client)
```

## MCP Tools

### Available Tools

The MCP server provides these tools:

- `execute_agent` - Execute request on specific agent
- `list_agents` - List all registered agents
- `get_agent_status` - Get agent status
- `register_agent` - Register new agent
- `execute_with_capability` - Execute using capability

### Using MCP Tools

```python
# List available tools
tools = await agent.list_available_tools()
print(f"Available tools: {len(tools)}")

# Get tool schema
schema = await agent.get_tool_schema("execute_agent")
print(f"Tool schema: {schema}")

# Execute tool directly
result = await agent.call_tool_directly(
    "list_agents",
    {}
)
print(f"Tool result: {result}")
```

## MCP Request Examples

### Text Generation

```python
# Execute text generation request
response = await agent.execute({
    "prompt": "Write a Python function to calculate fibonacci numbers",
    "model": "gpt-4",
    "tools": []
})

print(f"Generated text: {response.output_data['content']}")
```

### Tool Execution

```python
# Execute request with tools
response = await agent.execute({
    "prompt": "List all available agents",
    "model": "gpt-4",
    "tools": ["list_agents"]
})

print(f"Tool calls: {response.output_data['tool_calls']}")
print(f"Tool results: {response.output_data['tool_results']}")
```

## Troubleshooting

### Common Issues

1. **Connection Refused**: Check MCP server is running
2. **Authentication Error**: Verify API key
3. **Tool Not Found**: Check tool availability

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Create agent with debug
agent = create_mcp_agent(
    agent_id="debug_agent",
    name="Debug Agent",
    mcp_server_url="http://localhost:8000",
    log_level="DEBUG"
)
```

## Next Steps

- [MCP Integration Guide](../guides/mcp-integration.md)
- [Custom MCP Tools](../guides/custom-agents.md)
- [MCP Examples](../examples/mcp-examples.md)