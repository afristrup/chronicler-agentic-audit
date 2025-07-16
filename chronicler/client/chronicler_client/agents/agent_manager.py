"""
Agent Manager - Coordinates and manages all Chronicler agents
"""

import asyncio
import logging
import time
from collections import defaultdict
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from ..services.chronicler_service import ChroniclerService
from .agent_config import AgentConfig, AgentManagerConfig
from .agent_types import AgentCapability, AgentMetadata, AgentStatus, AgentType
from .base_agent import AgentRequest, AgentResponse, BaseAgent
from .chronicler_agent import ChroniclerAgent, create_chronicler_agent
from .mcp_agent import MCPAgent, create_mcp_agent


class AgentManagerStats(BaseModel):
    """Statistics for the agent manager"""

    total_agents: int
    active_agents: int
    idle_agents: int
    error_agents: int
    total_requests: int
    total_errors: int
    avg_response_time: float
    uptime: float


class AgentManager:
    """Manages and coordinates all Chronicler agents"""

    def __init__(self, config: Optional[AgentManagerConfig] = None):
        self.config = config or AgentManagerConfig()

        # Agent storage
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_types: Dict[str, AgentType] = {}
        self.agent_capabilities: Dict[str, List[AgentCapability]] = {}

        # Request tracking
        self.request_history: List[AgentResponse] = []
        self.request_stats: Dict[str, int] = defaultdict(int)
        self.error_stats: Dict[str, int] = defaultdict(int)

        # Performance tracking
        self.start_time = time.time()
        self.response_times: List[float] = []

        # Setup logging
        self.logger = logging.getLogger("agent_manager")
        self.logger.setLevel(getattr(logging, self.config.log_level.upper()))

        # Health check task
        self.health_check_task: Optional[asyncio.Task] = None

        # Initialize manager
        self._initialize()

    def _initialize(self):
        """Initialize the agent manager"""
        try:
            self.logger.info("Initializing Agent Manager")

            # Start health check task if enabled
            if self.config.enable_health_checks:
                self.health_check_task = asyncio.create_task(self._health_check_loop())

            self.logger.info("Agent Manager initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize Agent Manager: {e}")
            raise

    async def register_agent(self, agent: BaseAgent) -> bool:
        """Register an agent with the manager"""
        try:
            agent_id = agent.agent_id

            if agent_id in self.agents:
                self.logger.warning(f"Agent {agent_id} already registered")
                return False

            # Store agent
            self.agents[agent_id] = agent
            self.agent_types[agent_id] = agent.agent_type
            self.agent_capabilities[agent_id] = agent.capabilities

            self.logger.info(f"Registered agent {agent_id} ({agent.agent_type})")
            return True

        except Exception as e:
            self.logger.error(f"Failed to register agent {agent.agent_id}: {e}")
            return False

    async def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent from the manager"""
        try:
            if agent_id not in self.agents:
                self.logger.warning(f"Agent {agent_id} not found")
                return False

            # Shutdown agent
            agent = self.agents[agent_id]
            await agent.shutdown()

            # Remove from storage
            del self.agents[agent_id]
            del self.agent_types[agent_id]
            del self.agent_capabilities[agent_id]

            self.logger.info(f"Unregistered agent {agent_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to unregister agent {agent_id}: {e}")
            return False

    async def execute_request(
        self,
        agent_id: str,
        input_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[AgentResponse]:
        """Execute a request on a specific agent"""
        try:
            if agent_id not in self.agents:
                self.logger.error(f"Agent {agent_id} not found")
                return None

            agent = self.agents[agent_id]

            # Check if agent is available
            if agent.status == AgentStatus.ERROR:
                self.logger.error(f"Agent {agent_id} is in error state")
                return None

            # Execute request
            start_time = time.time()
            response = await agent.execute(input_data, metadata)
            execution_time = time.time() - start_time

            # Update response time
            response.execution_time = execution_time
            self.response_times.append(execution_time)

            # Track statistics
            self.request_history.append(response)
            self.request_stats[agent_id] += 1

            if response.status == "error":
                self.error_stats[agent_id] += 1

            # Keep only last 1000 requests
            if len(self.request_history) > 1000:
                self.request_history = self.request_history[-1000:]

            # Keep only last 1000 response times
            if len(self.response_times) > 1000:
                self.response_times = self.response_times[-1000:]

            return response

        except Exception as e:
            self.logger.error(f"Error executing request on agent {agent_id}: {e}")
            self.error_stats[agent_id] += 1
            return None

    async def find_agent_by_capability(
        self, capability: AgentCapability
    ) -> Optional[str]:
        """Find an agent with the specified capability"""
        for agent_id, capabilities in self.agent_capabilities.items():
            if (
                capability in capabilities
                and self.agents[agent_id].status != AgentStatus.ERROR
            ):
                return agent_id
        return None

    async def find_agent_by_type(self, agent_type: AgentType) -> Optional[str]:
        """Find an agent of the specified type"""
        for agent_id, a_type in self.agent_types.items():
            if (
                a_type == agent_type
                and self.agents[agent_id].status != AgentStatus.ERROR
            ):
                return agent_id
        return None

    async def execute_with_capability(
        self,
        capability: AgentCapability,
        input_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[AgentResponse]:
        """Execute a request using an agent with the specified capability"""
        agent_id = await self.find_agent_by_capability(capability)
        if agent_id:
            return await self.execute_request(agent_id, input_data, metadata)
        else:
            self.logger.error(f"No agent found with capability {capability}")
            return None

    async def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific agent"""
        if agent_id not in self.agents:
            return None

        agent = self.agents[agent_id]
        return agent.get_health_status()

    async def get_all_agent_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all agents"""
        statuses = {}
        for agent_id, agent in self.agents.items():
            statuses[agent_id] = agent.get_health_status()
        return statuses

    async def get_agent_metadata(self, agent_id: str) -> Optional[AgentMetadata]:
        """Get metadata of a specific agent"""
        if agent_id not in self.agents:
            return None

        agent = self.agents[agent_id]
        return agent.get_metadata()

    async def get_all_agent_metadata(self) -> Dict[str, AgentMetadata]:
        """Get metadata of all agents"""
        metadata = {}
        for agent_id, agent in self.agents.items():
            metadata[agent_id] = agent.get_metadata()
        return metadata

    async def get_manager_stats(self) -> AgentManagerStats:
        """Get manager statistics"""
        total_agents = len(self.agents)
        active_agents = sum(
            1 for agent in self.agents.values() if agent.status == AgentStatus.RUNNING
        )
        idle_agents = sum(
            1 for agent in self.agents.values() if agent.status == AgentStatus.IDLE
        )
        error_agents = sum(
            1 for agent in self.agents.values() if agent.status == AgentStatus.ERROR
        )

        total_requests = sum(self.request_stats.values())
        total_errors = sum(self.error_stats.values())

        avg_response_time = (
            sum(self.response_times) / len(self.response_times)
            if self.response_times
            else 0
        )
        uptime = time.time() - self.start_time

        return AgentManagerStats(
            total_agents=total_agents,
            active_agents=active_agents,
            idle_agents=idle_agents,
            error_agents=error_agents,
            total_requests=total_requests,
            total_errors=total_errors,
            avg_response_time=avg_response_time,
            uptime=uptime,
        )

    async def _health_check_loop(self):
        """Health check loop for all agents"""
        while True:
            try:
                await asyncio.sleep(self.config.health_check_interval)

                for agent_id, agent in self.agents.items():
                    try:
                        # Simple health check - try to get agent status
                        health_status = agent.get_health_status()

                        # Log if agent has high error rate
                        if health_status.get("error_rate", 0) > 0.5:
                            self.logger.warning(
                                f"Agent {agent_id} has high error rate: {health_status['error_rate']}"
                            )

                    except Exception as e:
                        self.logger.error(
                            f"Health check failed for agent {agent_id}: {e}"
                        )

            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in health check loop: {e}")

    async def shutdown(self):
        """Shutdown the agent manager"""
        try:
            self.logger.info("Shutting down Agent Manager")

            # Cancel health check task
            if self.health_check_task and not self.health_check_task.done():
                self.health_check_task.cancel()
                try:
                    await self.health_check_task
                except asyncio.CancelledError:
                    pass

            # Shutdown all agents
            shutdown_tasks = []
            for agent_id, agent in self.agents.items():
                shutdown_tasks.append(agent.shutdown())

            if shutdown_tasks:
                await asyncio.gather(*shutdown_tasks, return_exceptions=True)

            self.logger.info("Agent Manager shut down successfully")

        except Exception as e:
            self.logger.error(f"Error shutting down Agent Manager: {e}")


# Factory functions for creating agents
async def create_and_register_mcp_agent(
    manager: AgentManager,
    agent_id: str,
    name: str,
    description: str,
    mcp_server_url: str,
    mcp_api_key: Optional[str] = None,
    **kwargs,
) -> Optional[MCPAgent]:
    """Create and register an MCP agent"""
    try:
        agent = create_mcp_agent(
            agent_id=agent_id,
            name=name,
            description=description,
            mcp_server_url=mcp_server_url,
            mcp_api_key=mcp_api_key,
            **kwargs,
        )

        success = await manager.register_agent(agent)
        if success:
            return agent
        else:
            return None

    except Exception as e:
        manager.logger.error(f"Failed to create MCP agent {agent_id}: {e}")
        return None


async def create_and_register_chronicler_agent(
    manager: AgentManager, agent_id: str, name: str, description: str, **kwargs
) -> Optional[ChroniclerAgent]:
    """Create and register a Chronicler agent"""
    try:
        agent = create_chronicler_agent(
            agent_id=agent_id, name=name, description=description, **kwargs
        )

        success = await manager.register_agent(agent)
        if success:
            return agent
        else:
            return None

    except Exception as e:
        manager.logger.error(f"Failed to create Chronicler agent {agent_id}: {e}")
        return None
