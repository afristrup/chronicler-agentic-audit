# Deployment

Smart contract deployment and configuration.

## Prerequisites

- Node.js 18+ or Bun 1.0+
- Hardhat development environment
- Ethereum wallet with testnet funds
- RPC endpoint (Infura, Alchemy, etc.)

## Environment Setup

Create `.env` file:

```env
# Network Configuration
SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/YOUR_KEY
MAINNET_RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY

# Deployment Keys
PRIVATE_KEY=your_private_key_here
DEPLOYER_PRIVATE_KEY=your_deployer_private_key_here

# API Keys
ETHERSCAN_API_KEY=your_etherscan_api_key
POLYGONSCAN_API_KEY=your_polygonscan_api_key

# Database Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key

# IPFS Configuration
IPFS_URL=https://ipfs.infura.io:5001
IPFS_PROJECT_ID=your_ipfs_project_id
```

## Deployment Steps

### 1. Compile Contracts

```bash
cd chronicler/layer
bun run compile
```

### 2. Deploy to Testnet

```bash
# Deploy to Sepolia
bun run deploy --network sepolia

# Deploy to Polygon Mumbai
bun run deploy --network mumbai
```

### 3. Deploy to Mainnet

```bash
# Deploy to Ethereum mainnet
bun run deploy --network mainnet

# Deploy to Polygon
bun run deploy --network polygon
```

## Contract Addresses

After deployment, save the addresses:

```env
# Sepolia Testnet
REGISTRY_ADDRESS=0x...
AUDIT_LOG_ADDRESS=0x...
ACCESS_CONTROL_ADDRESS=0x...

# Mainnet
REGISTRY_ADDRESS=0x...
AUDIT_LOG_ADDRESS=0x...
ACCESS_CONTROL_ADDRESS=0x...
```

## Verification

### Etherscan Verification

```bash
# Verify on Etherscan
bun run verify --network sepolia

# Verify on Polygonscan
bun run verify --network polygon
```

### Manual Verification

1. Go to contract address on block explorer
2. Click "Contract" tab
3. Click "Verify and Publish"
4. Enter contract details and source code

## Post-Deployment

### 1. Initialize Contracts

```typescript
// Set up initial roles and permissions
await registry.grantRole(ADMIN_ROLE, adminAddress);
await accessControl.createPolicy(1000, 500000, 5, 3600);
```

### 2. Configure Services

Update service configuration with new addresses:

```env
REGISTRY_ADDRESS=0x...
AUDIT_LOG_ADDRESS=0x...
ACCESS_CONTROL_ADDRESS=0x...
```

### 3. Test Integration

```bash
# Run integration tests
bun test

# Test client connection
bun run test:integration
```

## Security Checklist

- [ ] Private keys secured
- [ ] Contracts verified on block explorer
- [ ] Access control configured
- [ ] Emergency pause tested
- [ ] Gas limits optimized
- [ ] Security audit completed