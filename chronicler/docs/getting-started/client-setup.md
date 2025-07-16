# Client Setup

Configure the Python client for Chronicler.

## Installation

```bash
cd chronicler/client
pip install -e .
```

## Environment Configuration

Create `.env` file:

```env
# Network
CHAIN_ID=1
RPC_URL=http://localhost:8545

# Contract Addresses
REGISTRY_ADDRESS=0x1234567890123456789012345678901234567890
AUDIT_LOG_ADDRESS=0x2345678901234567890123456789012345678901
ACCESS_CONTROL_ADDRESS=0x3456789012345678901234567890123456789012

# Database (optional)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key

# Audit Settings
AUDIT_ENABLED=true
LOG_INPUT=true
LOG_OUTPUT=true
BATCH_SIZE=100
```

## Dependencies

Required packages:
- `dspy` - DSPy integration
- `web3` - Blockchain interaction
- `python-dotenv` - Environment management
- `pydantic` - Data validation
- `fastapi` - API framework
- `uvicorn` - ASGI server
- `httpx` - HTTP client
- `pytest` - Testing
- `ruff` - Linting

## Verification

Test installation:

```bash
python -c "from chronicler_client.decorators import chronicler; print('Setup complete')"
```