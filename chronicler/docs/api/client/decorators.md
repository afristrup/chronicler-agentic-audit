# Decorators API

Complete API reference for Chronicler decorators.

## @chronicler

Main decorator for function and class decoration.

### Signature

```python
@chronicler(
    agent_id: str,
    tool_id: str,
    config: Optional[AuditConfig] = None,
    metadata: Optional[ActionMetadata] = None
)
```

### Parameters

- **agent_id** (str, required): Unique identifier for the agent
- **tool_id** (str, required): Unique identifier for the tool
- **config** (AuditConfig, optional): Audit configuration
- **metadata** (ActionMetadata, optional): Action metadata

### Returns

Decorated function or class with audit logging capabilities.

### Examples

#### Basic Function Decoration

```python
from chronicler_client.decorators import chronicler

@chronicler(agent_id="my_agent", tool_id="text_processor")
def process_text(text: str) -> str:
    return text.upper()
```

#### With Configuration

```python
from chronicler_client.decorators import chronicler, AuditConfig

config = AuditConfig(
    enabled=True,
    log_input=True,
    log_output=True,
    batch_size=100
)

@chronicler(
    agent_id="my_agent",
    tool_id="text_processor",
    config=config
)
def process_text(text: str) -> str:
    return text.upper()
```

#### With Metadata

```python
from chronicler_client.decorators import chronicler, ActionMetadata

metadata = ActionMetadata(
    agent_id="my_agent",
    tool_id="text_processor",
    description="Process text input",
    risk_level=1
)

@chronicler(
    agent_id="my_agent",
    tool_id="text_processor",
    metadata=metadata
)
def process_text(text: str) -> str:
    return text.upper()
```

#### DSPy Module Decoration

```python
import dspy
from chronicler_client.decorators import chronicler

@chronicler(agent_id="dspy_agent", tool_id="text_generator")
class TextGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predictor = dspy.Predict("context -> generated_text")

    def forward(self, context: str) -> str:
        result = self.predictor(context=context)
        return result.generated_text
```

## ActionMetadata

Metadata for agent actions.

### Constructor

```python
ActionMetadata(
    agent_id: str,
    tool_id: str,
    category_id: Optional[str] = None,
    risk_level: Optional[int] = None,
    description: Optional[str] = None,
    tags: Dict[str, Any] = field(default_factory=dict),
    custom_data: Dict[str, Any] = field(default_factory=dict)
)
```

### Fields

- **agent_id** (str): Unique agent identifier
- **tool_id** (str): Unique tool identifier
- **category_id** (str, optional): Category for grouping
- **risk_level** (int, optional): Risk assessment (1-5)
- **description** (str, optional): Human-readable description
- **tags** (Dict[str, Any]): Key-value metadata
- **custom_data** (Dict[str, Any]): Additional custom data

### Examples

```python
from chronicler_client.decorators import ActionMetadata

# Basic metadata
metadata = ActionMetadata(
    agent_id="my_agent",
    tool_id="text_processor"
)

# Full metadata
metadata = ActionMetadata(
    agent_id="data_agent",
    tool_id="statistics",
    category_id="analysis",
    risk_level=2,
    description="Calculate basic statistics",
    tags={"type": "analysis", "framework": "custom"},
    custom_data={"version": "1.0", "author": "team"}
)
```

## AuditConfig

Configuration for audit logging.

### Constructor

```python
AuditConfig(
    enabled: bool = True,
    log_input: bool = True,
    log_output: bool = True,
    log_metadata: bool = True,
    batch_size: int = 100,
    ipfs_gateway: str = "https://ipfs.io",
    timeout: int = 30000,
    retry_attempts: int = 3
)
```

### Fields

- **enabled** (bool): Enable/disable audit logging
- **log_input** (bool): Log function inputs
- **log_output** (bool): Log function outputs
- **log_metadata** (bool): Log metadata
- **batch_size** (int): Batch size for processing
- **ipfs_gateway** (str): IPFS gateway URL
- **timeout** (int): Request timeout (ms)
- **retry_attempts** (int): Number of retry attempts

### Examples

```python
from chronicler_client.decorators import AuditConfig

# Default configuration
config = AuditConfig()

# Custom configuration
config = AuditConfig(
    enabled=True,
    log_input=True,
    log_output=True,
    batch_size=50,
    timeout=60000,
    retry_attempts=5
)

# Performance configuration
config = AuditConfig(
    enabled=True,
    log_input=False,  # Skip input logging
    log_output=True,
    batch_size=500,  # Larger batches
    timeout=15000   # Shorter timeout
)
```

## Error Handling

The decorator automatically handles errors and logs them to the blockchain:

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

## Performance Considerations

- **Batch processing**: Actions are batched for efficiency
- **Async support**: Non-blocking operations
- **Configurable timeouts**: Prevent hanging operations
- **Retry logic**: Automatic retry on failures