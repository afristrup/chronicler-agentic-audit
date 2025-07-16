# Decorators

Function and class decoration for Chronicler integration.

## Basic Usage

```python
from chronicler_client.decorators import chronicler

@chronicler(agent_id="my_agent", tool_id="text_processor")
def process_text(text: str) -> str:
    return text.upper()
```

## Parameters

### Required
- `agent_id` (str): Unique agent identifier
- `tool_id` (str): Unique tool identifier

### Optional
- `config` (AuditConfig): Audit configuration
- `metadata` (ActionMetadata): Action metadata

## Configuration

```python
from chronicler_client.decorators import AuditConfig

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

## Metadata

```python
from chronicler_client.decorators import ActionMetadata

metadata = ActionMetadata(
    agent_id="my_agent",
    tool_id="text_processor",
    description="Process text input",
    risk_level=1,
    tags={"type": "text", "framework": "custom"}
)

@chronicler(
    agent_id="my_agent",
    tool_id="text_processor",
    metadata=metadata
)
def process_text(text: str) -> str:
    return text.upper()
```

## DSPy Integration

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

## Error Handling

The decorator automatically logs both successful and failed operations:

```python
@chronicler(agent_id="calculator", tool_id="math_operations")
def safe_divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Both success and failure are logged
result = safe_divide(10, 2)  # Success logged
try:
    safe_divide(10, 0)  # Failure logged
except ValueError:
    pass
```