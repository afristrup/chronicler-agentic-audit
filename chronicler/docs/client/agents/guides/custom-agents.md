# Creating Custom Agents

Learn how to create custom agents for your specific use cases.

## Overview

Custom agents allow you to extend the Chronicler system with specialized functionality.

## Basic Custom Agent

```python
from chronicler_client.agents import BaseAgent, AgentRequest, AgentResponse
from chronicler_client.agents import AgentConfig, AgentType, AgentCapability

class MyCustomAgent(BaseAgent):
    """A custom agent for specific tasks"""

    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process incoming requests"""

        # Extract input data
        input_data = request.input_data

        # Your custom logic here
        result = await self._process_custom_logic(input_data)

        # Create response
        return AgentResponse(
            request_id=request.request_id,
            agent_id=self.agent_id,
            output_data={"result": result},
            status="success",
            execution_time=0.0
        )

    async def _process_custom_logic(self, data: dict) -> str:
        """Your custom processing logic"""
        # Implement your specific logic here
        return f"Processed: {data}"
```

## Creating and Using Custom Agents

### Step 1: Define Configuration

```python
config = AgentConfig(
    agent_id="my_custom_agent",
    name="My Custom Agent",
    description="A custom agent for specific tasks",
    agent_type=AgentType.SPECIALIZED,
    capabilities=[
        AgentCapability.TEXT_GENERATION,
        AgentCapability.DATA_ANALYSIS
    ],
    audit_enabled=True,
    log_input=True,
    log_output=True
)
```

### Step 2: Create Agent Instance

```python
# Create agent
agent = MyCustomAgent(config)

# Register with manager
manager = AgentManager()
await manager.register_agent(agent)
```

### Step 3: Execute Requests

```python
# Execute custom request
response = await manager.execute_request(
    "my_custom_agent",
    {"custom_data": "test value"}
)

print(f"Result: {response.output_data}")
```

## Advanced Custom Agent

```python
import asyncio
from typing import Dict, Any
from chronicler_client.agents import BaseAgent, AgentRequest, AgentResponse

class AdvancedCustomAgent(BaseAgent):
    """Advanced custom agent with multiple capabilities"""

    def __init__(self, config, custom_service=None):
        super().__init__(config)
        self.custom_service = custom_service
        self.cache = {}

    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process requests with advanced logic"""

        try:
            # Determine operation type
            operation = request.input_data.get("operation", "default")

            if operation == "analyze":
                result = await self._analyze_data(request.input_data)
            elif operation == "transform":
                result = await self._transform_data(request.input_data)
            elif operation == "cache":
                result = await self._handle_cache(request.input_data)
            else:
                result = await self._default_operation(request.input_data)

            return AgentResponse(
                request_id=request.request_id,
                agent_id=self.agent_id,
                output_data={"result": result},
                status="success",
                execution_time=0.0
            )

        except Exception as e:
            return AgentResponse(
                request_id=request.request_id,
                agent_id=self.agent_id,
                output_data={"error": str(e)},
                status="error",
                execution_time=0.0
            )

    async def _analyze_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze input data"""
        # Your analysis logic here
        return {"analysis": "completed", "data": data}

    async def _transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform input data"""
        # Your transformation logic here
        return {"transformed": data}

    async def _handle_cache(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle caching operations"""
        key = data.get("key")
        value = data.get("value")

        if value is not None:
            self.cache[key] = value
            return {"cached": key}
        else:
            return {"retrieved": self.cache.get(key)}

    async def _default_operation(self, data: Dict[str, Any]) -> str:
        """Default operation"""
        return f"Default processing: {data}"
```

## Agent with External Services

```python
import httpx
from chronicler_client.agents import BaseAgent, AgentRequest, AgentResponse

class ExternalServiceAgent(BaseAgent):
    """Agent that integrates with external services"""

    def __init__(self, config, api_key: str = None):
        super().__init__(config)
        self.api_key = api_key
        self.client = httpx.AsyncClient()

    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process requests using external service"""

        try:
            # Call external service
            service_data = request.input_data.get("service_data", {})
            result = await self._call_external_service(service_data)

            return AgentResponse(
                request_id=request.request_id,
                agent_id=self.agent_id,
                output_data={"service_result": result},
                status="success",
                execution_time=0.0
            )

        except Exception as e:
            return AgentResponse(
                request_id=request.request_id,
                agent_id=self.agent_id,
                output_data={"error": str(e)},
                status="error",
                execution_time=0.0
            )

    async def _call_external_service(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Call external API"""
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

        response = await self.client.post(
            "https://api.external-service.com/process",
            json=data,
            headers=headers
        )

        return response.json()

    async def shutdown(self):
        """Cleanup resources"""
        await self.client.aclose()
        await super().shutdown()
```

## Agent with State Management

```python
from chronicler_client.agents import BaseAgent, AgentRequest, AgentResponse

class StatefulAgent(BaseAgent):
    """Agent that maintains state across requests"""

    def __init__(self, config):
        super().__init__(config)
        self.state = {}
        self.request_history = []

    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process requests with state management"""

        # Update state
        self.state["last_request"] = request.input_data
        self.request_history.append(request.request_id)

        # Process based on state
        if len(self.request_history) == 1:
            result = await self._first_request(request.input_data)
        else:
            result = await self._subsequent_request(request.input_data)

        return AgentResponse(
            request_id=request.request_id,
            agent_id=self.agent_id,
            output_data={
                "result": result,
                "state": self.state,
                "request_count": len(self.request_history)
            },
            status="success",
            execution_time=0.0
        )

    async def _first_request(self, data: Dict[str, Any]) -> str:
        """Handle first request"""
        return f"First request: {data}"

    async def _subsequent_request(self, data: Dict[str, Any]) -> str:
        """Handle subsequent requests"""
        return f"Subsequent request: {data}"
```

## Best Practices

### 1. Error Handling

```python
async def process_request(self, request: AgentRequest) -> AgentResponse:
    try:
        # Your logic here
        result = await self._process_logic(request.input_data)

        return AgentResponse(
            request_id=request.request_id,
            agent_id=self.agent_id,
            output_data={"result": result},
            status="success",
            execution_time=0.0
        )

    except Exception as e:
        self.logger.error(f"Error processing request: {e}")

        return AgentResponse(
            request_id=request.request_id,
            agent_id=self.agent_id,
            output_data={"error": str(e)},
            status="error",
            execution_time=0.0
        )
```

### 2. Logging

```python
async def process_request(self, request: AgentRequest) -> AgentResponse:
    self.logger.info(f"Processing request: {request.request_id}")

    # Your logic here

    self.logger.info(f"Request completed: {request.request_id}")
    return response
```

### 3. Resource Management

```python
async def shutdown(self):
    """Cleanup resources"""
    # Cleanup your resources
    await self._cleanup()

    # Call parent shutdown
    await super().shutdown()
```

### 4. Configuration Validation

```python
def __init__(self, config: AgentConfig):
    super().__init__(config)

    # Validate custom configuration
    if not config.custom_settings.get("required_setting"):
        raise ValueError("Required setting not found in configuration")
```

## Testing Custom Agents

```python
import pytest
from chronicler_client.agents import AgentRequest

@pytest.mark.asyncio
async def test_custom_agent():
    # Create agent
    config = AgentConfig(
        agent_id="test_agent",
        name="Test Agent",
        agent_type=AgentType.SPECIALIZED,
        capabilities=[AgentCapability.TEXT_GENERATION]
    )

    agent = MyCustomAgent(config)

    # Test request
    request = AgentRequest(
        request_id="test_request",
        agent_id="test_agent",
        input_data={"test": "data"}
    )

    response = await agent.process_request(request)

    assert response.status == "success"
    assert "result" in response.output_data
```

## Related Topics

- [Agent Types](../concepts/agent-types.md)
- [Capabilities](../concepts/capabilities.md)
- [Configuration](../concepts/configuration.md)
- [Error Handling](./error-handling.md)