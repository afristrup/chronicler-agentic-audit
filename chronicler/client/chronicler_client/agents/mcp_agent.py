"""
MCP (Model Context Protocol) Agent for Chronicler
"""

import asyncio
import json
import logging
import uuid
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import httpx
from fastapi_mcp import MCPClient, MCPRequest, MCPResponse
from pydantic import BaseModel

from .agent_config import AgentConfig
from .agent_types import AgentCapability, AgentStatus, AgentType
from .base_agent import AgentRequest, AgentResponse, BaseAgent


class MCPToolCall(BaseModel):
    """MCP tool call request"""

    tool_name: str
    arguments: Dict[str, Any]
    tool_call_id: Optional[str] = None


class MCPToolResult(BaseModel):
    """MCP tool call result"""

    tool_call_id: str
    content: List[Dict[str, Any]]
    is_error: bool = False


class MCPAgent(BaseAgent):
    """Agent that integrates with MCP (Model Context Protocol)"""

    def __init__(self, config: AgentConfig, mcp_client: Optional[MCPClient] = None):
        super().__init__(config)

        # Validate MCP configuration
        if not config.mcp_enabled:
            raise ValueError("MCP must be enabled for MCPAgent")

        if not config.mcp_server_url:
            raise ValueError("MCP server URL is required for MCPAgent")

        # Initialize MCP client
        self.mcp_client = mcp_client or MCPClient(
            server_url=config.mcp_server_url, api_key=config.mcp_api_key
        )

        # MCP-specific state
        self.available_tools: List[Dict[str, Any]] = []
        self.tool_schemas: Dict[str, Dict[str, Any]] = {}
        self.session_id: Optional[str] = None

        # Initialize MCP connection
        asyncio.create_task(self._initialize_mcp())

    async def _initialize_mcp(self):
        """Initialize MCP connection and discover tools"""
        try:
            self.logger.info(f"Initializing MCP connection for agent {self.agent_id}")

            # Initialize MCP session
            await self.mcp_client.initialize()
            self.session_id = self.mcp_client.session_id

            # List available tools
            tools_response = await self.mcp_client.list_tools()
            self.available_tools = tools_response.tools

            # Store tool schemas
            for tool in self.available_tools:
                self.tool_schemas[tool["name"]] = tool

            self.logger.info(
                f"MCP agent {self.agent_id} initialized with {len(self.available_tools)} tools"
            )

        except Exception as e:
            self.logger.error(
                f"Failed to initialize MCP for agent {self.agent_id}: {e}"
            )
            self.status = AgentStatus.ERROR
            raise

    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process a request using MCP tools"""
        async with self._execution_context(request.request_id):
            try:
                # Parse the request
                prompt = request.input_data.get("prompt", "")
                tools_to_use = request.input_data.get("tools", [])
                model = request.input_data.get("model", self.config.model_name)

                # Validate tools
                if tools_to_use:
                    for tool_name in tools_to_use:
                        if tool_name not in self.tool_schemas:
                            raise ValueError(f"Tool '{tool_name}' not available")

                # Create MCP request
                mcp_request = MCPRequest(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    tools=tools_to_use if tools_to_use else None,
                    tool_choice="auto" if tools_to_use else None,
                    max_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                    stream=False,
                )

                # Execute MCP request
                mcp_response = await self.mcp_client.chat_completion(mcp_request)

                # Process tool calls if any
                tool_results = []
                if mcp_response.choices and mcp_response.choices[0].tool_calls:
                    tool_results = await self._execute_tool_calls(
                        mcp_response.choices[0].tool_calls
                    )

                # Create response
                output_data = {
                    "content": mcp_response.choices[0].message.content
                    if mcp_response.choices
                    else "",
                    "tool_calls": mcp_response.choices[0].tool_calls
                    if mcp_response.choices
                    else [],
                    "tool_results": tool_results,
                    "model": model,
                    "usage": mcp_response.usage.model_dump()
                    if mcp_response.usage
                    else None,
                }

                # Audit the action
                audit_result = await self._audit_action(
                    request.request_id, request.input_data, output_data
                )

                return AgentResponse(
                    request_id=request.request_id,
                    agent_id=self.agent_id,
                    output_data=output_data,
                    status="success",
                    execution_time=0.0,  # Will be set by context manager
                    metadata={
                        "model": model,
                        "tools_used": len(tool_results),
                        "mcp_session_id": self.session_id,
                    },
                    audit_result=audit_result,
                )

            except Exception as e:
                self.logger.error(
                    f"Error processing MCP request {request.request_id}: {e}"
                )

                # Audit the error
                audit_result = await self._audit_action(
                    request.request_id, request.input_data, {"error": str(e)}
                )

                return AgentResponse(
                    request_id=request.request_id,
                    agent_id=self.agent_id,
                    output_data={"error": str(e)},
                    status="error",
                    execution_time=0.0,
                    metadata={"error_type": type(e).__name__},
                    audit_result=audit_result,
                )

    async def _execute_tool_calls(
        self, tool_calls: List[Dict[str, Any]]
    ) -> List[MCPToolResult]:
        """Execute MCP tool calls"""
        results = []

        for tool_call in tool_calls:
            try:
                tool_name = tool_call["function"]["name"]
                arguments = json.loads(tool_call["function"]["arguments"])
                tool_call_id = tool_call.get("id")

                self.logger.info(f"Executing MCP tool: {tool_name}")

                # Execute the tool
                tool_response = await self.mcp_client.call_tool(
                    tool_name=tool_name, arguments=arguments
                )

                # Create tool result
                result = MCPToolResult(
                    tool_call_id=tool_call_id,
                    content=tool_response.content,
                    is_error=False,
                )

                results.append(result)

            except Exception as e:
                self.logger.error(f"Error executing MCP tool {tool_name}: {e}")

                result = MCPToolResult(
                    tool_call_id=tool_call.get("id"),
                    content=[{"type": "text", "text": f"Error: {str(e)}"}],
                    is_error=True,
                )

                results.append(result)

        return results

    async def list_available_tools(self) -> List[Dict[str, Any]]:
        """List available MCP tools"""
        return self.available_tools

    async def get_tool_schema(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get schema for a specific tool"""
        return self.tool_schemas.get(tool_name)

    async def call_tool_directly(
        self, tool_name: str, arguments: Dict[str, Any]
    ) -> MCPToolResult:
        """Call an MCP tool directly"""
        try:
            tool_response = await self.mcp_client.call_tool(
                tool_name=tool_name, arguments=arguments
            )

            return MCPToolResult(
                tool_call_id=str(uuid.uuid4()),
                content=tool_response.content,
                is_error=False,
            )

        except Exception as e:
            self.logger.error(f"Error calling MCP tool {tool_name}: {e}")

            return MCPToolResult(
                tool_call_id=str(uuid.uuid4()),
                content=[{"type": "text", "text": f"Error: {str(e)}"}],
                is_error=True,
            )

    async def shutdown(self):
        """Shutdown the MCP agent"""
        try:
            # Close MCP connection
            if self.mcp_client:
                await self.mcp_client.close()

            await super().shutdown()

        except Exception as e:
            self.logger.error(f"Error shutting down MCP agent {self.agent_id}: {e}")


# Factory function for creating MCP agents
def create_mcp_agent(
    agent_id: str,
    name: str,
    description: str,
    mcp_server_url: str,
    mcp_api_key: Optional[str] = None,
    capabilities: Optional[List[AgentCapability]] = None,
    **kwargs,
) -> MCPAgent:
    """Create an MCP agent with the given configuration"""

    if capabilities is None:
        capabilities = [
            AgentCapability.MCP_PROTOCOL,
            AgentCapability.TEXT_GENERATION,
            AgentCapability.CODE_GENERATION,
        ]

    config = AgentConfig(
        agent_id=agent_id,
        name=name,
        description=description,
        agent_type=AgentType.MCP,
        capabilities=capabilities,
        mcp_enabled=True,
        mcp_server_url=mcp_server_url,
        mcp_api_key=mcp_api_key,
        **kwargs,
    )

    return MCPAgent(config)
