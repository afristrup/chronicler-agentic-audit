# Error Handling

Error handling patterns and best practices.

## Basic Error Handling

```python
from chronicler_client.decorators import chronicler

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

## Custom Exception Handling

```python
from chronicler_client.decorators import chronicler

class ValidationError(Exception):
    pass

@chronicler(agent_id="validator", tool_id="data_validation")
def validate_email(email: str) -> bool:
    if not email or '@' not in email:
        raise ValidationError("Invalid email format")

    if len(email) > 254:
        raise ValidationError("Email too long")

    return True

# Custom exceptions are logged
try:
    validate_email("invalid-email")
except ValidationError as e:
    print(f"Validation failed: {e}")
```

## Graceful Degradation

```python
from chronicler_client.decorators import chronicler
import requests

@chronicler(agent_id="api_agent", tool_id="external_api")
def fetch_data_with_fallback(url: str) -> dict:
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Log the error and return fallback data
        return {"error": str(e), "fallback": True}
    except Exception as e:
        # Unexpected errors are also logged
        raise e

# Network errors are handled gracefully
result = fetch_data_with_fallback("https://api.example.com/data")
```

## Retry Logic

```python
from chronicler_client.decorators import chronicler
import time

@chronicler(agent_id="retry_agent", tool_id="retry_operations")
def retry_operation(operation_func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return operation_func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e  # Final attempt failed
            time.sleep(2 ** attempt)  # Exponential backoff

# Usage
def unreliable_operation():
    import random
    if random.random() < 0.7:
        raise Exception("Random failure")
    return "success"

result = retry_operation(unreliable_operation)
```

## Input Validation

```python
from chronicler_client.decorators import chronicler
from typing import List, Dict, Any

@chronicler(agent_id="validator", tool_id="input_validation")
def process_user_data(data: Dict[str, Any]) -> Dict[str, Any]:
    # Validate required fields
    required_fields = ['name', 'email', 'age']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    # Validate data types
    if not isinstance(data['name'], str):
        raise TypeError("Name must be a string")

    if not isinstance(data['age'], int):
        raise TypeError("Age must be an integer")

    if data['age'] < 0 or data['age'] > 150:
        raise ValueError("Age must be between 0 and 150")

    # Process valid data
    return {
        "processed": True,
        "name": data['name'].title(),
        "email": data['email'].lower(),
        "age": data['age']
    }

# Validation errors are logged
try:
    result = process_user_data({
        "name": "john",
        "email": "john@example.com",
        "age": "invalid"
    })
except (ValueError, TypeError) as e:
    print(f"Validation error: {e}")
```

## Resource Cleanup

```python
from chronicler_client.decorators import chronicler
import tempfile
import os

@chronicler(agent_id="file_agent", tool_id="file_operations")
def process_file_with_cleanup(file_path: str) -> str:
    temp_file = None
    try:
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False)

        # Process the file
        with open(file_path, 'r') as f:
            content = f.read()

        # Write processed content
        temp_file.write(content.upper().encode())
        temp_file.close()

        return temp_file.name

    except Exception as e:
        # Clean up on error
        if temp_file and os.path.exists(temp_file.name):
            os.unlink(temp_file.name)
        raise e

# File operations with cleanup
try:
    result = process_file_with_cleanup("nonexistent.txt")
except FileNotFoundError as e:
    print(f"File error: {e}")
```

## Logging and Monitoring

```python
from chronicler_client.decorators import chronicler
import logging

logger = logging.getLogger(__name__)

@chronicler(agent_id="monitor_agent", tool_id="monitoring")
def monitored_operation(data: str) -> str:
    try:
        logger.info(f"Processing data: {data[:10]}...")

        if len(data) > 1000:
            raise ValueError("Data too large")

        result = data.upper()
        logger.info("Operation completed successfully")
        return result

    except Exception as e:
        logger.error(f"Operation failed: {e}")
        raise e

# Operations with logging
try:
    result = monitored_operation("a" * 2000)
except ValueError as e:
    print(f"Operation failed: {e}")
```