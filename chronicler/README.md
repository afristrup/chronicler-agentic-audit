# Chronicler

Complete transparency and accountability for AI agent actions through blockchain-based audit logging.

## Overview

Chronicler provides a comprehensive solution for auditing AI agent actions on the blockchain. Every agent action is automatically recorded and verifiable on-chain, ensuring complete transparency and accountability.

## Key Features

- **Blockchain Audit Logging** - All actions logged to smart contracts
- **Access Control** - Fine-grained permissions and rate limiting
- **Registry Management** - Agent and tool registration
- **DSPy Integration** - Seamless decorator-based integration
- **Real-time Monitoring** - Dashboard and analytics
- **Compliance Reporting** - Built-in compliance tools

## System Components

### Client Layer
Python SDK with decorators for easy integration with AI frameworks like DSPy.

```python
from chronicler_client.decorators import chronicler

@chronicler(agent_id="my_agent", tool_id="text_processor")
def process_text(text: str) -> str:
    return text.upper()

result = process_text("hello world")
```

### Blockchain Layer
Smart contracts and TypeScript services for on-chain audit logging.

```bash
cd chronicler/layer
bun install
bun run compile
bun run deploy --network sepolia
```

### Landing Page
Next.js frontend for monitoring and analytics.

```bash
cd chronicler/landing
npm install
npm run dev
```

## Quick Start

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

## Documentation

- **[Getting Started](./docs/getting-started/)** - Setup and first steps
- **[Architecture](./docs/architecture/)** - System design and components
- **[Client](./docs/client/)** - Python client documentation
- **[Layer](./docs/layer/)** - Blockchain layer documentation
- **[API Reference](./docs/api/)** - Complete API documentation
- **[Deployment](./docs/deployment/)** - Production deployment guides
- **[Examples](./docs/examples/)** - Code examples and tutorials

## Development

### Prerequisites

- Python 3.10+
- Node.js 18+ or Bun 1.0+
- Ethereum wallet with testnet funds
- Supabase account (optional)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/chronicler.git
   cd chronicler
   ```

2. **Install client dependencies**
   ```bash
   cd client
   pip install -e .
   ```

3. **Install layer dependencies**
   ```bash
   cd ../layer
   bun install
   ```

4. **Install landing page dependencies**
   ```bash
   cd ../landing
   npm install
   ```

### Testing

```bash
# Test client
cd client
python -m pytest tests/

# Test layer
cd ../layer
bun test
```

### Deployment

```bash
# Deploy contracts
cd layer
bun run deploy --network sepolia

# Start services
bun run dev
```

## Architecture

Chronicler consists of three main layers:

1. **Client Layer** - Python SDK with decorators
2. **Blockchain Layer** - Smart contracts and services
3. **Landing Page** - Next.js frontend

### Data Flow

1. AI agent action is decorated with `@chronicler`
2. Action is logged to blockchain via smart contracts
3. Indexer service processes blockchain events
4. Data is stored in Supabase for analytics
5. Dashboard provides real-time monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- Documentation: [docs/](./docs/)
- Issues: [GitHub Issues](https://github.com/your-org/chronicler/issues)
- Discussions: [GitHub Discussions](https://github.com/your-org/chronicler/discussions)
