# Getting Started

Quick setup guide for Chronicler.

## Prerequisites

- Python 3.10+
- Node.js 18+ or Bun 1.0+
- Ethereum wallet with testnet funds
- Supabase account (optional)

## Quick Setup

### 1. Install Client

```bash
cd chronicler/client
pip install -e .
```

### 2. Configure Environment

```bash
cp env.example .env
# Edit .env with your contract addresses
```

### 3. Basic Usage

```python
from chronicler_client.decorators import chronicler

@chronicler(agent_id="my_agent", tool_id="text_processor")
def process_text(text: str) -> str:
    return text.upper()

result = process_text("hello world")
```

## Next Steps

- [Client Configuration](./client-setup.md)
- [Blockchain Deployment](./blockchain-setup.md)
- [First Integration](./first-integration.md)