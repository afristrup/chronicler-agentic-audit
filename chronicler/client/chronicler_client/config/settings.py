"""
Settings and configuration for Chronicler Python client using Pydantic
"""

import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator

# Load environment variables
load_dotenv()


class ChroniclerConfig(BaseModel):
    """Configuration for Chronicler client using Pydantic"""

    # Network configuration
    chain_id: int = Field(default=int(os.getenv("CHAIN_ID", "1")))
    rpc_url: str = Field(default=os.getenv("RPC_URL", "http://localhost:8545"))

    # Contract addresses
    registry_address: str = Field(default=os.getenv("REGISTRY_ADDRESS", ""))
    audit_log_address: str = Field(default=os.getenv("AUDIT_LOG_ADDRESS", ""))
    access_control_address: str = Field(default=os.getenv("ACCESS_CONTROL_ADDRESS", ""))

    # Database configuration
    supabase_url: Optional[str] = Field(default=os.getenv("SUPABASE_URL"))
    supabase_key: Optional[str] = Field(default=os.getenv("SUPABASE_KEY"))

    # Service configuration
    ipfs_gateway: str = Field(default=os.getenv("IPFS_GATEWAY", "https://ipfs.io"))
    dashboard_port: int = Field(default=int(os.getenv("DASHBOARD_PORT", "3000")))

    # Audit configuration
    audit_enabled: bool = Field(
        default=os.getenv("AUDIT_ENABLED", "true").lower() == "true"
    )
    log_input: bool = Field(default=os.getenv("LOG_INPUT", "true").lower() == "true")
    log_output: bool = Field(default=os.getenv("LOG_OUTPUT", "true").lower() == "true")
    batch_size: int = Field(default=int(os.getenv("BATCH_SIZE", "100")))
    timeout: int = Field(default=int(os.getenv("TIMEOUT", "30000")))

    @validator("registry_address", "audit_log_address", "access_control_address")
    def validate_contract_addresses(cls, v, values):
        """Validate that required contract addresses are present"""
        if not v:
            raise ValueError("Contract address is required")
        return v

    def validate_config(self) -> bool:
        """Validate that required configuration is present"""
        if not self.registry_address:
            raise ValueError("REGISTRY_ADDRESS is required")
        if not self.audit_log_address:
            raise ValueError("AUDIT_LOG_ADDRESS is required")
        if not self.access_control_address:
            raise ValueError("ACCESS_CONTROL_ADDRESS is required")
        return True


# Global configuration instance
_config: Optional[ChroniclerConfig] = None


def get_config() -> ChroniclerConfig:
    """Get the global configuration instance"""
    global _config
    if _config is None:
        _config = ChroniclerConfig()
        _config.validate_config()
    return _config


def set_config(config: ChroniclerConfig) -> None:
    """Set the global configuration instance"""
    global _config
    config.validate_config()
    _config = config
