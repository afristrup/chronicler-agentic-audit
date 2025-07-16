# Services

Off-chain services architecture and design.

## Overview

Chronicler services provide off-chain processing, indexing, and monitoring capabilities.

## Service Components

### IndexerService
- **Purpose** - Process blockchain events and store in database
- **Features** - Real-time indexing, batch processing, IPFS integration
- **Data Flow** - Events → Processing → Database → Analytics

### OracleService
- **Purpose** - Provide off-chain data verification
- **Features** - Multi-sig validation, consensus mechanisms
- **Security** - Signature verification, stake-based validation

### DashboardService
- **Purpose** - Web API for monitoring and compliance
- **Features** - RESTful endpoints, real-time analytics
- **Security** - Rate limiting, authentication, CORS

## Service Communication

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Indexer    │    │   Oracle    │    │  Dashboard  │
│  Service    │    │  Service    │    │  Service    │
└─────┬───────┘    └─────┬───────┘    └─────┬───────┘
      │                  │                  │
      └──────────────────┼──────────────────┘
                         │
              ┌──────────┴──────────┐
              │     Database        │
              │   (Supabase)        │
              └─────────────────────┘
```

## Data Flow

1. **Event Capture** - Blockchain events captured by indexer
2. **Processing** - Events processed and enriched
3. **Storage** - Data stored in Supabase
4. **Verification** - Oracle validates critical data
5. **Analytics** - Dashboard provides insights

## Configuration

### Indexer
```typescript
{
  batchSize: 100,
  maxBatchSize: 1000,
  commitInterval: 30000,
  ipfsGateway: 'https://ipfs.io'
}
```

### Oracle
```typescript
{
  minConfirmations: 3,
  maxRetries: 5,
  retryDelay: 1000,
  timeout: 30000
}
```

### Dashboard
```typescript
{
  port: 3000,
  cors: true,
  rateLimit: 100,
  auth: false
}
```

## Monitoring

- **Health checks** - Service status monitoring
- **Metrics** - Performance and usage metrics
- **Alerts** - Error and performance alerts
- **Logging** - Structured logging with levels