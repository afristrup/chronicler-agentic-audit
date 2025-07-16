"""
Chronicler decorator for DSPy integration with blockchain layer
"""

import functools
import hashlib
import json
import time
import uuid
from typing import Any, Callable, Optional

from web3 import Web3

from .types import ActionMetadata, ActionStatus, AuditConfig, AuditResult


class ChroniclerClient:
    """Client for interacting with the Chronicler layer"""

    def __init__(
        self,
        rpc_url: str,
        registry_address: str,
        audit_log_address: str,
        access_control_address: str,
    ):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.registry_address = registry_address
        self.audit_log_address = audit_log_address
        self.access_control_address = access_control_address

    def log_action(
        self,
        action_id: str,
        metadata: ActionMetadata,
        input_data: Any,
        output_data: Any,
    ) -> AuditResult:
        """Log an action to the blockchain"""
        try:
            # Create action data hash
            action_data = {
                "action_id": action_id,
                "agent_id": metadata.agent_id,
                "tool_id": metadata.tool_id,
                "input": input_data,
                "output": output_data,
                "metadata": metadata.model_dump(),
                "timestamp": int(time.time()),
            }

            _data_hash = hashlib.sha256(
                json.dumps(action_data, sort_keys=True).encode()
            ).hexdigest()

            # Simulate blockchain interaction (in real implementation, this would call smart contracts)
            tx_hash = f"0x{hashlib.sha256(action_id.encode()).hexdigest()[:64]}"

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


def chronicler(
    agent_id: str,
    tool_id: str,
    config: Optional[AuditConfig] = None,
    metadata: Optional[ActionMetadata] = None,
):
    """
    DSPy decorator for integrating with Chronicler layer

    Args:
        agent_id: Unique identifier for the agent
        tool_id: Unique identifier for the tool being used
        config: Audit configuration
        metadata: Additional action metadata
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Initialize configuration
            audit_config = config or AuditConfig()
            action_metadata = metadata or ActionMetadata(
                agent_id=agent_id, tool_id=tool_id
            )

            # Generate unique action ID
            action_id = str(uuid.uuid4())

            # Capture input data if enabled
            input_data = None
            if audit_config.log_input:
                input_data = {"args": args, "kwargs": kwargs}

            # Execute the function
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time

                # Capture output data if enabled
                output_data = None
                if audit_config.log_output:
                    output_data = result

                # Log to blockchain if enabled
                if audit_config.enabled:
                    # Initialize client (in real implementation, this would be configured)
                    client = ChroniclerClient(
                        rpc_url="http://localhost:8545",
                        registry_address="0x...",
                        audit_log_address="0x...",
                        access_control_address="0x...",
                    )

                    audit_result = client.log_action(
                        action_id, action_metadata, input_data, output_data
                    )

                    # Add audit info to result if it's a DSPy object
                    if hasattr(result, "__dict__"):
                        result._audit_info = {
                            "action_id": action_id,
                            "execution_time": execution_time,
                            "audit_result": audit_result.model_dump(),
                        }

                return result

            except Exception as e:
                execution_time = time.time() - start_time

                # Log failure if enabled
                if audit_config.enabled:
                    client = ChroniclerClient(
                        rpc_url="http://localhost:8545",
                        registry_address="0x...",
                        audit_log_address="0x...",
                        access_control_address="0x...",
                    )

                    audit_result = client.log_action(
                        action_id, action_metadata, input_data, {"error": str(e)}
                    )

                raise e

        return wrapper

    return decorator
