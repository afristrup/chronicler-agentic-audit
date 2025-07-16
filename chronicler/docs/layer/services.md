# Services

TypeScript services for the Chronicler layer.

## IndexerService

Processes blockchain events and stores them in Supabase.

**Features:**
- Real-time event processing
- Batch IPFS uploads
- Event categorization
- Database optimization

**Configuration:**
```typescript
const config = {
  batchSize: 100,
  maxBatchSize: 1000,
  commitInterval: 30000,
  ipfsGateway: 'https://ipfs.io'
};
```

**Usage:**
```bash
bun run indexer
```

## OracleService

Provides off-chain data verification and multi-sig confirmation.

**Features:**
- Multi-sig validation
- Signature verification
- Consensus mechanisms
- Validation tracking

**Configuration:**
```typescript
const config = {
  minConfirmations: 3,
  maxRetries: 5,
  retryDelay: 1000,
  timeout: 30000
};
```

**Usage:**
```bash
bun run oracle
```

## DashboardService

Web API for monitoring and compliance reporting.

**Features:**
- RESTful API endpoints
- Real-time analytics
- Compliance reporting
- Rate limiting
- Security middleware

**Configuration:**
```typescript
const config = {
  port: 3000,
  cors: true,
  rateLimit: 100,
  auth: false
};
```

**Usage:**
```bash
bun run dashboard
```

## API Endpoints

### Registry
- `GET /api/agents` - Get all agents
- `GET /api/agents/:id` - Get specific agent
- `GET /api/tools` - Get all tools
- `GET /api/tools/:id` - Get specific tool

### Audit Log
- `GET /api/actions` - Get actions with pagination
- `GET /api/actions/:id` - Get specific action
- `GET /api/batches` - Get batch commitments

### Analytics
- `GET /api/analytics/overview` - System overview
- `GET /api/analytics/agents/:agentId` - Agent analytics
- `GET /api/analytics/tools/:toolId` - Tool analytics