"""
Chronicler service for blockchain interactions
"""

import json
import time
from typing import Any, Dict, Optional

from chronicler_client.config import get_config
from chronicler_client.decorators.types import ActionMetadata, ActionStatus, AuditResult
from web3 import Web3
from web3.contract import Contract


class ChroniclerService:
    """Service for interacting with Chronicler smart contracts"""

    def __init__(self):
        self.config = get_config()
        self.w3 = Web3(Web3.HTTPProvider(self.config.rpc_url))

        # Initialize contract interfaces (simplified for demo)
        self.registry_contract = self._get_contract(self.config.registry_address, [])
        self.audit_log_contract = self._get_contract(self.config.audit_log_address, [])
        self.access_control_contract = self._get_contract(
            self.config.access_control_address, []
        )

    def _get_contract(self, address: str, abi: list) -> Contract:
        """Get contract instance"""
        return self.w3.eth.contract(address=address, abi=abi)

    def log_action(
        self,
        action_id: str,
        metadata: ActionMetadata,
        input_data: Any,
        output_data: Any,
    ) -> AuditResult:
        """Log an action to the blockchain"""
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

    def check_access(self, agent_id: str, tool_id: str) -> bool:
        """Check if agent has access to tool"""
        try:
            # In real implementation, this would call the access control contract
            # return self.access_control_contract.functions.checkActionAllowed(agent_id, tool_id).call()
            return True  # Simplified for demo
        except Exception:
            return False

    def get_agent_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent information from registry"""
        try:
            # In real implementation, this would call the registry contract
            # return self.registry_contract.functions.getAgent(agent_id).call()
            return {"id": agent_id, "is_active": True, "total_actions": 0}
        except Exception:
            return None

    def get_tool_info(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """Get tool information from registry"""
        try:
            # In real implementation, this would call the registry contract
            # return self.registry_contract.functions.getTool(tool_id).call()
            return {"id": tool_id, "name": tool_id, "risk_level": 1, "is_active": True}
        except Exception:
            return None
