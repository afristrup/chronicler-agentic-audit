# Smart Contracts

On-chain components of the Chronicler system.

## Core Contracts

### ChroniclerRegistry

Central registry for agents, tools, and categories.

**Key Functions:**
- `registerAgent(agentId, operator, metadataURI)` - Register new agent
- `registerTool(toolId, riskLevel, metadataURI)` - Register new tool
- `getAgent(agentId)` - Get agent information
- `isValidAgent(agentId)` - Check agent validity

**Events:**
- `AgentRegistered(agentId, operator, metadataURI)`
- `ToolRegistered(toolId, riskLevel, metadataURI)`

### ChroniclerAuditLog

Efficient on-chain audit logging with batch processing.

**Key Functions:**
- `logAction(actionId, agentId, toolId, dataHash, status)` - Log action
- `commitBatch(ipfsHash)` - Commit batch to IPFS
- `verifyActionInBatch(batchId, actionIndex, merkleProof)` - Verify inclusion

**Events:**
- `ActionLogged(actionId, agentId, toolId, timestamp)`
- `BatchCommitted(batchId, ipfsHash, merkleRoot)`

### ChroniclerAccessControl

Fine-grained permission management with rate limiting.

**Key Functions:**
- `createPolicy(dailyLimit, maxGas, maxRisk, cooldownPeriod)` - Create policy
- `assignPolicyToAgent(agentId, policyId)` - Assign policy
- `checkActionAllowed(agentId, toolId, gasUsed)` - Check permissions

**Events:**
- `PolicyCreated(policyId, dailyLimit, maxGas)`
- `PolicyAssigned(agentId, policyId)`

## Gas Optimization

- Batch processing reduces gas costs
- Merkle tree verification for efficiency
- IPFS integration for detailed logs
- Optimized storage patterns

## Security Features

- Role-based access control
- Reentrancy protection
- Input validation
- Emergency pause functionality