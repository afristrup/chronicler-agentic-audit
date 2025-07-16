# Chronicler Agents

A comprehensive agent system for Chronicler with FastAPI MCP (Model Context Protocol) integration.

## Overview

The Chronicler Agents module provides a flexible and extensible framework for creating AI agents that can interact with the Chronicler blockchain system. It includes support for:

- **Base Agent Framework**: Abstract base classes for building custom agents
- **MCP Integration**: Full integration with the Model Context Protocol
- **Chronicler Agents**: Specialized agents for blockchain operations
- **Agent Manager**: Centralized agent coordination and management
- **FastAPI Server**: RESTful API server with MCP support

## Features

### 🤖 Agent Types

- **BaseAgent**: Abstract base class for all agents
- **MCPAgent**: Agent that integrates with MCP protocol
- **ChroniclerAgent**: Specialized agent for blockchain operations
- **AgentManager**: Coordinates and manages multiple agents

### 🔧 Capabilities

- **TEXT_GENERATION**: Generate text content
- **CODE_GENERATION**: Generate code
- **DATA_ANALYSIS**: Analyze data
- **FILE_OPERATIONS**: File system operations
- **WEB_SEARCH**: Web search capabilities
- **BLOCKCHAIN_INTERACTION**: Interact with blockchain
- **AUDIT_LOGGING**: Log actions to blockchain
- **ACCESS_CONTROL**: Manage access permissions
- **REGISTRY_MANAGEMENT**: Manage agent/tool registry
- **MCP_PROTOCOL**: MCP protocol support

### 🚀 MCP Integration

- Full FastAPI MCP server implementation
- Tool discovery and execution
- Session management
- Error handling and recovery

## Quick Start

### Basic Usage

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

    # Create and register a Chronicler agent
    agent = await create_and_register_chronicler_agent(
        manager=manager,
        agent_id="my_agent",
        name="My Agent",
        description="My custom agent",
        capabilities=[AgentCapability.AUDIT_LOGGING]
    )

    # Execute a request
    response = await manager.execute_request(
        "my_agent",
        {
            "action_type": "audit",
            "action_data": {"test": "data"}
        }
    )

    print(f"Response: {response.output_data}")

    await manager.shutdown()

asyncio.run(main())
```

### MCP Agent Usage

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

# Execute MCP request
response = await agent.execute({
    "prompt": "Write a Python function",
    "model": "gpt-4"
})
```

### Running the MCP Server

```python
from chronicler_client.agents.mcp_server import create_mcp_server
import uvicorn

# Create server
server = create_mcp_server()

# Run server
uvicorn.run(
    server.app,
    host="localhost",
    port=8000
)
```

## API Reference

### AgentManager

The central coordinator for all agents.

```python
class AgentManager:
    async def register_agent(self, agent: BaseAgent) -> bool
    async def unregister_agent(self, agent_id: str) -> bool
    async def execute_request(self, agent_id: str, input_data: Dict, metadata: Optional[Dict] = None) -> Optional[AgentResponse]
    async def find_agent_by_capability(self, capability: AgentCapability) -> Optional[str]
    async def execute_with_capability(self, capability: AgentCapability, input_data: Dict, metadata: Optional[Dict] = None) -> Optional[AgentResponse]
    async def get_agent_status(self, agent_id: str) -> Optional[Dict]
    async def get_manager_stats(self) -> AgentManagerStats
```

### BaseAgent

Abstract base class for all agents.

```python
class BaseAgent(ABC):
    async def process_request(self, request: AgentRequest) -> AgentResponse
    async def execute(self, input_data: Dict, metadata: Optional[Dict] = None) -> AgentResponse
    def get_metadata(self) -> AgentMetadata
    def get_health_status(self) -> Dict[str, Any]
    async def shutdown(self)
```

### MCPAgent

Agent with MCP protocol support.

```python
class MCPAgent(BaseAgent):
    async def list_available_tools(self) -> List[Dict[str, Any]]
    async def get_tool_schema(self, tool_name: str) -> Optional[Dict[str, Any]]
    async def call_tool_directly(self, tool_name: str, arguments: Dict[str, Any]) -> MCPToolResult
```

### ChroniclerAgent

Specialized agent for blockchain operations.

```python
class ChroniclerAgent(BaseAgent):
    async def get_blockchain_stats(self) -> Dict[str, Any]
    async def get_action_history(self, limit: int = 100) -> List[Dict[str, Any]]
```

## Configuration

### Agent Configuration

```python
from chronicler_client.agents import AgentConfig

config = AgentConfig(
    agent_id="my_agent",
    name="My Agent",
    description="Description",
    agent_type=AgentType.AUDIT,
    capabilities=[AgentCapability.AUDIT_LOGGING],
    model_name="gpt-4",
    max_tokens=4096,
    temperature=0.7,
    audit_enabled=True,
    log_input=True,
    log_output=True,
    risk_level=1
)
```

### Manager Configuration

```python
from chronicler_client.agents import AgentManagerConfig

config = AgentManagerConfig(
    max_concurrent_agents=10,
    agent_timeout=300,
    enable_auto_registration=True,
    enable_health_checks=True,
    health_check_interval=60,
    mcp_enabled=True,
    mcp_server_port=8000,
    log_level="INFO"
)
```

## MCP Server API

The MCP server provides RESTful endpoints:

### Endpoints

- `GET /` - Server information
- `GET /health` - Health check
- `GET /agents` - List all agents
- `GET /agents/{agent_id}` - Get agent information
- `GET /agents/{agent_id}/status` - Get agent status
- `POST /agents/execute` - Execute agent request
- `POST /agents/register` - Register new agent
- `DELETE /agents/{agent_id}` - Unregister agent
- `GET /stats` - Get manager statistics

### Example Requests

```bash
# List agents
curl http://localhost:8000/agents

# Execute agent request
curl -X POST http://localhost:8000/agents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "my_agent",
    "input_data": {
      "action_type": "audit",
      "action_data": {"test": "data"}
    }
  }'

# Get agent status
curl http://localhost:8000/agents/my_agent/status
```

## MCP Tools

The server exposes the following MCP tools:

- `execute_agent` - Execute a request on a specific agent
- `list_agents` - List all registered agents
- `get_agent_status` - Get status of a specific agent
- `register_agent` - Register a new agent
- `execute_with_capability` - Execute using agent with specific capability

## Examples

See the `examples/agent_example.py` file for comprehensive examples including:

- Basic agent usage
- MCP integration
- Agent capabilities
- MCP server setup

## Environment Variables

Configure the system using environment variables:

```bash
# Agent Configuration
DEFAULT_MODEL=gpt-4
MAX_TOKENS=4096
TEMPERATURE=0.7
AUDIT_ENABLED=true
LOG_INPUT=true
LOG_OUTPUT=true

# MCP Configuration
MCP_SERVER_URL=http://localhost:8000
MCP_API_KEY=your_api_key
MCP_SERVER_PORT=8000
MCP_SERVER_HOST=localhost

# Manager Configuration
MAX_CONCURRENT_AGENTS=10
AGENT_TIMEOUT=300
ENABLE_AUTO_REGISTRATION=true
ENABLE_HEALTH_CHECKS=true
HEALTH_CHECK_INTERVAL=60
LOG_LEVEL=INFO
```

## Development

### Running Tests

```bash
cd chronicler/client
pytest tests/test_agents.py -v
```

### Adding Custom Agents

1. Inherit from `BaseAgent`
2. Implement the `process_request` method
3. Register with the `AgentManager`

```python
from chronicler_client.agents import BaseAgent, AgentRequest, AgentResponse

class MyCustomAgent(BaseAgent):
    async def process_request(self, request: AgentRequest) -> AgentResponse:
        # Your custom logic here
        output_data = {"result": "custom processing"}

        return AgentResponse(
            request_id=request.request_id,
            agent_id=self.agent_id,
            output_data=output_data,
            status="success",
            execution_time=0.0
        )
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI MCP   │    │   Agent Manager │    │   Base Agent    │
│     Server      │◄──►│                 │◄──►│                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   MCP Agent     │    │ Chronicler Agent│
                       │                 │    │                 │
                       └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   MCP Client    │    │  Blockchain     │
                       │                 │    │   Services      │
                       └─────────────────┘    └─────────────────┘
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.