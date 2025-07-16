# Types

Data structures and interfaces used by Chronicler.

## ActionMetadata

Metadata for agent actions.

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

**Fields:**
- `agent_id`: Unique agent identifier
- `tool_id`: Unique tool identifier
- `category_id`: Optional category for grouping
- `risk_level`: Risk assessment (1-5)
- `description`: Human-readable description
- `tags`: Key-value metadata
- `custom_data`: Additional custom data

## AuditConfig

Configuration for audit logging.

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

**Fields:**
- `enabled`: Enable/disable audit logging
- `log_input`: Log function inputs
- `log_output`: Log function outputs
- `log_metadata`: Log metadata
- `batch_size`: Batch size for processing
- `ipfs_gateway`: IPFS gateway URL
- `timeout`: Request timeout (ms)
- `retry_attempts`: Number of retry attempts

## ActionStatus

Status of logged actions.

```python
class ActionStatus(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    PENDING = "pending"
    CANCELLED = "cancelled"
```

## NetworkConfig

Blockchain network configuration.

```python
@dataclass
class NetworkConfig:
    chain_id: int
    rpc_url: str
    contracts: Dict[str, str]
```

**Fields:**
- `chain_id`: Blockchain network ID
- `rpc_url`: RPC endpoint URL
- `contracts`: Contract addresses mapping