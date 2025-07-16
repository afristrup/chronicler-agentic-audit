# Layer Documentation

Blockchain layer and services for Chronicler.

## Overview

The Chronicler Layer consists of smart contracts and TypeScript services for blockchain-based audit logging.

## Components

- **[Smart Contracts](./smart-contracts.md)** - Solidity contracts
- **[Services](./services.md)** - TypeScript services
- **[Deployment](./deployment.md)** - Contract deployment
- **[API](./api.md)** - Service APIs

## Quick Start

```bash
cd chronicler/layer
bun install
cp env.example .env
# Edit .env with your configuration
bun run compile
bun run deploy --network sepolia
```

## Services

### IndexerService
Processes blockchain events and stores in Supabase.

### OracleService
Provides off-chain data verification.

### DashboardService
Web API for monitoring and analytics.

## Running Services

```bash
# Start all services
bun run dev

# Start individual services
bun run indexer
bun run dashboard
bun run oracle
```

## Testing

```bash
bun test
```