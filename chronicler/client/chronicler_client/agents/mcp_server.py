"""
FastAPI MCP Server for Chronicler Agents
"""

import asyncio
import json
import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi_mcp import MCPRequest, MCPResponse, MCPServer, MCPToolCall
from pydantic import BaseModel

from .agent_manager import AgentManager, AgentManagerConfig
from .agent_types import AgentCapability, AgentType
from .chronicler_agent import create_chronicler_agent
from .mcp_agent import create_mcp_agent


class AgentRequestModel(BaseModel):
    """Request model for agent operations"""

    agent_id: str
    input_data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


class AgentResponseModel(BaseModel):
    """Response model for agent operations"""

    request_id: str
    agent_id: str
    output_data: Dict[str, Any]
    status: str
    execution_time: float
    metadata: Optional[Dict[str, Any]] = None


class AgentRegistrationModel(BaseModel):
    """Model for agent registration"""

    agent_id: str
    name: str
    description: str
    agent_type: AgentType
    capabilities: List[AgentCapability]
    config: Optional[Dict[str, Any]] = None


class MCPChroniclerServer:
    """FastAPI MCP Server for Chronicler Agents"""

    def __init__(self, config: Optional[AgentManagerConfig] = None):
        self.config = config or AgentManagerConfig()

        # Initialize agent manager
        self.agent_manager = AgentManager(config)

        # Setup logging
        self.logger = logging.getLogger("mcp_server")
        self.logger.setLevel(getattr(logging, self.config.log_level.upper()))

        # Create FastAPI app
        self.app = FastAPI(
            title="Chronicler MCP Server",
            description="MCP Server for Chronicler Agents",
            version="1.0.0",
        )

        # Setup routes
        self._setup_routes()

        # MCP tools
        self.mcp_tools = [
            {
                "name": "execute_agent",
                "description": "Execute a request on a specific agent",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agent_id": {
                            "type": "string",
                            "description": "ID of the agent to execute",
                        },
                        "input_data": {
                            "type": "object",
                            "description": "Input data for the agent",
                        },
                        "metadata": {
                            "type": "object",
                            "description": "Optional metadata",
                        },
                    },
                    "required": ["agent_id", "input_data"],
                },
            },
            {
                "name": "list_agents",
                "description": "List all registered agents",
                "parameters": {"type": "object", "properties": {}, "required": []},
            },
            {
                "name": "get_agent_status",
                "description": "Get status of a specific agent",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agent_id": {"type": "string", "description": "ID of the agent"}
                    },
                    "required": ["agent_id"],
                },
            },
            {
                "name": "register_agent",
                "description": "Register a new agent",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agent_id": {
                            "type": "string",
                            "description": "Unique agent ID",
                        },
                        "name": {"type": "string", "description": "Agent name"},
                        "description": {
                            "type": "string",
                            "description": "Agent description",
                        },
                        "agent_type": {
                            "type": "string",
                            "enum": ["mcp", "audit", "general"],
                        },
                        "capabilities": {"type": "array", "items": {"type": "string"}},
                        "config": {
                            "type": "object",
                            "description": "Agent configuration",
                        },
                    },
                    "required": ["agent_id", "name", "description", "agent_type"],
                },
            },
            {
                "name": "execute_with_capability",
                "description": "Execute a request using an agent with specific capability",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "capability": {
                            "type": "string",
                            "description": "Required capability",
                        },
                        "input_data": {
                            "type": "object",
                            "description": "Input data for the agent",
                        },
                        "metadata": {
                            "type": "object",
                            "description": "Optional metadata",
                        },
                    },
                    "required": ["capability", "input_data"],
                },
            },
        ]

    def _setup_routes(self):
        """Setup FastAPI routes"""

        @self.app.get("/")
        async def root():
            return {"message": "Chronicler MCP Server", "version": "1.0.0"}

        @self.app.get("/health")
        async def health():
            stats = await self.agent_manager.get_manager_stats()
            return {"status": "healthy", "stats": stats.model_dump()}

        @self.app.post("/agents/execute")
        async def execute_agent(request: AgentRequestModel):
            """Execute a request on a specific agent"""
            try:
                response = await self.agent_manager.execute_request(
                    request.agent_id, request.input_data, request.metadata
                )

                if response is None:
                    raise HTTPException(
                        status_code=404, detail=f"Agent {request.agent_id} not found"
                    )

                return AgentResponseModel(
                    request_id=response.request_id,
                    agent_id=response.agent_id,
                    output_data=response.output_data,
                    status=response.status,
                    execution_time=response.execution_time,
                    metadata=response.metadata,
                )

            except Exception as e:
                self.logger.error(f"Error executing agent {request.agent_id}: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/agents")
        async def list_agents():
            """List all registered agents"""
            try:
                metadata = await self.agent_manager.get_all_agent_metadata()
                return {
                    "agents": [
                        {"agent_id": agent_id, "metadata": meta.model_dump()}
                        for agent_id, meta in metadata.items()
                    ]
                }

            except Exception as e:
                self.logger.error(f"Error listing agents: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/agents/{agent_id}")
        async def get_agent(agent_id: str):
            """Get agent information"""
            try:
                metadata = await self.agent_manager.get_agent_metadata(agent_id)
                if metadata is None:
                    raise HTTPException(
                        status_code=404, detail=f"Agent {agent_id} not found"
                    )

                return {"agent_id": agent_id, "metadata": metadata.model_dump()}

            except HTTPException:
                raise
            except Exception as e:
                self.logger.error(f"Error getting agent {agent_id}: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/agents/{agent_id}/status")
        async def get_agent_status(agent_id: str):
            """Get agent status"""
            try:
                status = await self.agent_manager.get_agent_status(agent_id)
                if status is None:
                    raise HTTPException(
                        status_code=404, detail=f"Agent {agent_id} not found"
                    )

                return {"agent_id": agent_id, "status": status}

            except HTTPException:
                raise
            except Exception as e:
                self.logger.error(f"Error getting agent status {agent_id}: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/agents/register")
        async def register_agent(request: AgentRegistrationModel):
            """Register a new agent"""
            try:
                if request.agent_type == AgentType.MCP:
                    # For MCP agents, we need additional configuration
                    config = request.config or {}
                    mcp_server_url = config.get("mcp_server_url")
                    if not mcp_server_url:
                        raise HTTPException(
                            status_code=400,
                            detail="MCP server URL required for MCP agents",
                        )

                    agent = create_mcp_agent(
                        agent_id=request.agent_id,
                        name=request.name,
                        description=request.description,
                        mcp_server_url=mcp_server_url,
                        mcp_api_key=config.get("mcp_api_key"),
                        capabilities=request.capabilities,
                        **config,
                    )

                elif request.agent_type == AgentType.AUDIT:
                    agent = create_chronicler_agent(
                        agent_id=request.agent_id,
                        name=request.name,
                        description=request.description,
                        capabilities=request.capabilities,
                        **(request.config or {}),
                    )

                else:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Unsupported agent type: {request.agent_type}",
                    )

                success = await self.agent_manager.register_agent(agent)
                if not success:
                    raise HTTPException(
                        status_code=500, detail="Failed to register agent"
                    )

                return {"message": f"Agent {request.agent_id} registered successfully"}

            except HTTPException:
                raise
            except Exception as e:
                self.logger.error(f"Error registering agent: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.delete("/agents/{agent_id}")
        async def unregister_agent(agent_id: str):
            """Unregister an agent"""
            try:
                success = await self.agent_manager.unregister_agent(agent_id)
                if not success:
                    raise HTTPException(
                        status_code=404, detail=f"Agent {agent_id} not found"
                    )

                return {"message": f"Agent {agent_id} unregistered successfully"}

            except HTTPException:
                raise
            except Exception as e:
                self.logger.error(f"Error unregistering agent {agent_id}: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/stats")
        async def get_stats():
            """Get manager statistics"""
            try:
                stats = await self.agent_manager.get_manager_stats()
                return stats.model_dump()

            except Exception as e:
                self.logger.error(f"Error getting stats: {e}")
                raise HTTPException(status_code=500, detail=str(e))

    async def handle_mcp_tool_call(self, tool_call: MCPToolCall) -> Dict[str, Any]:
        """Handle MCP tool calls"""
        try:
            tool_name = tool_call.tool_name
            arguments = tool_call.arguments

            if tool_name == "execute_agent":
                response = await self.agent_manager.execute_request(
                    arguments["agent_id"],
                    arguments["input_data"],
                    arguments.get("metadata"),
                )

                if response is None:
                    return {"error": f"Agent {arguments['agent_id']} not found"}

                return {
                    "request_id": response.request_id,
                    "status": response.status,
                    "output_data": response.output_data,
                    "execution_time": response.execution_time,
                }

            elif tool_name == "list_agents":
                metadata = await self.agent_manager.get_all_agent_metadata()
                return {
                    "agents": [
                        {
                            "agent_id": agent_id,
                            "name": meta.name,
                            "type": meta.agent_type,
                            "capabilities": [cap.value for cap in meta.capabilities],
                        }
                        for agent_id, meta in metadata.items()
                    ]
                }

            elif tool_name == "get_agent_status":
                status = await self.agent_manager.get_agent_status(
                    arguments["agent_id"]
                )
                if status is None:
                    return {"error": f"Agent {arguments['agent_id']} not found"}

                return status

            elif tool_name == "register_agent":
                # This would require more complex handling for different agent types
                return {"error": "Agent registration via MCP not yet implemented"}

            elif tool_name == "execute_with_capability":
                capability = AgentCapability(arguments["capability"])
                response = await self.agent_manager.execute_with_capability(
                    capability, arguments["input_data"], arguments.get("metadata")
                )

                if response is None:
                    return {
                        "error": f"No agent found with capability {arguments['capability']}"
                    }

                return {
                    "request_id": response.request_id,
                    "agent_id": response.agent_id,
                    "status": response.status,
                    "output_data": response.output_data,
                    "execution_time": response.execution_time,
                }

            else:
                return {"error": f"Unknown tool: {tool_name}"}

        except Exception as e:
            self.logger.error(
                f"Error handling MCP tool call {tool_call.tool_name}: {e}"
            )
            return {"error": str(e)}

    async def startup(self):
        """Startup the server"""
        self.logger.info("Starting Chronicler MCP Server")

        # Initialize default agents if configured
        if self.config.enable_auto_registration:
            await self._register_default_agents()

    async def shutdown(self):
        """Shutdown the server"""
        self.logger.info("Shutting down Chronicler MCP Server")
        await self.agent_manager.shutdown()

    async def _register_default_agents(self):
        """Register default agents"""
        try:
            # Register a default Chronicler agent
            chronicler_agent = create_chronicler_agent(
                agent_id="default_chronicler",
                name="Default Chronicler Agent",
                description="Default agent for blockchain operations",
                capabilities=[
                    AgentCapability.BLOCKCHAIN_INTERACTION,
                    AgentCapability.AUDIT_LOGGING,
                    AgentCapability.ACCESS_CONTROL,
                ],
            )

            await self.agent_manager.register_agent(chronicler_agent)
            self.logger.info("Registered default Chronicler agent")

        except Exception as e:
            self.logger.error(f"Failed to register default agents: {e}")


# Create and configure the server
def create_mcp_server(
    config: Optional[AgentManagerConfig] = None,
) -> MCPChroniclerServer:
    """Create a configured MCP server"""
    return MCPChroniclerServer(config)


# Example usage
if __name__ == "__main__":
    import uvicorn

    # Create server
    server = create_mcp_server()

    # Run with uvicorn
    uvicorn.run(
        server.app,
        host=server.config.mcp_server_host,
        port=server.config.mcp_server_port,
        log_level=server.config.log_level.lower(),
    )
