import { createClient } from '@supabase/supabase-js';
import { ethers } from 'ethers';
import { create } from 'ipfs-http-client';
import { v4 as uuidv4 } from 'uuid';
import { ChroniclerAccessControl } from '../contracts/ChroniclerAccessControl';
import { ChroniclerAuditLog } from '../contracts/ChroniclerAuditLog';
import {
    ActionData,
    ActionStatus,
    AuditEvent,
    OracleConfig
} from '../types';

export class OracleService {
    private provider: ethers.Provider;
    private auditLog: ChroniclerAuditLog;
    private accessControl: ChroniclerAccessControl;
    private supabase: any;
    private ipfs: any;
    private config: OracleConfig;
    private isRunning: boolean = false;
    private pendingValidations: Map<string, any> = new Map();

    constructor(
        provider: ethers.Provider,
        auditLog: ChroniclerAuditLog,
        accessControl: ChroniclerAccessControl,
        supabaseUrl: string,
        supabaseKey: string,
        config: OracleConfig
    ) {
        this.provider = provider;
        this.auditLog = auditLog;
        this.accessControl = accessControl;
        this.supabase = createClient(supabaseUrl, supabaseKey);
        this.ipfs = create({ url: 'https://ipfs.io' });
        this.config = config;
    }

    async start(): Promise<void> {
        if (this.isRunning) {
            throw new Error('Oracle is already running');
        }

        this.isRunning = true;
        console.log('Starting Chronicler Oracle...');

        // Set up event listeners
        this.setupEventListeners();

        // Start validation processing
        this.startValidationProcessing();

        console.log('Chronicler Oracle started successfully');
    }

    async stop(): Promise<void> {
        this.isRunning = false;
        console.log('Chronicler Oracle stopped');
    }

    private setupEventListeners(): void {
        // Listen for action logged events
        this.auditLog.onActionLogged(async (actionIndex, agentId, toolId, actionId, status, gasUsed) => {
            await this.handleActionLogged(actionIndex, agentId, toolId, actionId, status, gasUsed);
        });

        // Listen for action status updates
        this.auditLog.onActionStatusUpdated(async (actionIndex, oldStatus, newStatus) => {
            await this.handleActionStatusUpdated(actionIndex, oldStatus, newStatus);
        });
    }

    private async handleActionLogged(
        actionIndex: number,
        agentId: string,
        toolId: string,
        actionId: string,
        status: number,
        gasUsed: number
    ): Promise<void> {
        try {
            // Check access control before processing
            const [isAllowed, reason] = await this.accessControl.checkActionAllowed(agentId, toolId, gasUsed);
            if (!isAllowed) {
                console.warn(`Access denied for action ${actionId}: ${reason}`);
                return;
            }

            // Record action for rate limiting
            await this.accessControl.recordAction(agentId, gasUsed);

            // Get action data from IPFS
            const actionLog = await this.auditLog.getActionLog(actionIndex);
            const actionData = await this.getActionDataFromIPFS(actionLog.dataHash);

            // Create validation request
            const validationId = uuidv4();
            const validation = {
                id: validationId,
                actionIndex,
                actionId,
                agentId,
                toolId,
                actionData,
                status: ActionStatus.PENDING,
                confirmations: 0,
                requiredConfirmations: this.config.minConfirmations,
                createdAt: Date.now(),
                validators: []
            };

            this.pendingValidations.set(validationId, validation);

            // Store validation request
            await this.storeValidation(validation);

            console.log(`Validation request created for action: ${actionId}`);
        } catch (error) {
            console.error('Error handling action log:', error);
        }
    }

    private async handleActionStatusUpdated(
        actionIndex: number,
        oldStatus: number,
        newStatus: number
    ): Promise<void> {
        try {
            const event: AuditEvent = {
                type: 'ActionStatusUpdated',
                timestamp: Date.now(),
                data: {
                    actionIndex,
                    oldStatus,
                    newStatus
                }
            };

            await this.storeEvent(event);
            console.log(`Action status updated: ${actionIndex} from ${oldStatus} to ${newStatus}`);
        } catch (error) {
            console.error('Error handling action status update:', error);
        }
    }

    private async getActionDataFromIPFS(dataHash: string): Promise<ActionData> {
        try {
            // This is a simplified implementation
            // In a real scenario, you would decode the dataHash and fetch from IPFS
            const response = await this.ipfs.cat(dataHash);
            const data = JSON.parse(response.toString());
            return data;
        } catch (error) {
            console.error('Error fetching action data from IPFS:', error);
            throw error;
        }
    }

    private async storeValidation(validation: any): Promise<void> {
        try {
            const { error } = await this.supabase
                .from('oracle_validations')
                .insert({
                    id: validation.id,
                    action_index: validation.actionIndex,
                    action_id: validation.actionId,
                    agent_id: validation.agentId,
                    tool_id: validation.toolId,
                    action_data: validation.actionData,
                    status: validation.status,
                    confirmations: validation.confirmations,
                    required_confirmations: validation.requiredConfirmations,
                    created_at: new Date(validation.createdAt).toISOString(),
                    validators: validation.validators
                });

            if (error) {
                throw error;
            }
        } catch (error) {
            console.error('Error storing validation:', error);
            throw error;
        }
    }

    private async storeEvent(event: AuditEvent): Promise<void> {
        try {
            const { error } = await this.supabase
                .from('oracle_events')
                .insert({
                    id: uuidv4(),
                    type: event.type,
                    timestamp: new Date(event.timestamp).toISOString(),
                    data: event.data,
                    tx_hash: event.txHash,
                    block_number: event.blockNumber
                });

            if (error) {
                throw error;
            }
        } catch (error) {
            console.error('Error storing oracle event:', error);
            throw error;
        }
    }

    private startValidationProcessing(): void {
        setInterval(async () => {
            if (!this.isRunning) return;

            try {
                await this.processPendingValidations();
            } catch (error) {
                console.error('Error in validation processing:', error);
            }
        }, 5000); // Process every 5 seconds
    }

    private async processPendingValidations(): Promise<void> {
        for (const [validationId, validation] of this.pendingValidations) {
            try {
                if (validation.confirmations >= validation.requiredConfirmations) {
                    await this.finalizeValidation(validation);
                    this.pendingValidations.delete(validationId);
                }
            } catch (error) {
                console.error(`Error processing validation ${validationId}:`, error);
            }
        }
    }

    private async finalizeValidation(validation: any): Promise<void> {
        try {
            // Update validation status
            validation.status = ActionStatus.SUCCESS;

            const { error } = await this.supabase
                .from('oracle_validations')
                .update({
                    status: validation.status,
                    confirmations: validation.confirmations,
                    finalized_at: new Date().toISOString()
                })
                .eq('id', validation.id);

            if (error) {
                throw error;
            }

            // Create finalization event
            const event: AuditEvent = {
                type: 'ValidationFinalized',
                timestamp: Date.now(),
                data: {
                    validationId: validation.id,
                    actionId: validation.actionId,
                    confirmations: validation.confirmations,
                    validators: validation.validators
                }
            };

            await this.storeEvent(event);

            console.log(`Validation finalized for action: ${validation.actionId}`);
        } catch (error) {
            console.error('Error finalizing validation:', error);
            throw error;
        }
    }

    // Public methods for validators
    async submitValidation(
        validationId: string,
        validatorAddress: string,
        isValid: boolean,
        signature: string
    ): Promise<void> {
        try {
            // Verify signature
            const isValidSignature = await this.verifyValidatorSignature(
                validationId,
                validatorAddress,
                isValid,
                signature
            );

            if (!isValidSignature) {
                throw new Error('Invalid validator signature');
            }

            // Get validation
            const validation = this.pendingValidations.get(validationId);
            if (!validation) {
                throw new Error('Validation not found');
            }

            // Check if validator already confirmed
            if (validation.validators.includes(validatorAddress)) {
                throw new Error('Validator already confirmed');
            }

            // Add confirmation
            validation.confirmations++;
            validation.validators.push(validatorAddress);

            // Update database
            const { error } = await this.supabase
                .from('oracle_validations')
                .update({
                    confirmations: validation.confirmations,
                    validators: validation.validators
                })
                .eq('id', validationId);

            if (error) {
                throw error;
            }

            // Create confirmation event
            const event: AuditEvent = {
                type: 'ValidationConfirmed',
                timestamp: Date.now(),
                data: {
                    validationId,
                    validatorAddress,
                    isValid,
                    signature
                }
            };

            await this.storeEvent(event);

            console.log(`Validation confirmed by ${validatorAddress} for ${validationId}`);
        } catch (error) {
            console.error('Error submitting validation:', error);
            throw error;
        }
    }

    private async verifyValidatorSignature(
        validationId: string,
        validatorAddress: string,
        isValid: boolean,
        signature: string
    ): Promise<boolean> {
        try {
            const message = ethers.solidityPackedKeccak256(
                ['string', 'string', 'bool'],
                [validationId, validatorAddress, isValid]
            );

            const recoveredAddress = ethers.verifyMessage(ethers.getBytes(message), signature);
            return recoveredAddress.toLowerCase() === validatorAddress.toLowerCase();
        } catch (error) {
            console.error('Error verifying signature:', error);
            return false;
        }
    }

    // Query methods
    async getValidation(validationId: string): Promise<any> {
        const { data, error } = await this.supabase
            .from('oracle_validations')
            .select('*')
            .eq('id', validationId)
            .single();

        if (error) throw error;
        return data;
    }

    async getValidationsByAction(actionId: string): Promise<any[]> {
        const { data, error } = await this.supabase
            .from('oracle_validations')
            .select('*')
            .eq('action_id', actionId)
            .order('created_at', { ascending: false });

        if (error) throw error;
        return data || [];
    }

    async getPendingValidations(): Promise<any[]> {
        const { data, error } = await this.supabase
            .from('oracle_validations')
            .select('*')
            .eq('status', 'pending')
            .order('created_at', { ascending: true });

        if (error) throw error;
        return data || [];
    }

    async getOracleEvents(limit: number = 100): Promise<AuditEvent[]> {
        const { data, error } = await this.supabase
            .from('oracle_events')
            .select('*')
            .order('timestamp', { ascending: false })
            .limit(limit);

        if (error) throw error;
        return data || [];
    }

    // Access control integration functions
    async validateAgentAccess(agentId: string, toolId: string): Promise<[boolean, string]> {
        try {
            return await this.accessControl.validateAgentAccess(agentId, toolId);
        } catch (error) {
            return [false, 'Validation failed'];
        }
    }

    async getAgentRateLimit(agentId: string): Promise<any> {
        try {
            return await this.accessControl.getAgentRateLimit(agentId);
        } catch (error) {
            throw new Error('Failed to get agent rate limit');
        }
    }

    async isRateLimitExceeded(agentId: string): Promise<boolean> {
        try {
            return await this.accessControl.isRateLimitExceeded(agentId);
        } catch (error) {
            return true; // Default to exceeded if check fails
        }
    }

    async getRemainingActions(agentId: string): Promise<number> {
        try {
            return await this.accessControl.getRemainingActions(agentId);
        } catch (error) {
            return 0; // Default to 0 if check fails
        }
    }

    async getAgentPolicy(agentId: string): Promise<any> {
        try {
            return await this.accessControl.getAgentPolicy(agentId);
        } catch (error) {
            throw new Error('Failed to get agent policy');
        }
    }

    async getToolPolicy(toolId: string): Promise<any> {
        try {
            return await this.accessControl.getToolPolicy(toolId);
        } catch (error) {
            throw new Error('Failed to get tool policy');
        }
    }

    // Enhanced validation with access control
    async validateActionWithPolicies(
        agentId: string,
        toolId: string,
        gasUsed: number
    ): Promise<{
        isValid: boolean;
        reason: string;
        agentPolicy: any;
        toolPolicy: any;
        rateLimit: any;
    }> {
        try {
            // Get policies and rate limits
            const agentPolicy = await this.getAgentPolicy(agentId);
            const toolPolicy = await this.getToolPolicy(toolId);
            const rateLimit = await this.getAgentRateLimit(agentId);

            // Check access control
            const [isAllowed, reason] = await this.accessControl.checkActionAllowed(agentId, toolId, gasUsed);

            return {
                isValid: isAllowed,
                reason,
                agentPolicy,
                toolPolicy,
                rateLimit
            };
        } catch (error) {
            return {
                isValid: false,
                reason: 'Validation failed',
                agentPolicy: null,
                toolPolicy: null,
                rateLimit: null
            };
        }
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

    async getNetworkInfo(): Promise<{
        chainId: bigint;
        name: string;
        blockNumber: number;
        timestamp: number;
    }> {
        const network = await this.provider.getNetwork();
        const blockNumber = await this.getBlockNumber();
        const timestamp = await this.getBlockTimestamp();

        return {
            chainId: network.chainId,
            name: network.name || 'Unknown',
            blockNumber,
            timestamp
        };
    }

    // Enhanced validation with blockchain data
    async validateActionWithBlockchainData(
        agentId: string,
        toolId: string,
        gasUsed: number
    ): Promise<{
        isValid: boolean;
        reason: string;
        agentPolicy: any;
        toolPolicy: any;
        rateLimit: any;
        blockchainData: any;
    }> {
        try {
            // Get basic validation
            const validation = await this.validateActionWithPolicies(agentId, toolId, gasUsed);

            // Get blockchain data
            const networkInfo = await this.getNetworkInfo();

            return {
                ...validation,
                blockchainData: {
                    networkInfo,
                    currentGasPrice: await this.provider.getFeeData().then(fee => fee.gasPrice || BigInt(0)),
                    currentBlock: networkInfo.blockNumber
                }
            };
        } catch (error) {
            return {
                isValid: false,
                reason: 'Validation failed',
                agentPolicy: null,
                toolPolicy: null,
                rateLimit: null,
                blockchainData: null
            };
        }
    }

    // Gas estimation functions
    async estimateValidationGas(validationId: string): Promise<bigint> {
        // This would estimate gas for validation operations
        // For now, return a default value
        return BigInt(100000);
    }

    async getGasPrice(): Promise<bigint> {
        const feeData = await this.provider.getFeeData();
        return feeData.gasPrice || BigInt(0);
    }

    // Transaction monitoring
    async monitorTransaction(txHash: string): Promise<{
        status: 'pending' | 'confirmed' | 'failed';
        confirmations: number;
        receipt?: ethers.TransactionReceipt | null;
    }> {
        try {
            const receipt = await this.provider.waitForTransaction(txHash, 1, this.config.timeout);

            if (receipt) {
                return {
                    status: receipt.status === 1 ? 'confirmed' : 'failed',
                    confirmations: receipt.confirmations,
                    receipt
                };
            } else {
                return {
                    status: 'pending',
                    confirmations: 0
                };
            }
        } catch (error) {
            return {
                status: 'failed',
                confirmations: 0
            };
        }
    }
}
