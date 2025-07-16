"""
Configuration for Chronicler agents
"""

import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from .agent_types import AgentCapability, AgentType

# Load environment variables
load_dotenv()


class AgentConfig(BaseModel):
    """Configuration for an individual agent"""

    # Basic agent info
    agent_id: str
    name: str
    description: str
    agent_type: AgentType
    capabilities: List[AgentCapability]

    # Model configuration
    model_name: Optional[str] = Field(default=os.getenv("DEFAULT_MODEL", "gpt-4"))
    max_tokens: Optional[int] = Field(default=int(os.getenv("MAX_TOKENS", "4096")))
    temperature: Optional[float] = Field(default=float(os.getenv("TEMPERATURE", "0.7")))

    # Chronicler integration
    audit_enabled: bool = Field(default=True)
    log_input: bool = Field(default=True)
    log_output: bool = Field(default=True)
    risk_level: int = Field(default=1, ge=1, le=5)

    # MCP configuration
    mcp_enabled: bool = Field(default=False)
    mcp_server_url: Optional[str] = Field(default=os.getenv("MCP_SERVER_URL"))
    mcp_api_key: Optional[str] = Field(default=os.getenv("MCP_API_KEY"))

    # Performance settings
    timeout: int = Field(default=int(os.getenv("AGENT_TIMEOUT", "300")))
    retry_attempts: int = Field(default=int(os.getenv("RETRY_ATTEMPTS", "3")))
    batch_size: int = Field(default=int(os.getenv("BATCH_SIZE", "10")))

    # Advanced settings
    enable_streaming: bool = Field(default=False)
    enable_caching: bool = Field(default=True)
    cache_ttl: int = Field(default=int(os.getenv("CACHE_TTL", "3600")))

    # Custom settings
    custom_settings: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = "allow"


class AgentManagerConfig(BaseModel):
    """Configuration for the agent manager"""

    # Manager settings
    max_concurrent_agents: int = Field(
        default=int(os.getenv("MAX_CONCURRENT_AGENTS", "10"))
    )
    agent_timeout: int = Field(default=int(os.getenv("AGENT_TIMEOUT", "300")))
    enable_auto_registration: bool = Field(default=True)
    enable_health_checks: bool = Field(default=True)
    health_check_interval: int = Field(
        default=int(os.getenv("HEALTH_CHECK_INTERVAL", "60"))
    )

    # Storage settings
    storage_type: str = Field(default=os.getenv("STORAGE_TYPE", "memory"))
    storage_config: Dict[str, Any] = Field(default_factory=dict)

    # Logging settings
    log_level: str = Field(default=os.getenv("LOG_LEVEL", "INFO"))
    enable_structured_logging: bool = Field(default=True)

    # MCP settings
    mcp_enabled: bool = Field(default=True)
    mcp_server_port: int = Field(default=int(os.getenv("MCP_SERVER_PORT", "8000")))
    mcp_server_host: str = Field(default=os.getenv("MCP_SERVER_HOST", "localhost"))

    class Config:
        extra = "allow"
