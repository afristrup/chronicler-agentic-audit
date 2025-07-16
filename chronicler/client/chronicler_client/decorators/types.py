"""
Type definitions for Chronicler decorators using Pydantic
"""

from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ActionStatus(str, Enum):
    """Status of an action in the audit log"""

    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ActionMetadata(BaseModel):
    """Metadata for an action being audited"""

    agent_id: str
    tool_id: str
    category_id: Optional[str] = None
    risk_level: Optional[int] = None
    description: Optional[str] = None
    tags: Dict[str, Any] = Field(default_factory=dict)
    custom_data: Dict[str, Any] = Field(default_factory=dict)


class AuditConfig(BaseModel):
    """Configuration for audit logging"""

    enabled: bool = True
    log_input: bool = True
    log_output: bool = True
    log_metadata: bool = True
    batch_size: int = 100
    ipfs_gateway: str = "https://ipfs.io"
    timeout: int = 30000
    retry_attempts: int = 3


class AuditResult(BaseModel):
    """Result of an audit operation"""

    action_id: str
    status: ActionStatus
    tx_hash: Optional[str] = None
    gas_used: Optional[int] = None
    error_message: Optional[str] = None
    timestamp: Optional[int] = None
