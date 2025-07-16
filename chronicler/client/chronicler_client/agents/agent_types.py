"""
Agent types and capabilities for the Chronicler agent system
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class AgentType(str, Enum):
    """Types of agents supported by the system"""

    GENERAL = "general"
    SPECIALIZED = "specialized"
    MCP = "mcp"
    AUDIT = "audit"
    REGISTRY = "registry"
    ACCESS_CONTROL = "access_control"


class AgentCapability(str, Enum):
    """Capabilities that agents can have"""

    TEXT_GENERATION = "text_generation"
    CODE_GENERATION = "code_generation"
    DATA_ANALYSIS = "data_analysis"
    FILE_OPERATIONS = "file_operations"
    WEB_SEARCH = "web_search"
    BLOCKCHAIN_INTERACTION = "blockchain_interaction"
    AUDIT_LOGGING = "audit_logging"
    ACCESS_CONTROL = "access_control"
    REGISTRY_MANAGEMENT = "registry_management"
    MCP_PROTOCOL = "mcp_protocol"


class AgentMetadata(BaseModel):
    """Metadata for an agent"""

    agent_id: str
    name: str
    description: str
    version: str = "1.0.0"
    agent_type: AgentType
    capabilities: List[AgentCapability]
    model_name: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    risk_level: int = 1
    tags: List[str] = []
    metadata: Dict[str, Any] = {}


class AgentStatus(str, Enum):
    """Status of an agent"""

    IDLE = "idle"
    RUNNING = "running"
    ERROR = "error"
    DISABLED = "disabled"
    REGISTERING = "registering"
