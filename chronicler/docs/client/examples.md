# Examples

Client usage patterns and examples.

## Basic Usage

### Simple Function Decoration

```python
from chronicler_client.decorators import chronicler

@chronicler(agent_id="my_agent", tool_id="text_processor")
def process_text(text: str) -> str:
    return text.upper()

result = process_text("hello world")
```

### With Configuration

```python
from chronicler_client.decorators import chronicler, AuditConfig

config = AuditConfig(
    enabled=True,
    log_input=True,
    log_output=True,
    batch_size=50
)

@chronicler(
    agent_id="my_agent",
    tool_id="text_processor",
    config=config
)
def process_text(text: str) -> str:
    return text.upper()
```

## Advanced Usage

### Custom Metadata

```python
from chronicler_client.decorators import chronicler, ActionMetadata

metadata = ActionMetadata(
    agent_id="data_agent",
    tool_id="statistics",
    description="Calculate statistics",
    risk_level=2,
    tags={"type": "analysis", "framework": "custom"},
    custom_data={"version": "1.0", "author": "team"}
)

@chronicler(
    agent_id="data_agent",
    tool_id="statistics",
    metadata=metadata
)
def calculate_stats(data: list) -> dict:
    return {
        "mean": sum(data) / len(data),
        "max": max(data),
        "min": min(data)
    }
```

### Error Handling

```python
@chronicler(agent_id="calculator", tool_id="math_operations")
def safe_divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Both success and failure are logged
try:
    result = safe_divide(10, 2)  # Success logged
    result = safe_divide(10, 0)  # Failure logged
except ValueError as e:
    print(f"Error: {e}")
```

## Service Usage

### Direct Service Calls

```python
from chronicler_client.services import ChroniclerService

service = ChroniclerService()

# Log action directly
result = await service.log_action(
    action_id="action_123",
    agent_id="my_agent",
    tool_id="text_processor",
    input_data={"text": "hello"},
    output_data={"result": "HELLO"},
    status="success"
)
```

### Registry Operations

```python
from chronicler_client.services import RegistryService

registry = RegistryService()

# Register agent
await registry.register_agent(
    agent_id="my_agent",
    operator="0x1234567890123456789012345678901234567890",
    metadata_uri="ipfs://Qm..."
)

# Check validity
is_valid = await registry.is_valid_agent("my_agent")
```

## Integration Examples

### With FastAPI

```python
from fastapi import FastAPI
from chronicler_client.decorators import chronicler

app = FastAPI()

@chronicler(agent_id="api_agent", tool_id="endpoint_handler")
@app.post("/process")
async def process_data(data: dict):
    return {"processed": data["input"].upper()}
```

### With Celery

```python
from celery import Celery
from chronicler_client.decorators import chronicler

celery = Celery('tasks')

@chronicler(agent_id="worker_agent", tool_id="task_processor")
@celery.task
def process_task(data):
    return {"result": data["input"] * 2}
```