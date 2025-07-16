"""
Tests for Chronicler Agents
"""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest
from chronicler_client.agents import (
    AgentCapability,
    AgentConfig,
    AgentManager,
    AgentManagerConfig,
    AgentRequest,
    AgentResponse,
    AgentStatus,
    AgentType,
    BaseAgent,
)
from chronicler_client.agents.agent_manager import create_and_register_chronicler_agent
from chronicler_client.agents.chronicler_agent import (
    ChroniclerAgent,
    create_chronicler_agent,
)
from chronicler_client.agents.mcp_agent import MCPAgent, create_mcp_agent


class TestAgentConfig:
    """Test AgentConfig class"""

    def test_agent_config_defaults(self):
        """Test agent config with defaults"""
        config = AgentConfig(
            agent_id="test_agent",
            name="Test Agent",
            description="Test description",
            agent_type=AgentType.GENERAL,
            capabilities=[AgentCapability.TEXT_GENERATION],
        )

        assert config.agent_id == "test_agent"
        assert config.name == "Test Agent"
        assert config.description == "Test description"
        assert config.agent_type == AgentType.GENERAL
        assert config.capabilities == [AgentCapability.TEXT_GENERATION]
        assert config.audit_enabled is True
        assert config.log_input is True
        assert config.log_output is True

    def test_agent_config_custom(self):
        """Test agent config with custom values"""
        config = AgentConfig(
            agent_id="custom_agent",
            name="Custom Agent",
            description="Custom description",
            agent_type=AgentType.AUDIT,
            capabilities=[
                AgentCapability.AUDIT_LOGGING,
                AgentCapability.BLOCKCHAIN_INTERACTION,
            ],
            audit_enabled=False,
            log_input=False,
            log_output=False,
            risk_level=3,
        )

        assert config.agent_id == "custom_agent"
        assert config.agent_type == AgentType.AUDIT
        assert len(config.capabilities) == 2
        assert config.audit_enabled is False
        assert config.log_input is False
        assert config.log_output is False
        assert config.risk_level == 3


class TestAgentManagerConfig:
    """Test AgentManagerConfig class"""

    def test_manager_config_defaults(self):
        """Test manager config with defaults"""
        config = AgentManagerConfig()

        assert config.max_concurrent_agents == 10
        assert config.enable_auto_registration is True
        assert config.enable_health_checks is True
        assert config.mcp_enabled is True
        assert config.mcp_server_port == 8000

    def test_manager_config_custom(self):
        """Test manager config with custom values"""
        config = AgentManagerConfig(
            max_concurrent_agents=5,
            enable_auto_registration=False,
            enable_health_checks=False,
            mcp_enabled=False,
            mcp_server_port=9000,
        )

        assert config.max_concurrent_agents == 5
        assert config.enable_auto_registration is False
        assert config.enable_health_checks is False
        assert config.mcp_enabled is False
        assert config.mcp_server_port == 9000


class TestAgentManager:
    """Test AgentManager class"""

    @pytest.fixture
    def agent_manager(self):
        """Create an AgentManager instance for testing"""
        config = AgentManagerConfig(
            enable_health_checks=False,  # Disable for testing
            log_level="DEBUG",
        )
        return AgentManager(config)

    @pytest.fixture
    def mock_agent(self):
        """Create a mock agent for testing"""
        agent = Mock(spec=BaseAgent)
        agent.agent_id = "test_agent"
        agent.agent_type = AgentType.GENERAL
        agent.capabilities = [AgentCapability.TEXT_GENERATION]
        agent.status = AgentStatus.IDLE
        agent.execute = AsyncMock()
        agent.get_health_status = Mock(return_value={"status": "idle"})
        agent.get_metadata = Mock(return_value=Mock())
        agent.shutdown = AsyncMock()
        return agent

    @pytest.mark.asyncio
    async def test_register_agent(self, agent_manager, mock_agent):
        """Test agent registration"""
        success = await agent_manager.register_agent(mock_agent)

        assert success is True
        assert "test_agent" in agent_manager.agents
        assert agent_manager.agents["test_agent"] == mock_agent

    @pytest.mark.asyncio
    async def test_register_duplicate_agent(self, agent_manager, mock_agent):
        """Test registering duplicate agent"""
        # Register first time
        await agent_manager.register_agent(mock_agent)

        # Try to register again
        success = await agent_manager.register_agent(mock_agent)

        assert success is False

    @pytest.mark.asyncio
    async def test_unregister_agent(self, agent_manager, mock_agent):
        """Test agent unregistration"""
        # Register agent
        await agent_manager.register_agent(mock_agent)

        # Unregister agent
        success = await agent_manager.unregister_agent("test_agent")

        assert success is True
        assert "test_agent" not in agent_manager.agents

    @pytest.mark.asyncio
    async def test_unregister_nonexistent_agent(self, agent_manager):
        """Test unregistering nonexistent agent"""
        success = await agent_manager.unregister_agent("nonexistent")

        assert success is False

    @pytest.mark.asyncio
    async def test_execute_request(self, agent_manager, mock_agent):
        """Test executing request on agent"""
        # Register agent
        await agent_manager.register_agent(mock_agent)

        # Mock response
        mock_response = AgentResponse(
            request_id="test_request",
            agent_id="test_agent",
            output_data={"result": "success"},
            status="success",
            execution_time=0.1,
        )
        mock_agent.execute.return_value = mock_response

        # Execute request
        response = await agent_manager.execute_request("test_agent", {"test": "data"})

        assert response is not None
        assert response.request_id == "test_request"
        assert response.status == "success"
        assert response.output_data == {"result": "success"}

    @pytest.mark.asyncio
    async def test_execute_request_nonexistent_agent(self, agent_manager):
        """Test executing request on nonexistent agent"""
        response = await agent_manager.execute_request("nonexistent", {"test": "data"})

        assert response is None

    @pytest.mark.asyncio
    async def test_find_agent_by_capability(self, agent_manager, mock_agent):
        """Test finding agent by capability"""
        # Register agent
        await agent_manager.register_agent(mock_agent)

        # Find agent
        agent_id = await agent_manager.find_agent_by_capability(
            AgentCapability.TEXT_GENERATION
        )

        assert agent_id == "test_agent"

    @pytest.mark.asyncio
    async def test_find_agent_by_capability_not_found(self, agent_manager):
        """Test finding agent by capability when not found"""
        agent_id = await agent_manager.find_agent_by_capability(
            AgentCapability.TEXT_GENERATION
        )

        assert agent_id is None

    @pytest.mark.asyncio
    async def test_get_manager_stats(self, agent_manager, mock_agent):
        """Test getting manager statistics"""
        # Register agent
        await agent_manager.register_agent(mock_agent)

        # Get stats
        stats = await agent_manager.get_manager_stats()

        assert stats.total_agents == 1
        assert stats.idle_agents == 1
        assert stats.total_requests == 0

    @pytest.mark.asyncio
    async def test_shutdown(self, agent_manager, mock_agent):
        """Test manager shutdown"""
        # Register agent
        await agent_manager.register_agent(mock_agent)

        # Shutdown manager
        await agent_manager.shutdown()

        # Verify agent was shut down
        mock_agent.shutdown.assert_called_once()


class TestChroniclerAgent:
    """Test ChroniclerAgent class"""

    @pytest.fixture
    def agent_config(self):
        """Create agent config for testing"""
        return AgentConfig(
            agent_id="test_chronicler",
            name="Test Chronicler Agent",
            description="Test description",
            agent_type=AgentType.AUDIT,
            capabilities=[
                AgentCapability.AUDIT_LOGGING,
                AgentCapability.BLOCKCHAIN_INTERACTION,
            ],
        )

    @pytest.fixture
    def chronicler_agent(self, agent_config):
        """Create a ChroniclerAgent instance for testing"""
        with patch("chronicler_client.agents.chronicler_agent.ChroniclerService"):
            with patch("chronicler_client.agents.chronicler_agent.RegistryService"):
                with patch("chronicler_client.agents.chronicler_agent.AuditService"):
                    with patch(
                        "chronicler_client.agents.chronicler_agent.AccessControlService"
                    ):
                        return ChroniclerAgent(agent_config)

    def test_chronicler_agent_creation(self, chronicler_agent):
        """Test ChroniclerAgent creation"""
        assert chronicler_agent.agent_id == "test_chronicler"
        assert chronicler_agent.name == "Test Chronicler Agent"
        assert chronicler_agent.agent_type == AgentType.AUDIT
        assert len(chronicler_agent.capabilities) == 2

    @pytest.mark.asyncio
    async def test_process_audit_request(self, chronicler_agent):
        """Test processing audit request"""
        request = AgentRequest(
            request_id="test_request",
            agent_id="test_chronicler",
            input_data={
                "action_type": "audit",
                "action_data": {
                    "agent_id": "test_user",
                    "tool_id": "test_tool",
                    "data": {"test": "data"},
                },
            },
        )

        # Mock the audit service methods
        chronicler_agent.audit_service.create_data_hash = AsyncMock(
            return_value="test_hash"
        )
        chronicler_agent.audit_service.log_action = AsyncMock(
            return_value="test_tx_hash"
        )
        chronicler_agent.audit_service.get_action = AsyncMock(
            return_value={"action_id": "test_request"}
        )

        response = await chronicler_agent.process_request(request)

        assert response is not None
        assert response.request_id == "test_request"
        assert response.status == "success"

    @pytest.mark.asyncio
    async def test_get_blockchain_stats(self, chronicler_agent):
        """Test getting blockchain stats"""
        # Mock the service methods
        chronicler_agent.audit_service.get_action_statistics = AsyncMock(
            return_value={"total": 100}
        )
        chronicler_agent.access_control_service.get_usage_statistics = AsyncMock(
            return_value={"usage": 50}
        )

        stats = await chronicler_agent.get_blockchain_stats()

        assert "audit_statistics" in stats
        assert "access_control_statistics" in stats


class TestMCPAgent:
    """Test MCPAgent class"""

    @pytest.fixture
    def mcp_config(self):
        """Create MCP agent config for testing"""
        return AgentConfig(
            agent_id="test_mcp",
            name="Test MCP Agent",
            description="Test MCP description",
            agent_type=AgentType.MCP,
            capabilities=[
                AgentCapability.MCP_PROTOCOL,
                AgentCapability.TEXT_GENERATION,
            ],
            mcp_enabled=True,
            mcp_server_url="http://localhost:8000",
        )

    def test_mcp_agent_creation(self, mcp_config):
        """Test MCPAgent creation"""
        with patch("chronicler_client.agents.mcp_agent.MCPClient"):
            agent = MCPAgent(mcp_config)

            assert agent.agent_id == "test_mcp"
            assert agent.name == "Test MCP Agent"
            assert agent.agent_type == AgentType.MCP
            assert len(agent.capabilities) == 2

    def test_mcp_agent_creation_without_mcp_enabled(self):
        """Test MCPAgent creation without MCP enabled"""
        config = AgentConfig(
            agent_id="test_mcp",
            name="Test MCP Agent",
            description="Test description",
            agent_type=AgentType.MCP,
            capabilities=[AgentCapability.MCP_PROTOCOL],
            mcp_enabled=False,
        )

        with pytest.raises(ValueError, match="MCP must be enabled for MCPAgent"):
            MCPAgent(config)

    def test_mcp_agent_creation_without_server_url(self):
        """Test MCPAgent creation without server URL"""
        config = AgentConfig(
            agent_id="test_mcp",
            name="Test MCP Agent",
            description="Test description",
            agent_type=AgentType.MCP,
            capabilities=[AgentCapability.MCP_PROTOCOL],
            mcp_enabled=True,
            mcp_server_url=None,
        )

        with pytest.raises(ValueError, match="MCP server URL is required for MCPAgent"):
            MCPAgent(config)


class TestFactoryFunctions:
    """Test factory functions"""

    def test_create_chronicler_agent(self):
        """Test create_chronicler_agent factory function"""
        agent = create_chronicler_agent(
            agent_id="factory_test",
            name="Factory Test Agent",
            description="Test factory function",
            capabilities=[AgentCapability.AUDIT_LOGGING],
        )

        assert isinstance(agent, ChroniclerAgent)
        assert agent.agent_id == "factory_test"
        assert agent.name == "Factory Test Agent"
        assert agent.agent_type == AgentType.AUDIT

    def test_create_mcp_agent(self):
        """Test create_mcp_agent factory function"""
        with patch("chronicler_client.agents.mcp_agent.MCPClient"):
            agent = create_mcp_agent(
                agent_id="factory_mcp_test",
                name="Factory MCP Test Agent",
                description="Test MCP factory function",
                mcp_server_url="http://localhost:8000",
                capabilities=[AgentCapability.MCP_PROTOCOL],
            )

            assert isinstance(agent, MCPAgent)
            assert agent.agent_id == "factory_mcp_test"
            assert agent.name == "Factory MCP Test Agent"
            assert agent.agent_type == AgentType.MCP

    @pytest.mark.asyncio
    async def test_create_and_register_chronicler_agent(self):
        """Test create_and_register_chronicler_agent factory function"""
        manager = AgentManager(AgentManagerConfig(enable_health_checks=False))

        try:
            agent = await create_and_register_chronicler_agent(
                manager=manager,
                agent_id="register_test",
                name="Register Test Agent",
                description="Test registration function",
                capabilities=[AgentCapability.AUDIT_LOGGING],
            )

            assert agent is not None
            assert agent.agent_id == "register_test"
            assert "register_test" in manager.agents

        finally:
            await manager.shutdown()


if __name__ == "__main__":
    pytest.main([__file__])
