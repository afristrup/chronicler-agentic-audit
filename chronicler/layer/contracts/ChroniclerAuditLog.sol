// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/utils/Pausable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "./interfaces/IChroniclerRegistry.sol";

/**
 * @title ChroniclerAuditLog
 * @dev Efficient on-chain audit logging with batch commitments and Merkle tree verification
 */
contract ChroniclerAuditLog is Pausable, ReentrancyGuard, AccessControl {
    IChroniclerRegistry public immutable registry;

    bytes32 public constant LOGGER_ROLE = keccak256("LOGGER_ROLE");
    bytes32 public constant BATCH_COMMITTER_ROLE =
        keccak256("BATCH_COMMITTER_ROLE");

    struct ActionLog {
        bytes32 actionId;
        bytes32 agentId;
        bytes32 toolId;
        bytes32 dataHash; // Hash of input/output stored off-chain
        uint256 timestamp;
        uint8 status; // 0: pending, 1: success, 2: failed, 3: cancelled
        uint256 gasUsed;
        uint256 batchId; // Reference to batch commitment
    }

    struct BatchCommitment {
        bytes32 merkleRoot;
        uint256 startIndex;
        uint256 endIndex;
        uint256 timestamp;
        string ipfsHash; // Detailed logs stored in IPFS
        uint256 actionCount;
        bool isCommitted;
    }

    struct MerkleLeaf {
        bytes32 actionId;
        bytes32 agentId;
        bytes32 toolId;
        bytes32 dataHash;
        uint256 timestamp;
        uint8 status;
        uint256 gasUsed;
    }

    // Storage mappings
    mapping(uint256 => ActionLog) public actionLogs;
    mapping(bytes32 => uint256[]) public agentActionIndices;
    mapping(bytes32 => uint256[]) public toolActionIndices;
    mapping(uint256 => BatchCommitment) public batchCommitments;

    // Counters and state
    uint256 public actionCounter;
    uint256 public batchCounter;
    uint256 public constant BATCH_SIZE = 100;
    uint256 public constant MAX_BATCH_SIZE = 1000;

    // Pending actions for batch processing
    bytes32[] private pendingActions;
    mapping(bytes32 => uint256) private pendingActionIndices;

    // Events
    event ActionLogged(
        uint256 indexed actionIndex,
        bytes32 indexed agentId,
        bytes32 indexed toolId,
        bytes32 actionId,
        uint8 status,
        uint256 gasUsed
    );

    event BatchCommitted(
        uint256 indexed batchId,
        bytes32 merkleRoot,
        uint256 startIndex,
        uint256 endIndex,
        string ipfsHash,
        uint256 actionCount
    );

    event ActionStatusUpdated(
        uint256 indexed actionIndex,
        uint8 oldStatus,
        uint8 newStatus
    );

    constructor(address _registry) {
        require(_registry != address(0), "Invalid registry address");
        registry = IChroniclerRegistry(_registry);

        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(LOGGER_ROLE, msg.sender);
        _grantRole(BATCH_COMMITTER_ROLE, msg.sender);
    }

    /**
     * @dev Log a single action - optimized for gas efficiency
     */
    function logAction(
        bytes32 actionId,
        bytes32 agentId,
        bytes32 toolId,
        bytes32 dataHash,
        uint8 status,
        uint256 gasUsed
    ) external onlyRole(LOGGER_ROLE) whenNotPaused nonReentrant {
        require(registry.isValidAgent(agentId), "Invalid agent");
        require(registry.isValidTool(toolId), "Invalid tool");
        require(status <= 3, "Invalid status");
        require(actionId != bytes32(0), "Invalid action ID");
        require(dataHash != bytes32(0), "Invalid data hash");

        uint256 actionIndex = actionCounter++;

        ActionLog memory newAction = ActionLog({
            actionId: actionId,
            agentId: agentId,
            toolId: toolId,
            dataHash: dataHash,
            timestamp: block.timestamp,
            status: status,
            gasUsed: gasUsed,
            batchId: 0 // Will be set when batch is committed
        });

        actionLogs[actionIndex] = newAction;
        agentActionIndices[agentId].push(actionIndex);
        toolActionIndices[toolId].push(actionIndex);

        // Add to pending actions for batch processing
        pendingActions.push(actionId);
        pendingActionIndices[actionId] = actionIndex;

        // Update registry statistics
        registry.incrementAgentActions(agentId);
        registry.incrementToolUsage(toolId);

        emit ActionLogged(
            actionIndex,
            agentId,
            toolId,
            actionId,
            status,
            gasUsed
        );

        // Auto-commit batch if threshold reached
        if (pendingActions.length >= BATCH_SIZE) {
            _commitBatch();
        }
    }

    /**
     * @dev Commit a batch of actions with Merkle root
     */
    function commitBatch(
        string calldata ipfsHash
    ) external onlyRole(BATCH_COMMITTER_ROLE) whenNotPaused {
        require(pendingActions.length > 0, "No pending actions");
        require(bytes(ipfsHash).length > 0, "IPFS hash required");

        _commitBatchWithHash(ipfsHash);
    }

    /**
     * @dev Force commit batch (admin only)
     */
    function forceCommitBatch(
        string calldata ipfsHash
    ) external onlyRole(DEFAULT_ADMIN_ROLE) {
        require(bytes(ipfsHash).length > 0, "IPFS hash required");
        _commitBatchWithHash(ipfsHash);
    }

    /**
     * @dev Update action status
     */
    function updateActionStatus(
        uint256 actionIndex,
        uint8 newStatus
    ) external onlyRole(LOGGER_ROLE) {
        require(actionIndex < actionCounter, "Invalid action index");
        require(newStatus <= 3, "Invalid status");

        uint8 oldStatus = actionLogs[actionIndex].status;
        require(oldStatus != newStatus, "Status already set");

        actionLogs[actionIndex].status = newStatus;

        emit ActionStatusUpdated(actionIndex, oldStatus, newStatus);
    }

    /**
     * @dev Verify action inclusion in batch using Merkle proof
     */
    function verifyActionInBatch(
        uint256 batchId,
        uint256 actionIndex,
        bytes32[] calldata merkleProof
    ) external view returns (bool) {
        require(batchId < batchCounter, "Invalid batch ID");
        require(actionIndex < actionCounter, "Invalid action index");

        BatchCommitment memory batch = batchCommitments[batchId];
        require(batch.isCommitted, "Batch not committed");
        require(
            actionIndex >= batch.startIndex && actionIndex <= batch.endIndex,
            "Action not in batch"
        );

        ActionLog memory action = actionLogs[actionIndex];
        bytes32 leaf = _hashAction(action);

        return MerkleProof.verify(merkleProof, batch.merkleRoot, leaf);
    }

    /**
     * @dev Get action log by index
     */
    function getActionLog(
        uint256 actionIndex
    ) external view returns (ActionLog memory) {
        require(actionIndex < actionCounter, "Invalid action index");
        return actionLogs[actionIndex];
    }

    /**
     * @dev Get batch commitment by ID
     */
    function getBatchCommitment(
        uint256 batchId
    ) external view returns (BatchCommitment memory) {
        require(batchId < batchCounter, "Invalid batch ID");
        return batchCommitments[batchId];
    }

    /**
     * @dev Get agent action indices
     */
    function getAgentActionIndices(
        bytes32 agentId
    ) external view returns (uint256[] memory) {
        return agentActionIndices[agentId];
    }

    /**
     * @dev Get tool action indices
     */
    function getToolActionIndices(
        bytes32 toolId
    ) external view returns (uint256[] memory) {
        return toolActionIndices[toolId];
    }

    /**
     * @dev Get pending actions count
     */
    function getPendingActionsCount() external view returns (uint256) {
        return pendingActions.length;
    }

    // ============ INTERNAL FUNCTIONS ============

    function _commitBatch() private {
        _commitBatchWithHash("");
    }

    function _commitBatchWithHash(string memory ipfsHash) private {
        require(pendingActions.length > 0, "No pending actions to commit");

        uint256 startIndex = actionCounter - pendingActions.length;
        uint256 endIndex = actionCounter - 1;

        // Build Merkle tree from actions
        bytes32[] memory leaves = new bytes32[](pendingActions.length);
        for (uint256 i = 0; i < pendingActions.length; i++) {
            uint256 actionIndex = startIndex + i;
            ActionLog memory action = actionLogs[actionIndex];
            leaves[i] = _hashAction(action);

            // Update action with batch ID
            actionLogs[actionIndex].batchId = batchCounter;
        }

        bytes32 merkleRoot = _computeMerkleRoot(leaves);

        BatchCommitment memory newBatch = BatchCommitment({
            merkleRoot: merkleRoot,
            startIndex: startIndex,
            endIndex: endIndex,
            timestamp: block.timestamp,
            ipfsHash: ipfsHash,
            actionCount: pendingActions.length,
            isCommitted: true
        });

        batchCommitments[batchCounter] = newBatch;

        emit BatchCommitted(
            batchCounter,
            merkleRoot,
            startIndex,
            endIndex,
            ipfsHash,
            pendingActions.length
        );

        batchCounter++;

        // Clear pending actions
        delete pendingActions;
    }

    function _hashAction(
        ActionLog memory action
    ) private pure returns (bytes32) {
        return
            keccak256(
                abi.encodePacked(
                    action.actionId,
                    action.agentId,
                    action.toolId,
                    action.dataHash,
                    action.timestamp,
                    action.status,
                    action.gasUsed
                )
            );
    }

    function _computeMerkleRoot(
        bytes32[] memory leaves
    ) private pure returns (bytes32) {
        if (leaves.length == 0) return bytes32(0);
        if (leaves.length == 1) return leaves[0];

        uint256 length = leaves.length;
        uint256 newLength = (length + 1) / 2;
        bytes32[] memory newLeaves = new bytes32[](newLength);

        for (uint256 i = 0; i < newLength; i++) {
            uint256 leftIndex = i * 2;
            uint256 rightIndex = leftIndex + 1;

            if (rightIndex < length) {
                newLeaves[i] = keccak256(
                    abi.encodePacked(leaves[leftIndex], leaves[rightIndex])
                );
            } else {
                newLeaves[i] = leaves[leftIndex];
            }
        }

        return _computeMerkleRoot(newLeaves);
    }

    // ============ ADMIN FUNCTIONS ============

    function pause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _pause();
    }

    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _unpause();
    }
}
