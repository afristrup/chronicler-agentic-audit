# Configuration API

Complete API reference for Chronicler configuration.

## ChroniclerConfig

Main configuration class for the client.

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

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `chain_id` | int | Yes | - | Blockchain network ID |
| `rpc_url` | str | Yes | - | RPC endpoint URL |
| `registry_address` | str | Yes | - | Registry contract address |
| `audit_log_address` | str | Yes | - | Audit log contract address |
| `access_control_address` | str | Yes | - | Access control contract address |
| `audit_enabled` | bool | No | True | Enable audit logging |
| `log_input` | bool | No | True | Log function inputs |
| `log_output` | bool | No | True | Log function outputs |
| `batch_size` | int | No | 100 | Batch size for processing |
| `timeout` | int | No | 30000 | Request timeout (ms) |
| `retry_attempts` | int | No | 3 | Number of retry attempts |
| `ipfs_gateway` | str | No | "https://ipfs.io" | IPFS gateway URL |
| `supabase_url` | str | No | None | Supabase database URL |
| `supabase_key` | str | No | None | Supabase API key |

### Examples

```python
from chronicler_client.config import ChroniclerConfig

# Minimal configuration
config = ChroniclerConfig(
    chain_id=1,
    rpc_url="https://mainnet.infura.io/v3/YOUR_KEY",
    registry_address="0x1234567890123456789012345678901234567890",
    audit_log_address="0x2345678901234567890123456789012345678901",
    access_control_address="0x3456789012345678901234567890123456789012"
)

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

## set_config()

Set the global configuration.

### Signature

```python
set_config(config: ChroniclerConfig) -> None
```

### Parameters

- **config** (ChroniclerConfig): Configuration to set

### Examples

```python
from chronicler_client.config import ChroniclerConfig, set_config

config = ChroniclerConfig(
    chain_id=1,
    rpc_url="https://mainnet.infura.io/v3/YOUR_KEY",
    registry_address="0x1234567890123456789012345678901234567890",
    audit_log_address="0x2345678901234567890123456789012345678901",
    access_control_address="0x3456789012345678901234567890123456789012"
)

set_config(config)
```

## get_config()

Get the current global configuration.

### Signature

```python
get_config() -> ChroniclerConfig
```

### Returns

Current configuration object.

### Examples

```python
from chronicler_client.config import get_config

config = get_config()
print(f"Chain ID: {config.chain_id}")
print(f"RPC URL: {config.rpc_url}")
```

## load_config_from_env()

Load configuration from environment variables.

### Signature

```python
load_config_from_env() -> ChroniclerConfig
```

### Environment Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `CHAIN_ID` | int | Yes | Blockchain network ID |
| `RPC_URL` | str | Yes | RPC endpoint URL |
| `REGISTRY_ADDRESS` | str | Yes | Registry contract address |
| `AUDIT_LOG_ADDRESS` | str | Yes | Audit log contract address |
| `ACCESS_CONTROL_ADDRESS` | str | Yes | Access control contract address |
| `AUDIT_ENABLED` | bool | No | Enable audit logging |
| `LOG_INPUT` | bool | No | Log function inputs |
| `LOG_OUTPUT` | bool | No | Log function outputs |
| `BATCH_SIZE` | int | No | Batch size for processing |
| `TIMEOUT` | int | No | Request timeout (ms) |
| `RETRY_ATTEMPTS` | int | No | Number of retry attempts |
| `IPFS_GATEWAY` | str | No | IPFS gateway URL |
| `SUPABASE_URL` | str | No | Supabase database URL |
| `SUPABASE_KEY` | str | No | Supabase API key |

### Examples

```python
from chronicler_client.config import load_config_from_env, set_config

# Load from environment variables
config = load_config_from_env()
set_config(config)
```

## validate_config()

Validate configuration parameters.

### Signature

```python
validate_config(config: ChroniclerConfig) -> bool
```

### Parameters

- **config** (ChroniclerConfig): Configuration to validate

### Returns

True if valid, raises ValidationError if invalid.

### Examples

```python
from chronicler_client.config import ChroniclerConfig, validate_config

config = ChroniclerConfig(
    chain_id=1,
    rpc_url="https://mainnet.infura.io/v3/YOUR_KEY",
    registry_address="0x1234567890123456789012345678901234567890",
    audit_log_address="0x2345678901234567890123456789012345678901",
    access_control_address="0x3456789012345678901234567890123456789012"
)

try:
    validate_config(config)
    print("Configuration is valid")
except ValidationError as e:
    print(f"Configuration error: {e}")
```

## Configuration Presets

### Development Configuration

```python
def get_development_config() -> ChroniclerConfig:
    return ChroniclerConfig(
        chain_id=1337,  # Local network
        rpc_url="http://localhost:8545",
        registry_address="0x1234567890123456789012345678901234567890",
        audit_log_address="0x2345678901234567890123456789012345678901",
        access_control_address="0x3456789012345678901234567890123456789012",
        audit_enabled=True,
        log_input=True,
        log_output=True,
        batch_size=10,  # Smaller batches for development
        timeout=60000   # Longer timeout for development
    )
```

### Testnet Configuration

```python
def get_testnet_config() -> ChroniclerConfig:
    return ChroniclerConfig(
        chain_id=11155111,  # Sepolia
        rpc_url="https://sepolia.infura.io/v3/YOUR_KEY",
        registry_address="0x...",
        audit_log_address="0x...",
        access_control_address="0x...",
        audit_enabled=True,
        batch_size=50
    )
```

### Production Configuration

```python
def get_production_config() -> ChroniclerConfig:
    return ChroniclerConfig(
        chain_id=1,  # Ethereum mainnet
        rpc_url="https://mainnet.infura.io/v3/YOUR_KEY",
        registry_address="0x...",
        audit_log_address="0x...",
        access_control_address="0x...",
        audit_enabled=True,
        batch_size=500,  # Larger batches for production
        timeout=15000,   # Shorter timeout for production
        retry_attempts=1  # Fewer retries for production
    )
```

## Configuration Management

### Save Configuration

```python
import json
from chronicler_client.config import ChroniclerConfig

def save_config(config: ChroniclerConfig, filepath: str):
    with open(filepath, 'w') as f:
        json.dump(config.__dict__, f, indent=2)

# Usage
config = ChroniclerConfig(...)
save_config(config, "chronicler_config.json")
```

### Load Configuration

```python
import json
from chronicler_client.config import ChroniclerConfig

def load_config(filepath: str) -> ChroniclerConfig:
    with open(filepath, 'r') as f:
        data = json.load(f)
    return ChroniclerConfig(**data)

# Usage
config = load_config("chronicler_config.json")
set_config(config)
```

## Error Handling

```python
from chronicler_client.config import ChroniclerConfig, ValidationError

try:
    config = ChroniclerConfig(
        chain_id=1,
        rpc_url="invalid_url",
        registry_address="invalid_address",
        audit_log_address="0x...",
        access_control_address="0x..."
    )
except ValidationError as e:
    print(f"Configuration error: {e}")
    print(f"Field: {e.field}")
    print(f"Value: {e.value}")
```