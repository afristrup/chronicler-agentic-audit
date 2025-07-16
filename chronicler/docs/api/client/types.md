# Types API

Complete API reference for Chronicler data types.

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

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | Yes | Unique agent identifier |
| `tool_id` | str | Yes | Unique tool identifier |
| `category_id` | str | No | Category for grouping |
| `risk_level` | int | No | Risk assessment (1-5) |
| `description` | str | No | Human-readable description |
| `tags` | Dict[str, Any] | No | Key-value metadata |
| `custom_data` | Dict[str, Any] | No | Additional custom data |

### Examples

```python
from chronicler_client.decorators import ActionMetadata

# Minimal metadata
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

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | bool | True | Enable/disable audit logging |
| `log_input` | bool | True | Log function inputs |
| `log_output` | bool | True | Log function outputs |
| `log_metadata` | bool | True | Log metadata |
| `batch_size` | int | 100 | Batch size for processing |
| `ipfs_gateway` | str | "https://ipfs.io" | IPFS gateway URL |
| `timeout` | int | 30000 | Request timeout (ms) |
| `retry_attempts` | int | 3 | Number of retry attempts |

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
    log_input=False,
    log_output=True,
    batch_size=500,
    timeout=15000
)
```

## ActionStatus

Status of logged actions.

### Enum Values

```python
class ActionStatus(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    PENDING = "pending"
    CANCELLED = "cancelled"
```

### Usage

```python
from chronicler_client.decorators import ActionStatus

# Check action status
if status == ActionStatus.SUCCESS:
    print("Action completed successfully")
elif status == ActionStatus.FAILURE:
    print("Action failed")
elif status == ActionStatus.PENDING:
    print("Action is pending")
elif status == ActionStatus.CANCELLED:
    print("Action was cancelled")
```

## NetworkConfig

Blockchain network configuration.

### Constructor

```python
NetworkConfig(
    chain_id: int,
    rpc_url: str,
    contracts: Dict[str, str]
)
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `chain_id` | int | Blockchain network ID |
| `rpc_url` | str | RPC endpoint URL |
| `contracts` | Dict[str, str] | Contract addresses mapping |

### Examples

```python
from chronicler_client.config import NetworkConfig

# Ethereum mainnet
config = NetworkConfig(
    chain_id=1,
    rpc_url="https://mainnet.infura.io/v3/YOUR_KEY",
    contracts={
        "registry": "0x1234567890123456789012345678901234567890",
        "audit_log": "0x2345678901234567890123456789012345678901",
        "access_control": "0x3456789012345678901234567890123456789012"
    }
)

# Sepolia testnet
config = NetworkConfig(
    chain_id=11155111,
    rpc_url="https://sepolia.infura.io/v3/YOUR_KEY",
    contracts={
        "registry": "0x...",
        "audit_log": "0x...",
        "access_control": "0x..."
    }
)
```

## ChroniclerConfig

Complete client configuration.

### Constructor

```python
ChroniclerConfig(
    chain_id: int,
    rpc_url: str,
    registry_address: str,
    audit_log_address: str,
    access_control_address: str,
    audit_enabled: bool = True,
    log_input: bool = True,
    log_output: bool = True,
    batch_size: int = 100,
    timeout: int = 30000,
    retry_attempts: int = 3,
    ipfs_gateway: str = "https://ipfs.io",
    supabase_url: Optional[str] = None,
    supabase_key: Optional[str] = None
)
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `chain_id` | int | Yes | Blockchain network ID |
| `rpc_url` | str | Yes | RPC endpoint URL |
| `registry_address` | str | Yes | Registry contract address |
| `audit_log_address` | str | Yes | Audit log contract address |
| `access_control_address` | str | Yes | Access control contract address |
| `audit_enabled` | bool | No | Enable audit logging |
| `log_input` | bool | No | Log function inputs |
| `log_output` | bool | No | Log function outputs |
| `batch_size` | int | No | Batch size for processing |
| `timeout` | int | No | Request timeout (ms) |
| `retry_attempts` | int | No | Number of retry attempts |
| `ipfs_gateway` | str | No | IPFS gateway URL |
| `supabase_url` | str | No | Supabase database URL |
| `supabase_key` | str | No | Supabase API key |

### Examples

```python
from chronicler_client.config import ChroniclerConfig

# Complete configuration
config = ChroniclerConfig(
    chain_id=1,
    rpc_url="https://mainnet.infura.io/v3/YOUR_KEY",
    registry_address="0x1234567890123456789012345678901234567890",
    audit_log_address="0x2345678901234567890123456789012345678901",
    access_control_address="0x3456789012345678901234567890123456789012",
    audit_enabled=True,
    log_input=True,
    log_output=True,
    batch_size=100,
    timeout=30000,
    retry_attempts=3,
    ipfs_gateway="https://ipfs.io",
    supabase_url="https://your-project.supabase.co",
    supabase_key="your-supabase-key"
)
```

## ServiceConfig

Service-specific configuration.

### Constructor

```python
ServiceConfig(
    timeout: int = 30000,
    retry_attempts: int = 3,
    batch_size: int = 100,
    ipfs_gateway: str = "https://ipfs.io"
)
```

### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `timeout` | int | 30000 | Request timeout (ms) |
| `retry_attempts` | int | 3 | Number of retry attempts |
| `batch_size` | int | 100 | Batch size for processing |
| `ipfs_gateway` | str | "https://ipfs.io" | IPFS gateway URL |

### Examples

```python
from chronicler_client.services import ServiceConfig

# Default service configuration
config = ServiceConfig()

# Custom service configuration
config = ServiceConfig(
    timeout=60000,
    retry_attempts=5,
    batch_size=50,
    ipfs_gateway="https://gateway.pinata.cloud"
)
```

## Validation

All types include validation:

```python
# Valid metadata
metadata = ActionMetadata(
    agent_id="valid_agent",
    tool_id="valid_tool",
    risk_level=3  # Valid range: 1-5
)

# Invalid metadata (will raise validation error)
metadata = ActionMetadata(
    agent_id="",  # Empty agent_id
    tool_id="valid_tool",
    risk_level=10  # Invalid range
)
```

## Serialization

Types support JSON serialization:

```python
import json

# Serialize to JSON
metadata = ActionMetadata(
    agent_id="my_agent",
    tool_id="text_processor"
)
json_data = json.dumps(metadata.__dict__)

# Deserialize from JSON
data = json.loads(json_data)
metadata = ActionMetadata(**data)
```