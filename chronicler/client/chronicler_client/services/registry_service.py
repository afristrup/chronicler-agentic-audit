"""
Registry service for agent and tool registration
"""

import json
import time
from typing import Any, Dict, Optional

from chronicler_client.config import get_config
from chronicler_client.services.exceptions import RegistryError
from web3 import Web3
from web3.contract import Contract


class RegistryService:
    """Service for agent and tool registration"""

    def __init__(self, config=None):
        self.config = config or get_config()
        self.w3 = Web3(Web3.HTTPProvider(self.config.rpc_url))

        # Initialize registry contract (simplified for demo)
        self.registry_contract = self._get_contract(self.config.registry_address, [])

    def _get_contract(self, address: str, abi: list) -> Contract:
        """Get contract instance"""
        return self.w3.eth.contract(address=address, abi=abi)

    async def register_agent(
        self,
        agent_id: str,
        operator: str,
        metadata_uri: str,
        risk_level: int = 1,
        description: str = "",
    ) -> Dict[str, Any]:
        """Register an agent in the registry"""
        try:
            # In real implementation, this would call the registry contract
            # tx_hash = await self.registry_contract.functions.registerAgent(
            #     agent_id, operator, metadata_uri, risk_level, description
            # ).transact()

            # Simulate registration
            tx_hash = f"0x{agent_id.encode().hex()[:64]}"

            return {
                "agent_id": agent_id,
                "operator": operator,
                "metadata_uri": metadata_uri,
                "risk_level": risk_level,
                "description": description,
                "tx_hash": tx_hash,
                "timestamp": int(time.time()),
            }

        except Exception as e:
            raise RegistryError(
                f"Failed to register agent: {str(e)}", "REGISTRATION_FAILED"
            )

    async def register_tool(
        self,
        tool_id: str,
        agent_id: str,
        metadata_uri: str,
        risk_level: int = 1,
        description: str = "",
    ) -> Dict[str, Any]:
        """Register a tool in the registry"""
        try:
            # In real implementation, this would call the registry contract
            # tx_hash = await self.registry_contract.functions.registerTool(
            #     tool_id, agent_id, metadata_uri, risk_level, description
            # ).transact()

            # Simulate registration
            tx_hash = f"0x{tool_id.encode().hex()[:64]}"

            return {
                "tool_id": tool_id,
                "agent_id": agent_id,
                "metadata_uri": metadata_uri,
                "risk_level": risk_level,
                "description": description,
                "tx_hash": tx_hash,
                "timestamp": int(time.time()),
            }

        except Exception as e:
            raise RegistryError(
                f"Failed to register tool: {str(e)}", "REGISTRATION_FAILED"
            )

    async def is_valid_agent(self, agent_id: str) -> bool:
        """Check if agent is valid and registered"""
        try:
            # In real implementation, this would call the registry contract
            # return await self.registry_contract.functions.isValidAgent(agent_id).call()
            return True  # Simplified for demo
        except Exception:
            return False

    async def is_valid_tool(self, tool_id: str) -> bool:
        """Check if tool is valid and registered"""
        try:
            # In real implementation, this would call the registry contract
            # return await self.registry_contract.functions.isValidTool(tool_id).call()
            return True  # Simplified for demo
        except Exception:
            return False

    async def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent information from registry"""
        try:
            # In real implementation, this would call the registry contract
            # agent_data = await self.registry_contract.functions.getAgent(agent_id).call()

            # Simulate agent data
            return {
                "id": agent_id,
                "operator": "0x1234567890123456789012345678901234567890",
                "metadata_uri": f"ipfs://agent_{agent_id}_metadata",
                "risk_level": 1,
                "description": f"Agent {agent_id}",
                "is_active": True,
                "total_actions": 0,
                "created_at": int(time.time()),
            }
        except Exception:
            return None

    async def get_tool(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """Get tool information from registry"""
        try:
            # In real implementation, this would call the registry contract
            # tool_data = await self.registry_contract.functions.getTool(tool_id).call()

            # Simulate tool data
            return {
                "id": tool_id,
                "agent_id": "default_agent",
                "metadata_uri": f"ipfs://tool_{tool_id}_metadata",
                "risk_level": 1,
                "description": f"Tool {tool_id}",
                "is_active": True,
                "total_uses": 0,
                "created_at": int(time.time()),
            }
        except Exception:
            return None

    async def update_agent_metadata(
        self, agent_id: str, metadata_uri: str, description: str = ""
    ) -> Dict[str, Any]:
        """Update agent metadata"""
        try:
            # In real implementation, this would call the registry contract
            # tx_hash = await self.registry_contract.functions.updateAgentMetadata(
            #     agent_id, metadata_uri, description
            # ).transact()

            # Simulate update
            tx_hash = f"0x{agent_id.encode().hex()[:64]}"

            return {
                "agent_id": agent_id,
                "metadata_uri": metadata_uri,
                "description": description,
                "tx_hash": tx_hash,
                "timestamp": int(time.time()),
            }

        except Exception as e:
            raise RegistryError(
                f"Failed to update agent metadata: {str(e)}", "UPDATE_FAILED"
            )

    async def deactivate_agent(self, agent_id: str) -> Dict[str, Any]:
        """Deactivate an agent"""
        try:
            # In real implementation, this would call the registry contract
            # tx_hash = await self.registry_contract.functions.deactivateAgent(agent_id).transact()

            # Simulate deactivation
            tx_hash = f"0x{agent_id.encode().hex()[:64]}"

            return {
                "agent_id": agent_id,
                "status": "deactivated",
                "tx_hash": tx_hash,
                "timestamp": int(time.time()),
            }

        except Exception as e:
            raise RegistryError(
                f"Failed to deactivate agent: {str(e)}", "DEACTIVATION_FAILED"
            )
