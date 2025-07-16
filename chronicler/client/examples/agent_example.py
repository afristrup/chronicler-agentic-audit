#!/usr/bin/env python3
"""
Example script demonstrating Chronicler Agents with MCP integration
"""

import asyncio
import logging
import os
import sys
from typing import Any, Dict

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chronicler_client.agents import (
    AgentCapability,
    AgentManager,
    AgentManagerConfig,
    AgentType,
    create_and_register_chronicler_agent,
    create_and_register_mcp_agent,
    create_chronicler_agent,
    create_mcp_agent,
)
from chronicler_client.agents.mcp_server import create_mcp_server


async def example_basic_agents():
    """Example of basic agent usage"""
    print("=== Basic Agent Example ===\n")

    # Create agent manager
    manager_config = AgentManagerConfig(
        enable_auto_registration=True,
        enable_health_checks=True,
        health_check_interval=30,
        log_level="INFO",
    )

    manager = AgentManager(manager_config)

    try:
        # Create and register a Chronicler agent
        chronicler_agent = await create_and_register_chronicler_agent(
            manager=manager,
            agent_id="example_chronicler",
            name="Example Chronicler Agent",
            description="Example agent for blockchain operations",
            capabilities=[
                AgentCapability.BLOCKCHAIN_INTERACTION,
                AgentCapability.AUDIT_LOGGING,
                AgentCapability.ACCESS_CONTROL,
            ],
        )

        if chronicler_agent:
            print(f"✅ Created Chronicler agent: {chronicler_agent.agent_id}")

        # Execute a blockchain audit request
        audit_request = {
            "action_type": "audit",
            "action_data": {
                "agent_id": "example_user",
                "tool_id": "example_tool",
                "data": {"message": "Hello, blockchain!"},
            },
        }

        print("\n🔍 Executing audit request...")
        response = await manager.execute_request("example_chronicler", audit_request)

        if response:
            print(f"✅ Audit completed:")
            print(f"   Request ID: {response.request_id}")
            print(f"   Status: {response.status}")
            print(f"   Execution time: {response.execution_time:.3f}s")
            print(f"   Output: {response.output_data}")

        # Get agent statistics
        stats = await manager.get_manager_stats()
        print(f"\n📊 Manager Statistics:")
        print(f"   Total agents: {stats.total_agents}")
        print(f"   Total requests: {stats.total_requests}")
        print(f"   Average response time: {stats.avg_response_time:.3f}s")

    finally:
        await manager.shutdown()


async def example_mcp_integration():
    """Example of MCP agent integration"""
    print("\n=== MCP Integration Example ===\n")

    # Note: This example requires an MCP server to be running
    # You would typically connect to an existing MCP server

    manager_config = AgentManagerConfig(enable_auto_registration=True, log_level="INFO")

    manager = AgentManager(manager_config)

    try:
        # Example MCP agent (requires MCP server URL)
        # Uncomment and configure when you have an MCP server running

        """
        mcp_agent = await create_and_register_mcp_agent(
            manager=manager,
            agent_id="example_mcp",
            name="Example MCP Agent",
            description="Example agent for MCP operations",
            mcp_server_url="http://localhost:8000",  # Your MCP server URL
            capabilities=[
                AgentCapability.MCP_PROTOCOL,
                AgentCapability.TEXT_GENERATION,
                AgentCapability.CODE_GENERATION,
            ]
        )

        if mcp_agent:
            print(f"✅ Created MCP agent: {mcp_agent.agent_id}")

            # List available tools
            tools = await mcp_agent.list_available_tools()
            print(f"📋 Available MCP tools: {len(tools)}")

            # Execute a text generation request
            text_request = {
                "prompt": "Write a Python function to calculate fibonacci numbers",
                "model": "gpt-4",
                "tools": []  # No specific tools required
            }

            print("\n🤖 Executing text generation request...")
            response = await manager.execute_request(
                "example_mcp",
                text_request
            )

            if response:
                print(f"✅ Text generation completed:")
                print(f"   Status: {response.status}")
                print(f"   Content: {response.output_data.get('content', 'No content')}")
        """

        print("ℹ️  MCP integration example requires a running MCP server")
        print("   Configure the MCP server URL and uncomment the code above")

    finally:
        await manager.shutdown()


async def example_agent_capabilities():
    """Example of using agent capabilities"""
    print("\n=== Agent Capabilities Example ===\n")

    manager_config = AgentManagerConfig(enable_auto_registration=True, log_level="INFO")

    manager = AgentManager(manager_config)

    try:
        # Create multiple agents with different capabilities
        agents_to_create = [
            {
                "agent_id": "audit_agent",
                "name": "Audit Agent",
                "description": "Specialized for audit operations",
                "capabilities": [AgentCapability.AUDIT_LOGGING],
            },
            {
                "agent_id": "registry_agent",
                "name": "Registry Agent",
                "description": "Specialized for registry operations",
                "capabilities": [AgentCapability.REGISTRY_MANAGEMENT],
            },
            {
                "agent_id": "access_agent",
                "name": "Access Control Agent",
                "description": "Specialized for access control",
                "capabilities": [AgentCapability.ACCESS_CONTROL],
            },
        ]

        for agent_config in agents_to_create:
            agent = await create_and_register_chronicler_agent(
                manager=manager, **agent_config
            )
            if agent:
                print(f"✅ Created {agent_config['name']}: {agent.agent_id}")

        # Find agent by capability
        print("\n🔍 Finding agents by capability...")

        audit_agent_id = await manager.find_agent_by_capability(
            AgentCapability.AUDIT_LOGGING
        )
        if audit_agent_id:
            print(f"   Audit agent found: {audit_agent_id}")

        registry_agent_id = await manager.find_agent_by_capability(
            AgentCapability.REGISTRY_MANAGEMENT
        )
        if registry_agent_id:
            print(f"   Registry agent found: {registry_agent_id}")

        # Execute request using capability
        print("\n🚀 Executing request using capability...")

        audit_request = {
            "action_type": "audit",
            "action_data": {
                "agent_id": "test_user",
                "tool_id": "test_tool",
                "data": {"test": "data"},
            },
        }

        response = await manager.execute_with_capability(
            AgentCapability.AUDIT_LOGGING, audit_request
        )

        if response:
            print(f"✅ Capability-based execution completed:")
            print(f"   Agent used: {response.agent_id}")
            print(f"   Status: {response.status}")
            print(f"   Execution time: {response.execution_time:.3f}s")

        # Get all agent metadata
        print("\n📋 All registered agents:")
        metadata = await manager.get_all_agent_metadata()
        for agent_id, meta in metadata.items():
            print(f"   {agent_id}: {meta.name} ({meta.agent_type})")
            print(f"     Capabilities: {[cap.value for cap in meta.capabilities]}")

    finally:
        await manager.shutdown()


async def example_mcp_server():
    """Example of running the MCP server"""
    print("\n=== MCP Server Example ===\n")

    # Create MCP server
    server_config = AgentManagerConfig(
        mcp_enabled=True,
        mcp_server_host="localhost",
        mcp_server_port=8000,
        enable_auto_registration=True,
        log_level="INFO",
    )

    server = create_mcp_server(server_config)

    print("🚀 Starting MCP server...")
    print(f"   Host: {server.config.mcp_server_host}")
    print(f"   Port: {server.config.mcp_server_port}")
    print("   API Documentation: http://localhost:8000/docs")

    # Start the server (this would normally run indefinitely)
    # For this example, we'll just show the configuration

    print("\n📋 Available MCP tools:")
    for tool in server.mcp_tools:
        print(f"   {tool['name']}: {tool['description']}")

    print("\n🔗 Example API endpoints:")
    print("   GET  /health - Server health check")
    print("   GET  /agents - List all agents")
    print("   POST /agents/execute - Execute agent request")
    print("   POST /agents/register - Register new agent")
    print("   GET  /stats - Get manager statistics")

    print("\nℹ️  To run the server, use:")
    print("   python -m chronicler_client.agents.mcp_server")

    # Example of how to use the server programmatically
    print("\n💡 Example client usage:")
    print("""
    import httpx

    # Execute agent request
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/agents/execute",
            json={
                "agent_id": "example_chronicler",
                "input_data": {
                    "action_type": "audit",
                    "action_data": {"test": "data"}
                }
            }
        )
        result = response.json()
        print(result)
    """)


async def main():
    """Main example function"""
    print("🤖 Chronicler Agents with MCP Integration Examples")
    print("=" * 50)

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    try:
        # Run examples
        await example_basic_agents()
        await example_mcp_integration()
        await example_agent_capabilities()
        await example_mcp_server()

        print("\n✅ All examples completed successfully!")

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        logging.exception("Example error")


if __name__ == "__main__":
    asyncio.run(main())
