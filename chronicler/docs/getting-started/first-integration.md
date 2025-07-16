# First Integration

Your first steps with Chronicler decorators.

## Basic Function Decoration

```python
from chronicler_client.decorators import chronicler

@chronicler(agent_id="my_agent", tool_id="text_processor")
def process_text(text: str) -> str:
    return text.upper()

# Use the function
result = process_text("hello world")
print(result)  # "HELLO WORLD"
```

## With Metadata

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

# Use the module
generator = TextGenerator()
result = generator("Generate a story about a robot")
```

## Error Handling

```python
@chronicler(agent_id="calculator", tool_id="math_operations")
def safe_divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Errors are logged to blockchain
try:
    result = safe_divide(10, 0)
except ValueError as e:
    print(f"Error: {e}")
```