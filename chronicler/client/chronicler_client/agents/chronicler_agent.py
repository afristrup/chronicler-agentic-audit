"""
Chronicler Agent - Specialized agent for blockchain interactions
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from ..decorators.types import ActionMetadata, ActionStatus, AuditResult
from ..services.access_control_service import AccessControlService
from ..services.audit_service import AuditService
from ..services.chronicler_service import ChroniclerService
from ..services.registry_service import RegistryService
from .agent_config import AgentConfig
from .agent_types import AgentCapability, AgentStatus, AgentType
from .base_agent import AgentRequest, AgentResponse, BaseAgent


class BlockchainAction(BaseModel):
    """Blockchain action request"""

    action_type: str
    contract_address: Optional[str] = None
    function_name: str
    parameters: Dict[str, Any]
    gas_limit: Optional[int] = None
    priority: str = "normal"  # low, normal, high


class BlockchainResult(BaseModel):
    """Blockchain action result"""

    action_id: str
    tx_hash: Optional[str] = None
    gas_used: Optional[int] = None
    status: str
    block_number: Optional[int] = None
    error_message: Optional[str] = None
    timestamp: datetime


class ChroniclerAgent(BaseAgent):
    """Specialized agent for Chronicler blockchain interactions"""

    def __init__(
        self,
        config: AgentConfig,
        chronicler_service: Optional[ChroniclerService] = None,
    ):
        super().__init__(config, chronicler_service)

        # Initialize specialized services
        self.registry_service = RegistryService(self.chronicler_service.config)
        self.audit_service = AuditService(self.chronicler_service.config)
        self.access_control_service = AccessControlService(
            self.chronicler_service.config
        )

        # Agent-specific state
        self.registered_agents: List[str] = []
        self.registered_tools: List[str] = []
        self.pending_actions: List[BlockchainAction] = []
        self.completed_actions: List[BlockchainResult] = []

        # Initialize blockchain capabilities
        asyncio.create_task(self._initialize_blockchain())

    async def _initialize_blockchain(self):
        """Initialize blockchain capabilities"""
        try:
            self.logger.info(
                f"Initializing blockchain capabilities for agent {self.agent_id}"
            )

            # Check if agent is registered
            is_registered = await self.registry_service.is_valid_agent(self.agent_id)
            if not is_registered:
                await self._register_agent()

            # Load registered agents and tools
            await self._load_registrations()

            self.logger.info(
                f"Blockchain agent {self.agent_id} initialized successfully"
            )

        except Exception as e:
            self.logger.error(
                f"Failed to initialize blockchain for agent {self.agent_id}: {e}"
            )
            self.status = AgentStatus.ERROR
            raise

    async def _register_agent(self):
        """Register the agent with the registry"""
        try:
            result = await self.registry_service.register_agent(
                agent_id=self.agent_id,
                name=self.name,
                description=self.description,
                capabilities=[cap.value for cap in self.capabilities],
                risk_level=self.config.risk_level,
                metadata=self.config.model_dump(),
            )

            self.logger.info(f"Agent {self.agent_id} registered: {result}")

        except Exception as e:
            self.logger.error(f"Failed to register agent {self.agent_id}: {e}")
            raise

    async def _load_registrations(self):
        """Load registered agents and tools"""
        try:
            # This would typically load from the blockchain registry
            # For now, we'll simulate with empty lists
            self.registered_agents = []
            self.registered_tools = []

        except Exception as e:
            self.logger.error(f"Failed to load registrations: {e}")

    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process a blockchain-related request"""
        async with self._execution_context(request.request_id):
            try:
                action_type = request.input_data.get("action_type", "audit")

                if action_type == "audit":
                    return await self._handle_audit_request(request)
                elif action_type == "registry":
                    return await self._handle_registry_request(request)
                elif action_type == "access_control":
                    return await self._handle_access_control_request(request)
                elif action_type == "blockchain":
                    return await self._handle_blockchain_request(request)
                else:
                    raise ValueError(f"Unknown action type: {action_type}")

            except Exception as e:
                self.logger.error(f"Error processing request {request.request_id}: {e}")

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

    async def _handle_audit_request(self, request: AgentRequest) -> AgentResponse:
        """Handle audit-related requests"""
        try:
            action_data = request.input_data.get("action_data", {})
            agent_id = action_data.get("agent_id")
            tool_id = action_data.get("tool_id")
            data_hash = action_data.get("data_hash")

            # Create data hash if not provided
            if not data_hash:
                data_hash = await self.audit_service.create_data_hash(action_data)

            # Log action to blockchain
            tx_hash = await self.audit_service.log_action(
                action_id=request.request_id,
                agent_id=agent_id or self.agent_id,
                tool_id=tool_id or "audit_agent",
                data_hash=data_hash,
                status="success",
            )

            # Get action details
            action_details = await self.audit_service.get_action(request.request_id)

            output_data = {
                "action_id": request.request_id,
                "tx_hash": tx_hash,
                "data_hash": data_hash,
                "action_details": action_details,
                "status": "success",
            }

            # Audit this action itself
            audit_result = await self._audit_action(
                request.request_id, request.input_data, output_data
            )

            return AgentResponse(
                request_id=request.request_id,
                agent_id=self.agent_id,
                output_data=output_data,
                status="success",
                execution_time=0.0,
                metadata={"action_type": "audit"},
                audit_result=audit_result,
            )

        except Exception as e:
            raise Exception(f"Audit request failed: {e}")

    async def _handle_registry_request(self, request: AgentRequest) -> AgentResponse:
        """Handle registry-related requests"""
        try:
            operation = request.input_data.get("operation", "get")

            if operation == "register_agent":
                agent_data = request.input_data.get("agent_data", {})
                result = await self.registry_service.register_agent(**agent_data)

            elif operation == "register_tool":
                tool_data = request.input_data.get("tool_data", {})
                result = await self.registry_service.register_tool(**tool_data)

            elif operation == "get_agent":
                agent_id = request.input_data.get("agent_id")
                result = await self.registry_service.get_agent(agent_id)

            elif operation == "get_tool":
                tool_id = request.input_data.get("tool_id")
                result = await self.registry_service.get_tool(tool_id)

            elif operation == "is_valid_agent":
                agent_id = request.input_data.get("agent_id")
                result = await self.registry_service.is_valid_agent(agent_id)

            elif operation == "is_valid_tool":
                tool_id = request.input_data.get("tool_id")
                result = await self.registry_service.is_valid_tool(tool_id)

            else:
                raise ValueError(f"Unknown registry operation: {operation}")

            output_data = {
                "operation": operation,
                "result": result,
                "status": "success",
            }

            # Audit this action
            audit_result = await self._audit_action(
                request.request_id, request.input_data, output_data
            )

            return AgentResponse(
                request_id=request.request_id,
                agent_id=self.agent_id,
                output_data=output_data,
                status="success",
                execution_time=0.0,
                metadata={"action_type": "registry"},
                audit_result=audit_result,
            )

        except Exception as e:
            raise Exception(f"Registry request failed: {e}")

    async def _handle_access_control_request(
        self, request: AgentRequest
    ) -> AgentResponse:
        """Handle access control requests"""
        try:
            operation = request.input_data.get("operation", "check")

            if operation == "check_access":
                agent_id = request.input_data.get("agent_id")
                tool_id = request.input_data.get("tool_id")
                (
                    is_allowed,
                    reason,
                ) = await self.access_control_service.check_action_allowed(
                    agent_id, tool_id
                )
                result = {"is_allowed": is_allowed, "reason": reason}

            elif operation == "get_agent_policy":
                agent_id = request.input_data.get("agent_id")
                result = await self.access_control_service.get_agent_policy(agent_id)

            elif operation == "get_tool_policy":
                tool_id = request.input_data.get("tool_id")
                result = await self.access_control_service.get_tool_policy(tool_id)

            elif operation == "set_agent_policy":
                policy_data = request.input_data.get("policy_data", {})
                result = await self.access_control_service.set_agent_policy(
                    **policy_data
                )

            elif operation == "set_tool_policy":
                policy_data = request.input_data.get("policy_data", {})
                result = await self.access_control_service.set_tool_policy(
                    **policy_data
                )

            elif operation == "check_rate_limit":
                agent_id = request.input_data.get("agent_id")
                tool_id = request.input_data.get("tool_id")
                (
                    is_within_limit,
                    reason,
                ) = await self.access_control_service.check_rate_limit(
                    agent_id, tool_id
                )
                result = {"is_within_limit": is_within_limit, "reason": reason}

            else:
                raise ValueError(f"Unknown access control operation: {operation}")

            output_data = {
                "operation": operation,
                "result": result,
                "status": "success",
            }

            # Audit this action
            audit_result = await self._audit_action(
                request.request_id, request.input_data, output_data
            )

            return AgentResponse(
                request_id=request.request_id,
                agent_id=self.agent_id,
                output_data=output_data,
                status="success",
                execution_time=0.0,
                metadata={"action_type": "access_control"},
                audit_result=audit_result,
            )

        except Exception as e:
            raise Exception(f"Access control request failed: {e}")

    async def _handle_blockchain_request(self, request: AgentRequest) -> AgentResponse:
        """Handle general blockchain requests"""
        try:
            action = BlockchainAction(**request.input_data.get("action", {}))

            # Add to pending actions
            self.pending_actions.append(action)

            # Simulate blockchain execution
            # In a real implementation, this would interact with actual smart contracts
            result = BlockchainResult(
                action_id=request.request_id,
                tx_hash=f"0x{request.request_id[:64]}",
                gas_used=21000,
                status="success",
                block_number=12345,
                timestamp=datetime.now(),
            )

            # Add to completed actions
            self.completed_actions.append(result)

            output_data = {
                "action": action.model_dump(),
                "result": result.model_dump(),
                "status": "success",
            }

            # Audit this action
            audit_result = await self._audit_action(
                request.request_id, request.input_data, output_data
            )

            return AgentResponse(
                request_id=request.request_id,
                agent_id=self.agent_id,
                output_data=output_data,
                status="success",
                execution_time=0.0,
                metadata={"action_type": "blockchain"},
                audit_result=audit_result,
            )

        except Exception as e:
            raise Exception(f"Blockchain request failed: {e}")

    async def get_blockchain_stats(self) -> Dict[str, Any]:
        """Get blockchain statistics"""
        try:
            audit_stats = await self.audit_service.get_action_statistics()
            access_stats = await self.access_control_service.get_usage_statistics()

            return {
                "audit_statistics": audit_stats,
                "access_control_statistics": access_stats,
                "pending_actions": len(self.pending_actions),
                "completed_actions": len(self.completed_actions),
                "registered_agents": len(self.registered_agents),
                "registered_tools": len(self.registered_tools),
            }

        except Exception as e:
            self.logger.error(f"Failed to get blockchain stats: {e}")
            return {"error": str(e)}

    async def get_action_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get action history"""
        try:
            # Get recent actions from audit service
            actions = await self.audit_service.get_actions_by_agent(
                agent_id=self.agent_id, limit=limit
            )

            return actions

        except Exception as e:
            self.logger.error(f"Failed to get action history: {e}")
            return []


# Factory function for creating Chronicler agents
def create_chronicler_agent(
    agent_id: str,
    name: str,
    description: str,
    capabilities: Optional[List[AgentCapability]] = None,
    **kwargs,
) -> ChroniclerAgent:
    """Create a Chronicler agent with the given configuration"""

    if capabilities is None:
        capabilities = [
            AgentCapability.BLOCKCHAIN_INTERACTION,
            AgentCapability.AUDIT_LOGGING,
            AgentCapability.ACCESS_CONTROL,
            AgentCapability.REGISTRY_MANAGEMENT,
        ]

    config = AgentConfig(
        agent_id=agent_id,
        name=name,
        description=description,
        agent_type=AgentType.AUDIT,
        capabilities=capabilities,
        **kwargs,
    )

    return ChroniclerAgent(config)
