# Chronicler Python Client

A Python client for integrating with the Chronicler blockchain layer, providing DSPy decorators for on-chain audit logging, access control, and registry management.

## Features

- **DSPy Integration**: Seamless decorator-based integration with DSPy modules
- **Blockchain Audit Logging**: Automatic logging of AI agent actions to the blockchain
- **Access Control**: Integration with permission management and rate limiting
- **Registry Management**: Agent and tool registration and validation
- **Configurable**: Flexible configuration for different deployment scenarios

## Installation

```bash
# Install from the client directory
cd chronicler/client
pip install -e .

# Or install dependencies manually
pip install dspy web3 python-dotenv fastapi uvicorn httpx pytest ruff
```

## Quick Start

### 1. Environment Configuration

Create a `.env` file in the client directory:

```env
# Network Configuration
CHAIN_ID=1
RPC_URL=http://localhost:8545
REGISTRY_ADDRESS=0x1234567890123456789012345678901234567890
AUDIT_LOG_ADDRESS=0x2345678901234567890123456789012345678901
ACCESS_CONTROL_ADDRESS=0x3456789012345678901234567890123456789012

# Database Configuration (optional)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key

# Audit Configuration
AUDIT_ENABLED=true
LOG_INPUT=true
LOG_OUTPUT=true
BATCH_SIZE=100
```

### 2. Basic Usage

```python
from chronicler.client.source.decorators import chronicler, ActionMetadata

# Simple function decoration
@chronicler(
    agent_id="my_agent",
    tool_id="text_processor"
)
def process_text(text: str) -> str:
    return text.upper()

# Use the function
result = process_text("hello world")
print(result)  # "HELLO WORLD"
```

### 3. DSPy Integration

```python
import dspy
from chronicler.client.source.decorators import chronicler, ActionMetadata

@chronicler(
    agent_id="dspy_agent",
    tool_id="text_generator",
    metadata=ActionMetadata(
        agent_id="dspy_agent",
        tool_id="text_generator",
        description="Generate text using DSPy",
        risk_level=2
    )
)
class TextGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predictor = dspy.Predict("context -> generated_text")

    def forward(self, context: str) -> str:
        result = self.predictor(context=context)
        return result.generated_text

# Use the DSPy module
generator = TextGenerator()
result = generator("Generate a story about a robot")
```

## API Reference

### Decorator

#### `@chronicler(agent_id, tool_id, config=None, metadata=None)`

Decorates a function or DSPy module to enable blockchain audit logging.

**Parameters:**
- `agent_id` (str): Unique identifier for the agent
- `tool_id` (str): Unique identifier for the tool being used
- `config` (AuditConfig, optional): Audit configuration
- `metadata` (ActionMetadata, optional): Additional action metadata

### Types

#### `ActionMetadata`

```python
@dataclass
class ActionMetadata:
    agent_id: str
    tool_id: str
    category_id: Optional[str] = None
    risk_level: Optional[int] = None
    description: Optional[str] = None
    tags: Dict[str, Any] = field(default_factory=dict)
    custom_data: Dict[str, Any] = field(default_factory=dict)
```

#### `AuditConfig`

```python
@dataclass
class AuditConfig:
    enabled: bool = True
    log_input: bool = True
    log_output: bool = True
    log_metadata: bool = True
    batch_size: int = 100
    ipfs_gateway: str = "https://ipfs.io"
    timeout: int = 30000
    retry_attempts: int = 3
```

## Examples

### Basic Function Decoration

```python
from chronicler.client.source.decorators import chronicler, ActionMetadata

@chronicler(
    agent_id="data_analyzer",
    tool_id="statistics",
    metadata=ActionMetadata(
        agent_id="data_analyzer",
        tool_id="statistics",
        description="Calculate statistics",
        risk_level=1
    )
)
def calculate_stats(data: list) -> dict:
    return {
        "mean": sum(data) / len(data),
        "max": max(data),
        "min": min(data)
    }
```

### DSPy Module with Custom Configuration

```python
import dspy
from chronicler.client.source.decorators import chronicler, ActionMetadata, AuditConfig

@chronicler(
    agent_id="qa_agent",
    tool_id="question_answering",
    config=AuditConfig(
        enabled=True,
        log_input=True,
        log_output=True,
        batch_size=50
    ),
    metadata=ActionMetadata(
        agent_id="qa_agent",
        tool_id="question_answering",
        description="Answer questions based on context",
        risk_level=2,
        tags={"type": "qa", "framework": "dspy"}
    )
)
class QASystem(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predictor = dspy.Predict("context, question -> answer")

    def forward(self, context: str, question: str) -> str:
        result = self.predictor(context=context, question=question)
        return result.answer
```

### Error Handling

```python
@chronicler(
    agent_id="calculator",
    tool_id="math_operations"
)
def safe_divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# The decorator will log both successful and failed operations
try:
    result = safe_divide(10, 2)  # Success
    result = safe_divide(10, 0)  # Failure - logged to blockchain
except ValueError as e:
    print(f"Error: {e}")
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CHAIN_ID` | Blockchain network ID | `1` |
| `RPC_URL` | Ethereum RPC endpoint | `http://localhost:8545` |
| `REGISTRY_ADDRESS` | Registry contract address | Required |
| `AUDIT_LOG_ADDRESS` | Audit log contract address | Required |
| `ACCESS_CONTROL_ADDRESS` | Access control contract address | Required |
| `SUPABASE_URL` | Supabase database URL | Optional |
| `SUPABASE_KEY` | Supabase API key | Optional |
| `AUDIT_ENABLED` | Enable/disable audit logging | `true` |
| `LOG_INPUT` | Log function inputs | `true` |
| `LOG_OUTPUT` | Log function outputs | `true` |
| `BATCH_SIZE` | Batch size for logging | `100` |

### Programmatic Configuration

```python
from chronicler.client.source.config import ChroniclerConfig, set_config

config = ChroniclerConfig(
    chain_id=1,
    rpc_url="https://mainnet.infura.io/v3/YOUR_KEY",
    registry_address="0x...",
    audit_log_address="0x...",
    access_control_address="0x...",
    audit_enabled=True
)

set_config(config)
```

## Testing

Run the test suite:

```bash
cd chronicler/client
python -m pytest tests/
```

Run specific examples:

```bash
# Basic usage example
python -m chronicler.client.examples.basic_usage

# DSPy integration example
python -m chronicler.client.examples.dspy_integration
```

## Architecture

The Python client integrates with the Chronicler layer through:

1. **Decorators**: Capture function calls and metadata
2. **Services**: Handle blockchain interactions
3. **Configuration**: Manage environment and settings
4. **Types**: Define data structures and interfaces

### Integration Flow

1. Function decorated with `@chronicler`
2. Decorator captures input/output data
3. Service logs action to blockchain
4. Audit information attached to result
5. Error handling and failure logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

See the main repository license.