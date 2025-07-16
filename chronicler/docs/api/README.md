# API Reference

Complete API documentation for Chronicler.

## Client API

- **[Decorators](./client/decorators.md)** - Function decoration API
- **[Types](./client/types.md)** - Data structures
- **[Configuration](./client/configuration.md)** - Configuration options
- **[Services](./client/services.md)** - Service interfaces

## Layer API

- **[Smart Contracts](./layer/contracts.md)** - Contract interfaces
- **[Services](./layer/services.md)** - Service APIs
- **[Dashboard](./layer/dashboard.md)** - Dashboard endpoints

## REST Endpoints

### Registry
- `GET /api/agents` - List agents
- `GET /api/agents/:id` - Get agent
- `POST /api/agents` - Register agent
- `GET /api/tools` - List tools
- `GET /api/tools/:id` - Get tool

### Audit Log
- `GET /api/actions` - List actions
- `GET /api/actions/:id` - Get action
- `GET /api/batches` - List batches
- `GET /api/batches/:id` - Get batch

### Analytics
- `GET /api/analytics/overview` - System overview
- `GET /api/analytics/agents/:id` - Agent analytics
- `GET /api/analytics/tools/:id` - Tool analytics

### Compliance
- `GET /api/compliance/report` - Compliance report
- `GET /api/compliance/agents/:id` - Agent compliance