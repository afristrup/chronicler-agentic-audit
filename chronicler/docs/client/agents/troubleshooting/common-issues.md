# Common Issues and Solutions

Solutions to frequently encountered problems with Chronicler Agents.

## Installation Issues

### Import Error: No module named 'chronicler_client'

**Problem:**
```python
ImportError: No module named 'chronicler_client'
```

**Solutions:**
1. **Check installation:**
   ```bash
   pip list | grep chronicler
   ```

2. **Reinstall package:**
   ```bash
   pip uninstall chronicler-client
   pip install chronicler-client
   ```

3. **Check Python version:**
   ```bash
   python --version  # Should be 3.10+
   ```

4. **Use virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   pip install chronicler-client
   ```

### Missing Dependencies

**Problem:**
```python
ModuleNotFoundError: No module named 'fastapi_mcp'
```

**Solutions:**
1. **Install with extras:**
   ```bash
   pip install chronicler-client[mcp]
   ```

2. **Install manually:**
   ```bash
   pip install fastapi-mcp web3 pydantic
   ```

## Configuration Issues

### REGISTRY_ADDRESS is required

**Problem:**
```
ValueError: REGISTRY_ADDRESS is required
```

**Solutions:**
1. **Set environment variables:**
   ```bash
   export REGISTRY_ADDRESS="0x1234567890123456789012345678901234567890"
   export AUDIT_LOG_ADDRESS="0x2345678901234567890123456789012345678901"
   export ACCESS_CONTROL_ADDRESS="0x3456789012345678901234567890123456789012"
   ```

2. **Use .env file:**
   ```bash
   # .env
   REGISTRY_ADDRESS=0x1234567890123456789012345678901234567890
   AUDIT_LOG_ADDRESS=0x2345678901234567890123456789012345678901
   ACCESS_CONTROL_ADDRESS=0x3456789012345678901234567890123456789012
   ```

3. **Mock configuration for testing:**
   ```python
   with patch("chronicler_client.config.settings.get_config") as mock_config:
       mock_config.return_value = Mock(
           registry_address="0x1234567890123456789012345678901234567890",
           audit_log_address="0x2345678901234567890123456789012345678901",
           access_control_address="0x3456789012345678901234567890123456789012"
       )
   ```

## Agent Issues

### Agent Not Found

**Problem:**
```
Agent 'my_agent' not found
```

**Solutions:**
1. **Check agent registration:**
   ```python
   # List all agents
   metadata = await manager.get_all_agent_metadata()
   print(f"Registered agents: {list(metadata.keys())}")
   ```

2. **Register agent properly:**
   ```python
   # Create and register agent
   agent = await create_and_register_chronicler_agent(
       manager=manager,
       agent_id="my_agent",
       name="My Agent",
       description="Test agent",
       capabilities=[AgentCapability.AUDIT_LOGGING]
   )
   ```

3. **Check agent status:**
   ```python
   status = await manager.get_agent_status("my_agent")
   print(f"Agent status: {status}")
   ```

### Agent in Error State

**Problem:**
```
Agent 'my_agent' is in error state
```

**Solutions:**
1. **Check logs:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Restart agent:**
   ```python
   # Unregister and re-register
   await manager.unregister_agent("my_agent")
   agent = await create_and_register_chronicler_agent(...)
   ```

3. **Check configuration:**
   ```python
   # Verify agent config
   config = agent.config
   print(f"Agent config: {config.model_dump()}")
   ```

## MCP Issues

### MCP Connection Failed

**Problem:**
```
ConnectionError: Failed to connect to MCP server
```

**Solutions:**
1. **Check server status:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Verify server configuration:**
   ```python
   # Check MCP server config
   server = create_mcp_server()
   print(f"Server host: {server.config.mcp_server_host}")
   print(f"Server port: {server.config.mcp_server_port}")
   ```

3. **Start MCP server:**
   ```python
   import uvicorn
   from chronicler_client.agents.mcp_server import create_mcp_server

   server = create_mcp_server()
   uvicorn.run(server.app, host="localhost", port=8000)
   ```

### MCP Tool Not Found

**Problem:**
```
Tool 'execute_agent' not available
```

**Solutions:**
1. **List available tools:**
   ```python
   tools = await agent.list_available_tools()
   print(f"Available tools: {[t['name'] for t in tools]}")
   ```

2. **Check tool schema:**
   ```python
   schema = await agent.get_tool_schema("execute_agent")
   print(f"Tool schema: {schema}")
   ```

3. **Verify MCP initialization:**
   ```python
   # Check if MCP client is initialized
   if hasattr(agent, 'mcp_client') and agent.mcp_client:
       print("MCP client is initialized")
   ```

## Performance Issues

### Slow Response Times

**Problem:**
```
Agent responses are very slow
```

**Solutions:**
1. **Check agent statistics:**
   ```python
   stats = await manager.get_manager_stats()
   print(f"Average response time: {stats.avg_response_time}")
   ```

2. **Monitor agent health:**
   ```python
   status = await manager.get_agent_status("my_agent")
   print(f"Error rate: {status.get('error_rate', 0)}")
   ```

3. **Optimize configuration:**
   ```python
   config = AgentManagerConfig(
       max_concurrent_agents=10,
       agent_timeout=300,
       enable_health_checks=True
   )
   ```

### High Memory Usage

**Problem:**
```
Memory usage is very high
```

**Solutions:**
1. **Limit request history:**
   ```python
   # The manager automatically limits history to 1000 requests
   # Check current usage
   stats = await manager.get_manager_stats()
   print(f"Total requests: {stats.total_requests}")
   ```

2. **Clean up resources:**
   ```python
   # Shutdown unused agents
   await manager.unregister_agent("unused_agent")
   ```

3. **Monitor agent count:**
   ```python
   stats = await manager.get_manager_stats()
   print(f"Total agents: {stats.total_agents}")
   ```

## Network Issues

### Connection Timeout

**Problem:**
```
TimeoutError: Connection timed out
```

**Solutions:**
1. **Increase timeout:**
   ```python
   config = AgentConfig(
       timeout=600,  # 10 minutes
       retry_attempts=5
   )
   ```

2. **Check network connectivity:**
   ```python
   import httpx

   async with httpx.AsyncClient() as client:
       response = await client.get("http://localhost:8000/health")
       print(f"Server status: {response.status_code}")
   ```

3. **Use retry logic:**
   ```python
   import asyncio

   for attempt in range(3):
       try:
           response = await manager.execute_request("my_agent", data)
           break
       except Exception as e:
           print(f"Attempt {attempt + 1} failed: {e}")
           await asyncio.sleep(1)
   ```

## Debugging

### Enable Debug Logging

```python
import logging

# Enable debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Check Agent Logs

```python
# Agent logs are available through the logger
agent.logger.debug("Debug message")
agent.logger.info("Info message")
agent.logger.error("Error message")
```

### Monitor Health

```python
# Regular health checks
async def monitor_health():
    while True:
        stats = await manager.get_manager_stats()
        print(f"Health check: {stats}")
        await asyncio.sleep(60)  # Check every minute

# Start monitoring
asyncio.create_task(monitor_health())
```

## Getting Help

### Check Documentation
- [API Reference](../api/)
- [Configuration Guide](../concepts/configuration.md)
- [Examples](../examples/)

### Report Issues
- [GitHub Issues](https://github.com/chronicler-foundation/chronicler/issues)
- Include error messages and stack traces
- Provide minimal reproduction code

### Community Support
- [Discord](https://discord.gg/chronicler)
- [Discussions](https://github.com/chronicler-foundation/chronicler/discussions)

## Related Topics

- [Debugging](./debugging.md)
- [Performance Issues](./performance.md)
- [MCP Problems](./mcp-problems.md)