"""
Chronicler service for blockchain interactions
"""

import json
import time
from typing import Any, Dict, Optional

from chronicler_client.config import get_config
from chronicler_client.decorators.types import ActionMetadata, ActionStatus, AuditResult
from chronicler_client.services.access_control_service import AccessControlService
from chronicler_client.services.audit_service import AuditService
from chronicler_client.services.exceptions import ChroniclerError
from chronicler_client.services.registry_service import RegistryService
from web3 import Web3
from web3.contract import Contract


class ChroniclerService:
    """Service for interacting with Chronicler smart contracts"""

    def __init__(self, config=None):
        self.config = config or get_config()
        self.w3 = Web3(Web3.HTTPProvider(self.config.rpc_url))

        # Initialize contract interfaces (simplified for demo)
        self.registry_contract = self._get_contract(self.config.registry_address, [])
        self.audit_log_contract = self._get_contract(self.config.audit_log_address, [])
        self.access_control_contract = self._get_contract(
            self.config.access_control_address, []
        )

        # Initialize sub-services
        self.audit_service = AuditService(config)
        self.registry_service = RegistryService(config)
        self.access_control_service = AccessControlService(config)

    def _get_contract(self, address: str, abi: list) -> Contract:
        """Get contract instance"""
        return self.w3.eth.contract(address=address, abi=abi)

    async def log_action(
        self,
        action_id: str,
        agent_id: str,
        tool_id: str,
        input_data: Any,
        output_data: Any,
        status: str = "success",
    ) -> AuditResult:
        """Log an action to the blockchain"""
        try:
            # Check access control first
            is_allowed, reason = await self.access_control_service.check_action_allowed(
                agent_id, tool_id
            )

            if not is_allowed:
                return AuditResult(
                    action_id=action_id,
                    status=ActionStatus.FAILED,
                    error_message=f"Access denied: {reason}",
                    timestamp=int(time.time()),
                )

            # Create action data
            action_data = {
                "action_id": action_id,
                "agent_id": agent_id,
                "tool_id": tool_id,
                "input": input_data,
                "output": output_data,
                "status": status,
                "timestamp": int(time.time()),
            }

            # Create data hash
            data_hash = await self.audit_service.create_data_hash(action_data)

            # Log to blockchain
            tx_hash = await self.audit_service.log_action(
                action_id, agent_id, tool_id, data_hash, status
            )

            return AuditResult(
                action_id=action_id,
                status=ActionStatus.SUCCESS,
                tx_hash=tx_hash,
                gas_used=21000,
                timestamp=int(time.time()),
            )

        except Exception as e:
            return AuditResult(
                action_id=action_id,
                status=ActionStatus.FAILED,
                error_message=str(e),
                timestamp=int(time.time()),
            )

    def log_action_sync(
        self,
        action_id: str,
        metadata: ActionMetadata,
        input_data: Any,
        output_data: Any,
    ) -> AuditResult:
        """Synchronous version of log_action for backward compatibility"""
        try:
            # Create action data
            action_data = {
                "action_id": action_id,
                "agent_id": metadata.agent_id,
                "tool_id": metadata.tool_id,
                "input": input_data,
                "output": output_data,
                "metadata": metadata.model_dump(),
                "timestamp": int(time.time()),
            }

            # In a real implementation, this would:
            # 1. Check access control permissions
            # 2. Validate agent and tool registration
            # 3. Call the audit log contract
            # 4. Handle gas estimation and transaction signing

            # Simulate blockchain interaction
            tx_hash = self._simulate_transaction(action_data)

            return AuditResult(
                action_id=action_id,
                status=ActionStatus.SUCCESS,
                tx_hash=tx_hash,
                gas_used=21000,
                timestamp=int(time.time()),
            )

        except Exception as e:
            return AuditResult(
                action_id=action_id,
                status=ActionStatus.FAILED,
                error_message=str(e),
                timestamp=int(time.time()),
            )

    def _simulate_transaction(self, action_data: Dict[str, Any]) -> str:
        """Simulate a blockchain transaction"""
        # In real implementation, this would create and send a transaction
        import hashlib

        data_str = json.dumps(action_data, sort_keys=True)
        return f"0x{hashlib.sha256(data_str.encode()).hexdigest()[:64]}"

    async def check_access(self, agent_id: str, tool_id: str) -> bool:
        """Check if agent has access to tool"""
        try:
            is_allowed, _ = await self.access_control_service.check_action_allowed(
                agent_id, tool_id
            )
            return is_allowed
        except Exception:
            return False

    async def get_agent_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent information from registry"""
        try:
            return await self.registry_service.get_agent(agent_id)
        except Exception:
            return None

    async def get_tool_info(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """Get tool information from registry"""
        try:
            return await self.registry_service.get_tool(tool_id)
        except Exception:
            return None

    async def get_action_statistics(
        self, agent_id: Optional[str] = None, tool_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get action statistics"""
        try:
            return await self.audit_service.get_action_statistics(agent_id, tool_id)
        except Exception as e:
            raise ChroniclerError(f"Failed to get statistics: {str(e)}", "STATS_FAILED")

    async def get_usage_statistics(
        self, agent_id: Optional[str] = None, tool_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get usage statistics"""
        try:
            return await self.access_control_service.get_usage_statistics(
                agent_id, tool_id
            )
        except Exception as e:
            raise ChroniclerError(
                f"Failed to get usage statistics: {str(e)}", "USAGE_STATS_FAILED"
            )
