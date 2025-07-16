"""
Tests for Chronicler services
"""

import asyncio
from unittest.mock import Mock, patch

import pytest
from chronicler_client.decorators.types import ActionStatus, AuditResult
from chronicler_client.services import (
    AccessControlError,
    AccessControlService,
    AuditError,
    AuditService,
    ChroniclerError,
    ChroniclerService,
    RegistryError,
    RegistryService,
    ServiceConfig,
)


class TestServiceConfig:
    """Test ServiceConfig class"""

    def test_service_config_defaults(self):
        """Test ServiceConfig default values"""
        config = ServiceConfig()
        assert config.timeout == 30000
        assert config.retry_attempts == 3
        assert config.batch_size == 100
        assert config.ipfs_gateway == "https://ipfs.io"
        assert config.max_concurrent_requests == 10
        assert config.connection_pool_size == 20

    def test_service_config_custom(self):
        """Test ServiceConfig with custom values"""
        config = ServiceConfig(
            timeout=60000,
            retry_attempts=5,
            batch_size=200,
            ipfs_gateway="https://gateway.pinata.cloud",
        )
        assert config.timeout == 60000
        assert config.retry_attempts == 5
        assert config.batch_size == 200
        assert config.ipfs_gateway == "https://gateway.pinata.cloud"


class TestRegistryService:
    """Test RegistryService class"""

    @pytest.fixture
    def registry_service(self):
        """Create a RegistryService instance for testing"""
        mock_config = Mock(
            rpc_url="http://localhost:8545",
            registry_address="0x1234567890123456789012345678901234567890",
            audit_log_address="0x2345678901234567890123456789012345678901",
            access_control_address="0x3456789012345678901234567890123456789012",
        )

        # Patch get_config at the module level where it's imported
        with patch(
            "chronicler_client.config.settings.get_config", return_value=mock_config
        ):
            return RegistryService(config=mock_config)

    @pytest.mark.asyncio
    async def test_register_agent(self, registry_service):
        """Test agent registration"""
        result = await registry_service.register_agent(
            agent_id="test_agent",
            operator="0x1234567890123456789012345678901234567890",
            metadata_uri="ipfs://test_metadata",
        )

        assert result["agent_id"] == "test_agent"
        assert result["operator"] == "0x1234567890123456789012345678901234567890"
        assert result["metadata_uri"] == "ipfs://test_metadata"
        assert "tx_hash" in result
        assert "timestamp" in result

    @pytest.mark.asyncio
    async def test_register_tool(self, registry_service):
        """Test tool registration"""
        result = await registry_service.register_tool(
            tool_id="test_tool",
            agent_id="test_agent",
            metadata_uri="ipfs://test_metadata",
        )

        assert result["tool_id"] == "test_tool"
        assert result["agent_id"] == "test_agent"
        assert result["metadata_uri"] == "ipfs://test_metadata"
        assert "tx_hash" in result
        assert "timestamp" in result

    @pytest.mark.asyncio
    async def test_is_valid_agent(self, registry_service):
        """Test agent validation"""
        result = await registry_service.is_valid_agent("test_agent")
        assert isinstance(result, bool)

    @pytest.mark.asyncio
    async def test_is_valid_tool(self, registry_service):
        """Test tool validation"""
        result = await registry_service.is_valid_tool("test_tool")
        assert isinstance(result, bool)

    @pytest.mark.asyncio
    async def test_get_agent(self, registry_service):
        """Test getting agent info"""
        result = await registry_service.get_agent("test_agent")
        assert result is not None
        assert result["id"] == "test_agent"
        assert "is_active" in result

    @pytest.mark.asyncio
    async def test_get_tool(self, registry_service):
        """Test getting tool info"""
        result = await registry_service.get_tool("test_tool")
        assert result is not None
        assert result["id"] == "test_tool"
        assert "is_active" in result


class TestAuditService:
    """Test AuditService class"""

    @pytest.fixture
    def audit_service(self):
        """Create an AuditService instance for testing"""
        mock_config = Mock(
            rpc_url="http://localhost:8545",
            registry_address="0x1234567890123456789012345678901234567890",
            audit_log_address="0x2345678901234567890123456789012345678901",
            access_control_address="0x3456789012345678901234567890123456789012",
        )

        # Patch get_config at the module level where it's imported
        with patch(
            "chronicler_client.config.settings.get_config", return_value=mock_config
        ):
            return AuditService(config=mock_config)

    @pytest.mark.asyncio
    async def test_log_action(self, audit_service):
        """Test action logging"""
        result = await audit_service.log_action(
            action_id="test_action",
            agent_id="test_agent",
            tool_id="test_tool",
            data_hash="0x1234567890abcdef",
            status="success",
        )

        assert isinstance(result, str)
        assert result.startswith("0x")

    @pytest.mark.asyncio
    async def test_verify_action_in_batch(self, audit_service):
        """Test action verification"""
        result = await audit_service.verify_action_in_batch(
            batch_id="test_batch", action_index=0, merkle_proof=["0x123", "0x456"]
        )

        assert isinstance(result, bool)

    @pytest.mark.asyncio
    async def test_get_action(self, audit_service):
        """Test getting action info"""
        result = await audit_service.get_action("test_action")
        assert result is not None
        assert result["action_id"] == "test_action"
        assert "status" in result

    @pytest.mark.asyncio
    async def test_get_actions_by_agent(self, audit_service):
        """Test getting actions by agent"""
        result = await audit_service.get_actions_by_agent("test_agent")
        assert isinstance(result, list)
        if result:
            assert result[0]["agent_id"] == "test_agent"

    @pytest.mark.asyncio
    async def test_get_actions_by_tool(self, audit_service):
        """Test getting actions by tool"""
        result = await audit_service.get_actions_by_tool("test_tool")
        assert isinstance(result, list)
        if result:
            assert result[0]["tool_id"] == "test_tool"

    @pytest.mark.asyncio
    async def test_create_data_hash(self, audit_service):
        """Test data hash creation"""
        data = {"test": "data", "number": 123}
        result = await audit_service.create_data_hash(data)
        assert isinstance(result, str)
        assert result.startswith("0x")

    @pytest.mark.asyncio
    async def test_get_action_statistics(self, audit_service):
        """Test getting action statistics"""
        result = await audit_service.get_action_statistics()
        assert isinstance(result, dict)
        assert "total_actions" in result
        assert "successful_actions" in result


class TestAccessControlService:
    """Test AccessControlService class"""

    @pytest.fixture
    def access_control_service(self):
        """Create an AccessControlService instance for testing"""
        mock_config = Mock(
            rpc_url="http://localhost:8545",
            registry_address="0x1234567890123456789012345678901234567890",
            audit_log_address="0x2345678901234567890123456789012345678901",
            access_control_address="0x3456789012345678901234567890123456789012",
        )

        # Patch get_config at the module level where it's imported
        with patch(
            "chronicler_client.config.settings.get_config", return_value=mock_config
        ):
            return AccessControlService(config=mock_config)

    @pytest.mark.asyncio
    async def test_check_action_allowed(self, access_control_service):
        """Test action permission check"""
        is_allowed, reason = await access_control_service.check_action_allowed(
            agent_id="test_agent", tool_id="test_tool"
        )

        assert isinstance(is_allowed, bool)
        assert reason is None or isinstance(reason, str)

    @pytest.mark.asyncio
    async def test_get_agent_policy(self, access_control_service):
        """Test getting agent policy"""
        result = await access_control_service.get_agent_policy("test_agent")
        assert result is not None
        assert result["agent_id"] == "test_agent"
        assert "max_gas_per_action" in result

    @pytest.mark.asyncio
    async def test_get_tool_policy(self, access_control_service):
        """Test getting tool policy"""
        result = await access_control_service.get_tool_policy("test_tool")
        assert result is not None
        assert result["tool_id"] == "test_tool"
        assert "max_gas_per_action" in result

    @pytest.mark.asyncio
    async def test_set_agent_policy(self, access_control_service):
        """Test setting agent policy"""
        result = await access_control_service.set_agent_policy(
            agent_id="test_agent",
            max_gas_per_action=1000000,
            max_actions_per_hour=1000,
            max_actions_per_day=10000,
            allowed_tools=["tool1", "tool2"],
            risk_level=1,
        )

        assert result["agent_id"] == "test_agent"
        assert result["max_gas_per_action"] == 1000000
        assert "tx_hash" in result

    @pytest.mark.asyncio
    async def test_set_tool_policy(self, access_control_service):
        """Test setting tool policy"""
        result = await access_control_service.set_tool_policy(
            tool_id="test_tool",
            max_gas_per_action=500000,
            max_actions_per_hour=500,
            max_actions_per_day=5000,
            allowed_agents=["agent1", "agent2"],
            risk_level=2,
        )

        assert result["tool_id"] == "test_tool"
        assert result["max_gas_per_action"] == 500000
        assert "tx_hash" in result

    @pytest.mark.asyncio
    async def test_get_usage_statistics(self, access_control_service):
        """Test getting usage statistics"""
        result = await access_control_service.get_usage_statistics()
        assert isinstance(result, dict)
        assert "total_actions" in result
        assert "total_gas_used" in result

    @pytest.mark.asyncio
    async def test_check_rate_limit(self, access_control_service):
        """Test rate limit check"""
        is_within_limit, reason = await access_control_service.check_rate_limit(
            agent_id="test_agent", tool_id="test_tool"
        )

        assert isinstance(is_within_limit, bool)
        assert reason is None or isinstance(reason, str)


class TestChroniclerService:
    """Test ChroniclerService class"""

    @pytest.fixture
    def chronicler_service(self):
        """Create a ChroniclerService instance for testing"""
        mock_config = Mock(
            rpc_url="http://localhost:8545",
            registry_address="0x1234567890123456789012345678901234567890",
            audit_log_address="0x2345678901234567890123456789012345678901",
            access_control_address="0x3456789012345678901234567890123456789012",
        )

        # Patch get_config at the module level where it's imported
        with patch(
            "chronicler_client.config.settings.get_config", return_value=mock_config
        ):
            return ChroniclerService(config=mock_config)

    @pytest.mark.asyncio
    async def test_log_action(self, chronicler_service):
        """Test action logging"""
        result = await chronicler_service.log_action(
            action_id="test_action",
            agent_id="test_agent",
            tool_id="test_tool",
            input_data={"test": "input"},
            output_data={"test": "output"},
            status="success",
        )

        assert isinstance(result, AuditResult)
        assert result.action_id == "test_action"
        assert result.status in [ActionStatus.SUCCESS, ActionStatus.FAILED]

    @pytest.mark.asyncio
    async def test_check_access(self, chronicler_service):
        """Test access check"""
        result = await chronicler_service.check_access("test_agent", "test_tool")
        assert isinstance(result, bool)

    @pytest.mark.asyncio
    async def test_get_agent_info(self, chronicler_service):
        """Test getting agent info"""
        result = await chronicler_service.get_agent_info("test_agent")
        assert result is None or isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_get_tool_info(self, chronicler_service):
        """Test getting tool info"""
        result = await chronicler_service.get_tool_info("test_tool")
        assert result is None or isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_get_action_statistics(self, chronicler_service):
        """Test getting action statistics"""
        result = await chronicler_service.get_action_statistics()
        assert isinstance(result, dict)
        assert "total_actions" in result

    @pytest.mark.asyncio
    async def test_get_usage_statistics(self, chronicler_service):
        """Test getting usage statistics"""
        result = await chronicler_service.get_usage_statistics()
        assert isinstance(result, dict)
        assert "total_actions" in result


class TestExceptions:
    """Test exception classes"""

    def test_chronicler_error(self):
        """Test ChroniclerError"""
        error = ChroniclerError("Test error", "TEST_CODE")
        assert error.message == "Test error"
        assert error.code == "TEST_CODE"
        assert str(error) == "Test error"

    def test_registry_error(self):
        """Test RegistryError"""
        error = RegistryError("Registry error", "REGISTRY_CODE")
        assert error.message == "Registry error"
        assert error.code == "REGISTRY_CODE"
        assert isinstance(error, ChroniclerError)

    def test_audit_error(self):
        """Test AuditError"""
        error = AuditError("Audit error", "AUDIT_CODE")
        assert error.message == "Audit error"
        assert error.code == "AUDIT_CODE"
        assert isinstance(error, ChroniclerError)

    def test_access_control_error(self):
        """Test AccessControlError"""
        error = AccessControlError("Access control error", "ACCESS_CODE")
        assert error.message == "Access control error"
        assert error.code == "ACCESS_CODE"
        assert isinstance(error, ChroniclerError)
