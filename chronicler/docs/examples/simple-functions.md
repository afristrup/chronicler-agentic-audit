# Simple Functions

Basic function decoration examples.

## Text Processing

```python
from chronicler_client.decorators import chronicler

@chronicler(agent_id="text_agent", tool_id="text_processor")
def process_text(text: str) -> str:
    return text.upper()

result = process_text("hello world")
print(result)  # "HELLO WORLD"
```

## Data Analysis

```python
from chronicler_client.decorators import chronicler, ActionMetadata

metadata = ActionMetadata(
    agent_id="data_agent",
    tool_id="statistics",
    description="Calculate basic statistics",
    risk_level=1
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
        "min": min(data),
        "count": len(data)
    }

stats = calculate_stats([1, 2, 3, 4, 5])
print(stats)  # {"mean": 3.0, "max": 5, "min": 1, "count": 5}
```

## File Operations

```python
from chronicler_client.decorators import chronicler
import json

@chronicler(agent_id="file_agent", tool_id="json_parser")
def parse_json(data: str) -> dict:
    return json.loads(data)

data = parse_json('{"name": "John", "age": 30}')
print(data)  # {"name": "John", "age": 30}
```

## API Calls

```python
from chronicler_client.decorators import chronicler
import requests

@chronicler(agent_id="api_agent", tool_id="http_client")
def fetch_data(url: str) -> dict:
    response = requests.get(url)
    return response.json()

data = fetch_data("https://api.example.com/data")
```