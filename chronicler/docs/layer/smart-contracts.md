# Smart Contracts

Detailed smart contract documentation and interfaces.

## ChroniclerRegistry

Central registry for agents, tools, and categories.

### Key Functions

```solidity
function registerAgent(
    string memory agentId,
    address operator,
    string memory metadataURI
) external returns (bool);

function registerTool(
    string memory toolId,
    uint8 riskLevel,
    string memory metadataURI
) external returns (bool);

function getAgent(string memory agentId)
    external view returns (Agent memory);

function isValidAgent(string memory agentId)
    external view returns (bool);
```

### Events

```solidity
event AgentRegistered(
    string indexed agentId,
    address indexed operator,
    string metadataURI
);

event ToolRegistered(
    string indexed toolId,
    uint8 riskLevel,
    string metadataURI
);
```

## ChroniclerAuditLog

Efficient on-chain audit logging with batch processing.

### Key Functions

```solidity
function logAction(
    string memory actionId,
    string memory agentId,
    string memory toolId,
    bytes32 dataHash,
    ActionStatus status
) external returns (bool);

function commitBatch(string memory ipfsHash)
    external returns (uint256);

function verifyActionInBatch(
    uint256 batchId,
    uint256 actionIndex,
    bytes32[] memory merkleProof
) external view returns (bool);
```

### Events

```solidity
event ActionLogged(
    string indexed actionId,
    string indexed agentId,
    string indexed toolId,
    uint256 timestamp
);

event BatchCommitted(
    uint256 indexed batchId,
    string ipfsHash,
    bytes32 merkleRoot
);
```

## ChroniclerAccessControl

Fine-grained permission management with rate limiting.

### Key Functions

```solidity
function createPolicy(
    uint256 dailyLimit,
    uint256 maxGas,
    uint8 maxRisk,
    uint256 cooldownPeriod
) external returns (uint256);

function assignPolicyToAgent(
    string memory agentId,
    uint256 policyId
) external returns (bool);

function checkActionAllowed(
    string memory agentId,
    string memory toolId,
    uint256 gasUsed
) external view returns (bool, string memory);
```

### Events

```solidity
event PolicyCreated(
    uint256 indexed policyId,
    uint256 dailyLimit,
    uint256 maxGas
);

event PolicyAssigned(
    string indexed agentId,
    uint256 indexed policyId
);
```

## Gas Optimization

- **Batch processing** - Group multiple actions
- **Merkle trees** - Efficient verification
- **IPFS integration** - Off-chain storage
- **Optimized storage** - Packed structs

## Security Features

- **Access control** - Role-based permissions
- **Reentrancy protection** - Secure patterns
- **Input validation** - Parameter checking
- **Emergency pause** - Circuit breakers