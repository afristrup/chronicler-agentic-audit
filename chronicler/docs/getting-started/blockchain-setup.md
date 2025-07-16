# Blockchain Setup

Deploy Chronicler smart contracts to your network.

## Prerequisites

- Node.js 18+ or Bun 1.0+
- Hardhat
- Ethereum wallet with testnet funds
- RPC endpoint (Infura, Alchemy, etc.)

## Installation

```bash
cd chronicler/layer
bun install
```

## Environment Configuration

Create `.env` file:

```env
# Network
SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/YOUR_KEY
PRIVATE_KEY=your_private_key_here

# API Keys
ETHERSCAN_API_KEY=your_etherscan_key

# Database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key

# IPFS
IPFS_URL=https://ipfs.infura.io:5001
IPFS_PROJECT_ID=your_ipfs_project_id
```

## Deployment

```bash
# Compile contracts
bun run compile

# Deploy to testnet
bun run deploy --network sepolia

# Deploy to mainnet
bun run deploy --network mainnet
```

## Contract Addresses

After deployment, save the addresses:

- Registry: `0x...`
- Audit Log: `0x...`
- Access Control: `0x...`

## Verification

```bash
# Verify on Etherscan
bun run verify --network sepolia
```