"""
Service configuration for Chronicler services
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ServiceConfig(BaseModel):
    """Configuration for Chronicler services"""

    timeout: int = Field(default=30000, description="Request timeout in milliseconds")
    retry_attempts: int = Field(default=3, description="Number of retry attempts")
    batch_size: int = Field(default=100, description="Batch size for processing")
    ipfs_gateway: str = Field(default="https://ipfs.io", description="IPFS gateway URL")

    # Optional configuration
    max_concurrent_requests: int = Field(
        default=10, description="Maximum concurrent requests"
    )
    connection_pool_size: int = Field(default=20, description="Connection pool size")

    # Validation
    @field_validator("timeout")
    @classmethod
    def validate_timeout(cls, v):
        if v <= 0:
            raise ValueError("Timeout must be positive")
        return v

    @field_validator("retry_attempts")
    @classmethod
    def validate_retry_attempts(cls, v):
        if v < 0:
            raise ValueError("Retry attempts must be non-negative")
        return v

    @field_validator("batch_size")
    @classmethod
    def validate_batch_size(cls, v):
        if v <= 0:
            raise ValueError("Batch size must be positive")
        return v
