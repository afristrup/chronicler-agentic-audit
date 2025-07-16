import { ethers } from 'ethers';
import { ActionLog, ActionStatus, BatchCommitment } from '../types';

export class ChroniclerAuditLog {
    private contract: ethers.Contract;
    private provider: ethers.Provider;
    private signer?: ethers.Signer;

    constructor(
        address: string,
        abi: any,
        provider: ethers.Provider,
        signer?: ethers.Signer
    ) {
        this.contract = new ethers.Contract(address, abi, signer || provider);
        this.provider = provider;
        this.signer = signer;
    }

    // Core logging functions
    async logAction(
        actionId: string,
        agentId: string,
        toolId: string,
        dataHash: string,
        status: ActionStatus,
        gasUsed: number
    ): Promise<ethers.ContractTransaction> {
        return this.contract.logAction(actionId, agentId, toolId, dataHash, status, gasUsed);
    }

    async commitBatch(ipfsHash: string): Promise<ethers.ContractTransaction> {
        return this.contract.commitBatch(ipfsHash);
    }

    async forceCommitBatch(ipfsHash: string): Promise<ethers.ContractTransaction> {
        return this.contract.forceCommitBatch(ipfsHash);
    }

    async updateActionStatus(
        actionIndex: number,
        newStatus: ActionStatus
    ): Promise<ethers.ContractTransaction> {
        return this.contract.updateActionStatus(actionIndex, newStatus);
    }

    // Query functions
    async getActionLog(actionIndex: number): Promise<ActionLog> {
        const action = await this.contract.getActionLog(actionIndex);
        return {
            actionId: action.actionId,
            agentId: action.agentId,
            toolId: action.toolId,
            dataHash: action.dataHash,
            timestamp: Number(action.timestamp),
            status: Number(action.status) as ActionStatus,
            gasUsed: Number(action.gasUsed),
            batchId: Number(action.batchId)
        };
    }

    async getBatchCommitment(batchId: number): Promise<BatchCommitment> {
        const batch = await this.contract.getBatchCommitment(batchId);
        return {
            merkleRoot: batch.merkleRoot,
            startIndex: Number(batch.startIndex),
            endIndex: Number(batch.endIndex),
            timestamp: Number(batch.timestamp),
            ipfsHash: batch.ipfsHash,
            actionCount: Number(batch.actionCount),
            isCommitted: batch.isCommitted
        };
    }

    async getAgentActionIndices(agentId: string): Promise<number[]> {
        const indices = await this.contract.getAgentActionIndices(agentId);
        return indices.map((index: any) => Number(index));
    }

    async getToolActionIndices(toolId: string): Promise<number[]> {
        const indices = await this.contract.getToolActionIndices(toolId);
        return indices.map((index: any) => Number(index));
    }

    async getPendingActionsCount(): Promise<number> {
        const count = await this.contract.getPendingActionsCount();
        return Number(count);
    }

    // Verification functions
    async verifyActionInBatch(
        batchId: number,
        actionIndex: number,
        merkleProof: string[]
    ): Promise<boolean> {
        return this.contract.verifyActionInBatch(batchId, actionIndex, merkleProof);
    }

    // Counter functions
    async getActionCounter(): Promise<number> {
        const counter = await this.contract.actionCounter();
        return Number(counter);
    }

    async getBatchCounter(): Promise<number> {
        const counter = await this.contract.batchCounter();
        return Number(counter);
    }

    // Constants
    async getBatchSize(): Promise<number> {
        const size = await this.contract.BATCH_SIZE();
        return Number(size);
    }

    async getMaxBatchSize(): Promise<number> {
        const size = await this.contract.MAX_BATCH_SIZE();
        return Number(size);
    }

    // Admin functions
    async pause(): Promise<ethers.ContractTransaction> {
        return this.contract.pause();
    }

    async unpause(): Promise<ethers.ContractTransaction> {
        return this.contract.unpause();
    }

    // Role management
    async hasRole(role: string, account: string): Promise<boolean> {
        return this.contract.hasRole(role, account);
    }

    async grantRole(role: string, account: string): Promise<ethers.ContractTransaction> {
        return this.contract.grantRole(role, account);
    }

    async revokeRole(role: string, account: string): Promise<ethers.ContractTransaction> {
        return this.contract.revokeRole(role, account);
    }

    // Event listeners
    onActionLogged(
        callback: (
            actionIndex: number,
            agentId: string,
            toolId: string,
            actionId: string,
            status: number,
            gasUsed: number
        ) => void
    ): void {
        this.contract.on('ActionLogged', callback);
    }

    onBatchCommitted(
        callback: (
            batchId: number,
            merkleRoot: string,
            startIndex: number,
            endIndex: number,
            ipfsHash: string,
            actionCount: number
        ) => void
    ): void {
        this.contract.on('BatchCommitted', callback);
    }

    onActionStatusUpdated(
        callback: (actionIndex: number, oldStatus: number, newStatus: number) => void
    ): void {
        this.contract.on('ActionStatusUpdated', callback);
    }

    // Get contract instance
    getContract(): ethers.Contract {
        return this.contract;
    }

    // Get contract address
    getAddress(): string {
        return this.contract.target as string;
    }

    // Get registry address
    async getRegistry(): Promise<string> {
        return this.contract.registry();
    }

    // Provider-based functions
    async getBlockNumber(): Promise<number> {
        return await this.provider.getBlockNumber();
    }

    async getBlockTimestamp(): Promise<number> {
        const block = await this.provider.getBlock('latest');
        return block?.timestamp || 0;
    }

    async waitForTransaction(txHash: string, confirmations: number = 1): Promise<ethers.TransactionReceipt | null> {
        return await this.provider.waitForTransaction(txHash, confirmations);
    }

    // Signer-based functions
    async getSignerAddress(): Promise<string | null> {
        if (!this.signer) {
            return null;
        }
        return await this.signer.getAddress();
    }

    async hasSigner(): Promise<boolean> {
        return this.signer !== undefined;
    }

    async signMessage(message: string): Promise<string> {
        if (!this.signer) {
            throw new Error('No signer available');
        }
        return await this.signer.signMessage(message);
    }

    // Enhanced logging functions with signer
    async logActionWithGasLimit(
        actionId: string,
        agentId: string,
        toolId: string,
        dataHash: string,
        status: ActionStatus,
        gasUsed: number,
        gasLimit: bigint
    ): Promise<ethers.ContractTransaction> {
        if (!this.signer) {
            throw new Error('No signer available');
        }
        return this.contract.logAction(actionId, agentId, toolId, dataHash, status, gasUsed, { gasLimit });
    }

    async commitBatchWithGasLimit(ipfsHash: string, gasLimit: bigint): Promise<ethers.ContractTransaction> {
        if (!this.signer) {
            throw new Error('No signer available');
        }
        return this.contract.commitBatch(ipfsHash, { gasLimit });
    }

    // Gas estimation functions
    async estimateLogActionGas(
        actionId: string,
        agentId: string,
        toolId: string,
        dataHash: string,
        status: ActionStatus,
        gasUsed: number
    ): Promise<bigint> {
        return await this.contract.logAction.estimateGas(actionId, agentId, toolId, dataHash, status, gasUsed);
    }

    async estimateCommitBatchGas(ipfsHash: string): Promise<bigint> {
        return await this.contract.commitBatch.estimateGas(ipfsHash);
    }

    // Batch operations with signer
    async batchLogActions(actions: Array<{
        actionId: string;
        agentId: string;
        toolId: string;
        dataHash: string;
        status: ActionStatus;
        gasUsed: number;
    }>): Promise<ethers.ContractTransaction[]> {
        if (!this.signer) {
            throw new Error('No signer available');
        }

        const transactions: ethers.ContractTransaction[] = [];
        for (const action of actions) {
            const tx = await this.logAction(
                action.actionId,
                action.agentId,
                action.toolId,
                action.dataHash,
                action.status,
                action.gasUsed
            );
            transactions.push(tx);
        }
        return transactions;
    }

    // Enhanced query functions
    async getRecentActions(limit: number = 100): Promise<ActionLog[]> {
        const actionCounter = await this.getActionCounter();
        const actions: ActionLog[] = [];

        const startIndex = Math.max(0, actionCounter - limit);
        for (let i = startIndex; i < actionCounter; i++) {
            try {
                const action = await this.getActionLog(i);
                actions.push(action);
            } catch (error) {
                continue;
            }
        }

        return actions;
    }

    async getRecentBatches(limit: number = 50): Promise<BatchCommitment[]> {
        const batchCounter = await this.getBatchCounter();
        const batches: BatchCommitment[] = [];

        const startIndex = Math.max(0, batchCounter - limit);
        for (let i = startIndex; i < batchCounter; i++) {
            try {
                const batch = await this.getBatchCommitment(i);
                batches.push(batch);
            } catch (error) {
                continue;
            }
        }

        return batches;
    }

    // Statistics functions
    async getAuditStats(): Promise<{
        totalActions: number;
        totalBatches: number;
        pendingActions: number;
        lastActionTime: number;
        lastBatchTime: number;
    }> {
        const totalActions = await this.getActionCounter();
        const totalBatches = await this.getBatchCounter();
        const pendingActions = await this.getPendingActionsCount();

        const recentActions = await this.getRecentActions(1);
        const recentBatches = await this.getRecentBatches(1);

        return {
            totalActions,
            totalBatches,
            pendingActions,
            lastActionTime: recentActions.length > 0 ? recentActions[0].timestamp : 0,
            lastBatchTime: recentBatches.length > 0 ? recentBatches[0].timestamp : 0
        };
    }

    // Validation functions
    async validateActionLog(actionIndex: number): Promise<[boolean, string]> {
        try {
            const action = await this.getActionLog(actionIndex);
            if (!action.actionId || action.actionId === '0x0000000000000000000000000000000000000000000000000000000000000000') {
                return [false, 'Invalid action ID'];
            }
            return [true, 'Action log is valid'];
        } catch (error) {
            return [false, 'Action log not found'];
        }
    }

    async validateBatchCommitment(batchId: number): Promise<[boolean, string]> {
        try {
            const batch = await this.getBatchCommitment(batchId);
            if (!batch.isCommitted) {
                return [false, 'Batch not committed'];
            }
            return [true, 'Batch commitment is valid'];
        } catch (error) {
            return [false, 'Batch commitment not found'];
        }
    }
}