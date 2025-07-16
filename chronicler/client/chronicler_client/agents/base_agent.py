"""
Base agent class for Chronicler agents
"""

import asyncio
import logging
import time
import uuid
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from ..decorators.types import ActionMetadata, ActionStatus, AuditResult
from ..services.chronicler_service import ChroniclerService
from ..services.exceptions import ChroniclerError
from .agent_config import AgentConfig
from .agent_types import AgentCapability, AgentMetadata, AgentStatus, AgentType


class AgentRequest(BaseModel):
    """Request model for agent operations"""

    request_id: str
    agent_id: str
    input_data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None
    timeout: Optional[int] = None


class AgentResponse(BaseModel):
    """Response model for agent operations"""

    request_id: str
    agent_id: str
    output_data: Dict[str, Any]
    status: str
    execution_time: float
    metadata: Optional[Dict[str, Any]] = None
    audit_result: Optional[AuditResult] = None


class BaseAgent(ABC):
    """Base class for all Chronicler agents"""

    def __init__(
        self,
        config: AgentConfig,
        chronicler_service: Optional[ChroniclerService] = None,
    ):
        self.config = config
        self.agent_id = config.agent_id
        self.name = config.name
        self.description = config.description
        self.agent_type = config.agent_type
        self.capabilities = config.capabilities

        # Initialize services
        self.chronicler_service = chronicler_service or ChroniclerService()

        # State management
        self.status = AgentStatus.IDLE
        self.current_task: Optional[asyncio.Task] = None
        self.request_count = 0
        self.error_count = 0
        self.last_activity = time.time()

        # Setup logging
        self.logger = logging.getLogger(f"agent.{self.agent_id}")
        self.logger.setLevel(getattr(logging, self.config.log_level.upper()))

        # Performance tracking
        self.execution_times: List[float] = []
        self.cache_hits = 0
        self.cache_misses = 0

        # Initialize agent
        self._initialize()

    def _initialize(self):
        """Initialize the agent"""
        try:
            self.logger.info(f"Initializing agent {self.agent_id}")

            # Register with Chronicler if audit is enabled
            if self.config.audit_enabled:
                asyncio.create_task(self._register_with_chronicler())

            self.status = AgentStatus.IDLE
            self.logger.info(f"Agent {self.agent_id} initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize agent {self.agent_id}: {e}")
            self.status = AgentStatus.ERROR
            raise

    async def _register_with_chronicler(self):
        """Register the agent with the Chronicler system"""
        try:
            # Register agent metadata
            metadata = ActionMetadata(
                agent_id=self.agent_id,
                tool_id="agent_registration",
                description=f"Registering agent {self.name}",
                risk_level=self.config.risk_level,
            )

            # Log registration action
            await self.chronicler_service.log_action(
                action_id=str(uuid.uuid4()),
                agent_id=self.agent_id,
                tool_id="agent_registration",
                input_data={"agent_config": self.config.model_dump()},
                output_data={"status": "registered"},
                status="success",
            )

            self.logger.info(f"Agent {self.agent_id} registered with Chronicler")

        except Exception as e:
            self.logger.error(
                f"Failed to register agent {self.agent_id} with Chronicler: {e}"
            )

    @abstractmethod
    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process a request - must be implemented by subclasses"""
        pass

    async def execute(
        self, input_data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Execute the agent with input data"""
        request_id = str(uuid.uuid4())
        request = AgentRequest(
            request_id=request_id,
            agent_id=self.agent_id,
            input_data=input_data,
            metadata=metadata,
        )

        return await self.process_request(request)

    async def _audit_action(
        self, action_id: str, input_data: Any, output_data: Any
    ) -> Optional[AuditResult]:
        """Audit an action if audit is enabled"""
        if not self.config.audit_enabled:
            return None

        try:
            metadata = ActionMetadata(
                agent_id=self.agent_id,
                tool_id="agent_execution",
                description=f"Agent {self.name} execution",
                risk_level=self.config.risk_level,
            )

            return await self.chronicler_service.log_action(
                action_id=action_id,
                agent_id=self.agent_id,
                tool_id="agent_execution",
                input_data=input_data if self.config.log_input else None,
                output_data=output_data if self.config.log_output else None,
                status="success",
            )

        except Exception as e:
            self.logger.error(f"Failed to audit action {action_id}: {e}")
            return None

    def get_metadata(self) -> AgentMetadata:
        """Get agent metadata"""
        return AgentMetadata(
            agent_id=self.agent_id,
            name=self.name,
            description=self.description,
            agent_type=self.agent_type,
            capabilities=self.capabilities,
            model_name=self.config.model_name,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            risk_level=self.config.risk_level,
            metadata={
                "request_count": self.request_count,
                "error_count": self.error_count,
                "status": self.status,
                "last_activity": self.last_activity,
                "avg_execution_time": sum(self.execution_times)
                / len(self.execution_times)
                if self.execution_times
                else 0,
                "cache_hits": self.cache_hits,
                "cache_misses": self.cache_misses,
            },
        )

    def get_health_status(self) -> Dict[str, Any]:
        """Get agent health status"""
        return {
            "agent_id": self.agent_id,
            "status": self.status,
            "request_count": self.request_count,
            "error_count": self.error_count,
            "error_rate": self.error_count / max(self.request_count, 1),
            "last_activity": self.last_activity,
            "uptime": time.time() - self.last_activity,
            "avg_execution_time": sum(self.execution_times) / len(self.execution_times)
            if self.execution_times
            else 0,
            "cache_hit_rate": self.cache_hits
            / max(self.cache_hits + self.cache_misses, 1),
        }

    async def shutdown(self):
        """Shutdown the agent"""
        try:
            self.logger.info(f"Shutting down agent {self.agent_id}")

            # Cancel current task if running
            if self.current_task and not self.current_task.done():
                self.current_task.cancel()
                try:
                    await self.current_task
                except asyncio.CancelledError:
                    pass

            self.status = AgentStatus.DISABLED
            self.logger.info(f"Agent {self.agent_id} shut down successfully")

        except Exception as e:
            self.logger.error(f"Error shutting down agent {self.agent_id}: {e}")

    @asynccontextmanager
    async def _execution_context(self, request_id: str):
        """Context manager for agent execution"""
        start_time = time.time()
        self.status = AgentStatus.RUNNING
        self.request_count += 1
        self.last_activity = time.time()

        try:
            yield
        except Exception as e:
            self.error_count += 1
            self.logger.error(f"Error in agent execution {request_id}: {e}")
            raise
        finally:
            execution_time = time.time() - start_time
            self.execution_times.append(execution_time)
            self.status = AgentStatus.IDLE

            # Keep only last 100 execution times
            if len(self.execution_times) > 100:
                self.execution_times = self.execution_times[-100:]
