# Chronicler Layer

The blockchain layer of the Chronicler system, providing on-chain audit logging, access control, and registry management for AI agent actions.

## Architecture

The Chronicler Layer consists of three main smart contracts and supporting TypeScript services:

### Smart Contracts

1. **ChroniclerRegistry** - Central registry for agents, tools, and categories
2. **ChroniclerAuditLog** - Efficient on-chain audit logging with batch commitments
3. **ChroniclerAccessControl** - Fine-grained permission management with rate limiting

### Services

1. **IndexerService** - Processes blockchain events and stores them in Supabase
2. **OracleService** - Provides off-chain data verification and multi-sig confirmation
3. **DashboardService** - Web API for monitoring and compliance reporting

## Quick Start

### Prerequisites

- Node.js 18+ or Bun 1.0+
- Hardhat for smart contract development
- Supabase account for database
- IPFS gateway access

### Installation

```bash
# Install dependencies
bun install

# Copy environment file
cp env.example .env

# Edit environment variables
nano .env
```

### Environment Configuration

```env
# Network Configuration
CHAIN_ID=1
RPC_URL=http://localhost:8545
REGISTRY_ADDRESS=0x...
AUDIT_LOG_ADDRESS=0x...
ACCESS_CONTROL_ADDRESS=0x...

# Database Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key

# Service Configuration
IPFS_GATEWAY=https://ipfs.io
DASHBOARD_PORT=3000
```

### Smart Contract Deployment

```bash
# Compile contracts
bun run compile

# Deploy to local network
bun run deploy

# Deploy to testnet/mainnet
bun run deploy --network sepolia
```

### Running Services

```bash
# Start all services
bun run dev

# Start individual services
bun run indexer
bun run dashboard
bun run oracle
```

## Smart Contracts

### ChroniclerRegistry

The central registry manages agents, tools, and categories with comprehensive validation and access control.

**Key Features:**
- Agent registration and management
- Tool registration with risk levels
- Category management with risk multipliers
- Role-based access control
- Enumeration and querying capabilities

**Usage Example:**
```typescript
import { ChroniclerRegistry } from './source/contracts/ChroniclerRegistry';

const registry = new ChroniclerRegistry(address, abi, provider, signer);

// Register an agent
await registry.registerAgent(agentId, operator, metadataURI);

// Get agent information
const agent = await registry.getAgent(agentId);

// Check if agent is valid
const isValid = await registry.isValidAgent(agentId);
```

### ChroniclerAuditLog

Efficient on-chain audit logging with batch commitments and Merkle tree verification.

**Key Features:**
- Gas-optimized action logging
- Batch processing with Merkle roots
- IPFS integration for detailed logs
- Action status management
- Verification capabilities

**Usage Example:**
```typescript
import { ChroniclerAuditLog } from './source/contracts/ChroniclerAuditLog';

const auditLog = new ChroniclerAuditLog(address, abi, provider, signer);

// Log an action
await auditLog.logAction(actionId, agentId, toolId, dataHash, status, gasUsed);

// Commit a batch
await auditLog.commitBatch(ipfsHash);

// Verify action inclusion
const isValid = await auditLog.verifyActionInBatch(batchId, actionIndex, merkleProof);
```

### ChroniclerAccessControl

Fine-grained permission management with rate limiting and risk controls.

**Key Features:**
- Policy-based access control
- Rate limiting per agent
- Risk level validation
- Cooldown periods
- Daily action limits

**Usage Example:**
```typescript
import { ChroniclerAccessControl } from './source/contracts/ChroniclerAccessControl';

const accessControl = new ChroniclerAccessControl(address, abi, provider, signer);

// Create a policy
const policyId = await accessControl.createPolicy(dailyLimit, maxGas, maxRisk, cooldownPeriod);

// Assign policy to agent
await accessControl.assignPolicyToAgent(agentId, policyId);

// Check if action is allowed
const [isAllowed, reason] = await accessControl.checkActionAllowed(agentId, toolId, gasUsed);
```

## Services

### IndexerService

Processes blockchain events and stores them in Supabase for efficient querying and analytics.

**Features:**
- Real-time event processing
- Batch IPFS uploads
- Event categorization
- Database optimization

**Configuration:**
```typescript
const indexerConfig = {
  batchSize: 100,
  maxBatchSize: 1000,
  commitInterval: 30000,
  ipfsGateway: 'https://ipfs.io'
};
```

### OracleService

Provides off-chain data verification and multi-sig confirmation for critical actions.

**Features:**
- Multi-sig validation
- Signature verification
- Consensus mechanisms
- Validation tracking

**Configuration:**
```typescript
const oracleConfig = {
  minConfirmations: 3,
  maxRetries: 5,
  retryDelay: 1000,
  timeout: 30000
};
```

### DashboardService

Web API for monitoring and compliance reporting with comprehensive analytics.

**Features:**
- RESTful API endpoints
- Real-time analytics
- Compliance reporting
- Rate limiting
- Security middleware

**Configuration:**
```typescript
const dashboardConfig = {
  port: 3000,
  cors: true,
  rateLimit: 100,
  auth: false
};
```

## API Endpoints

### Registry Endpoints

- `GET /api/agents` - Get all agents
- `GET /api/agents/:id` - Get specific agent
- `GET /api/tools` - Get all tools
- `GET /api/tools/:id` - Get specific tool
- `GET /api/categories` - Get all categories
- `GET /api/categories/:id` - Get specific category

### Audit Log Endpoints

- `GET /api/actions` - Get actions with pagination
- `GET /api/actions/:id` - Get specific action
- `GET /api/batches` - Get batch commitments
- `GET /api/batches/:id` - Get specific batch

### Analytics Endpoints

- `GET /api/analytics/overview` - System overview
- `GET /api/analytics/agents/:agentId` - Agent analytics
- `GET /api/analytics/tools/:toolId` - Tool analytics

### Compliance Endpoints

- `GET /api/compliance/report` - Compliance report
- `GET /api/compliance/agents/:agentId` - Agent compliance

## Testing

### Running Tests

```bash
# Run all tests
bun test

# Run tests with coverage
bun test --coverage

# Run specific test file
bun test ChroniclerRegistry.test.ts

# Run tests in watch mode
bun test --watch
```

### Test Structure

```
tests/
├── contracts/           # Smart contract tests
│   ├── ChroniclerRegistry.test.ts
│   ├── ChroniclerAuditLog.test.ts
│   └── ChroniclerAccessControl.test.ts
├── services/            # Service tests
│   ├── IndexerService.test.ts
│   ├── OracleService.test.ts
│   └── DashboardService.test.ts
├── utils/               # Test utilities
│   └── test-utils.ts
└── setup.ts            # Test setup
```

### Writing Tests

```typescript
import { TestUtils } from './utils/test-utils';

describe('MyComponent', () => {
  it('should work correctly', async () => {
    const mockData = TestUtils.createMockAgent();
    expect(TestUtils.validateAgent(mockData)).toBe(true);
  });
});
```

## Development

### Code Style

- Use TypeScript for all new code
- Follow ESLint configuration
- Use Prettier for formatting
- Write comprehensive tests
- Document public APIs

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

### Building

```bash
# Build TypeScript
bun run build

# Type check
bun run type-check

# Lint code
bun run lint

# Format code
bun run format
```

## Security

### Best Practices

- Always validate inputs
- Use role-based access control
- Implement rate limiting
- Monitor for suspicious activity
- Keep dependencies updated
- Use secure random number generation
- Validate signatures and proofs

### Audit Considerations

- Gas optimization
- Reentrancy protection
- Access control validation
- Input sanitization
- Event emission
- Error handling

## Monitoring

### Metrics

- Action throughput
- Gas usage
- Error rates
- Response times
- Database performance
- IPFS upload success rate

### Alerts

- High error rates
- Service downtime
- Database connection issues
- Contract interaction failures
- Rate limit violations

## Troubleshooting

### Common Issues

1. **Contract deployment fails**
   - Check network configuration
   - Verify gas limits
   - Ensure sufficient funds

2. **Service startup fails**
   - Verify environment variables
   - Check database connectivity
   - Validate contract addresses

3. **High gas usage**
   - Optimize batch sizes
   - Review contract interactions
   - Consider off-chain processing

### Debug Mode

```bash
# Enable debug logging
DEBUG=chronicler:* bun run dev

# Check service status
curl http://localhost:3000/health
```

## License

MIT License - see LICENSE file for details.