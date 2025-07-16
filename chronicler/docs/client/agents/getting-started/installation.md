# Installation Guide

Complete installation guide for Chronicler Agents.

## System Requirements

- **Python**: 3.10 or higher
- **OS**: Windows, macOS, or Linux
- **Memory**: 512MB RAM minimum
- **Storage**: 100MB free space

## Package Managers

### Using pip

```bash
# Install from PyPI
pip install chronicler-client

# Install with extras
pip install chronicler-client[mcp,dev]

# Install specific version
pip install chronicler-client==0.1.0
```

### Using uv (Recommended)

```bash
# Install uv if not already installed
pip install uv

# Add to project
uv add chronicler-client

# Add with extras
uv add "chronicler-client[mcp,dev]"
```

### Using Poetry

```bash
# Add to project
poetry add chronicler-client

# Add with extras
poetry add "chronicler-client[mcp,dev]"
```

## Development Installation

```bash
# Clone repository
git clone https://github.com/chronicler-foundation/chronicler.git
cd chronicler/client

# Install in development mode
pip install -e .

# Or with uv
uv sync --dev
```

## Dependencies

### Required Dependencies

- `dspy` - DSPy framework
- `web3` - Ethereum interaction
- `pydantic` - Data validation
- `fastapi` - Web framework
- `fastapi-mcp` - MCP integration

### Optional Dependencies

- `uvicorn` - ASGI server
- `httpx` - HTTP client
- `pytest` - Testing framework

## Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Verification

```python
# Test installation
import chronicler_client.agents
print("✅ Installation successful!")
```

## Troubleshooting

### Common Issues

1. **Import Error**: Ensure Python 3.10+
2. **Missing Dependencies**: Install with `[mcp]` extras
3. **Permission Errors**: Use virtual environment

### Getting Help

- [Common Issues](../../troubleshooting/common-issues.md)
- [GitHub Issues](https://github.com/chronicler-foundation/chronicler/issues)