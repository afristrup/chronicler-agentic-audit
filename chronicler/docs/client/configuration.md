# Configuration

Client configuration and environment setup.

## Environment Variables

### Required Configuration

```env
# Network Configuration
CHAIN_ID=1
RPC_URL=http://localhost:8545

# Contract Addresses
REGISTRY_ADDRESS=0x1234567890123456789012345678901234567890
AUDIT_LOG_ADDRESS=0x2345678901234567890123456789012345678901
ACCESS_CONTROL_ADDRESS=0x3456789012345678901234567890123456789012
```

### Optional Configuration

```env
# Database Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key

# Service Configuration
IPFS_GATEWAY=https://ipfs.io
DASHBOARD_PORT=3000

# Audit Configuration
AUDIT_ENABLED=true
LOG_INPUT=true
LOG_OUTPUT=true
LOG_METADATA=true
BATCH_SIZE=100
TIMEOUT=30000
RETRY_ATTEMPTS=3

# Development Configuration
DEBUG=false
LOG_LEVEL=INFO
```

## Programmatic Configuration

```python
from chronicler_client.config import ChroniclerConfig, set_config

config = ChroniclerConfig(
    chain_id=1,
    rpc_url="https://mainnet.infura.io/v3/YOUR_KEY",
    registry_address="0x...",
    audit_log_address="0x...",
    access_control_address="0x...",
    audit_enabled=True,
    log_input=True,
    log_output=True,
    batch_size=100
)

set_config(config)
```

## Configuration Validation

The client validates configuration on startup:

- **Contract addresses** - Valid Ethereum addresses
- **Network configuration** - Valid chain ID and RPC URL
- **Database configuration** - Valid Supabase credentials
- **Audit settings** - Valid boolean and numeric values

## Environment-Specific Configs

### Development
```env
CHAIN_ID=1337
RPC_URL=http://localhost:8545
DEBUG=true
LOG_LEVEL=DEBUG
```

### Testnet
```env
CHAIN_ID=11155111
RPC_URL=https://sepolia.infura.io/v3/YOUR_KEY
AUDIT_ENABLED=true
```

### Production
```env
CHAIN_ID=1
RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY
AUDIT_ENABLED=true
DEBUG=false
```

## Configuration Precedence

1. **Environment variables** - Highest priority
2. **Programmatic config** - Set via `set_config()`
3. **Default values** - Built-in defaults