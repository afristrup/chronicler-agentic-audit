# API

Service API documentation and endpoints.

## Dashboard Service API

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

### Registry Endpoints

#### Get All Agents

```http
GET /api/agents?page=1&limit=10
```

**Response:**
```json
{
  "agents": [
    {
      "id": "agent_001",
      "operator": "0x...",
      "metadata_uri": "ipfs://...",
      "created_at": "2024-01-01T00:00:00Z",
      "status": "active"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100
  }
}
```

#### Get Agent

```http
GET /api/agents/{agentId}
```

#### Register Agent

```http
POST /api/agents
Content-Type: application/json

{
  "agent_id": "agent_001",
  "operator": "0x...",
  "metadata_uri": "ipfs://..."
}
```

### Audit Log Endpoints

#### Get Actions

```http
GET /api/actions?agent_id=agent_001&page=1&limit=10
```

**Response:**
```json
{
  "actions": [
    {
      "id": "action_001",
      "agent_id": "agent_001",
      "tool_id": "text_processor",
      "status": "success",
      "timestamp": "2024-01-01T00:00:00Z",
      "gas_used": 50000,
      "tx_hash": "0x..."
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 1000
  }
}
```

#### Get Action

```http
GET /api/actions/{actionId}
```

#### Get Batches

```http
GET /api/batches?page=1&limit=10
```

### Analytics Endpoints

#### System Overview

```http
GET /api/analytics/overview
```

**Response:**
```json
{
  "total_agents": 150,
  "total_tools": 75,
  "total_actions": 10000,
  "actions_today": 500,
  "gas_used_today": 25000000,
  "success_rate": 0.98
}
```

#### Agent Analytics

```http
GET /api/analytics/agents/{agentId}
```

#### Tool Analytics

```http
GET /api/analytics/tools/{toolId}
```

### Compliance Endpoints

#### Compliance Report

```http
GET /api/compliance/report?start_date=2024-01-01&end_date=2024-01-31
```

#### Agent Compliance

```http
GET /api/compliance/agents/{agentId}
```

## Indexer Service API

### Status

```http
GET /status
```

### Metrics

```http
GET /metrics
```

## Oracle Service API

### Validation Status

```http
GET /validation/{actionId}
```

### Submit Validation

```http
POST /validation
Content-Type: application/json

{
  "action_id": "action_001",
  "validators": ["0x...", "0x...", "0x..."],
  "signatures": ["0x...", "0x...", "0x..."]
}
```

## Error Responses

### Standard Error Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid agent ID format",
    "details": {
      "field": "agent_id",
      "value": "invalid_id"
    }
  }
}
```

### Common Error Codes

- `VALIDATION_ERROR` - Invalid input data
- `NOT_FOUND` - Resource not found
- `UNAUTHORIZED` - Authentication required
- `FORBIDDEN` - Insufficient permissions
- `RATE_LIMITED` - Rate limit exceeded
- `INTERNAL_ERROR` - Server error

## Rate Limiting

- **Default limit**: 100 requests per minute
- **Headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- **Response**: 429 Too Many Requests when exceeded

## Authentication

Currently, the API supports:

- **No authentication** - Public endpoints
- **API key** - For privileged operations (future)
- **JWT tokens** - For user-specific data (future)