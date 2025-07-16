# Deployment

Production deployment guides for Chronicler.

## Overview

Deploy Chronicler components to production environments.

## Components

- **[Smart Contracts](./smart-contracts.md)** - Contract deployment
- **[Client](./client.md)** - Client deployment
- **[Services](./services.md)** - Service deployment
- **[Monitoring](./monitoring.md)** - Production monitoring

## Quick Deployment

### 1. Deploy Contracts

```bash
cd chronicler/layer
bun run deploy --network mainnet
```

### 2. Configure Client

```env
REGISTRY_ADDRESS=0x...
AUDIT_LOG_ADDRESS=0x...
ACCESS_CONTROL_ADDRESS=0x...
```

### 3. Deploy Services

```bash
bun run dashboard
bun run indexer
bun run oracle
```

## Production Checklist

- [ ] Smart contracts deployed and verified
- [ ] Environment variables configured
- [ ] Database setup complete
- [ ] IPFS gateway configured
- [ ] Monitoring enabled
- [ ] Security audit completed
- [ ] Backup strategy implemented
- [ ] Load testing performed

## Security Considerations

- Use secure private keys
- Enable rate limiting
- Monitor for suspicious activity
- Regular security updates
- Access control implementation